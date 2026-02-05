import random
from dataclasses import dataclass
from typing import List, Callable, Any

from bookoftench.data.discoverables import Search_Discoverables, MYTHIC, LEGENDARY, RARE, UNCOMMON, COMMON
from bookoftench.ui import purple, orange, blue, green, yellow


@dataclass
class Discoverable:
    pre: str | None
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


def rarity_color(rarity: str) -> Callable[[Any], str] | Any:
    if rarity == MYTHIC:
        return orange
    elif rarity == LEGENDARY:
        return purple
    elif rarity == RARE:
        return blue
    elif rarity == UNCOMMON:
        return green
    else:
        return yellow


def load_discoverables() -> List[Discoverable]:
    return [Discoverable(**d) for d in Search_Discoverables]
