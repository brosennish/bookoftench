from __future__ import annotations

import copy
import random
from dataclasses import dataclass, field
from typing import List, Dict, Set

from bookoftench.data import Areas
from bookoftench.data.areas import EncounterType, FOREST, CITY, CAVE
from bookoftench.data.components import ActionMenuDefaults, DISCOVER_DISCOVERABLE, DISCOVER_ITEM, DISCOVER_PERK, \
    DISCOVER_WEAPON, \
    SPAWN_ENEMY, ENCOUNTER_SUB_BOSS, SPECIAL_EVENT
from bookoftench.data.enemies import Enemy_Adjectives, Traits, WEREWOLF, CONTAGIOUS, NIGHT_OWL, HOHKKEN, BOSS, \
    NORMAL, SPECIAL_BOSS, Cave_Special_Bosses, City_Special_Bosses, Forest_Special_Bosses, \
    Swamp_Special_Bosses
from bookoftench.ui import purple, yellow, blue
from bookoftench.util import print_and_sleep
from .enemy import Enemy, load_enemy, Boss, load_boss, load_final_boss, load_special_boss, SpecialBoss
from .illness import load_illnesses
from .perk import perk_is_active
from .shop import Shop
from .trait import load_traits, load_trait
from .weapon import load_weapon, make_elite_weapon
from bookoftench.data.enviroment import NIGHT, FULL
from bookoftench.data.illnesses import Illnesses, LATE_ONSET_SIDS
from bookoftench.data.perks import SHERLOCK_TENCH
from bookoftench.data.weapons import CLAWS, BLIND, SPECIAL
from ..audio import play_sound
from ..data.audio import ENEMY_APPEARS, OWL_SFX, WEREWOLF_SFX

# ================================================================================================

_search_defaults = {
    DISCOVER_PERK: 0,
    DISCOVER_WEAPON: 0,
    DISCOVER_ITEM: 0,
    ENCOUNTER_SUB_BOSS: 0,
    DISCOVER_DISCOVERABLE: 0,
    SPECIAL_EVENT: 100,
    SPAWN_ENEMY: 0
}

'''_search_defaults = {
    DISCOVER_PERK: 1,
    DISCOVER_WEAPON: 2,
    DISCOVER_ITEM: 3,
    ENCOUNTER_SUB_BOSS: 3,
    DISCOVER_DISCOVERABLE: 45,
    SPECIAL_EVENT: 9,
    SPAWN_ENEMY: 30
}'''

_event_defaults = {
    SPECIAL_EVENT: 100,
}

# ================================================================================================

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

# ================================================================================================

@dataclass
class Area:
    name: str
    enemies: list[str]
    boss_name: str
    theme: str
    enemy_count: int = field(default_factory=lambda: random.randint(7, 9))
    enemies_killed: int = 0
    enemies_seen: Set[str] = field(default_factory=set)
    boss_defeated: bool = False
    boss: Boss = None
    current_enemy = None
    special_bosses: list[str] = field(default_factory=list)

    shop: Shop = field(default_factory=Shop)
    search_probabilities: Dict[str, int] = field(default_factory=lambda: _search_defaults)
    event_probabilities: Dict[str, int] = field(default_factory=lambda: _event_defaults)
    actions_menu: AreaActions = field(default_factory=AreaActions.defaults)
    encounters: List[AreaEncounter] = field(default_factory=list)

    def __post_init__(self):
        self.boss = load_boss(self.boss_name)
        if self.name == CAVE:
            self.special_bosses = [i for i in Cave_Special_Bosses]
        elif self.name == CITY:
            self.special_bosses = [i for i in City_Special_Bosses]
        elif self.name == FOREST:
            self.special_bosses = [i for i in Forest_Special_Bosses]
        else:
            self.special_bosses = [i for i in Swamp_Special_Bosses]

    @property
    def post_kill_components(self) -> List[str]:
        return [e.component for e in self.encounters if e.type == EncounterType.POST_KILL]

    @property
    def enemies_remaining(self) -> int:
        return max(self.enemy_count - self.enemies_killed, 0)

