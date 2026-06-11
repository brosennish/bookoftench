import random
from dataclasses import dataclass, field
from typing import List

from bookoftench.data import fish as f
from bookoftench.data.fish import VARIANTS, Fish_Species, TWO_HEADED, TRANSLUCENT, THREE_EYED, TELEPATHIC, SCARRED, \
    SAPIENT, RADIOACTIVE, ONE_EYED, IRIDESCENT, GLOWING, ALBINO, PREGNANT
from bookoftench.ui import dim, cyan, orange, green, yellow, blue, purple


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

    min_weight_factor: float
    max_weight_factor: float
    base_value: int

    rage_factor: float
    speed: float
    strength: float
    max_stamina: int
    preferred_bait: list[str]
    spit_hook_chance: float
    max_age: int
    protected: bool

    distance: int = 0
    stamina: int = 0
    rage: int = 0

    base_name: str | None = None
    length: int | None = None
    weight: int | float | None = None
    value: int | None = None
    size: int | None = None
    size_percentile: int | None = None
    sex: str | None = None
    state: str | None = None
    variant: str | None = None
    age: int | None = None

    adrenaline_ready: bool = True

    caught: bool = False
    catch_location: str | None = None # assigned when caught
    lost: bool = False

    # --- ObserveFish ---
    observed_characteristics: list[str] = field(default_factory=list)
    species_observed: bool = False
    variant_observed: bool = False
    rarity_observed: bool = False
    strength_observed: bool = False
    speed_observed: bool = False
    rage_factor_observed: bool = False
    species_known: bool = False

    # --- FishingItems ---
    barb_hook_active: bool = False
    speed_multiplier: float | None = 1
    stamina_multiplier: float | None = 1
    rage_multiplier: float | None = 1
    strength_multiplier: float | None = 1

# ================================================================================================

    def __post_init__(self):
        # --- core characteristics ---
        self.base_name = self.name
        self.age = random.randint(1, self.max_age)
        self.sex = self.get_sex()

        # --- size and value ---
        self.length = random.randint(self.min_length, self.max_length)
        weight_factor = random.uniform(self.min_weight_factor, self.max_weight_factor)
        self.weight = round(((self.length ** 2) * weight_factor) / 144, 2)
        self.size = self.get_size()
        self.size_percentile = self.get_size_percentile(weight_factor)
        self.value = self.get_value()

        # --- state, variant, and related variables ---
        self.get_state()
        self.get_variant()
        if self.variant:
            self.name = f"{self.variant} {self.base_name}"
        self.stamina = self.max_stamina
        self.rage = random.randint(5, 15)

# ================================================================================================

    @staticmethod
    def get_sex() -> str:
        if random.random() < 0.45:
            return f.MALE
        elif random.random() < 0.9:
            return f.FEMALE
        else:
            return f.HERMAPHRODITE

    def get_size(self) -> float | int:
        size = self.length * self.weight
        return size

    def get_size_percentile(self, weight_factor: float) -> int:
        length_pct = (
                (self.length - self.min_length) / (self.max_length - self.min_length)
        )

        weight_pct = (
                (weight_factor - self.min_weight_factor) / (self.max_weight_factor - self.min_weight_factor)
        )

        size_pct = (length_pct + weight_pct) / 2

        return round(size_pct * 100)

    def get_value(self) -> int:
        size_pct = self.size_percentile / 100
        modifier = 0.80 + (size_pct * 0.4)
        value = round(self.base_value * modifier)

        return max(1, value)

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

    def get_variant(self):
        variants = VARIANTS.copy()
        random.shuffle(variants)
        if random.random() < 0.5:
            for i in variants:
                if random.random() < i['chance']:
                    self.variant = i['name']
                    self.init_variant_effects()
                    break

    def init_variant_effects(self):
        if self.variant == ALBINO:
            self.value *= 1.1

        elif self.variant == GLOWING:
            self.value *= 1.8
            self.rage_factor *= 1.15

        elif self.variant == IRIDESCENT:
            self.value *= 2.0
            self.max_stamina *= 1.1

        elif self.variant == ONE_EYED:
            self.value *= 0.95
            self.speed *= 0.9
            self.rage_factor *= 1.2

        elif self.variant == PREGNANT and self.sex != f.MALE:
            self.value *= 1.1
            self.speed *= 0.9
            self.rage_factor *= 1.2

        elif self.variant == RADIOACTIVE:
            self.value *= 0.75
            self.rage_factor *= 1.4
            self.strength *= 1.15
            self.max_stamina *= 1.15

        elif self.variant == SAPIENT:
            self.value *= 5.0
            self.rage_factor *= 0.8
            self.max_stamina *= 1.2

        elif self.variant == SCARRED:
            self.strength *= 1.2
            self.max_stamina *= 1.15

        elif self.variant == TELEPATHIC:
            self.value *= 3.0
            self.rage_factor *= 0.7
            self.speed *= 1.2

        elif self.variant == THREE_EYED:
            self.value *= 1.7
            self.rage_factor *= 1.1
            self.speed *= 1.1

        elif self.variant == TRANSLUCENT:
            self.value *= 1.5
            self.strength *= 0.9
            self.speed *= 1.15

        elif self.variant == TWO_HEADED:
            self.value *= 2.0
            self.rage_factor *= 1.35
            self.strength *= 1.25
            self.max_stamina *= 1.2

        self.value = round(self.value)
        self.max_stamina = round(self.max_stamina)
        self.stamina = self.max_stamina

    def get_rarity_text(self):
        if self.rarity == f.COMMON:
            return yellow(self.rarity)
        elif self.rarity == f.UNCOMMON:
            return green(self.rarity)
        elif self.rarity == f.RARE:
            return blue(self.rarity)
        elif self.rarity == f.LEGENDARY:
            return orange(self.rarity)
        else:
            return purple(self.rarity)

    def get_rarity_color(self):
        if self.rarity == f.COMMON:
            return yellow
        elif self.rarity == f.UNCOMMON:
            return green
        elif self.rarity == f.RARE:
            return blue
        else:
            return orange

# ================================================================================================

    def get_simple_format(self) -> str:
        return dim(' | ').join([
            cyan(f"{self.name:<19}"),
            f"{self.get_rarity_text()}",
            f"{self.length} in",
            f"{self.weight} lbs",
            blue(f"{self.catch_location}"),
        ])

    def __repr__(self):
        return dim(' | ').join([
            cyan(f"{self.name:<19}"),
            f"{self.get_rarity_text()}",
            f"Value: {orange(self.value)}",
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