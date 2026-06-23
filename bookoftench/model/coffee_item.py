from dataclasses import dataclass

from bookoftench.model.base import Buyable
from bookoftench.ui import cyan, dim, green, orange, red

# ================================================================================================

@dataclass
class CoffeeItem(Buyable):
    name: str
    hp: int
    cost: int
    risk: float

    def get_simple_format(self) -> str:
        return dim(" | ").join([
            cyan(f"{self.name:<19}"),
            f"HP: +{green(self.hp)}",
        ])

    def __repr__(self) -> str:
        risk_percent = int(self.risk * 100)

        return dim(" | ").join([
            cyan(f"{self.name:<19}"),
            f"Cost: {orange(self.cost)}",
            f"HP: +{green(self.hp)}",
            f"Risk: {red(risk_percent)}%",
        ])
