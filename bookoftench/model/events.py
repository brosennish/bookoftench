from typing import Optional

from bookoftench import event_logger
from bookoftench.audio import play_sound
from bookoftench.data.audio import PURCHASE, GREAT_JOB
from bookoftench.event_base import Event, EventType
from bookoftench.model.illness import Illness
from bookoftench.ui import green, cyan, red, yellow, dim, blue
from bookoftench.util import print_and_sleep


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

    def sub_callback(self) -> None:
        pass

    def _callback(self, name, amount):
        play_sound(PURCHASE)
        print_and_sleep(green(f"You purchased {name} for {amount} of coin."), 1)
        self.sub_callback()


class BuyItemEvent(PurchaseEvent):
    def __init__(self, name: str, amount: int):
        super().__init__(EventType.BUY_ITEM, name, amount)
        self.sub_msg = f"{name} added to sack."

    def sub_callback(self) -> None:
        print_and_sleep(cyan(self.sub_msg), 1)


class BuyWeaponEvent(PurchaseEvent):
    def __init__(self, name: str, amount: int, uses: int):
        super().__init__(EventType.BUY_WEAPON, name, amount)
        self.sub_msg = f"{name} added to weapons. Uses: {uses}\n"

    def sub_callback(self) -> None:
        print_and_sleep(cyan(self.sub_msg), 1)


class BuyPerkEvent(PurchaseEvent):
    def __init__(self, name: str, amount: int):
        super().__init__(EventType.BUY_PERK, name, amount)


class StealEventBase(Event):
    def __init__(self, event_type: EventType, name: str, amount: int):
        super().__init__(event_type)
        self.callback = lambda: self._callback(name, amount)

    @staticmethod
    def _callback(name, amount):
        # TODO - sound effect
        print_and_sleep(green(f"You successfully stole {name}."), 1)
        print_and_sleep(yellow(f"Saved yourself {amount} of coin there."), 1)
        print_and_sleep(red(f"But you are now destined for Hell."), 2)


class GenericStealEvent(Event):
    def __init__(self):
        super().__init__(EventType.STEAL)


class StealItemEvent(StealEventBase):
    def __init__(self, item_name: str, amount: int):
        super().__init__(EventType.STEAL_ITEM, item_name, amount)


class StealPerkEvent(StealEventBase):
    def __init__(self, perk_name: str, amount: int):
        super().__init__(EventType.STEAL_PERK, perk_name, amount)


class StealWeaponEvent(StealEventBase):
    def __init__(self, weapon_name: str, amount: int):
        super().__init__(EventType.STEAL_WEAPON, weapon_name, amount)


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
            print(cyan(f"\nReward: {item_reward.name}"))
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


class DiscoveryEventCommon(Event):
    def __init__(self):
        super().__init__(EventType.DISCOVERY_COMMON)

class DiscoveryEventUncommon(Event):
    def __init__(self):
        super().__init__(EventType.DISCOVERY_UNCOMMON)

class DiscoveryEventRare(Event):
    def __init__(self):
        super().__init__(EventType.DISCOVERY_RARE)

class DiscoveryEventLegendary(Event):
    def __init__(self):
        super().__init__(EventType.DISCOVERY_LEGENDARY)

class DiscoveryEventMythic(Event):
    def __init__(self):
        super().__init__(EventType.DISCOVERY_MYTHIC)


class OccultistEvent(Event):
    def __init__(self):
        super().__init__(EventType.PAY_OCCULTIST)

class ShamanEvent(Event):
    def __init__(self):
        super().__init__(EventType.PAY_SHAMAN)

class WizardEvent(Event):
    def __init__(self):
        super().__init__(EventType.PAY_WIZARD)


class CoffeeEvent(Event):
    def __init__(self, coffee_item, event_type: EventType):
        super().__init__(event_type)
        self.coffee_item = coffee_item


class TreatmentEvent(Event):
    def __init__(self, illness: Illness, event_type: EventType):
        super().__init__(event_type, callback=self._callback)
        self.illness = illness

    def _callback(self):
        if self.type == EventType.TREATMENT_SUCCESS:
            print_and_sleep(green(f"You have been cured of {self.illness.name}!"), 2)


class OfficerEvent(Event):
    def __init__(self, event_type: EventType):
        super().__init__(event_type, callback=self.paid if event_type == event_type.OFFICER_PAID else self.unpaid)

    def paid(self) -> None:
        print_and_sleep(f"{blue("Thanks for the coin ther'.")}", 1.5)
        print_and_sleep(f"{blue("Unfortunately, uh... I got some bad news for ya's.")}", 1.5)
        print_and_sleep(f"{blue("Your whole family was, uh... dragged down.")}", 1.5)
        print_and_sleep(f"{blue("The whole bunch.")}", 1.5)

    def unpaid(self) -> None:
        print_and_sleep(f"{blue("...")}", 1.5)
        print_and_sleep(f"{blue("This is Officer Hohkken.")}", 1.5)


# TODO for crypto events, figure out a method of alerting that doesn't print to console
# printing to console screws up curses display if player is in the crypto market component when a coin is (de)listed
class CoinDelistingScheduledEvent(Event):
    def __init__(self, coin_name: str, seconds_to_delist: int):
        super().__init__(EventType.COIN_DELISTING_SCHEDULED)
        # callback=lambda: print_and_sleep(f"{coin_name} will be delisted in {seconds_to_delist} seconds."))


class CoinDelistedEvent(Event):
    def __init__(self, coin_name: str):
        super().__init__(EventType.COIN_DELISTED)
        # callback=lambda: print_and_sleep(f"{coin_name} has been delisted."))


class CoinListedEvent(Event):
    def __init__(self, coin_name: str, price: int):
        super().__init__(EventType.COIN_LISTED)
        # callback=lambda: print_and_sleep(f"{coin_name} is now available for {price} of coin."))
