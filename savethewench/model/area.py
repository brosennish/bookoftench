from __future__ import annotations

import copy
import random
from dataclasses import dataclass, field
from typing import List

from savethewench.data import Areas
from savethewench.data.components import MenuDefaults
from savethewench.ui import purple, yellow
from savethewench.util import print_and_sleep
from .enemy import Enemy, load_enemy, Boss, load_boss, load_final_boss
from .shop import Shop


@dataclass
class ExploreProbabilities:
    coin_chance: int = 20
    enemy_chance: int = 45
    item_chance: int = 10
    perk_chance: int = 1
    weapon_chance: int = 10


@dataclass
class AreaActions:
    pages: List[List[str]]

    @classmethod
    def defaults(cls) -> AreaActions:
        return AreaActions(pages=[MenuDefaults.page_one, MenuDefaults.page_two])


@dataclass
class Area:
    name: str
    enemies: list[str]
    boss_name: str
    theme: str
    enemy_count: int = field(default_factory=lambda: random.randint(10, 15))
    enemies_killed: int = 0
    boss_defeated: bool = False
    boss: Boss = None
    current_enemy = None

    shop: Shop = field(default_factory=Shop)
    explore_probabilities: ExploreProbabilities = field(default_factory=ExploreProbabilities)
    unique_components: List[str] = field(default_factory=list)
    actions_menu: AreaActions = field(default_factory=AreaActions.defaults)

    def __post_init__(self):
        self.boss = load_boss(self.boss_name)
        self.shop = Shop(self.name)

    @property
    def enemies_remaining(self) -> int:
        return max(self.enemy_count - self.enemies_killed, 0)

    def spawn_enemy(self, player_level: int) -> Enemy:
        enemy = load_enemy(random.choice(self.enemies))
        enemy.hp += player_level - 1
        enemy.hp += random.randint(-5, 5)
        if random.random() < 0.10:
            enemy.name = f"Elite {enemy.name}"
            enemy.hp = int(enemy.hp * 1.5)
            enemy.max_hp = int(enemy.max_hp * 1.5)
            enemy.coins = int(enemy.coins * 1.5)
            print_and_sleep(f"{yellow("An enemy appears!")} {purple("(Elite enemy!)")}", 1)
        else:
            print_and_sleep(yellow("An enemy appears!"), 1)
        self.current_enemy = enemy
        return self.current_enemy

    def summon_boss(self) -> Boss:
        self.current_enemy = self.boss
        return self.current_enemy

    def summon_final_boss(self) -> Boss:
        final_boss: Boss = load_final_boss()
        self.current_enemy = final_boss
        return self.current_enemy

    def kill_current_enemy(self):
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
        if 'explore_probabilities' in data:
            data['explore_probabilities'] = ExploreProbabilities(**data['explore_probabilities'])
        if 'actions_menu' in data:
            data['actions_menu'] = AreaActions(**data['actions_menu'])
        res.append(Area(**data))
    return res
