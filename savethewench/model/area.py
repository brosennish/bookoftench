import random
from dataclasses import dataclass
from typing import List

from savethewench.data import Areas
from savethewench.ui import purple, yellow
from savethewench.util import print_and_sleep
from .enemy import Enemy, load_enemy, Boss, load_boss, load_final_boss


@dataclass
class Area:
    name: str
    enemies: list[str]
    boss_name: str
    theme: str
    enemy_count: int = random.randint(10, 15)
    enemies_killed: int = 0
    boss_defeated: bool = False
    boss: Boss = None
    current_enemy = None

    def __post_init__(self):
        self.boss = load_boss(self.boss_name)

    @property
    def enemies_remaining(self) -> int:
        return max(self.enemy_count - self.enemies_killed, 0)

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
    return [Area(**d) for d in Areas]
