import random
from dataclasses import dataclass

from bookoftench.data.fish import COMMON, UNCOMMON, RARE
from bookoftench.ui import dim, cyan, orange, green, yellow, blue

# ================================================================================================

@dataclass
class Fish():
    name: str
    rarity: str
    areas: list[str]
    time: list[str]
    moon: list[str]
    min_length: int
    max_length: int
    length: int
    min_weight_factor: float
    max_weight_factor: float
    weight: int
    value_for_size: float
    value: int
    hp_for_size: float
    hp: int
    rage: float
    speed: float
    strength: float
    preferred_bait: list[str]
    spit_hook_chance: float
    catch_location: str

# ================================================================================================

    def __post_init__(self):
        self.length = random.randint(self.min_length, self.max_length)
        weight_factor = random.uniform(self.min_weight_factor, self.max_weight_factor)
        self.weight = round(((self.length ** 2) * weight_factor) / 144)
        size = self.length * self.weight
        self.hp = round(size * self.hp_for_size)
        self.value = round(size * self.value_for_size)

# ================================================================================================

    def get_rarity(self):
        if self.rarity == COMMON:
            return yellow(self.rarity)
        elif self.rarity == UNCOMMON:
            return green(self.rarity)
        elif self.rarity == RARE:
            return blue(self.rarity)
        else:
            return orange(self.rarity)

    def get_simple_format(self) -> str:
        return dim(' | ').join([
            cyan(f"{self.name:<19}"),
            f"{self.get_rarity()}",
            f"{self.length} in",
            f"{self.weight} lbs",
            blue(f"{self.catch_location}"),
        ])

    def __repr__(self):
        return dim(' | ').join([
            cyan(f"{self.name:<19}"),
            f"{self.get_rarity()}",
            f"Value: {orange(self.hp)}",
            f"HP: {green(self.hp)}",
            f"{self.length} in",
            f"{self.weight} lbs",
        ])
