from dataclasses import dataclass, field

from bookoftench.data.coffee_items import Coffee_Items
from bookoftench.data.perks import BARTER_SAUCE, TENCH_GENES, TRADE_SHIP, WrapperIndices
from .coffee_item import CoffeeItem
from .perk import attach_perk, attach_perks

# ================================================================================================

@dataclass
class CoffeeShop:
    _coffee_item_inventory: list[CoffeeItem] = field(init=False)

    def __post_init__(self) -> None:
        self._all_coffee_items = [item for item in Coffee_Items]

    @property
    def coffee_inventory(self) -> list[CoffeeItem]:
        return [
            CoffeeItem(**item_dict)
            for item_dict in Coffee_Items
        ]

# ================================================================================================

    @attach_perks(BARTER_SAUCE, TRADE_SHIP, silent=True)
    def _discounted_cost(self, cost: int) -> int:
        return cost

    @attach_perk(TENCH_GENES, WrapperIndices.TenchGenes.RISK, silent=True)
    def _discounted_risk(self, risk: float) -> float:
        return risk

# ================================================================================================

    def apply_discounts(self, buyables: list[CoffeeItem]) -> list[CoffeeItem]:
        for buyable in buyables:
            buyable.cost = max(3, self._discounted_cost(buyable.cost))
            buyable.risk = max(0.05, self._discounted_risk(buyable.risk))

        return buyables
