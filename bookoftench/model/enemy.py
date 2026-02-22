from __future__ import annotations

import copy
import random
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Self

from bookoftench.audio import play_sound
from bookoftench.data import Enemies
from bookoftench.data.audio import AREA_BOSS_THEME, GATOR
from bookoftench.data.enemies import Bosses, Final_Boss, BAYOU_BILL, Enemy_Lines
from bookoftench.data.perks import RICKETY_PICKPOCKET
from bookoftench.data.weapons import BARE_HANDS
from bookoftench.ui import purple, cyan
from bookoftench.util import print_and_sleep
from .base import Combatant, NPC, DisplayableText
from .perk import attach_perk
from .weapon import Weapon, load_weapon, load_weapons

# Constants
ENEMY_SWITCH_WEAPON_CHANCE = 0.2


@dataclass
class Enemy(Combatant, NPC):
    name: str = ''
    hp: int = 0
    weapons: List[str] = field(default_factory=list)
    bounty: int = 0
    type: str = ''
    flee: float = 0
    strength: float = 0
    areas: List[str] = field(default_factory=list)
    items: List[str] = field(default_factory=list)
    coins: int = random.randint(10, 60)
    alive: bool = True

    current_weapon: Weapon = field(init=False)
    weapon_dict: Dict[str, Weapon] = field(init=False)
    max_hp: int = field(init=False)

    def __post_init__(self):
        self.weapon_dict = dict((w.name, w) for w in load_weapons(self.weapons))
        self.current_weapon = random.choice(list(self.weapon_dict.values()))
        self.max_hp = self.hp

    def drop_weapon(self) -> Optional[Weapon]:
        if self.current_weapon.sell_value > 0:
            return self.current_weapon
        return None

    @attach_perk(RICKETY_PICKPOCKET, value_description="coins dropped")
    def drop_coins(self) -> int:
        self.coins += random.randint(-5, 10)
        return self.coins

    def handle_broken_weapon(self) -> None:
        del self.weapon_dict[self.current_weapon.name]
        if len(self.weapon_dict) == 0:
            self.weapon_dict[BARE_HANDS] = load_weapon(BARE_HANDS)
        self.current_weapon = random.choice(list(self.weapon_dict.values()))

    def enemy_switch_weapon(self) -> Weapon:
        current_weapon = self.current_weapon
        options = [i for i in self.weapon_dict if i != current_weapon.name
                   and i != BARE_HANDS]
        if options:
            selection = random.choice(options)
            self.current_weapon = load_weapon(selection)
            print_and_sleep(cyan(f"{self.name} equipped {self.current_weapon.name}."), 1)
        return self.current_weapon

    def get_enemy_encounter_line(self) -> str | None:
        if self.name not in Enemy_Lines:
            return None
        return random.choice(Enemy_Lines[self.name])

def load_enemy(name: str) -> Enemy:
    matches = load_enemies([name])
    if len(matches) == 0:
        raise ValueError(f"Could not find enemy data for {name}")
    return matches[0]

def load_enemies(restriction: List[str] = None) -> List[Enemy]:
    return [Enemy(**d) for d in Enemies if restriction is None or d['name'] in restriction]


@dataclass
class Boss(Enemy):
    theme: str = AREA_BOSS_THEME
    preamble: List[DisplayableText] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        data = copy.deepcopy(data)
        if 'preamble' in data:
            data['preamble'] = [DisplayableText(**d) for d in data['preamble']]
        return super().from_dict(data)

    def do_preamble(self) -> None:
        for displayableText in self.preamble:
            displayableText.display()

    def handle_hit(self, other: "Combatant") -> None:
        super().handle_hit(other)
        if self.name == BAYOU_BILL:
            gator = random.random() < 0.10
            if gator:
                bite = random.randint(3, 5)
                play_sound(GATOR)
                print_and_sleep(purple(f"Mama Gator attacked you for {bite} damage!"), 2)
                other.take_damage(bite, self)


def load_boss(name: str) -> Boss:
    matches = [Boss.from_dict(d) for d in Bosses if d['name'] == name]
    if len(matches) == 0:
        raise ValueError(f"Could not find boss data for {name}")
    return matches[0]


def load_final_boss() -> Boss:
    return Boss.from_dict(Final_Boss)