# ================================================================================================

    # todo - refactor
    def spawn_enemy(self, gs, player_level: int, wanted: str, time: str, moon: str) -> Enemy:
        enemy_name = self.handle_enemy_selection(wanted)  # select enemy name

        # --- load Enemy, log encounter, add to seen ---
        enemy = load_enemy(enemy_name)
        self.log_encounter(enemy, gs)
        self.enemies_seen.add(enemy_name)

        # --- trait and illness ---
        if not enemy.trait and enemy.type == NORMAL:
            enemy = handle_trait_and_illness(enemy)

        # --- standard stat adjustments ---
        enemy_line = self.handle_stat_adjustments(enemy, player_level)

        # --- trait transformation logic ---
        enemy = self.handle_trait_transformation(enemy, time, moon)

        # --- elite logic ---
        elite = self.handle_elite_chance(enemy, player_level)

        if elite:
            print_and_sleep(f"{yellow("An enemy appears!")} {purple("(Elite enemy!)")}", 1)
        else:
            play_sound(ENEMY_APPEARS)
            print_and_sleep(yellow("An enemy appears!"), 1.5)

        # --- print enemy line, add adjective, and set current_enemy ---
        if enemy_line:
            print_and_sleep(f"{blue(f'{enemy_line}')}", 3)
        adj = random.choice(Enemy_Adjectives)
        enemy.name = f"{adj} {enemy.name}"

        self.current_enemy = enemy

        # --- werewolf and night owl final initialization ---
        self.handle_final_trait_initialization(time)

        # --- elite weapon logic ---
        self.handle_elite_weapon()

        return self.current_enemy

    # ================================================================================================

    def handle_enemy_selection(self, wanted: str):
        wanted_obj = load_enemy(wanted)
        available = [i for i in self.enemies if i not in self.enemies_seen]

        if not available:
            self.enemies_seen.clear()  # if all enemies seen, reset the pool
            available = [i for i in self.enemies if i not in self.enemies_seen]

        enemy_name = random.choice(available)  # Initial enemy selection

        if len(self.enemies_seen) >= 1:  # Calculate odds of seeing a seen enemy if 1+ in enemies_seen
            if random.random() < min(0.15, 0.01 * len(self.enemies_seen)):  # If random < scaling float value
                enemy_name = random.choice(tuple(self.enemies_seen))  # Select enemy from seen

        # --- if Sherlock Tench, 15% chance of wanted if correct area ---
        if perk_is_active(SHERLOCK_TENCH):
            if self.name in wanted_obj.areas and random.random() < 0.15:
                enemy_name = wanted

        return enemy_name

# ================================================================================================

    @staticmethod
    def handle_stat_adjustments(enemy: Enemy, player_level: int):
        enemy.hp += random.randint(-2, 2)  # apply hp spread first
        enemy.hp += round((enemy.hp * 0.03) * max(player_level - 1, 0))  # then apply hp scaling
        enemy.max_hp = enemy.hp
        enemy.strength = enemy.strength + random.uniform(-0.03, 0.03)
        enemy.acc = enemy.acc + random.uniform(-0.03, 0.03)
        enemy.coins = max(0, enemy.coins + random.randint(-10, 20))
        if random.random() < 0.20:
            enemy.coins += round(enemy.coins * random.uniform(0.05, 0.25))
        enemy_line = enemy.get_enemy_encounter_line()

        return enemy_line


    @staticmethod
    def handle_trait_transformation(enemy: Enemy, time: str, moon: str):
        if enemy.trait.name == NIGHT_OWL and time == NIGHT:
            enemy = create_night_owl(enemy)
        if enemy.trait.name == WEREWOLF and time == NIGHT and moon == FULL:
            enemy = create_werewolf(enemy)

        return enemy


    @staticmethod
    def handle_elite_chance(enemy: Enemy, player_level: int):
        elite_chance = min(0.15, max(0.0, (player_level - 1) * 0.03))

        if random.random() < elite_chance:
            enemy.name = f"Elite {enemy.name}"
            enemy.hp = int(enemy.hp * 1.5)
            enemy.max_hp = int(enemy.max_hp * 1.5)
            enemy.strength += 0.1
            enemy.acc += 0 if enemy.trait.name == WEREWOLF else 0.1
            enemy.coins = int(enemy.coins * 1.5)
            return True
        else:
            return False


    def handle_final_trait_initialization(self, time: str):
        if WEREWOLF in self.current_enemy.name:
            self.current_enemy.current_weapon = load_weapon(CLAWS)
            play_sound(WEREWOLF_SFX)
        elif self.current_enemy.trait.name == NIGHT_OWL and time == NIGHT:
            play_sound(OWL_SFX)


    def handle_elite_weapon(self):
        if self.current_enemy.current_weapon.type not in [BLIND, SPECIAL] and random.random() < 0.15:
            base = self.current_enemy.current_weapon
            self.current_enemy.current_weapon = make_elite_weapon(base)

