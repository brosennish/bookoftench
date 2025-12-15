from typing import Callable

from savethewench.event_base import Event, EventType
from savethewench.ui import green
from savethewench.util import print_and_sleep


class ItemUsedEvent(Event):
    def __init__(self, item_name: str, items_remaining: int, player_hp: int,
                 player_max_hp: int, bonus: int = 0):
        super().__init__(EventType.USE_ITEM)
        self.item_name = item_name
        self.items_remaining = items_remaining
        self.player_hp = player_hp
        self.player_max_hp = player_max_hp
        self.bonus = bonus


class PurchaseEvent(Event):
    def __init__(self):
        super().__init__(EventType.BUY_ITEM)



class ItemSoldEvent(Event):
    def __init__(self, name: str, value: int):
        super().__init__(EventType.SELL_ITEM,
                         lambda: print_and_sleep(green(f"You sold {name} for {value} coins.\n"), 1))


class TravelEvent(Event):
    def __init__(self, area_name: str):
        super().__init__(EventType.TRAVEL)
        self.area_name = area_name


class CritEvent(Event):
    def __init__(self, callback: Callable[[], None]):
        super().__init__(EventType.CRIT, callback)


class HitEvent(Event):
    def __init__(self, callback: Callable[[], None]):
        super().__init__(EventType.HIT, callback)


class KillEvent(Event):
    def __init__(self):
        super().__init__(EventType.KILL)


class MissEvent(Event):
    def __init__(self, callback: Callable[[], None]):
        super().__init__(EventType.MISS, callback)
