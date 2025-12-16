import random
from dataclasses import dataclass
from functools import cache
from typing import List

from savethewench.data import Areas
from savethewench.ui import purple, yellow
from savethewench.util import print_and_sleep
from .enemy import load_enemy, Enemy


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

    @property
    def enemies_remaining(self) -> int:
        return self.enemy_count - self.enemies_killed

    def spawn_enemy(self) -> Enemy:
        enemy = load_enemy(random.choice(self.enemies))
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

    def reset_current_enemy(self):
        self.current_enemy = None

    def kill_current_enemy(self):
        self.enemies_killed += 1
        self.enemy_count -= 1
        self.reset_current_enemy()

    def __hash__(self) -> int:
        return hash((self.name, self.enemy_count, self.enemies_killed, self.boss_defeated, self.current_enemy))


@cache
def load_areas() -> List[Area]:
    return [Area(**d) for d in Areas]
