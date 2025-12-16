from typing import Callable

from savethewench.audio import play_sound
from savethewench.data.audio import PURCHASE
from savethewench.event_base import Event, EventType
from savethewench.ui import green, cyan
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
    def __init__(self, event_type: EventType, name: str, amount: int):
        super().__init__(event_type)
        self.callback = lambda: self._callback(name, amount)

    def sub_callback(self):
        pass

    def _callback(self, name, amount):
        play_sound(PURCHASE)
        print_and_sleep(green(f"You purchased {name} for {amount} coins.\n"), 1)
        self.sub_callback()


class BuyItemEvent(PurchaseEvent):
    def __init__(self, name: str, amount: int):
        super().__init__(EventType.BUY_ITEM, name, amount)
        self.sub_msg = f"{name} added to sack."

    def sub_callback(self):
        print_and_sleep(cyan(self.sub_msg), 1)


class BuyWeaponEvent(PurchaseEvent):
    def __init__(self, name: str, amount: int, uses: int):
        super().__init__(EventType.BUY_WEAPON, name, amount)
        self.sub_msg = f"{name} added to weapons. Uses: {uses}\n"

    def sub_callback(self):
        print_and_sleep(cyan(self.sub_msg), 1)


class BuyPerkEvent(PurchaseEvent):
    def __init__(self, name: str, amount: int):
        super().__init__(EventType.BUY_PERK, name, amount)


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

class BankWithdrawalEvent(Event):
    def __init__(self, amount: int):
        super().__init__(EventType.WITHDRAW, lambda:
        print_and_sleep(f"You withdrew {green(amount)} coins from the bank.\n", 1))