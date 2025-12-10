from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List, TypeVar

from model.item import Item
from model.perk import Perk


class EventType(Enum):
    BOUNTY_COLLECTED = "bounty_collected"
    BUY_ITEM = "buy_item"
    BUY_PERK = "buy_perk"
    BUY_WEAPON = "buy_weapon"
    CRIT = "crit"
    DEPOSIT = "deposit"
    FLEE = "flee"
    HIT = "hit"
    KILL = "kill"
    LEVEL_UP = "level_up"
    MISS = "miss"
    SELL_ITEM = "sell_item"
    SELL_WEAPON = "sell_weapon"
    SWAP_WEAPON = "swap_weapon"
    TRAVEL = "travel"
    USE_ITEM = "use_item"
    WEAPON_BROKE = "weapon_broke"
    WITHDRAW = "withdraw"

    _CLASS_INTERACTION = "_class_interaction"

    @classmethod
    def get_class_interaction_type(cls):
        return cls._CLASS_INTERACTION


@dataclass
class Event:
    type: EventType


class Listener(ABC):
    @abstractmethod
    def handle_event(self, event: Event) -> None:
        pass


class ItemUsedEvent(Event):
    def __init__(self, item: Item, items_remaining: int, player_hp: int,
                 player_max_hp: int, bonus: int = 0, perks: List[Perk] = None):
        super().__init__(EventType.USE_ITEM)
        self.item = item
        self.items_remaining = items_remaining
        self.player_hp = player_hp
        self.player_max_hp = player_max_hp
        self.bonus = bonus
        self.perks = perks


class TravelEvent(Event):
    def __init__(self, area_name: str):
        super().__init__(EventType.TRAVEL)
        self.area_name = area_name

class KillEvent(Event):
    def __init__(self):
        super().__init__(EventType.KILL)