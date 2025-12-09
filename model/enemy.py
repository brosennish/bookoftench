import random

import data.weapons as weapons

from dataclasses import dataclass, field
from typing import List, Dict
from data.enemies import Enemies
from model.weapon import Weapon

"""
name = enemy_data['name'],
            hp = random.randint(enemy_data['hp'] - hp_spread, enemy_data['hp'] + hp_spread),
            max_hp = enemy_data['hp'],
            weapons = list(enemy_data['weapon']),        # copy names
            weapon_uses = {
                w: random.randint(1, max(get_weapon_data(w)['uses'], 1))
                for w in enemy_data['weapon']
            },                                        
            current_weapon = random.choice(enemy_data['weapon']), # assigns random weapon from their list
            items = [],
            type = enemy_data['type'],
            coins = random.randint(5, 50),
            current_area = area_name
"""

@dataclass
class Enemy:
    name: str
    hp: int
    weapons: List[str]
    bounty: int
    type: str
    items: List[str] = field(default_factory=list)
    coins: int = random.randint(5, 50)
    current_area: str = ""
    alive: bool = True
    weapon_uses: Dict[str, int] = field(
        default_factory=lambda: {
            weapons.BARE_HANDS: 0  # TODO
        })

    blind: bool = False
    blinded_by: str = ''
    blind_effect: float = 0.0
    blind_turns: int = 0

    current_weapon: Weapon = field(init=False)
    max_hp: int = field(init=False)


def load_enemy(name: str) -> Enemy:
    matches = load_enemies([name])
    if len(matches) == 0:
        raise ValueError(f"Could not find enemy data for {name}")
    return matches[0]


def load_enemies(restriction: List[str] = None) -> List[Enemy]:
    return [Enemy(**d) for d in Enemies if restriction is None or d['name'] in restriction]
