from typing import Optional
from savethewench.audio import play_sound
from savethewench.data.audio import PURCHASE, GREAT_JOB
from savethewench.event_base import Event, EventType
from savethewench.ui import green, cyan, red, yellow, dim
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
        print_and_sleep(green(f"You purchased {name} for {amount} of coin."), 1)
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
                         lambda: print_and_sleep(green(f"You sold {name} for {value} of coin.\n"), 1))


class TravelEvent(Event):
    def __init__(self, area_name: str):
        super().__init__(EventType.TRAVEL)
        self.area_name = area_name


class CritEvent(Event):
    def __init__(self):
        super().__init__(EventType.CRIT)


class HitEvent(Event):
    def __init__(self, weapon_type: str):
        super().__init__(EventType.HIT)
        self.weapon_type = weapon_type


class KillEvent(Event):
    def __init__(self):
        super().__init__(EventType.KILL)


class MissEvent(Event):
    def __init__(self):
        super().__init__(EventType.MISS)


class BankDepositEvent(Event):
    def __init__(self, amount: int):
        super().__init__(EventType.DEPOSIT, lambda:
        print_and_sleep(f"You deposited {green(amount)} of coin into the bank.", 1))


class BankWithdrawalEvent(Event):
    def __init__(self, amount: int):
        super().__init__(EventType.WITHDRAW, lambda:
        print_and_sleep(f"You withdrew {green(amount)} of coin from the bank.", 1))


class LevelUpEvent(Event):
    def __init__(self, level: int, old_max_hp: int, new_max_hp: int, item_reward: Optional[str], cash_reward: int):
        super().__init__(EventType.LEVEL_UP,
                         lambda: self._display(level, old_max_hp, new_max_hp, item_reward, cash_reward))

    @staticmethod
    def _display(level, old_max_hp, new_max_hp, item_reward, cash_reward):
        play_sound(GREAT_JOB)
        print_and_sleep(green(f"You have reached level {level}!\n"), 2)
        print(green(f"MAX HP: {old_max_hp} -> {new_max_hp}"))
        if item_reward is not None:
            print(cyan(f"\nReward: {item_reward}"))
        print_and_sleep(green(f"You were awarded {cash_reward} of coin."), 2)


class SwapWeaponEvent(Event):
    def __init__(self):
        super().__init__(EventType.SWAP_WEAPON)


class FleeEvent(Event):
    def __init__(self, enemy_name: str):
        super().__init__(EventType.FLEE,
                         callback=lambda: print_and_sleep(
                             dim(f"You ran away from {enemy_name}!"), 1))


class FailedFleeEvent(Event):
    def __init__(self):
        super().__init__(EventType.FAILED_FLEE,
                         callback=lambda: print_and_sleep(yellow("Couldn't escape!")))


class PlayerDeathEvent(Event):
    def __init__(self, lives_remaining: int):
        super().__init__(EventType.PLAYER_DEATH,
                         callback=lambda: print_and_sleep(
                             f"{red('You died.')} Lives remaining: {yellow(lives_remaining)}", 2))


class WeaponBrokeEvent(Event):
    def __init__(self):
        super().__init__(EventType.WEAPON_BROKE)


class BountyCollectedEvent(Event):
    def __init__(self, enemy_name):
        super().__init__(EventType.BOUNTY_COLLECTED)
        self.enemy_name = enemy_name


class CoffeeEvent(Event):
    def __init__(self, coffee_item):
        super().__init__(EventType.COFFEE_EVENT)
        self.coffee_item = coffee_item


class TreatmentEvent(Event):
    def __init__(self, illness):
        super().__init__(EventType.TREATMENT_EVENT)
        self.illness = illness


class OfficerEvent(Event):
    def __init__(self, event_type: EventType):
        super().__init__(event_type)
