import random
from collections import Counter
from dataclasses import dataclass, field
from typing import List

from savethewench import event_logger
from savethewench.audio import play_music
from savethewench.data.perks import TENCH_THE_BOUNTY_HUNTER
from savethewench.event_logger import subscribe_function
from .area import Area, load_areas
from .bank import Bank
from .enemy import Enemy, load_enemy
from .events import TravelEvent, LevelUpEvent
from .perk import attach_perk
from .player import Player
from .shop import Shop



@dataclass
class GameState:
    player: Player = field(default_factory=Player)
    shop: Shop = field(default_factory=Shop)
    bank: Bank = field(default_factory=Bank)
    areas: List[Area] = field(default_factory=load_areas)
    current_area: Area = field(init=False)

    wench_area: str = 'Hell'  # TODO

    wanted: str = field(init=False)
    _bounty: int = field(init=False)

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

    def refresh_bounty(self):
        enemy_choice: Enemy = load_enemy(random.choice(self.current_area.enemies))  # = random.choice(load_enemies())
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
