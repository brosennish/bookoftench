import random
from collections import Counter
from dataclasses import dataclass, field
from typing import List, Dict

import bookoftench.service.crypto_service as crypto_service
from bookoftench import event_logger
from bookoftench.audio import play_music, play_sound
from bookoftench.data.perks import TENCH_THE_BOUNTY_HUNTER, NEPTUNE
from bookoftench.event_base import EventType, Event
from bookoftench.event_logger import subscribe_function
from bookoftench.settings import Settings, set_settings
from bookoftench.ui import green, red, yellow
from bookoftench.util import print_and_sleep
from .FishingArea import FishingArea
from .achievement import AchievementEvent, set_achievement_cache, load_achievements, Achievement
from .area import Area, load_areas
from .bank import Bank
from .build import Build
from .discoverable import Discoverable
# from .crypto import CryptoMarketState
from .enemy import Enemy, load_enemy
from .events import TravelEvent, BountyCollectedEvent, LevelUpEvent, HohkkenEvent
from .fish import Fish
from .illness import load_illness
from .item import Item, load_items
from .perk import attach_perk, Perk, set_perk_cache, load_perk, perk_is_active
from .player import Player
from .shop import Shop
from .weapon import Weapon, load_weapons
from ..data.audio import COINS
from ..data.builds import Builds
from ..data.enemies import HOHKKEN
from ..data.fishing_areas import DRY_SEASON, WET_SEASON
from ..data.illnesses import Illnesses
from ..data.enviroment import DRY, DAY, NIGHT, WETTING, FULL, DRYING

# ================================================================================================

@dataclass
class GameState:
    player: Player = field(default_factory=Player)

    bank: Bank = field(default_factory=Bank)
    areas: List[Area] = field(default_factory=load_areas)

    current_area: Area = None
    current_fishing_area: FishingArea | None = None
    current_fish: Fish | None = None
    all_fish: bool = True

    pending_boss: bool = False

    casino_is_open: bool = True
    coffee_is_open: bool = True
    hospital_is_open: bool = True
    wizard_is_open: bool = True
    shaman_is_open: bool = True
    blacksmith_is_open: bool = True
    fishmonger_is_open: bool = True
    hohkken_is_alive: bool = True

    season: str = DRY_SEASON
    time_of_day: str = field(default=DAY)
    moon: str = field(default=DRY)

    wench_area: Area = None

    found_item: Item = None
    found_weapon: Weapon = None

    wanted: str = ''
    _bounty: int = 0

    victory = False

    achievement_cache: Dict[str, Achievement] = field(default_factory=dict)
    crypto_market_state = None
    discoveries: List[Discoverable] = field(default_factory=list)
    encountered_enemies: List[dict] = field(default_factory=list)
    event_counter: Counter = field(default_factory=Counter)
    liberated_enemies: List[Enemy] = field(default_factory=list)
    perk_cache: Dict[str, Perk] = field(default_factory=dict)
    settings: Settings = field(default_factory=Settings.defaults)
    _all_builds: List[Build] = field(init=False)

# ================================================================================================

    @property
    def build_inventory(self) -> List[Build]:
        builds_list = []
        for d in Builds:
            items = load_items([i_name for i_name in d["items"]])
            weapons = load_weapons([w_name for w_name in d["weapons"]])
            perks = []
            for i in d["perks"]:
                p = load_perk(i)
                perks.append(p)
            if d['illness']:
                illness_dict = next(b for b in Illnesses if b['name'] == d["illness"])
                illness = load_illness(illness_dict)
            else:
                illness = None

            build_obj = Build(
                name=d["name"],
                notes=d.get("notes"),
                lives=d["lives"],
                hp=d["hp"],
                str=d["str"],
                acc=d["acc"],
                coins=d["coins"],
                illness=illness,
                items=items,
                weapons=weapons,
                perks=perks,
            )
            builds_list.append(build_obj)
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
    def bounty(self, value):
        self._bounty = value

    def __post_init__(self):
        if self.current_area is None:
            self.current_area = self.areas[0]
        if self.wench_area is None:
            self.wench_area = random.choice(self.areas)
        if len(self.wanted) == 0:
            self.refresh_bounty()
        self.discoveries = []
        self.encountered_enemies = []
        self.liberated_enemies = []
        self.set_moon()
        self.set_time_of_day()
        event_logger.set_counter(self.event_counter)
        set_achievement_cache(self.achievement_cache)
        set_perk_cache(self.perk_cache)
        set_settings(self.settings)
        load_achievements()
        if self.crypto_market_state is not None:
            crypto_service.init(self.crypto_market_state)
        self._subscribe_listeners()

