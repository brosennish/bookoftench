import random
from dataclasses import dataclass, field
from typing import List

from savethewench.data.perks import BROWN_FRIDAY
from .base import Buyable
from .item import Item, load_items
from .perk import Perk, load_perks, attach_perk
from .weapon import load_weapons, Weapon

# TODO maybe read these from config
_MAX_ITEMS: int = 3
_MAX_WEAPONS: int = 3
_MAX_PERKS: int = 3


@dataclass
class Shop:
    _all_items: List[Item] = field(init=False)
    _all_weapons: List[Weapon] = field(init=False)
    _all_perks: List[Perk] = field(init=False)

    item_inventory: List[Item] = field(init=False)
    weapon_inventory: List[Weapon] = field(init=False)
    perk_inventory: List[Perk] = field(init=False)

    @property
    @attach_perk(BROWN_FRIDAY, silent=True)
    def max_items(self):
        return _MAX_ITEMS

    @property
    @attach_perk(BROWN_FRIDAY, silent=True)
    def max_weapons(self):
        return _MAX_WEAPONS

    @property
    @attach_perk(BROWN_FRIDAY, silent=True)
    def max_perks(self):
        return _MAX_PERKS

    def __post_init__(self):
        self._all_items = load_items()
        self._all_weapons = load_weapons()
        self._all_perks = load_perks()
        self.reset_inventory()

    def remove_listing(self, buyable: Buyable):
        if isinstance(buyable, Item) and buyable in self.item_inventory:
            self.item_inventory.remove(buyable)
        if isinstance(buyable, Weapon) and buyable in self.weapon_inventory:
            self.weapon_inventory.remove(buyable)
        if isinstance(buyable, Perk) and buyable in self.perk_inventory:
            self.perk_inventory.remove(buyable)

    def reset_inventory(self):
        self.item_inventory = random.sample(self._all_items, k=min(self.max_items, len(self._all_items)))
        self.weapon_inventory = random.sample([w for w in self._all_weapons if w.sell_value > 0],
                                              k=min(self.max_weapons, len(self._all_weapons)))
        self.perk_inventory = random.sample(self._all_perks, k=min(self.max_perks, len(self._all_perks)))
