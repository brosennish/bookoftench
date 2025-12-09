import random
from dataclasses import dataclass, field
from typing import List

from events import EventLogger
from stw_classes import GameState
from .area import Area, load_areas
from .enemy import Enemy, load_enemies
from .player import Player
from .shop import Shop


@dataclass
class GameState:
    event_logger: EventLogger = None
    player: Player = None
    shop: Shop = None  # Shop()
    rescued: bool = False
    areas: List[Area] = field(default_factory=lambda: load_areas())
    current_area: Area = field(init=False)

    wanted: str = field(init=False)
    bounty: int = field(init=False)


    def __post_init__(self):
        self.current_area = self.areas[0]
        enemy_choice: Enemy = random.choice(load_enemies())
        self.wanted = enemy_choice.name
        self.bounty = enemy_choice.bounty
        self.event_logger = EventLogger()
        self.player = Player(self.event_logger)

    def update_current_area(self, area_name: str) -> GameState:
        for area in self.areas:
            if area.name == area_name:
                self.current_area = area
                #self.event_logger.log_event(TravelEvent(area_name))
                return self
        raise KeyError(f"Area '{area_name}' not found")
