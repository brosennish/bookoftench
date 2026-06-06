from dataclasses import dataclass
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