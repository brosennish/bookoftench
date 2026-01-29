from dataclasses import dataclass

from savethewench.model.base import Buyable
from savethewench.ui import cyan, orange, dim, purple


@dataclass
class Ritual(Buyable):
    name: str
    description: str
    cost: int

    def __repr__(self):
        return dim(' | ').join([
            cyan(f"{self.name:<15}"),
            f"Cost: {orange(self.cost)}",
            f"{purple(self.description)}",
        ])