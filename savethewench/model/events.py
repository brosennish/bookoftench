from typing import List

from savethewench.event_base import Event, EventType
from .item import Item
from .perk import Perk


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
