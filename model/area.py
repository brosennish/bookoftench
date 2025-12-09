import random

from dataclasses import dataclass
from typing import List
from data.areas import Areas
from model.enemy import load_enemies
from .player import Player

@dataclass
class AudioTrigger:
    file_name: str
    stop_all: bool

@dataclass
class Area:
    name: str
    enemies: list[str]
    boss: str
    audio: str
    enemy_count: int = random.randint(10, 15)
    enemies_killed: int = 0
    boss_defeated: bool = False

    def explore(self, player: Player): #-> ExploreResult:
        # 40% chance of enemy (10% for elite), 15% for item, 15% weapon, 20% coins, 10% dry
        roll = random.random()
        if roll < 0.4:
            print("TODO - battle enemy")
            enemy = load_enemies(random.choice(self.enemies))[0]
            if random.random() < 0.10:
                enemy.name = f"Elite {enemy.name}"
                enemy.hp = int(enemy.hp * 1.5)
                enemy.max_hp = int(enemy.max_hp * 1.5)
                enemy.coins = int(enemy.coins * 1.5)
                print(f"{y}An enemy appears!{rst} {p}(Elite enemy!)")
            else:
                print(f"{y}An enemy appears!{rst}")
            # t.sleep(1)
            # battle(player, enemy, gs, shop)
        elif roll < 0.55:
            print("TODO - found item")
        elif roll < 0.7:
            print("TODO - found weapon")
        elif roll < 0.9:
            print("TODO - found coins")
        else:
            print("TODO - dry")



def load_areas() -> List[Area]:
    return [Area(**d) for d in Areas]