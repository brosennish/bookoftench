import random
from collections import Counter
from dataclasses import dataclass, field

# import bookoftench.service.crypto_service as crypto_service
from bookoftench import event_logger
from bookoftench.audio import play_music, play_sound
from bookoftench.data.perks import NEPTUNE, TENCH_THE_BOUNTY_HUNTER
from bookoftench.event_base import Event, EventType
from bookoftench.event_logger import subscribe_function
from bookoftench.settings import Settings, set_settings
from bookoftench.ui import green, red, yellow
from bookoftench.util import print_and_sleep
from .achievement import Achievement, AchievementEvent, load_achievements, set_achievement_cache
from .area import Area, load_areas
from .bait import Bait, load_baits, Bait_And_Lures
from .bank import Bank
from .build import Build
from .discoverable import Discoverable
from .enemy import Enemy, load_enemy
from .events import BountyCollectedEvent, HohkkenEvent, LevelUpEvent, TravelEvent, PlayerDeathEvent
from .fish import Fish
from .fishing_area import FishingArea
from .fishing_item import load_fishing_items, FishingItem
from .illness import load_illness
from .item import Item, load_items
from .perk import Perk, attach_perk, load_perk, perk_is_active, set_perk_cache
from .player import Player
from .shop import Shop
from .special_event import SpecialEvent
from .weapon import Weapon, load_weapons
from ..data.audio import COINS
from ..data.builds import Builds
from ..data.crimes import CRIMES
from ..data.enemies import HOHKKEN
from ..data.environment import DAY, DRY, DRYING, FULL, NIGHT, WETTING, Water_Conditions, CLEAR, CLOUDY, MURKY
from ..data.fishing_areas import DRY_SEASON, WET_SEASON
from ..data.fishing_items import Fishing_Items
from ..data.illnesses import Illnesses

# ================================================================================================

@dataclass
class GameState:
    player: Player = field(default_factory=Player)

    bank: Bank = field(default_factory=Bank)
    areas: list[Area] = field(default_factory=load_areas)

    current_area: Area | None = None
    current_fishing_area: FishingArea | None = None
    current_fish: Fish | None = None
    all_fish: bool = True
    player_went_fishing: bool = False

    pending_boss: bool = False

    unlimited_fishing: bool = False

    casino_is_open: bool = True
    coffee_is_open: bool = True
    hospital_is_open: bool = True
    wizard_is_open: bool = True
    shaman_is_open: bool = True
    blacksmith_is_open: bool = True
    fishmonger_is_open: bool = True
    hohkken_is_alive: bool = True

    season: str = field(default=DRY_SEASON)
    water_condition: str = field(default=CLEAR)
    time_of_day: str = field(default=DAY)
    moon: str = field(default=DRY)
    day: int = 1

    wench_area: Area | None = None

    found_item: Item | None = None
    found_weapon: Weapon | None = None

    wanted: Enemy = None
    crimes: list[dict] = field(default_factory=list)
    _bounty: int = 0
    display_bounty_pending: bool = True

    status_view: int = 1
    weapon_format: int = 1

    victory: bool = False

    achievement_cache: dict[str, Achievement] = field(default_factory=dict)
    bait_shop_inventory: list[Bait] = field(default_factory=list)
    fishing_item_shop_inventory: list[FishingItem] = field(default_factory=list)
    # crypto_market_state = None
    discoveries: list[Discoverable] = field(default_factory=list)
    encountered_enemies: list[dict] = field(default_factory=list)
    event_counter: Counter = field(default_factory=Counter)
    expired_special_events: list[SpecialEvent] = field(default_factory=list)
    liberated_enemies: list[Enemy] = field(default_factory=list)
    perk_cache: dict[str, Perk] = field(default_factory=dict)
    settings: Settings = field(default_factory=Settings.defaults)
    _all_builds: list[Build] = field(init=False)

# ================================================================================================

    @property
    def build_inventory(self) -> list[Build]:
        builds_list = []

        for build_data in Builds:
            items = load_items(build_data["items"])
            weapons = load_weapons(build_data["weapons"])
            perks = [load_perk(perk_name) for perk_name in build_data["perks"]]

            if build_data["illness"]:
                illness_data = next(
                    illness
                    for illness in Illnesses
                    if illness["name"] == build_data["illness"]
                )
                illness = load_illness(illness_data)
            else:
                illness = None

            build = Build(
                name=build_data["name"],
                label=build_data["label"],
                notes=build_data.get("notes"),
                lives=build_data["lives"],
                lvl=build_data["lvl"],
                hp=build_data["hp"],
                str=build_data["str"],
                acc=build_data["acc"],
                coins=build_data["coins"],
                luck=build_data["luck"],
                fishing_lvl=build_data["fishing_lvl"],
                rod_lvl=build_data["rod_lvl"],
                illness=illness,
                items=items,
                weapons=weapons,
                perks=perks,
            )
            builds_list.append(build)

        return builds_list