# ================================================================================================

    def update_season(self):
        if self.season == DRY_SEASON:
            self.season = WET_SEASON
        else:
            self.season = DRY_SEASON

    def set_time_of_day(self):
        self.time_of_day = random.choice([DAY, NIGHT])

    def update_time_of_day(self) -> None:
        if self.time_of_day == DAY:
            self.time_of_day = NIGHT
        elif self.time_of_day == NIGHT:
            self.time_of_day = DAY

    def set_moon(self):
        moons = [DRY, DRYING, WETTING, FULL]
        self.moon = random.choice(moons)

    def update_moon(self) -> None:
        if self.moon == DRY:
            self.moon = WETTING
        elif self.moon == WETTING:
            self.moon = FULL
        elif self.moon == FULL:
            self.moon = DRYING
        elif self.moon == DRYING:
            self.moon = DRY

    def refresh_bounty(self) -> None:
        valid_areas = [i for i in self.areas if i.enemies_remaining > 0]
        if valid_areas:
            bounty_area = random.choice(valid_areas)
        else:
            bounty_area = random.choice(self.areas)
        enemy_choice: Enemy = load_enemy(random.choice(bounty_area.enemies))  # = random.choice(load_enemies())
        self.wanted = enemy_choice.name
        self.bounty = enemy_choice.bounty

    def update_current_area(self, area_name: str) -> None:
        for area in self.areas:
            if area.name == area_name:
                self.current_area = area
                event_logger.log_event(TravelEvent(area_name))
                if not perk_is_active(NEPTUNE) and self.hohkken_is_alive:
                    if self.time_of_day == DAY and random.random() < 0.04:
                        event_logger.log_event(HohkkenEvent())
                    elif self.time_of_day == NIGHT and random.random() < 0.08:
                        event_logger.log_event(HohkkenEvent())
                return

        raise KeyError(f"Area '{area_name}' not found")

    def play_current_area_theme(self) -> None:
        play_music(self.current_area.theme)

# ================================================================================================

    def _subscribe_listeners(self):
        @subscribe_function(BountyCollectedEvent)
        def handle_bounty_collected_event(event: BountyCollectedEvent):
            print_and_sleep(green(f"You killed {event.enemy_name} and collected a bounty of {self.bounty} coins!"), 1)
            play_sound(COINS)
            self.player.coins += self.bounty
            self.refresh_bounty()

        @subscribe_function(AchievementEvent)
        def handle_achievement_event(event: AchievementEvent):
            event.activate(self.player)

        @subscribe_function(HohkkenEvent)
        def handle_hohkken_event(event: HohkkenEvent):
            self.current_area.set_boss_to_current_enemy(HOHKKEN)
            self.pending_boss = True

        @subscribe_function(LevelUpEvent)
        def trigger_level_up_events(_: LevelUpEvent):
            event_logger.log_event(BankVisitDecisionTriggerEvent(self))
            event_logger.log_event(SaveGameDecisionTriggerEvent(self))
            self.update_season()
            self.refresh_bounty()
            self.handle_component_statuses()

# ================================================================================================

    def handle_component_statuses(self):
        # --- casino ---
        if self.casino_is_open:
            if random.random() < 0.10:
                self.casino_is_open = False
                print_and_sleep(yellow(f"The casino has closed pending investigation."), 1)
        else:
            if random.random() < 0.75:
                self.casino_is_open = True
                print_and_sleep(green(f"The casino has reopened following a successful bribe."), 1)

        # --- coffee ---
        if self.coffee_is_open:
            if random.random() < 0.10:
                self.coffee_is_open = False
                print_and_sleep(red(f"Coughy has died."), 1)
        else:
            if random.random() < 0.50:
                self.coffee_is_open = True
                print_and_sleep(green(f"Coughy's Coffee has reopened following Coughy's resurrection."), 1)

        # --- hospital ---
        if self.hospital_is_open:
            if random.random() < 0.10:
                self.hospital_is_open = False
                print_and_sleep(yellow(f"The hospital has closed due to pending litigation."), 1)
        else:
            if random.random() < 0.50:
                self.hospital_is_open = True
                print_and_sleep(green(f"The hospital has reopened following a successful bribe."), 1)

        # --- wizard ---
        if self.wizard_is_open:
            if random.random() < 0.15:
                self.wizard_is_open = False
                print_and_sleep(yellow(f"The Wizard has disappeared."), 1)
        else:
            if random.random() < 0.50:
                self.wizard_is_open = True
                print_and_sleep(green(f"The Wizard has reappeared."), 1)

        # --- shaman ---
        if self.shaman_is_open:
            if random.random() < 0.15:
                self.shaman_is_open = False
                print_and_sleep(yellow(f"The Shaman has gone to the underworld."), 1)
        else:
            if random.random() < 0.50:
                self.shaman_is_open = True
                print_and_sleep(green(f"The Shaman has returned from the underworld."), 1)

        # --- blacksmith ---
        if self.blacksmith_is_open:
            if random.random() < 0.20:
                self.blacksmith_is_open = False
                print_and_sleep(yellow(f"Sledge Jr. went on an HTH run."), 1)
        else:
            if random.random() < 0.65:
                self.blacksmith_is_open = True
                print_and_sleep(green(f"Sledge Jr. has returned from his HTH run."), 1)

        # --- fishmonger ---
        if self.fishmonger_is_open:
            if random.random() < 0.15:
                self.fishmonger_is_open = False
                print_and_sleep(yellow(f"The Fishmonger got lost at sea."), 1)
        else:
            if random.random() < 0.75:
                self.fishmonger_is_open = True
                print_and_sleep(green(f"The Fishmonger has returned from being lost at sea."), 1)

# ================================================================================================

    def is_final_boss_available(self) -> bool:
        return self.current_area.boss_defeated and (self.wench_area == self.current_area) and not self.victory

    def is_wanted(self, combatant):
        return self.wanted in combatant.name


    # for loading from save file
    def __setstate__(self, state):
        self.__dict__.update(state)
        self.__post_init__()


class BankVisitDecisionTriggerEvent(Event):
    def __init__(self, game_state: GameState):
        super().__init__(EventType.BANK_VISIT_DECISION_TRIGGER)
        self.game_state = game_state


class SaveGameDecisionTriggerEvent(Event):
    def __init__(self, game_state: GameState):
        super().__init__(EventType.SAVE_GAME_DECISION_TRIGGER)
        self.game_state = game_state
