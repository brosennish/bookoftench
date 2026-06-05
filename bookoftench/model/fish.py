import random
from dataclasses import dataclass

from bookoftench.data import fish as f
from bookoftench.ui import dim, cyan, orange, green, yellow, blue

# ================================================================================================

@dataclass
class Fish:
    name: str
    description: str
    rarity: str
    areas: list[str]
    time: list[str]
    moon: list[str] | None
    min_length: int
    max_length: int
    length: int
    min_weight_factor: float
    max_weight_factor: float
    weight: int | float
    value_for_size: float
    value: int
    hp_for_size: float
    hp: int
    rage: float
    speed: float
    strength: float
    preferred_bait: list[str]
    spit_hook_chance: float
    sex: str
    state: str
    max_age: int
    age: int | None = None
    catch_location: str | None = None # assigned when caught

# ================================================================================================

    def __post_init__(self):
        self.age = random.randint(1, self.max_age)
        self.sex = random.choice([f.MALE, f.FEMALE])
        self.length = random.randint(self.min_length, self.max_length)
        weight_factor = random.uniform(self.min_weight_factor, self.max_weight_factor)
        self.weight = round(((self.length ** 2) * weight_factor) / 144)
        size = self.length * self.weight
        self.state = self.get_state()
        self.hp = round(size * self.hp_for_size)
        self.value = round(size * self.value_for_size)

# ================================================================================================

    def get_state(self):
        roll = random.random()
        if roll < 0.05:
            self.state = f.ENRAGED
        elif roll < 0.15:
            self.state = f.AGITATED
        elif roll < 0.35:
            self.state = f.SPOOKED
        else:
            self.state = f.CALM

        return self.state

    def get_rarity(self):
        if self.rarity == f.COMMON:
            return yellow(self.rarity)
        elif self.rarity == f.UNCOMMON:
            return green(self.rarity)
        elif self.rarity == f.RARE:
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
            f"Value: {orange(self.value)}",
            f"HP: {green(self.hp)}",
            f"{self.length} in",
            f"{self.weight} lbs",
        ])
