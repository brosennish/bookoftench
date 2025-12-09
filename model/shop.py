import random

from dataclasses import dataclass, field
from typing import List, Dict, Union

from model.item import Item, load_items
from model.perk import Perk, load_perks
from model.weapon import load_weapons

# TODO maybe read these from config
_MAX_ITEMS: int = 4
_MAX_WEAPONS: int = 4
_MAX_PERKS: int = 4

@dataclass
class Shop:

    _all_items: List[Item] = field(init=False)
    _all_weapons: List[Item] = field(init=False)
    _all_perks: List[Perk] = field(init=False)

    item_inventory: List[Item] = field(init=False)
    weapon_inventory: List[Dict] = field(init=False)
    perk_inventory: List[Dict] = field(init=False)

    def __post_init__(self):
        self._all_items = load_items()
        self._all_weapons = load_weapons()
        self._all_perks = load_perks()
        self.item_inventory = random.sample(self._all_items, k=min(_MAX_ITEMS, len(self._all_items)))
        self.weapon_inventory = random.sample([w for w in self._all_weapons if w.sell_value > 0],
                                              k=min(_MAX_WEAPONS, len(self._all_weapons)))
        self.perk_inventory = random.sample(self._all_perks, k=min(_MAX_PERKS, len(self._all_perks)))
