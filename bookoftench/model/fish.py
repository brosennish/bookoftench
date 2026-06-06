import random
from dataclasses import dataclass
from typing import List

from bookoftench.data import fish as f
from bookoftench.data.fish import VARIANTS, Fish_Species
from bookoftench.ui import dim, cyan, orange, green, yellow, blue

# ================================================================================================

@dataclass
class Fish:
    name: str
    base_name: str
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
    rage: float
    speed: float
    strength: float
    preferred_bait: list[str]
    spit_hook_chance: float
    max_age: int

    sex: str | None = None
    state: str | None = None
    variant: str | None = None
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
        self.get_state()
        self.get_variant()
        self.value = round(size * self.value_for_size)

# ================================================================================================

    def get_variant(self):
        variants = VARIANTS.copy()
        random.shuffle(variants)
        for i in variants:
            if random.random() < i['chance']:
                self.variant = i['name']
                break

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

    def get_rarity(self):
        if self.rarity == f.COMMON:
            return yellow(self.rarity)
        elif self.rarity == f.UNCOMMON:
            return green(self.rarity)
        elif self.rarity == f.RARE:
            return blue(self.rarity)
        else:
            return orange(self.rarity)

# ================================================================================================

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

# ================================================================================================

def load_fish(name: str) -> Fish:
    matches = load_fishes([name])
    if len(matches) == 0:
        raise ValueError(f"Could not find fish data for {name}")
    return matches[0]

def load_fishes(restriction: List[str] = None) -> List[Fish]:
    return [Fish(**d) for d in Fish_Species if restriction is None or d['name'] in restriction]