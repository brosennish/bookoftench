import random
from collections import Counter
from dataclasses import dataclass, field
from typing import List

from savethewench import event_logger
from savethewench.audio import play_music
from savethewench.data.perks import TENCH_THE_BOUNTY_HUNTER
from savethewench.event_logger import subscribe_function
from savethewench.ui import green
from savethewench.util import print_and_sleep
from .area import Area, load_areas
from .bank import Bank
from .enemy import Enemy, load_enemy
from .events import TravelEvent, BountyCollectedEvent
from .perk import attach_perk
from .player import Player
from .shop import Shop


@dataclass
class GameState:
    player: Player = field(default_factory=Player)
    shop: Shop = field(default_factory=Shop)
    bank: Bank = field(default_factory=Bank)
    areas: List[Area] = field(default_factory=load_areas)
    current_area: Area = None

    wench_area: Area = field(default_factory=lambda: random.choice(load_areas()))  # TODO

    wanted: str = ''
    _bounty: int = 0

    victory = False

    event_counter: Counter = field(default_factory=Counter)

    @property
    @attach_perk(TENCH_THE_BOUNTY_HUNTER, silent=True)
    def bounty(self):
        return self._bounty

    @bounty.setter
    def bounty(self, value):
        self._bounty = value

    def __post_init__(self):
        self.current_area = self.areas[0]
        self.refresh_bounty()
        event_logger.set_counter(self.event_counter)
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

    def _subscribe_listeners(self):
        @subscribe_function(BountyCollectedEvent)
        def handle_bounty_collected_event(event: BountyCollectedEvent):
            print_and_sleep(green(f"You killed {event.enemy_name} and collected a bounty of {self.bounty} coins!"), 1)
            self.player.coins += self.bounty
            self.refresh_bounty()

    def is_final_boss_available(self) -> bool:
        return self.current_area.boss_defeated and (self.wench_area == self.current_area) and not self.victory
