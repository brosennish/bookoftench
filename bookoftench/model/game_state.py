import random
from collections import Counter
from dataclasses import dataclass, field
from typing import List, Dict

import bookoftench.service.crypto_service as crypto_service
from bookoftench import event_logger
from bookoftench.audio import play_music
from bookoftench.data.perks import TENCH_THE_BOUNTY_HUNTER
from bookoftench.event_base import EventType, Event
from bookoftench.event_logger import subscribe_function
from bookoftench.settings import Settings, set_settings
from bookoftench.ui import green
from bookoftench.util import print_and_sleep
from .achievement import AchievementEvent, set_achievement_cache, load_achievements, Achievement
from .area import Area, load_areas
from .bank import Bank
from .build import Build
from .crypto import CryptoMarketState
from .enemy import Enemy, load_enemy
from .events import TravelEvent, BountyCollectedEvent, LevelUpEvent
from .item import Item, load_items
from .perk import attach_perk, Perk, set_perk_cache, load_perk
from .player import Player
from .shop import Shop
from .weapon import Weapon, load_weapons
from ..data.builds import Builds


@dataclass
class GameState:
    player: Player = field(default_factory=Player)

    bank: Bank = field(default_factory=Bank)
    areas: List[Area] = field(default_factory=load_areas)
    current_area: Area = None

    wench_area: Area = None

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

    _all_builds: List[Build] = field(init=False)

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

            build_obj = Build(
                name=d["name"],
                notes=d.get("notes"),
                hp=d["hp"],
                str=d["str"],
                acc=d["acc"],
                coins=d["coins"],
                items=items,
                weapons=weapons,
                perks=perks,
            )
            builds_list.append(build_obj)
        return builds_list

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
        event_logger.set_counter(self.event_counter)
        set_achievement_cache(self.achievement_cache)
        set_perk_cache(self.perk_cache)
        set_settings(self.settings)
        load_achievements()
        crypto_service.init(self.crypto_market_state)
        crypto_service.start()
        self._subscribe_listeners()

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
                return
        raise KeyError(f"Area '{area_name}' not found")

    def play_current_area_theme(self) -> None:
        play_music(self.current_area.theme)

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
        def trigger_level_up_events(_: LevelUpEvent):
            event_logger.log_event(BankVisitDecisionTriggerEvent(self))
            event_logger.log_event(SaveGameDecisionTriggerEvent(self))

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
