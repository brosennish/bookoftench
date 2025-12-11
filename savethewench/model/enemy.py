import random
from dataclasses import dataclass, field
from typing import List

from savethewench.data import Enemies
from .weapon import Weapon, load_weapon


@dataclass
class Enemy:
    name: str
    hp: int
    weapons: List[str]
    bounty: int
    type: str
    items: List[str] = field(default_factory=list)
    coins: int = random.randint(5, 50)
    alive: bool = True

    blind: bool = False
    blinded_by: str = ''
    blind_effect: float = 0.0
    blind_turns: int = 0

    current_weapon: Weapon = field(init=False)
    max_hp: int = field(init=False)

    def __post_init__(self):
        self.current_weapon = load_weapon(random.choice(self.weapons))
        self.max_hp = self.hp


def load_enemy(name: str) -> Enemy:
    matches = load_enemies([name])
    if len(matches) == 0:
        raise ValueError(f"Could not find enemy data for {name}")
    return matches[0]


def load_enemies(restriction: List[str] = None) -> List[Enemy]:
    return [Enemy(**d) for d in Enemies if restriction is None or d['name'] in restriction]
