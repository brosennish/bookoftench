from __future__ import annotations

import copy
import random
from dataclasses import dataclass, field
from typing import List, Dict, Set

from bookoftench.data import Areas
from bookoftench.data.areas import EncounterType
from bookoftench.data.components import ActionMenuDefaults, DISCOVER_DISCOVERABLE, DISCOVER_ITEM, DISCOVER_PERK, \
    DISCOVER_WEAPON, \
    SPAWN_ENEMY
from bookoftench.data.enemies import Enemy_Adjectives
from bookoftench.ui import purple, yellow, blue
from bookoftench.util import print_and_sleep
from .enemy import Enemy, load_enemy, Boss, load_boss, load_final_boss, load_enemies
from .shop import Shop

_search_defaults = {
    DISCOVER_PERK: 1,
    DISCOVER_ITEM: 4,
    DISCOVER_WEAPON: 4,
    DISCOVER_DISCOVERABLE: 45,
    SPAWN_ENEMY: 30
}


@dataclass
class AreaActions:
    pages: List[List[str]]

    @classmethod
    def defaults(cls) -> AreaActions:
        return AreaActions(pages=[ActionMenuDefaults.page_one, ActionMenuDefaults.page_two])


@dataclass
class AreaEncounter:
    type: EncounterType
    component: str


@dataclass
class Area:
    name: str
    enemies: list[str]
    boss_name: str
    theme: str
    enemy_count: int = field(default_factory=lambda: random.randint(10, 15))
    enemies_killed: int = 0
    enemies_seen: Set[str] = field(default_factory=set)
    boss_defeated: bool = False
    boss: Boss = None
    current_enemy = None

    shop: Shop = field(default_factory=Shop)
    search_probabilities: Dict[str, int] = field(default_factory=lambda: _search_defaults)
    actions_menu: AreaActions = field(default_factory=AreaActions.defaults)
    encounters: List[AreaEncounter] = field(default_factory=list)

    def __post_init__(self):
        self.boss = load_boss(self.boss_name)

    @property
    def post_kill_components(self) -> List[str]:
        return [e.component for e in self.encounters if e.type == EncounterType.POST_KILL]

    @property
    def enemies_remaining(self) -> int:
        return max(self.enemy_count - self.enemies_killed, 0)

    def spawn_enemy(self, player_level: int) -> Enemy:
        available = [i for i in self.enemies if i not in self.enemies_seen]
        if not available:
            self.enemies_seen.clear()
            available = [i for i in self.enemies if i not in self.enemies_seen]
        enemy_name = random.choice(available)
        if len(self.enemies_seen) >= 1:
            if random.random() < min(0.15, 0.01 * len(self.enemies_seen)):
                enemy_name = random.choice(tuple(self.enemies_seen))
        enemy = load_enemy(enemy_name)
        self.enemies_seen.add(enemy_name)

        enemy.hp += round((enemy.hp * 0.03) * player_level - 1)
        enemy.hp += random.randint(-3, 3)
        elite_chance = min(0.15, max(0.0, (player_level - 1) * 0.03))
        if random.random() < elite_chance:
            enemy.name = f"Elite {enemy.name}"
            enemy.hp = int(enemy.hp * 1.5)
            enemy.max_hp = int(enemy.max_hp * 1.5)
            enemy.coins = int(enemy.coins * 1.5)
            print_and_sleep(f"{yellow("An enemy appears!")} {purple("(Elite enemy!)")}", 1)
        else:
            print_and_sleep(yellow("An enemy appears!"), 1)

        enemy_lines = enemy.get_enemy_encounter_line()
        if enemy_lines:
            print_and_sleep(f"{blue(f'{enemy_lines}')}", 3)

        adj = random.choice(Enemy_Adjectives)
        enemy.name = f"{adj} {enemy.name}"

        self.current_enemy = enemy
        return self.current_enemy

    def summon_boss(self) -> Boss:
        self.current_enemy = self.boss
        return self.current_enemy

    def summon_final_boss(self) -> Boss:
        final_boss: Boss = load_final_boss()
        self.current_enemy = final_boss
        return self.current_enemy

    def kill_current_enemy(self) -> None:
        self.enemies_killed += 1
        if self.current_enemy == self.boss:
            self.boss_defeated = True
        self.current_enemy = None

    def __hash__(self) -> int:
        return hash((self.name, self.enemy_count, self.enemies_killed, self.boss_defeated, self.current_enemy))


def load_areas() -> List[Area]:
    res = []
    for d in Areas:
        data = copy.deepcopy(d)
        data['shop'] = Shop(data['name'])
        if 'actions_menu' in data:
            data['actions_menu'] = AreaActions(**data['actions_menu'])
        if 'encounters' in data:
            data['encounters'] = [AreaEncounter(**d) for d in data['encounters']]
        res.append(Area(**data))
    return res
