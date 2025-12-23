import random
from dataclasses import dataclass, field
from typing import List, TypeVar

from savethewench.data.perks import BROWN_FRIDAY, BARTER_SAUCE, TRADE_SHIP
from savethewench.event_logger import subscribe_function
from .base import Buyable
from .events import LevelUpEvent, PlayerDeathEvent
from .item import Item, load_items
from .perk import Perk, load_perks, attach_perk
from .weapon import load_weapons, Weapon
from ..event_base import Event

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
        self._subscribe_listeners()

    @attach_perk(BARTER_SAUCE, TRADE_SHIP, silent=True)
    def _discounted_cost(self, cost):
        return cost

    B = TypeVar("B", bound=Buyable)

    def apply_discounts(self, buyables: List[B]) -> List[B]:
        for buyable in buyables:
            buyable.cost = self._discounted_cost(buyable.cost)
        return buyables

    def remove_listing(self, buyable: Buyable):
        if isinstance(buyable, Item) and buyable in self.item_inventory:
            self.item_inventory.remove(buyable)
        if isinstance(buyable, Weapon) and buyable in self.weapon_inventory:
            self.weapon_inventory.remove(buyable)
        if isinstance(buyable, Perk) and buyable in self.perk_inventory:
            self.perk_inventory.remove(buyable)

    def reset_inventory(self):
        self.item_inventory = self.apply_discounts(
            random.sample(self._all_items, k=min(self.max_items, len(self._all_items))))
        self.weapon_inventory = self.apply_discounts(
            random.sample([w for w in self._all_weapons if w.sell_value > 0],
                                              k=min(self.max_weapons, len(self._all_weapons))))
        self.perk_inventory = self.apply_discounts(
            random.sample(self._all_perks, k=min(self.max_perks, len(self._all_perks))))

    def _subscribe_listeners(self):
        @subscribe_function(LevelUpEvent, PlayerDeathEvent)
        def handle_level_up(_: Event):
            self.reset_inventory()

    # for loading from save file
    def __setstate__(self, state):
        self.__dict__.update(state)
        self._subscribe_listeners()