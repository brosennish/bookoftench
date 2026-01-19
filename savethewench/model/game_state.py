import random
from collections import Counter
from dataclasses import dataclass, field
from typing import List, Dict

import savethewench.service.crypto_service as crypto_service
from savethewench import event_logger
from savethewench.audio import play_music
from savethewench.data.illnesses import LATE_ONSET_SIDS
from savethewench.data.perks import TENCH_THE_BOUNTY_HUNTER
from savethewench.event_base import EventType, Event
from savethewench.event_logger import subscribe_function
from savethewench.settings import Settings, set_settings
from savethewench.ui import green, yellow, cyan, blue, red
from savethewench.util import print_and_sleep
from .achievement import AchievementEvent, set_achievement_cache, load_achievements, Achievement
from .area import Area, load_areas
from .bank import Bank
from .coffee_item import CoffeeItem
from .crypto import CryptoMarketState
from .enemy import Enemy, load_enemy
from .events import TravelEvent, BountyCollectedEvent, PlayerDeathEvent, TreatmentEvent, LevelUpEvent
from .illness import Illness
from .illnesses import Illnesses
from .item import Item
from .perk import attach_perk, Perk, set_perk_cache
from .player import Player
from .shop import Shop
from .weapon import Weapon


@dataclass
class GameState:
    player: Player = field(default_factory=Player)

    bank: Bank = field(default_factory=Bank)
    areas: List[Area] = field(default_factory=load_areas)
    current_area: Area = None

    wench_area: Area = field(default_factory=lambda: random.choice(load_areas()))  # TODO

    found_item: Item = None
    found_weapon: Weapon = None

    wanted: str = ''
    _bounty: int = 0

    victory = False

    event_counter: Counter = field(default_factory=Counter)
    perk_cache: Dict[str, Perk] = field(default_factory=dict)
    achievement_cache: Dict[str, Achievement] = field(default_factory=dict)
    settings: Settings = field(default_factory=Settings.defaults)
    crypto_market_state: CryptoMarketState = field(default_factory=CryptoMarketState.defaults)

    @property
    def shop(self) -> Shop:
        return self.current_area.shop

    @property
    @attach_perk(TENCH_THE_BOUNTY_HUNTER, silent=True)
    def bounty(self):
        return self._bounty

    @bounty.setter
    def bounty(self, value):
        self._bounty = value

    def __post_init__(self):
        if self.current_area is None:
            self.current_area = self.areas[0]
        if len(self.wanted) == 0:
            self.refresh_bounty()
        event_logger.set_counter(self.event_counter)
        set_achievement_cache(self.achievement_cache)
        set_perk_cache(self.perk_cache)
        set_settings(self.settings)
        load_achievements()
        crypto_service.init(self.crypto_market_state)
        crypto_service.start()
        self._subscribe_listeners()

    def refresh_bounty(self):
        bounty_area = random.choice(self.areas)
        enemy_choice: Enemy = load_enemy(random.choice(bounty_area.enemies))  # = random.choice(load_enemies())
        self.wanted = enemy_choice.name
        self.bounty = enemy_choice.bounty

    def update_current_area(self, area_name: str):
        for area in self.areas:
            if area.name == area_name:
                self.current_area = area
                event_logger.log_event(TravelEvent(area_name))
                return
        raise KeyError(f"Area '{area_name}' not found")

    def play_current_area_theme(self):
        play_music(self.current_area.theme)

    def make_treatment_purchase(self):
        illness = self.player.illness

        if self.player.coins < illness.cost:
            print_and_sleep(yellow(f"Need more coin"), 1)
            return False

        if isinstance(illness, Illness):
            self.do_treatment()
        else:
            return False
        self.player.coins -= illness.cost
        return True

    def do_treatment(self):
        player = self.player
        illness = player.illness

        if random.random() < illness.success_rate:
            print_and_sleep(f"{cyan('Woah, I really didn\'t expect that to work.')}\n", 2)
            player.illness = None
            player.illness_death_lvl = None
            event_logger.log_event(TreatmentEvent(illness, EventType.TREATMENT_SUCCESS))
            return self
        else:
            print_and_sleep(blue(
                f"Shit didn't take. You owe me {illness.cost} of coin. Also - you into crypto?"),
                2)
            event_logger.log_event(TreatmentEvent(illness, EventType.TREATMENT_FAIL))
            return self

    def make_coffee_purchase(self, coffee_item: CoffeeItem):
        if self.player.coins < coffee_item.cost:
            print_and_sleep(yellow(f"Need more coin"), 1)
            return False

        if isinstance(coffee_item, CoffeeItem):
            self.coffee_effect(coffee_item)
        else:
            return False
        self.player.coins -= coffee_item.cost
        return True

    def coffee_effect(self, item: CoffeeItem):
        player = self.player
        original_hp = player.hp
        player.gain_hp(item.hp)
        print_and_sleep(f"You restored {green(self.player.hp - original_hp)} hp!\n", 1)

        illnesses = Illnesses()
        illness = random.choice(illnesses.all_illnesses)

        if random.random() < item.risk:
            if illness.name != LATE_ONSET_SIDS:
                player.illness = illness
                player.illness_death_lvl = player.lvl + illness.levels_until_death

                print_and_sleep(yellow(f"Coughy coughed on your coffee and now you're sicker than Hell."), 2)
                print_and_sleep(f"Illness: {yellow(f'{illness.name}')}", 2)
                print_and_sleep(f"{yellow(f'{illness.description}')}", 2)
                print_and_sleep(
                    f"Visit the Free Range Children's Hospital for treatment "
                    f"or die at level {red(f'{player.illness_death_lvl}')}\n",
                    3
                )
            else:
                print_and_sleep(yellow(f"Coughy coughed on your coffee and now you're just a worthless bag of bones."),
                                2)
                print_and_sleep(f"Cause of Death: {red(f'{illness.name}')}", 2)
                print_and_sleep(f"{red(f'{illness.description}')}", 3)
                player.hp = 0
                player.lives -= 1
                event_logger.log_event(PlayerDeathEvent(player.lives))

    def _subscribe_listeners(self):
        @subscribe_function(BountyCollectedEvent)
        def handle_bounty_collected_event(event: BountyCollectedEvent):
            print_and_sleep(green(f"You killed {event.enemy_name} and collected a bounty of {self.bounty} coins!"), 1)
            self.player.coins += self.bounty
            self.refresh_bounty()

        @subscribe_function(AchievementEvent)
        def handle_achievement_event(event: AchievementEvent):
            event.activate(self.player)

        @subscribe_function(LevelUpEvent)
        def trigger_bank_visit_decision(_: LevelUpEvent):
            event_logger.log_event(BankVisitDecisionTriggerEvent(self))

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
