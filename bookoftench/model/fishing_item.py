import random
from dataclasses import dataclass

from bookoftench.data.fishing_items import Fishing_Items
from bookoftench.model.base import Buyable
from bookoftench.ui import blue, cyan, dim, orange, purple, red, yellow

# ================================================================================================

@dataclass
class FishingItem(Buyable):
    name: str
    description: str
    type: str
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

    def __post_init__(self) -> None:
        super().__post_init__()
        self.turns = random.randint(self.min_turns, self.max_turns)

# ================================================================================================

    def get_simple_format(self) -> str:
        return dim(" | ").join([
            cyan(f"{self.name:<16}"),
            orange(f"{self.cost}c"),
        ])

    def _effect_text(self):
        effects = []

        if self.speed_reduction:
            effects.append(f"Speed {cyan(f'-{int(self.speed_reduction * 100)}%')}")

        if self.stamina_reduction:
            effects.append(f"Stamina Loss {yellow(f'+{int(self.stamina_reduction * 100)}%')}")

        if self.rage_reduction:
            effects.append(f"Rage Gain {red(f'-{int(self.rage_reduction * 100)}%')}")

        if self.strength_reduction:
            effects.append(f"Strength {orange(f'-{int(self.strength_reduction * 100)}%')}")

        if self.spit_hook_prevention:
            effects.append(blue("No Spit Hook"))

        return ", ".join(effects)

    def _turn_text(self):
        return (
            str(self.min_turns)
            if self.min_turns == self.max_turns
            else f"{self.min_turns}-{self.max_turns}"
        )

    def shop_repr(self):
        return dim(' | ').join([
            cyan(f"{self.name:<16}"),
            f"Cost: {orange(self.cost)}",
            f"Turns: {purple(f'{self._turn_text():<3}')}",
            self._effect_text()
        ])

    def inventory_repr(self):
        return dim(' | ').join([
            cyan(f"{self.name:<16}"),
            f"Count: {cyan(str(self.count))}",
            f"Turns: {purple(f'{self._turn_text():<3}')}",
            self._effect_text()
        ])

    def __repr__(self):
        return self.shop_repr()

# ================================================================================================

def load_fishing_item(name: str) -> FishingItem:
    matches = load_fishing_items([name])

    if not matches:
        raise ValueError(f"Could not find fishing item data for {name}")

    return matches[0]


def load_fishing_items(restriction: list[str] | None = None) -> list[FishingItem]:
    return [
        FishingItem(**data)
        for data in Fishing_Items
        if restriction is None or data["name"] in restriction
    ]