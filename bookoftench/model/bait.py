from dataclasses import dataclass
from typing import List

from bookoftench.data.bait import Bait_And_Lures
from bookoftench.model.base import Buyable
from bookoftench.ui import dim, cyan, orange, green, red, white


# ================================================================================================

@dataclass
class Bait(Buyable):
    name: str
    areas: list
    casts: int
    cost: int
    description: str

# ================================================================================================

    def get_simple_format(self) -> str:
        return dim(' | ').join([
            cyan(f"{self.name:<19}"),
            f"Casts: {cyan(self.casts)}",
        ])

    def __repr__(self):
        return dim(' | ').join([
            f"{cyan(f"{self.name:<16}")}",
            f"Cost: {orange(f'{self.cost:>2}')}",
            f"Casts: {cyan(f'{self.casts:>3}')}",
            f"{self.description}",
        ])

# ================================================================================================

def load_bait(name: str) -> Bait:
    matches = load_baits([name])
    if len(matches) == 0:
        raise ValueError(f"Could not find bait data for {name}")
    return matches[0]

def load_baits(restriction: List[str] = None) -> List[Bait]:
    return [Bait(**d) for d in Bait_And_Lures if restriction is None or d['name'] in restriction]