from dataclasses import dataclass

from bookoftench.data.fishing_areas import Fishing_Areas
from bookoftench.ui import blue, cyan, dim, orange

# ================================================================================================

@dataclass
class FishingArea:
    name: str
    bite_chance: float
    hook_chance: float
    lvl: int
    pull_mult: float
    run_mult: float
    min_hook_distance: int
    max_hook_distance: int
    escape_distance: int
    travel_cost: int
    casts: int

# ================================================================================================

    def get_simple_format(self) -> str:
        return dim(" | ").join([
            blue(f"{self.name:<10}"),
            f"Cost: {orange(self.travel_cost)}",
            f"Casts: {cyan(self.casts)}",
        ])

    def __repr__(self) -> str:
        return self.get_simple_format()

# ================================================================================================

def load_fishing_area(name: str) -> FishingArea:
    matches = load_fishing_areas([name])

    if not matches:
        raise ValueError(f"Could not find fishing area data for {name}")

    return matches[0]


def load_fishing_areas(restriction: list[str] | None = None) -> list[FishingArea]:
    return [
        FishingArea(**data)
        for data in Fishing_Areas
        if restriction is None or data["name"] in restriction
    ]