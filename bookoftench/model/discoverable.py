import random
from dataclasses import dataclass
from typing import List, Callable, Any

from bookoftench.data.discoverables import Search_Discoverables, MYTHIC, LEGENDARY, RARE, UNCOMMON, COMMON
from bookoftench.ui import purple, orange, blue, green, yellow

# ================================================================================================

@dataclass
class Discoverable:
    pre: str | None
    name: str
    value: int
    hp: int
    rarity: str
    areas: List[str]
    count: int
    desc: str | None
    quest_item: bool = False
    event_item: bool = False
    related_event: str | None = None

# ================================================================================================

def search_discoverable_rarity(player) -> str:
    roll = random.random()
    luck = player.luck

    if roll < luck * 0.0004:
        rarity = MYTHIC
    elif roll < luck * 0.0014:
        rarity = LEGENDARY
    elif roll < luck * 0.08:
        rarity = RARE
    elif roll < luck * 0.3:
        rarity = UNCOMMON
    else:
        rarity = COMMON

    return rarity

# ================================================================================================

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
