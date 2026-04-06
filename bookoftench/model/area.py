from __future__ import annotations

import copy
import random
from dataclasses import dataclass, field
from typing import List, Dict, Set

from bookoftench.data import Areas
from bookoftench.data.areas import EncounterType
from bookoftench.data.components import ActionMenuDefaults, DISCOVER_DISCOVERABLE, DISCOVER_ITEM, DISCOVER_PERK, \
    DISCOVER_WEAPON, \
    SPAWN_ENEMY, DISCOVER_SPECIAL, THREE_HOLES, TRIPLE_TENCH_DARE, SHEBOKKEN_ROULETTE, ZONKED, GREEDY_BASTARD
from bookoftench.data.enemies import Enemy_Adjectives, Traits, PLANT, WEREWOLF, COWARD, CONTAGIOUS
from bookoftench.ui import purple, yellow, blue
from bookoftench.util import print_and_sleep
from .enemy import Enemy, load_enemy, Boss, load_boss, load_final_boss
from .illness import load_illness
from .perk import perk_is_active
from .shop import Shop
from .trait import load_traits
from .weapon import load_weapon
from ..data.enviroment import NIGHTTIME, FULL
from ..data.illnesses import Illnesses, LATE_ONSET_SIDS
from ..data.perks import SHERLOCK_TENCH
from ..data.weapons import CLAWS

_search_defaults = {
    DISCOVER_PERK: 1,
    DISCOVER_ITEM: 1,
    DISCOVER_WEAPON: 1,
    DISCOVER_DISCOVERABLE: 42,
    DISCOVER_SPECIAL: 7,
    SPAWN_ENEMY: 30
}

_event_defaults = {
    GREEDY_BASTARD: 25,
    SHEBOKKEN_ROULETTE: 25,
    THREE_HOLES: 25,
    TRIPLE_TENCH_DARE: 10,
    ZONKED: 15
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
    event_probabilities: Dict[str, int] = field(default_factory=lambda: _event_defaults)
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

    def spawn_enemy(self, wanted: str, player_level: int, time: str, moon: str) -> Enemy:
        wanted = load_enemy(wanted)
        available = [i for i in self.enemies if i not in self.enemies_seen]

        if not available:
            self.enemies_seen.clear()  # if all enemies seen, reset the pool
            available = [i for i in self.enemies if i not in self.enemies_seen]

        enemy_name = random.choice(available)  # Initial enemy selection

        if len(self.enemies_seen) >= 1:  # Calculate odds of seeing a seen enemy if 1+ in enemies_seen
            if random.random() < min(0.15, 0.01 * len(self.enemies_seen)):  # If random < scaling float value
                enemy_name = random.choice(tuple(self.enemies_seen))  # Select enemy from seen

        if perk_is_active(SHERLOCK_TENCH):  # 10% chance of wanted enemy encounter if perk is active
            if self.name in wanted.areas and random.random() < 0.15:
                enemy_name = wanted.name

        enemy = load_enemy(enemy_name)  # convert selected enemy to Enemy
        self.enemies_seen.add(enemy_name)  # add selected enemy to enemies_seen

        # --- traits and illness ---
        valid = [i['name'] for i in Traits]
        if time == NIGHTTIME:
            valid = [i['name'] for i in Traits if i['name'] not in [COWARD]]
        traits = load_traits(valid)
        enemy.trait = random.choice(traits)

        if enemy.trait.name == CONTAGIOUS:
            valid = [i['name'] for i in Illnesses if i['name'] not in [LATE_ONSET_SIDS]]
            illness = random.choice(valid)
            enemy.illness = load_illness(illness)

        enemy.hp += random.randint(-2, 2)  # apply hp spread first
        enemy.hp += round((enemy.hp * 0.03) * max(player_level - 1, 0))  # then apply hp scaling
        enemy.strength = enemy.strength + random.uniform(-0.03, 0.03)
        enemy.acc = enemy.acc + random.uniform(-0.03, 0.03)
        enemy.coins = max(0, enemy.coins + random.randint(-5, 5))
        if random.random() < 0.20:
            enemy.coins += round(enemy.coins * random.uniform(0.05, 0.25))
        enemy_lines = enemy.get_enemy_encounter_line()  # get the line before mutating enemy.name
        elite_chance = min(0.15, max(0.0, (player_level - 1) * 0.03))

        # --- werewolf logic ---
        if enemy.trait.name == WEREWOLF and time == NIGHTTIME and moon == FULL:
            enemy.name = "Werewolf"
            enemy.hp += random.randint(10, 25)
            enemy.strength = 1.25
            enemy.acc = 0
            enemy.coins = 0

        if random.random() < elite_chance:
            enemy.name = f"Elite {enemy.name}"
            enemy.hp = int(enemy.hp * 1.5)
            enemy.max_hp = int(enemy.max_hp * 1.5)
            enemy.strength += 0.1
            enemy.acc += 0 if enemy.trait.name == WEREWOLF else 0.1
            enemy.coins = int(enemy.coins * 1.5)
            print_and_sleep(f"{yellow("An enemy appears!")} {purple("(Elite enemy!)")}", 1)
        else:
            print_and_sleep(yellow("An enemy appears!"), 1)

        if enemy_lines:
            print_and_sleep(f"{blue(f'{enemy_lines}')}", 3)
        adj = random.choice(Enemy_Adjectives)
        enemy.name = f"{adj} {enemy.name}"

        self.current_enemy = enemy
        if self.current_enemy.trait.name == WEREWOLF:
            self.current_enemy.current_weapon = load_weapon(CLAWS)
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
