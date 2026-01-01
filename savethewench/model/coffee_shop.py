from dataclasses import dataclass, field
from typing import List, TypeVar

from savethewench.data.perks import BARTER_SAUCE, TRADE_SHIP
from .base import Buyable
from .coffee_item import CoffeeItem
from .perk import attach_perk
from ..data.coffee_items import Coffee_Items


@dataclass
class CoffeeShop: # class creation
    area_name: str

    _all_coffee_items: List[CoffeeItem] = field(init=False) # nature of list

    coffee_item_inventory: List[CoffeeItem] = field(init=False) # nature of list

    def __post_init__(self):
        self._all_coffee_items = [i for i in Coffee_Items] # creation of list with all items in that List

    @attach_perk(BARTER_SAUCE, TRADE_SHIP, silent=True) # apply perks to cost if owned
    def _discounted_cost(self, cost):
        return cost

    B = TypeVar("B", bound=Buyable)

    def apply_discounts(self, buyables: List[B]) -> List[B]: # apply any discounts to get the updated costs
        for buyable in buyables:
            buyable.cost = self._discounted_cost(buyable.cost)
        return buyables