# ================================================================================================

    @property
    def shop(self) -> Shop:
        return self.current_area.shop

    @property
    @attach_perk(TENCH_THE_BOUNTY_HUNTER, silent=True)
    def bounty(self) -> int:
        return self._bounty

    @bounty.setter
    def bounty(self, value: int) -> None:
        self._bounty = value

    def __post_init__(self) -> None:
        if self.current_area is None:
            self.current_area = self.areas[0]

        if self.wench_area is None:
            self.wench_area = random.choice(self.areas)

        if not self.wanted:
            self.refresh_bounty()

        self.discoveries = []
        self.encountered_enemies = []
        self.liberated_enemies = []

        self.set_moon()
        self.set_time_of_day()
        self.set_season()
        self.set_water_condition()
        self.update_bait_shop_inventory()
        self.update_fishing_item_shop_inventory()

        event_logger.set_counter(self.event_counter)
        set_achievement_cache(self.achievement_cache)
        set_perk_cache(self.perk_cache)
        set_settings(self.settings)
        load_achievements()

        # if self.crypto_market_state is not None:
            # crypto_service.init(self.crypto_market_state)

        self._subscribe_listeners()

# ================================================================================================

    def set_season(self) -> None:
        self.season = random.choice([DRY_SEASON, WET_SEASON])

    def update_season(self) -> None:
        if self.season == DRY_SEASON:
            self.season = WET_SEASON
        else:
            self.season = DRY_SEASON

    def set_water_condition(self):
        self.water_condition = random.choice(Water_Conditions)

    def get_bite_chance(self) -> float:
        bite_chance = self.current_fishing_area.bite_chance
        season = self.season
        water_condition = self.water_condition

        if season == WET_SEASON:
            bite_chance += random.uniform(0.05, 0.10)
        else:
            bite_chance -= random.uniform(0.05, 0.10)

        if water_condition == CLEAR:
            bite_chance += random.uniform(0.03, 0.06)
        elif water_condition == CLOUDY:
            bite_chance += random.uniform(-0.03, 0.03)
        elif water_condition == MURKY:
            bite_chance -= random.uniform(0.03, 0.06)

        bite_chance += min((self.player.fishing_lvl - 1) / 100, 0.05)

        if bite_chance < 0.10:
            bite_chance = 0.10
        elif bite_chance > 0.45:
            bite_chance = 0.45

        return bite_chance

# ================================================================================================

    def update_bait_shop_inventory(self) -> None:
        selections = random.sample(
            [bait["name"] for bait in Bait_And_Lures],
            min(4, len(Bait_And_Lures)),
        )
        self.bait_shop_inventory = load_baits(selections)

    def update_fishing_item_shop_inventory(self) -> None:
        selections = random.sample(
            [item["name"] for item in Fishing_Items],
            min(4, len(Fishing_Items)),
        )
        self.fishing_item_shop_inventory = load_fishing_items(selections)

# ================================================================================================

    def set_time_of_day(self) -> None:
        self.time_of_day = DAY

    def update_time_of_day(self) -> None:
        if self.time_of_day == DAY:
            self.time_of_day = NIGHT
        else:
            self.day += 1
            self.time_of_day = DAY
            self.set_water_condition()
            self.update_bait_shop_inventory()
            self.update_fishing_item_shop_inventory()

        self.player_went_fishing = False

    def set_moon(self) -> None:
        self.moon = random.choice([DRY, DRYING, WETTING, FULL])

    def update_moon(self) -> None:
        if self.moon == DRY:
            self.moon = WETTING
        elif self.moon == WETTING:
            self.moon = FULL
        elif self.moon == FULL:
            self.moon = DRYING
        elif self.moon == DRYING:
            self.moon = DRY

# ================================================================================================

    def refresh_bounty(self) -> None:
        self.set_wanted_enemy()
        self.set_crimes()
        self.set_bounty()

    def set_wanted_enemy(self) -> None:
        valid_areas = [
            area
            for area in self.areas
            if area.enemies_remaining > 0
        ]

        if valid_areas:
            bounty_area = random.choice(valid_areas)
        else:
            bounty_area = random.choice(self.areas)

        enemy: Enemy = load_enemy(random.choice(bounty_area.enemies))
        self.wanted = enemy

    def set_crimes(self) -> None:
        count = random.randint(1, 3)
        crimes = random.sample(CRIMES, count)
        self.crimes = crimes

    def set_bounty(self) -> None:
        bounty = sum(i['bounty'] for i in self.crimes)
        self.bounty = bounty

# ================================================================================================

    def update_current_area(self, area_name: str, season: str) -> None:
        for area in self.areas:
            if area.name == area_name:
                self.current_area = area
                event_logger.log_event(TravelEvent(area_name))

                if not perk_is_active(NEPTUNE) and self.hohkken_is_alive:
                    if self.time_of_day == DAY:
                        if season == DRY_SEASON:
                            odds = 0.06
                        else:
                            odds = 0.02
                    else:
                        if season == DRY_SEASON:
                            odds = 0.10
                        else:
                            odds = 0.06

                    if random.random() < odds:
                        event_logger.log_event(HohkkenEvent())

                return

        raise KeyError(f"Area '{area_name}' not found")

    def play_current_area_theme(self) -> None:
        play_music(self.current_area.theme)

