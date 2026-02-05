from dataclasses import dataclass, field
from typing import List, TypeVar

from bookoftench.data.coffee_items import Coffee_Items
from bookoftench.data.perks import BARTER_SAUCE, TRADE_SHIP, TENCH_GENES, WrapperIndices
from .coffee_item import CoffeeItem
from .perk import attach_perk, attach_perks


@dataclass
class CoffeeShop:  # class creation
    _coffee_item_inventory: List[CoffeeItem] = field(init=False)  # nature of list

    def __post_init__(self):
        self._all_coffee_items = [i for i in Coffee_Items]  # creation of list with all items in that List

    @property
    def coffee_inventory(self) -> List[CoffeeItem]:
        return [
            CoffeeItem(**item_dict)
            for item_dict in Coffee_Items
        ]

    @attach_perks(BARTER_SAUCE, TRADE_SHIP, silent=True)  # apply perks to cost if owned
    def _discounted_cost(self, cost):
        return cost

    @attach_perk(TENCH_GENES, WrapperIndices.TenchGenes.RISK, silent=True)  # apply perks to cost if owned
    def _discounted_risk(self, risk):
        return risk

    C = TypeVar("C", bound=CoffeeItem)

    def apply_discounts(self, buyables: List[C]) -> List[C]:  # apply any discounts to get the updated costs
        for buyable in buyables:
            buyable.cost = max(3, self._discounted_cost(buyable.cost))
            buyable.risk = max(0.05, self._discounted_risk(buyable.risk))
        return buyables
