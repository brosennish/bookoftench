import random
from dataclasses import dataclass, field
from typing import List, Dict

from savethewench.data.discoverables import Search_Discoverables, MYTHIC, LEGENDARY, RARE, UNCOMMON, COMMON


@dataclass
class Discoverable:
    name: str
    value: int
    hp: int
    rarity: str
    areas: List[str]


def search_discoverable_rarity() -> str:
    roll = random.random()

    if roll < 0.001:
        rarity = MYTHIC
    elif roll < 0.01:
        rarity = LEGENDARY
    elif roll < 0.1:
        rarity = RARE
    elif roll < 0.3:
        rarity = UNCOMMON
    else:
        rarity = COMMON

    return rarity

def load_discoverables() -> List[Discoverable]:
    return [Discoverable(**d) for d in Search_Discoverables]