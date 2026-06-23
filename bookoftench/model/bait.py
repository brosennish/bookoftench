from dataclasses import dataclass
from typing import List

from bookoftench.data.bait import Bait_And_Lures
from bookoftench.model.base import Buyable
from bookoftench.ui import dim, cyan, orange, green, red, white


from dataclasses import dataclass

from bookoftench.data.bait import Bait_And_Lures
from bookoftench.model.base import Buyable
from bookoftench.ui import cyan, dim, orange

# ================================================================================================

@dataclass
class Bait(Buyable):
    name: str
    areas: list[str]
    casts: int
    cost: int
    description: str

    def get_simple_format(self) -> str:
        return dim(" | ").join([
            cyan(f"{self.name:<19}"),
            f"Casts: {cyan(self.casts)}",
        ])

    def __repr__(self) -> str:
        return dim(" | ").join([
            cyan(f"{self.name:<16}"),
            f"Cost: {orange(f'{self.cost:>2}')}",
            f"Casts: {cyan(f'{self.casts:>3}')}",
            self.description,
        ])


# ================================================================================================

def load_bait(name: str) -> Bait:
    matches = load_baits([name])

    if not matches:
        raise ValueError(f"Could not find bait data for {name}")

    return matches[0]


def load_baits(restriction: list[str] | None = None) -> list[Bait]:
    return [
        Bait(**data)
        for data in Bait_And_Lures
        if restriction is None or data["name"] in restriction
    ]