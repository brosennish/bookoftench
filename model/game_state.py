import random
from dataclasses import dataclass, field
from typing import List

import event_logger
from events import TravelEvent
from stw_classes import GameState
from .area import Area, load_areas
from .enemy import Enemy, load_enemies
from .player import Player
from .shop import Shop


@dataclass
class GameState:
    player: Player = field(default_factory=Player)
    shop: Shop = field(default_factory=Shop)
    rescued: bool = False
    areas: List[Area] = field(default_factory=load_areas)
    current_area: Area = field(init=False)

    wench_area: str = 'Hell' #TODO

    wanted: str = field(init=False)
    bounty: int = field(init=False)


    def __post_init__(self):
        self.current_area = self.areas[0]
        enemy_choice: Enemy = random.choice(load_enemies())
        self.wanted = enemy_choice.name
        self.bounty = enemy_choice.bounty

    def update_current_area(self, area_name: str) -> GameState:
        for area in self.areas:
            if area.name == area_name:
                self.current_area = area
                event_logger.log_event(TravelEvent(area_name))
                return self
        raise KeyError(f"Area '{area_name}' not found")
