import random
from dataclasses import dataclass, field
from typing import List, Optional

from savethewench.data import Enemies
from savethewench.data.perks import RICKETY_PICKPOCKET
from .base import Combatant, NPC
from .perk import attach_perk
from .weapon import Weapon, load_weapon


@dataclass
class Enemy(Combatant, NPC):
    name: str = ''
    hp: int = 0
    weapons: List[str] = field(default_factory=list)
    bounty: int = 0
    type: str = ''
    items: List[str] = field(default_factory=list)
    coins: int = random.randint(5, 50)
    alive: bool = True

    current_weapon: Weapon = field(init=False)
    max_hp: int = field(init=False)

    def __post_init__(self):
        self.current_weapon = load_weapon(random.choice(self.weapons))
        self.max_hp = self.hp

    def drop_weapon(self) -> Optional[Weapon]:
        if self.current_weapon.sell_value > 0:
            return self.current_weapon
        return None

    @attach_perk(RICKETY_PICKPOCKET, value_description="coins dropped")
    def drop_coins(self) -> int:
        return self.coins


def load_enemy(name: str) -> Enemy:
    matches = load_enemies([name])
    if len(matches) == 0:
        raise ValueError(f"Could not find enemy data for {name}")
    return matches[0]


def load_enemies(restriction: List[str] = None) -> List[Enemy]:
    return [Enemy(**d) for d in Enemies if restriction is None or d['name'] in restriction]
