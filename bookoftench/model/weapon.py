from __future__ import annotations

import random
from dataclasses import asdict, dataclass, field

from bookoftench.data import Weapons
from bookoftench.data.perks import BULLETPROOF
from bookoftench.data.weapons import PISTOL, REVOLVER, RIFLE, SHOTGUN
from bookoftench.model.base import Buyable, WeaponBase
from bookoftench.model.perk import attach_perk
from bookoftench.ui import cyan, dim, orange, red, yellow

# ================================================================================================

@dataclass
class Weapon(WeaponBase, Buyable):
    sell_value: int = 0
    tier: int = 0

    blind_effect: float = 0.0
    blind_turns_min: int = 0
    blind_turns_max: int = 0

    def _is_gun(self) -> bool:
        return self.name in (PISTOL, REVOLVER, RIFLE, SHOTGUN)

    def calculate_base_damage_no_perk(self) -> int:
        return super().calculate_base_damage()

    def calculate_base_damage(self) -> int:
        base_damage = self.calculate_base_damage_no_perk()

        @attach_perk(
            BULLETPROOF,
            value_description="enemy bullet damage",
            condition=lambda: self._is_gun(),
        )
        def apply_perks() -> int:
            return base_damage

        return int(apply_perks())

    def get_blind_effect(self) -> float:
        effect = self.blind_effect
        if effect > 0:
            return effect + random.uniform(-0.05, 0.05)
        return effect

    def get_blind_turns(self) -> int:
        return random.randint(self.blind_turns_min, self.blind_turns_max)

    def to_sellable_weapon(self) -> SellableWeapon:
        return SellableWeapon.from_dict(asdict(self))

    def __repr__(self) -> str:
        return dim(" | ").join([
            cyan(f"{self.name:<24}"),
            f"Cost: {orange(self.cost):<18}",
            f"Dmg: {red(f'{self.damage:<3}')}",
            f"Acc: {yellow(f'{self.acc:<4}')}",
            f"Var: {red(f'{self.var}')}",
            f"Crit: {yellow(f'{self.crit:<4}')}",
            f"Uses: {self.format_uses()}",
        ])

# ================================================================================================

@dataclass
class SellableWeapon(Weapon):
    _sell_value: int = field(init=False)

    def __post_init__(self) -> None:
        self._sell_value = self.sell_value

    @property
    def sell_value(self) -> int:
        max_uses = load_weapon(self.base_name).uses  # TODO optimize out object construction overhead
        if max_uses == -1:
            return self._sell_value

        proportion = self.uses / max_uses
        price = self._sell_value * proportion
        return max(int(price), 1)

    @sell_value.setter
    def sell_value(self, value: int) -> None:
        self._sell_value = value

    def __repr__(self) -> str:
        return dim(" | ").join([
            cyan(f"{self.name:<24}"),
            f"Value: {orange(self.sell_value):<18}",
            f"{dim('Dmg:')} {red(f'{self.damage:<3}')}",
            f"{dim('Acc:')} {yellow(f'{self.acc:<4}')}",
            f"{dim('Var:')} {red(f'{self.var}')}",
            f"{dim('Crit:')} {yellow(f'{self.crit:<4}')}",
            f"{dim('Uses:')} {self.format_uses()}",
        ])

# ================================================================================================

def load_weapon(name: str) -> Weapon:
    matches = load_weapons([name])
    if not matches:
        raise ValueError(f"Could not find weapon data for {name}")
    return matches[0]


def load_weapons(restriction: list[str] | None = None) -> list[Weapon]:
    return [
        Weapon(**weapon_data)
        for weapon_data in Weapons
        if restriction is None or weapon_data["name"] in restriction
    ]


def load_discoverable_weapons() -> list[Weapon]:
    return [
        weapon for weapon in load_weapons()
        if weapon.uses > 0
    ]

# ================================================================================================

def make_elite_weapon(weapon: Weapon) -> Weapon:
    name = weapon.name
    weapon.name = f"Elite {name}"

    weapon.damage += random.randint(4, 6)

    original_accuracy = weapon.acc
    accuracy_gain = random.uniform(0.03, 0.06)
    weapon.acc = round(min(accuracy_gain + original_accuracy, 1), 2)

    original_crit = weapon.crit
    crit_gain = random.uniform(0.03, 0.09)
    weapon.crit = round(original_crit + crit_gain, 2)

    if weapon.uses > 0:
        weapon.uses += random.randint(3, 5)

    increase = round(weapon.cost * 0.12)
    weapon.cost += increase

    if weapon.sell_value > 0:
        increase = round(weapon.sell_value * 0.12)
        weapon.sell_value += increase

    weapon.is_elite = True
    return weapon

# ================================================================================================

def make_autographed_weapon(weapon: Weapon) -> Weapon:
    name = weapon.name
    weapon.name = f"Autographed {name}"

    if weapon.sell_value > 0:
        weapon.sell_value *= random.randint(3, 6)

    return weapon