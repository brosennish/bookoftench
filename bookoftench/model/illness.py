from dataclasses import dataclass
from typing import List

from bookoftench.data.illnesses import Illnesses
from bookoftench.ui import dim, cyan, orange, yellow


@dataclass
class Illness:
    name: str
    description: str
    levels_until_death: int
    cost: int
    success_rate: float

    @property
    def causes_instant_death(self):
        return self.levels_until_death == 0

    def get_simple_format(self) -> str:
        return dim(' | ').join([
            cyan(f"{self.name:<19}"),
            f"Cost: +{orange(self.cost)}"
            f"Success rate: +{yellow(int(self.success_rate * 100))}",
        ])

    def __repr__(self):
        return self.get_simple_format()


def load_illnesses(restriction: List[str] = None) -> List[Illness]:
    return [Illness(**d) for d in Illnesses if restriction is None or d['name'] in restriction]

def load_illness(entry: dict | None) -> Illness | None:
    if entry:
        return Illness(**entry)
    else:
        return None
