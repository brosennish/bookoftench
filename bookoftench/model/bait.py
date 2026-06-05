from dataclasses import dataclass
from bookoftench.model.base import Buyable
from bookoftench.ui import dim, cyan, orange, green, red

# ================================================================================================

@dataclass
class Bait(Buyable):
    name: str
    areas: list
    casts: int
    cost: int

    def get_casts(self):
        if self.casts > 1:
            return green(self.casts)
        else:
            return red(self.casts)

    def get_simple_format(self) -> str:
        return dim(' | ').join([
            cyan(f"{self.name:<19}"),
            f"Casts: {self.get_casts()}",
        ])

    def __repr__(self):
        return dim(' | ').join([
            cyan(f"{self.name:<19}"),
            f"Cost: {orange(self.cost)}",
            f"Casts: {self.get_casts()}",
        ])