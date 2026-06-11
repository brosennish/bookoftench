import random
from dataclasses import dataclass
from typing import List

from bookoftench.data.fishing_items import Fishing_Items
from bookoftench.model.base import Buyable
from bookoftench.ui import dim, cyan, orange, yellow, green, red, blue, purple


# ================================================================================================

@dataclass
class FishingItem(Buyable):
    name: str
    description: str
    cost: int
    min_turns: int
    max_turns: int
    speed_reduction: float
    stamina_reduction: float
    rage_reduction: float
    strength_reduction: float
    spit_hook_prevention: bool
    count: int = 1
    turns: int = 0

# ================================================================================================

    def __post_init__(self):
        self.turns = random.randint(self.min_turns, self.max_turns)

# ================================================================================================

    def get_simple_format(self) -> str:
        return dim(' | ').join([
            cyan(f"{self.name:<16}"),
            orange(f"{self.cost}c"),
        ])

    def __repr__(self):
        effects = []

        if self.speed_reduction:
            effects.append(f"Speed {cyan(f'-{int(self.speed_reduction * 100)}%')}")

        if self.stamina_reduction:
            effects.append(f"Stamina {yellow(f'+{int(self.stamina_reduction * 100)}%')}")

        if self.rage_reduction:
            effects.append(f"Rage {red(f'-{int(self.rage_reduction * 100)}%')}")

        if self.strength_reduction:
            effects.append(f"Strength {orange(f'-{int(self.strength_reduction * 100)}%')}")

        if self.spit_hook_prevention:
            effects.append(blue("No Spit Hook"))

        turns = (
            str(self.min_turns)
            if self.min_turns == self.max_turns
            else f"{self.min_turns}-{self.max_turns}"
        )

        return dim(' | ').join([
            cyan(f"{self.name:<16}"),
            f"Cost: {orange(self.cost)}",
            f"Turns: {purple(f'{turns:<3}')}",
            ", ".join(effects)
        ])

# ================================================================================================

def load_fishing_item(name: str) -> FishingItem:
    matches = load_fishing_items([name])
    if len(matches) == 0:
        raise ValueError(f"Could not find fishing item data for {name}")
    return matches[0]

def load_fishing_items(restriction: List[str] = None) -> List[FishingItem]:
    return [FishingItem(**d) for d in Fishing_Items if restriction is None or d['name'] in restriction]