from abc import ABC, abstractmethod
from collections import Counter, defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, TypeVar, Set

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


@dataclass
class Event:
    type: EventType


E = TypeVar("E", bound=Event)


class Listener[E](ABC):
    @abstractmethod
    def get_listen_type(self) -> E:
        pass

    @abstractmethod
    def register(self, event: E):
        pass


class EventLogger:
    def __init__(self):
        super().__init__()
        self.counter = Counter()
        self.listeners: Dict[type[Event], Set[Listener]] = defaultdict(set)

    def log_event(self, event: Event):
        self.counter[event.type.value] += 1
        self._notify(event)

    def add_subscriber(self, listener: Listener):
        self.listeners[listener.get_listen_type()].add(listener)

    def get_count(self, event_type: EventType) -> int:
        return self.counter[event_type]

    def _notify(self, event: Event):
        for listener in self.listeners[type(event)]:
            listener.register(event)


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