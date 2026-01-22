import random
from dataclasses import dataclass, field
from typing import List, TypeVar

from savethewench.data.perks import BROWN_FRIDAY, BARTER_SAUCE, TRADE_SHIP
from savethewench.event_base import Event
from savethewench.event_logger import subscribe_function
from .base import Buyable
from .events import LevelUpEvent, PlayerDeathEvent
from .item import Item, load_items
from .perk import Perk, load_perks, attach_perk, attach_perks
from .weapon import Weapon, load_discoverable_weapons

# TODO maybe read these from config
_MAX_ITEMS: int = 3
_MAX_WEAPONS: int = 3
_MAX_PERKS: int = 3


@dataclass
class Shop:
    area_name: str

    _all_items: List[Item] = field(init=False)
    _all_weapons: List[Weapon] = field(init=False)
    _all_perks: List[Perk] = field(init=False)

    _item_inventory: List[Item] = field(init=False)
    _weapon_inventory: List[Weapon] = field(init=False)
    _perk_inventory: List[Perk] = field(init=False)

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
    def item_inventory(self) -> List[Item]:
        while len(self._item_inventory) < self.max_items:
            self._item_inventory.append(random.choice(self._all_items))
        return self.apply_discounts(self._item_inventory)

    @item_inventory.setter
    def item_inventory(self, items: List[Item]):
        self._item_inventory = items

    @property
    def weapon_inventory(self) -> List[Weapon]:
        while len(self._weapon_inventory) < self.max_weapons:
            self._weapon_inventory.append(Weapon(**random.choice(self._all_weapons).__dict__))
        return self.apply_discounts(self._weapon_inventory)

    @weapon_inventory.setter
    def weapon_inventory(self, weapons: List[Weapon]):
        self._weapon_inventory = weapons

    @property
    def perk_inventory(self) -> List[Perk]:
        while len(self._perk_inventory) < self.max_perks:
            self._perk_inventory.append(Perk(**random.choice(self._perk_inventory).__dict__))
        return self.apply_discounts(self._perk_inventory)

    @perk_inventory.setter
    def perk_inventory(self, perks: List[Perk]):
        self._perk_inventory = perks

    def __post_init__(self):
        self._all_items = [i for i in load_items() if self.area_name in i.areas]
        self._all_weapons = load_discoverable_weapons()
        self._all_perks = load_perks()
        self.reset_inventory()
        self._subscribe_listeners()

    @attach_perks(BARTER_SAUCE, TRADE_SHIP, silent=True)
    def _discounted_cost(self, cost) -> int:
        return cost

    B = TypeVar("B", bound=Buyable)

    def apply_discounts(self, buyables: List[B]) -> List[B]:
        for buyable in buyables:
            buyable.cost = self._discounted_cost(buyable.cost)
        return buyables

    def remove_listing(self, buyable: Buyable) -> None:
        if isinstance(buyable, Item) and buyable in self.item_inventory:
            self.item_inventory.remove(buyable)
        if isinstance(buyable, Weapon) and buyable in self.weapon_inventory:
            self.weapon_inventory.remove(buyable)
        if isinstance(buyable, Perk) and buyable in self.perk_inventory:
            self.perk_inventory.remove(buyable)

    def reset_inventory(self) -> None:
        self._item_inventory = random.sample(self._all_items, k=min(self.max_items, len(self._all_items)))
        self._weapon_inventory = random.sample([w for w in self._all_weapons if w.sell_value > 0],
                                               k=min(self.max_weapons, len(self._all_weapons)))
        self.perk_inventory = random.sample(self._all_perks, k=min(self.max_perks, len(self._all_perks)))

    def _subscribe_listeners(self):
        @subscribe_function(LevelUpEvent, PlayerDeathEvent)
        def handle_level_up(_: Event):
            self.reset_inventory()

    # for loading from save file
    def __setstate__(self, state):
        self.__dict__.update(state)
        self._subscribe_listeners()