# ================================================================================================

    def spawn_special_boss(self, name: str, time: str, gs) -> SpecialBoss:
        special_boss = load_special_boss(name)  # convert selected special boss to Enemy type
        self.enemies_seen.add(name)  # add selected enemy to enemies_seen

        # --- assign Trait ---
        if special_boss.trait:
            if isinstance(special_boss.trait, str):
                trait_dict = next((i for i in Traits if i['name'] == special_boss.trait), None)

                if trait_dict:
                    special_boss.trait = load_trait(trait_dict)

            # --- traits and illness ---
            if special_boss.trait and special_boss.trait.name == CONTAGIOUS:
                enemy = handle_trait_and_illness(special_boss)

            # --- night owl logic ---
            if special_boss.trait.name == NIGHT_OWL and time == NIGHT:
                special_boss = create_night_owl(special_boss)
                play_sound(OWL_SFX)

        self.current_enemy = special_boss
        self.log_encounter(self.current_enemy, gs)

        # --- elite weapon logic ---
        if self.current_enemy.current_weapon.type not in [BLIND, SPECIAL] and random.random() < 0.15:
            base = self.current_enemy.current_weapon
            self.current_enemy.current_weapon = make_elite_weapon(base)

        return self.current_enemy


    @staticmethod
    def log_encounter(enemy: Enemy | SpecialBoss, game_state):
        area = game_state.current_area.name
        game_state.encountered_enemies.append({"area": area, "enemy": enemy})

# ================================================================================================

    def set_boss_to_current_enemy(self, name: str):
        self.current_enemy = load_boss(name)
        if self.current_enemy.name != HOHKKEN:
            self.current_enemy.current_weapon = make_elite_weapon(self.current_enemy.current_weapon)
        return self.current_enemy

    def summon_boss(self) -> Boss:
        self.current_enemy = self.boss
        self.current_enemy.current_weapon = make_elite_weapon(self.current_enemy.current_weapon)
        return self.current_enemy

    def summon_final_boss(self) -> Boss:
        final_boss: Boss = load_final_boss()
        self.current_enemy = final_boss
        self.current_enemy.current_weapon = make_elite_weapon(self.current_enemy.current_weapon)
        return self.current_enemy

    def kill_current_enemy(self, current_area, wench_area) -> None:
        if self.current_enemy.type not in [BOSS, SPECIAL_BOSS]:
            self.enemies_killed += 1
        if self.current_enemy == self.boss:
            self.boss_defeated = True
            if current_area == wench_area:
                self.current_enemy = load_final_boss()
                return
        self.current_enemy = None

    def __hash__(self) -> int:
        return hash((self.name, self.enemy_count, self.enemies_killed, self.boss_defeated, self.current_enemy))

# ================================================================================================

def create_night_owl(enemy) -> Enemy:
    enemy.max_hp += random.randint(5, 10)
    enemy.hp = enemy.max_hp
    enemy.strength += round(random.uniform(0.01, 0.1), 2)
    enemy.acc += round(random.uniform(0.01, 0.1), 2)
    return enemy

def create_werewolf(enemy) -> Enemy:
    enemy.name = WEREWOLF
    enemy.hp += random.randint(10, 25)
    enemy.max_hp = enemy.hp
    enemy.strength = 1.50
    enemy.acc = 1.25
    enemy.coins = 0
    return enemy

def handle_trait_and_illness(enemy) -> Enemy:
    if enemy.type == NORMAL:
        valid = [i['name'] for i in Traits]
        traits = load_traits(valid)
        enemy.trait = random.choice(traits)

    if enemy.trait.name == CONTAGIOUS:
        valid = [i['name'] for i in Illnesses if i['name'] not in [LATE_ONSET_SIDS]]
        illness_name = random.choice(valid)
        illness_list = load_illnesses([illness_name])
        enemy.illness = next(i for i in illness_list)
    return enemy

# ================================================================================================

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
