from dataclasses import dataclass
from typing import List

from data.perks import Perks


@dataclass
class Perk:
    name: str
    cost: int
    description: str


def load_perks(restriction: List[str] = None) -> List[Perk]:
    return [Perk(**d) for d in Perks if restriction is None or d['name'] in restriction]