# ================================================================================================

    def _subscribe_listeners(self) -> None:
        @subscribe_function(BountyCollectedEvent)
        def handle_bounty_collected_event(event: BountyCollectedEvent) -> None:
            print_and_sleep(
                green(f"You killed {event.enemy_name} and collected a bounty of {self.bounty} coins!"),
                1,
            )
            play_sound(COINS)
            self.player.coins += self.bounty
            self.refresh_bounty()

        @subscribe_function(AchievementEvent)
        def handle_achievement_event(event: AchievementEvent) -> None:
            event.activate(self.player)

        @subscribe_function(HohkkenEvent)
        def handle_hohkken_event(_: HohkkenEvent) -> None:
            self.current_area.set_boss_to_current_enemy(HOHKKEN)
            self.pending_boss = True

        @subscribe_function(LevelUpEvent)
        def trigger_level_up_events(_: LevelUpEvent) -> None:
            event_logger.log_event(BankVisitDecisionTriggerEvent(self))
            event_logger.log_event(SaveGameDecisionTriggerEvent(self))
            self.update_season()
            self.refresh_bounty()
            self.handle_component_statuses()

# ================================================================================================

    def handle_component_statuses(self) -> None:
        # --- casino ---
        if self.casino_is_open:
            if random.random() < 0.10:
                self.casino_is_open = False
                print_and_sleep(yellow("The casino has closed pending investigation."), 1)
        else:
            if random.random() < 0.75:
                self.casino_is_open = True
                print_and_sleep(green("The casino has reopened following a successful bribe."), 1)

        # --- coffee ---
        if self.coffee_is_open:
            if random.random() < 0.10:
                self.coffee_is_open = False
                print_and_sleep(red("Coughy has died."), 1)
        else:
            if random.random() < 0.50:
                self.coffee_is_open = True
                print_and_sleep(green("Coughy's Coffee has reopened following Coughy's resurrection."), 1)

        # --- hospital ---
        if self.hospital_is_open:
            if random.random() < 0.10:
                self.hospital_is_open = False
                print_and_sleep(yellow("The hospital has closed due to pending litigation."), 1)
        else:
            if random.random() < 0.50:
                self.hospital_is_open = True
                print_and_sleep(green("The hospital has reopened following a successful bribe."), 1)

        # --- wizard ---
        if self.wizard_is_open:
            if random.random() < 0.15:
                self.wizard_is_open = False
                print_and_sleep(yellow("The Wizard has disappeared."), 1)
        else:
            if random.random() < 0.50:
                self.wizard_is_open = True
                print_and_sleep(green("The Wizard has reappeared."), 1)

        # --- shaman ---
        if self.shaman_is_open:
            if random.random() < 0.15:
                self.shaman_is_open = False
                print_and_sleep(yellow("The Shaman has gone to the underworld."), 1)
        else:
            if random.random() < 0.50:
                self.shaman_is_open = True
                print_and_sleep(green("The Shaman has returned from the underworld."), 1)

        # --- blacksmith ---
        if self.blacksmith_is_open:
            if random.random() < 0.20:
                self.blacksmith_is_open = False
                print_and_sleep(yellow("Sledge Jr. went on an HTH run."), 1)
        else:
            if random.random() < 0.65:
                self.blacksmith_is_open = True
                print_and_sleep(green("Sledge Jr. has returned from his HTH run."), 1)

        # --- fishmonger ---
        if self.fishmonger_is_open:
            if random.random() < 0.15:
                self.fishmonger_is_open = False
                print_and_sleep(yellow("The Fishmonger got lost at sea."), 1)
        else:
            if random.random() < 0.75:
                self.fishmonger_is_open = True
                print_and_sleep(green("The Fishmonger has returned from being lost at sea."), 1)

# ================================================================================================

    def is_final_boss_available(self) -> bool:
        return (
                self.current_area.boss_defeated
                and self.wench_area == self.current_area
                and not self.victory
        )

    def is_wanted(self, combatant: Enemy) -> bool:
        return self.wanted in combatant.name

    # For loading from save file.
    def __setstate__(self, state: dict) -> None:
        self.__dict__.update(state)
        self.__post_init__()


class BankVisitDecisionTriggerEvent(Event):
    def __init__(self, game_state: GameState) -> None:
        super().__init__(EventType.BANK_VISIT_DECISION_TRIGGER)
        self.game_state = game_state


class SaveGameDecisionTriggerEvent(Event):
    def __init__(self, game_state: GameState) -> None:
        super().__init__(EventType.SAVE_GAME_DECISION_TRIGGER)
        self.game_state = game_state
