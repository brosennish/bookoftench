import random
from dataclasses import dataclass, field
from typing import TypeVar

from bookoftench.data.perks import BARTER_SAUCE, BROWN_FRIDAY, TRADE_SHIP
from bookoftench.event_base import Event
from bookoftench.event_logger import subscribe_function
from bookoftench.ui import green, red
from bookoftench.util import print_and_sleep

from .base import Buyable
from .events import LevelUpEvent, PlayerDeathEvent
from .item import Item, load_items
from .perk import Perk, attach_perk, attach_perks, load_perks, perk_is_active
from .weapon import Weapon, load_discoverable_weapons

# ================================================================================================

# TODO maybe read these from config
_MAX_ITEMS: int = 3
_MAX_WEAPONS: int = 3
_MAX_PERKS: int = 3

B = TypeVar("B", bound=Buyable)

# ================================================================================================

@dataclass
class Shop:
    area_name: str

    player_is_banned: bool = False

    _all_items: list[Item] = field(init=False)
    _all_weapons: list[Weapon] = field(init=False)
    _all_perks: list[Perk] = field(init=False)

    _item_inventory: list[Item] = field(init=False)
    _weapon_inventory: list[Weapon] = field(init=False)
    _perk_inventory: list[Perk] = field(init=False)

# ================================================================================================

    def __post_init__(self) -> None:
        self._all_items = [
            item for item in load_items()
            if item.areas and self.area_name in item.areas
        ]
        self._all_weapons = load_discoverable_weapons()
        self._all_perks = load_perks()
        self.reset_inventory()
        self._subscribe_listeners()

# ================================================================================================

    @staticmethod
    @attach_perks(BARTER_SAUCE, TRADE_SHIP, silent=True)
    def _discounted_cost(cost: int) -> int:
        return cost

    @property
    @attach_perk(BROWN_FRIDAY, silent=True)
    def max_items(self) -> int:
        return _MAX_ITEMS

    @property
    @attach_perk(BROWN_FRIDAY, silent=True)
    def max_weapons(self) -> int:
        return _MAX_WEAPONS

    @property
    @attach_perk(BROWN_FRIDAY, silent=True)
    def max_perks(self) -> int:
        return _MAX_PERKS

    @property
    def item_inventory(self) -> list[Item]:
        while len(self._item_inventory) < self.max_items:
            self._item_inventory.append(random.choice(self._all_items))
        return self.apply_discounts(self._item_inventory)

    @item_inventory.setter
    def item_inventory(self, items: list[Item]) -> None:
        self._item_inventory = items

    @property
    def weapon_inventory(self) -> list[Weapon]:
        if len(self._weapon_inventory) < self.max_weapons:
            available = [
                weapon for weapon in self._all_weapons
                if self.area_name in weapon.areas and weapon not in self._weapon_inventory
            ]
            random.shuffle(available)
            self._weapon_inventory += available[:self.max_weapons - len(self._weapon_inventory)]
        return self.apply_discounts(self._weapon_inventory)

    @weapon_inventory.setter
    def weapon_inventory(self, weapons: list[Weapon]) -> None:
        self._weapon_inventory = weapons

    @property
    def perk_inventory(self) -> list[Perk]:
        self._perk_inventory = [
            perk for perk in self._perk_inventory
            if not perk_is_active(perk.name)
        ]
        if len(self._perk_inventory) < self.max_perks:
            available = [
                perk for perk in self._all_perks
                if not (perk_is_active(perk.name) or perk in self._perk_inventory)
            ]
            random.shuffle(available)
            self._perk_inventory += available[:self.max_perks - len(self._perk_inventory)]
        return self.apply_discounts(self._perk_inventory)

    @perk_inventory.setter
    def perk_inventory(self, perks: list[Perk]) -> None:
        self._perk_inventory = perks

# ================================================================================================

    def apply_discounts(self, buyables: list[B]) -> list[B]:
        for buyable in buyables:
            original_cost = buyable.cost
            buyable.cost = round(max(5, self._discounted_cost(original_cost)))
        return buyables

# ================================================================================================

    def remove_listing(self, buyable: Buyable) -> None:
        if isinstance(buyable, Item) and buyable in self.item_inventory:
            self.item_inventory.remove(buyable)
        if isinstance(buyable, Weapon) and buyable in self.weapon_inventory:
            self.weapon_inventory.remove(buyable)
        if isinstance(buyable, Perk) and buyable in self.perk_inventory:
            self.perk_inventory.remove(buyable)

# ================================================================================================

    def reset_inventory(self) -> None:
        self._item_inventory = random.sample(
            self._all_items,
            k=min(self.max_items, len(self._all_items)),
        )

        sellable_weapons = [
            weapon for weapon in self._all_weapons
            if weapon.sell_value > 0
        ]
        self._weapon_inventory = random.sample(
            sellable_weapons,
            k=min(self.max_weapons, len(sellable_weapons)),
        )

        self.perk_inventory = random.sample(
            self._all_perks,
            k=min(self.max_perks, len(self._all_perks)),
        )
# ================================================================================================

    def ban_player(self):
        self.player_is_banned = True
        # TODO - some kind of sound effect here
        print_and_sleep(red(f"You think you're slick?"), 1)
        print_and_sleep(red(
            f"Well bad news - you're not welcome at this here shop here in the {self.area_name} no more, bozo."), 2)
        print_and_sleep(red(f"Come back when you level up."), 1)

# ================================================================================================

    def _subscribe_listeners(self):
        @subscribe_function(LevelUpEvent, PlayerDeathEvent, name_override=f"{self.area_name}_shop_reset")
        def handle_reset_events(_: Event):
            if self.player_is_banned:
                print_and_sleep(green(f"You can once again access the shop in the {self.area_name}."), 1.5)
            self.player_is_banned = False
            self.reset_inventory()

# ================================================================================================

    # for loading from save file
    def __setstate__(self, state):
        self.__dict__.update(state)
        self._subscribe_listeners()
