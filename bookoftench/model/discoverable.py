import random
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from bookoftench.data.discoverables import (
    COMMON,
    LEGENDARY,
    MYTHIC,
    RARE,
    Search_Discoverables,
    UNCOMMON,
)
from bookoftench.ui import blue, green, orange, purple, yellow

# ================================================================================================

@dataclass
class Discoverable:
    pre: str | None
    name: str
    value: int
    hp: int
    rarity: str
    areas: list[str]
    desc: str | None
    count: int = 0

# ================================================================================================

def search_discoverable_rarity(player) -> str:
    roll = random.random()
    luck = player.luck

    if roll < luck * 0.0004:
        return MYTHIC

    if roll < luck * 0.0014:
        return LEGENDARY

    if roll < luck * 0.08:
        return RARE

    if roll < luck * 0.3:
        return UNCOMMON

    return COMMON

# ================================================================================================

def rarity_color(rarity: str) -> Callable[[Any], str]:
    if rarity == MYTHIC:
        return orange

    if rarity == LEGENDARY:
        return purple

    if rarity == RARE:
        return blue

    if rarity == UNCOMMON:
        return green

    return yellow

# ================================================================================================

def load_discoverables() -> list[Discoverable]:
    return [Discoverable(**data) for data in Search_Discoverables]
