import random
import time as t
from dataclasses import dataclass
from functools import cache
from typing import List

from savethewench.data import Areas
from savethewench.ui import purple, yellow
from .enemy import load_enemy


@dataclass
class Area:
    name: str
    enemies: list[str]
    boss: str
    theme: str
    enemy_count: int = random.randint(10, 15)
    enemies_killed: int = 0
    boss_defeated: bool = False
    current_enemy = None

    def __hash__(self) -> int:
        return hash((self.name, self.enemy_count, self.enemies_killed, self.boss_defeated, self.current_enemy))

    def spawn_enemy(self):
        enemy = load_enemy(random.choice(self.enemies))
        if random.random() < 0.10:
            enemy.name = f"Elite {enemy.name}"
            enemy.hp = int(enemy.hp * 1.5)
            enemy.max_hp = int(enemy.max_hp * 1.5)
            enemy.coins = int(enemy.coins * 1.5)
            print(f"{yellow("An enemy appears!")} {purple("(Elite enemy!)")}")
        else:
            print(yellow("An enemy appears!"))
        self.current_enemy = enemy
        t.sleep(1)

    def reset_current_enemy(self):
        self.current_enemy = None

    def kill_current_enemy(self):
        self.enemies_killed += 1
        self.enemy_count -= 1
        self.reset_current_enemy()


@cache
def load_areas() -> List[Area]:
    return [Area(**d) for d in Areas]
