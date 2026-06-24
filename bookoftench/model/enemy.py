from __future__ import annotations

import copy
import random
from dataclasses import dataclass, field
from typing import Self

from bookoftench.audio import play_sound
from bookoftench.data import Enemies
from bookoftench.data.audio import AREA_BOSS_THEME, EQUIP_WEAPON, GATOR
from bookoftench.data.enemies import BAYOU_BILL, Bosses, Enemy_Lines, Final_Boss, Special_Bosses, WEREWOLF
from bookoftench.data.perks import RICKETY_PICKPOCKET
from bookoftench.data.weapons import BARE_HANDS, BLIND, SPECIAL
from bookoftench.ui import purple, cyan
from bookoftench.util import print_and_sleep
from .base import Combatant, NPC, DisplayableText
from .illness import Illness
from .perk import attach_perk
from .trait import Trait
from .weapon import Weapon, load_weapon, load_weapons

# ================================================================================================

# Constants
ENEMY_SWITCH_WEAPON_CHANCE = 0.2

# ================================================================================================

@dataclass
class Enemy(Combatant, NPC):
    name: str = ""
    trait: Trait | None = None
    illness: Illness | None = None
    hp: int = 0
    weapons: list[str] = field(default_factory=list)
    bounty: int = 0
    coins: int = 0
    type: str = ""
    flee: float = 0
    strength: float = 0
    acc: float = 0
    areas: list[str] = field(default_factory=list)
    items: list[str] = field(default_factory=list)
    alive: bool = True

    current_weapon: Weapon = field(init=False)
    weapon_dict: dict[str, Weapon] = field(init=False)
    max_hp: int = field(init=False)

    def __post_init__(self) -> None:
        self.weapon_dict = {
            weapon.name: weapon
            for weapon in load_weapons(self.weapons)
        }
        self.current_weapon = random.choice([
            weapon
            for weapon in self.weapon_dict.values()
            if weapon.type != BLIND
        ])
        self.max_hp = self.hp

    def drop_weapon(self) -> Weapon | None:
        if self.current_weapon.sell_value > 0 and self.current_weapon.type != SPECIAL:
            return self.current_weapon

        return None

    @attach_perk(RICKETY_PICKPOCKET, value_description="coins dropped")
    def drop_coins(self, enemy) -> int:
        return enemy.coins

    def handle_broken_weapon(self) -> None:
        del self.weapon_dict[self.current_weapon.base_name]
        if len(self.weapon_dict) == 0:
            self.weapon_dict[BARE_HANDS] = load_weapon(BARE_HANDS)
        self.current_weapon = random.choice(list(self.weapon_dict.values()))

    def enemy_switch_weapon(self, weapon: str | None) -> Weapon:
        current_weapon = self.current_weapon
        if self.trait and self.trait.name == WEREWOLF: # werewolf just uses claws
            return self.current_weapon
        if weapon:
            self.current_weapon = load_weapon(weapon)
        else:
            options = [i for i in self.weapon_dict if i != current_weapon.base_name
                       and i != BARE_HANDS]
            if options:
                selection = random.choice(options)
                self.current_weapon = load_weapon(selection)
        play_sound(EQUIP_WEAPON)
        print_and_sleep(cyan(f"{self.name} equipped {self.current_weapon.name}."), 1)
        return self.current_weapon

    def get_enemy_encounter_line(self) -> str | None:
        if self.name not in Enemy_Lines:
            return None
        return random.choice(Enemy_Lines[self.name])

def load_enemy(name: str) -> Enemy:
    matches = load_enemies([name])

    if not matches:
        raise ValueError(f"Could not find enemy data for {name}")

    return matches[0]


def load_enemies(restriction: list[str] | None = None) -> list[Enemy]:
    return [
        Enemy(**data)
        for data in Enemies
        if restriction is None or data["name"] in restriction
    ]

# ================================================================================================

@dataclass
class Boss(Enemy):
    theme: str = AREA_BOSS_THEME
    preamble: list[DisplayableText] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        data = copy.deepcopy(data)

        if "preamble" in data:
            data["preamble"] = [
                DisplayableText(**preamble_data)
                for preamble_data in data["preamble"]
            ]

        return super().from_dict(data)

    def do_preamble(self) -> None:
        for displayable_text in self.preamble:
            displayable_text.display()

    def handle_hit(self, other: "Combatant") -> None:
        super().handle_hit(other)

        if self.name == BAYOU_BILL:
            gator = random.random() < 0.20

            if gator:
                bite = random.randint(1, 10)
                play_sound(GATOR)
                print_and_sleep(purple(f"Mama Gator attacked you for {bite} damage!"), 2)
                other.take_damage(bite, self)

def load_boss(name: str) -> Boss:
    matches = [
        Boss.from_dict(data)
        for data in Bosses
        if data["name"] == name
    ]

    if not matches:
        raise ValueError(f"Could not find boss data for {name}")

    return matches[0]


def load_final_boss() -> Boss:
    return Boss.from_dict(Final_Boss)

# ================================================================================================

@dataclass
class SpecialBoss(Enemy):
    preamble: list[DisplayableText] = field(default_factory=list)
    theme: str = ""
    item: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        data = copy.deepcopy(data)

        if "preamble" in data:
            data["preamble"] = [
                DisplayableText(**preamble_data)
                for preamble_data in data["preamble"]
            ]

        return super().from_dict(data)

    def do_preamble(self) -> None:
        for displayable_text in self.preamble:
            displayable_text.display()

def load_special_boss(name: str) -> SpecialBoss:
    matches = load_special_bosses([name])

    if not matches:
        raise ValueError(f"Could not find special boss data for {name}")

    return matches[0]


def load_special_bosses(restriction: list[str] | None = None) -> list[SpecialBoss]:
    return [
        SpecialBoss.from_dict(data)
        for data in Special_Bosses
        if restriction is None or data["name"] in restriction
    ]
