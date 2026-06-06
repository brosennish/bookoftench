from dataclasses import dataclass
from typing import List

from bookoftench.data.fishing_areas import Fishing_Areas
from bookoftench.ui import dim, orange, green, blue

# ================================================================================================

@dataclass
class FishingArea:
    name: str
    bite_chance: float
    hook_chance: float
    lvl: int
    min_hook_distance: int
    max_hook_distance: int
    escape_distance: int
    travel_cost: int
    casts: int

# ================================================================================================

    def get_simple_format(self) -> str:
        return dim(' | ').join([
            blue(f"{self.name:<19}"),
            f"Cost: {orange(self.travel_cost)}",
            f"Casts: {green(self.casts)}",
        ])

    def __repr__(self):
        return self.get_simple_format()

# ================================================================================================

def load_fishing_area(name: str) -> FishingArea:
    matches = load_fishing_areas([name])
    if len(matches) == 0:
        raise ValueError(f"Could not find fishing area data for {name}")
    return matches[0]

def load_fishing_areas(restriction: List[str] = None) -> List[FishingArea]:
    return [FishingArea(**d) for d in Fishing_Areas if restriction is None or d['name'] in restriction]