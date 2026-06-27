from __future__ import annotations

import copy
import random
from dataclasses import dataclass, field

from bookoftench.data import Areas
from bookoftench.data.areas import EncounterType, CAVE, CITY, FOREST, SWAMP
from bookoftench.data.components import ActionMenuDefaults, DISCOVER_DISCOVERABLE, DISCOVER_ITEM, DISCOVER_PERK, \
    DISCOVER_WEAPON, \
    SPAWN_ENEMY, ENCOUNTER_SUB_BOSS, SPECIAL_EVENT
from bookoftench.data.enemies import Enemy_Adjectives, Traits, WEREWOLF, CONTAGIOUS, NIGHT_OWL, HOHKKEN, BOSS, \
    NORMAL, SPECIAL_BOSS
from bookoftench.ui import purple, yellow, blue
from bookoftench.util import print_and_sleep
from .enemy import Enemy, load_enemy, Boss, load_boss, load_final_boss, load_special_boss, SpecialBoss
from .illness import load_illnesses
from .perk import perk_is_active
from .shop import Shop
from .trait import load_traits, load_trait
from .weapon import load_weapon, make_elite_weapon
from bookoftench.data.environment import NIGHT, FULL
from bookoftench.data.illnesses import Illnesses, LATE_ONSET_SIDS
from bookoftench.data.perks import SHERLOCK_TENCH
from bookoftench.data.weapons import CLAWS, BLIND, SPECIAL
from ..audio import play_sound
from ..data.audio import ENEMY_APPEARS, OWL_SFX, WEREWOLF_SFX

# ================================================================================================

_search_defaults = {
    DISCOVER_PERK: 1,
    DISCOVER_WEAPON: 2,
    DISCOVER_ITEM: 3,
    ENCOUNTER_SUB_BOSS: 3,
    DISCOVER_DISCOVERABLE: 45,
    SPECIAL_EVENT: 9,
    SPAWN_ENEMY: 30,
}

_search_defaults_by_area = {
    CITY: {
        DISCOVER_PERK: 1,
        DISCOVER_WEAPON: 3,
        DISCOVER_ITEM: 4,
        ENCOUNTER_SUB_BOSS: 3,
        DISCOVER_DISCOVERABLE: 45,
        SPECIAL_EVENT: 11,
        SPAWN_ENEMY: 30,
    },

    FOREST: {
        DISCOVER_PERK: 2,
        DISCOVER_WEAPON: 2,
        DISCOVER_ITEM: 4,
        ENCOUNTER_SUB_BOSS: 3,
        DISCOVER_DISCOVERABLE: 45,
        SPECIAL_EVENT: 10,
        SPAWN_ENEMY: 28,
    },

    CAVE: {
        DISCOVER_PERK: 1,
        DISCOVER_WEAPON: 2,
        DISCOVER_ITEM: 2,
        ENCOUNTER_SUB_BOSS: 4,
        DISCOVER_DISCOVERABLE: 40,
        SPECIAL_EVENT: 9,
        SPAWN_ENEMY: 35,
    },

    SWAMP: {
        DISCOVER_PERK: 1,
        DISCOVER_WEAPON: 2,
        DISCOVER_ITEM: 3,
        ENCOUNTER_SUB_BOSS: 4,
        DISCOVER_DISCOVERABLE: 40,
        SPECIAL_EVENT: 10,
        SPAWN_ENEMY: 32,
    },
}

_event_defaults = {
    SPECIAL_EVENT: 100,
}

# ================================================================================================

@dataclass
class AreaActions:
    pages: list[list[str]]

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
    enemies_seen: set[str] = field(default_factory=set)
    boss_defeated: bool = False
    boss: Boss | None = None
    current_enemy: Enemy | Boss | SpecialBoss | None = None
    special_bosses: list[str] = field(default_factory=list)

    shop: Shop = field(default_factory=Shop)
    search_probabilities: dict[str, int] = field(default_factory=lambda: _search_defaults.copy())
    event_probabilities: dict[str, int] = field(default_factory=lambda: _event_defaults.copy())
    actions_menu: AreaActions = field(default_factory=AreaActions.defaults)
    encounters: list[AreaEncounter] = field(default_factory=list)

# ================================================================================================

    def __post_init__(self) -> None:
        self.boss = load_boss(self.boss_name)
        self.search_probabilities = _search_defaults_by_area.get(
            self.name,
            _search_defaults,
        ).copy()

# ================================================================================================

    @property
    def post_kill_components(self) -> list[str]:
        return [
            encounter.component
            for encounter in self.encounters
            if encounter.type == EncounterType.POST_KILL
        ]

    @property
    def enemies_remaining(self) -> int:
        return max(0, self.enemy_count - self.enemies_killed)

# ================================================================================================

    # todo - refactor
    def spawn_enemy(self, game_state, player_level: int, wanted: str, time: str, moon: str) -> Enemy:
        enemy_name = self.handle_enemy_selection(wanted)

        # --- load Enemy, log encounter, add to seen ---
        enemy = load_enemy(enemy_name)
        self.log_encounter(enemy, game_state)
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
            print_and_sleep(f"{yellow('An enemy appears!')} {purple('(Elite enemy!)')}", 1)
        else:
            play_sound(ENEMY_APPEARS)
            print_and_sleep(yellow("An enemy appears!"), 1.5)

        # --- print enemy line, add adjective, and set current_enemy ---
        if enemy_line:
            print_and_sleep(blue(enemy_line), 3)

        adjective = random.choice(Enemy_Adjectives)
        enemy.name = f"{adjective} {enemy.name}"
        self.current_enemy = enemy

        # --- werewolf and night owl final initialization ---
        self.handle_final_trait_initialization(time)

        # --- elite weapon logic ---
        self.handle_elite_weapon()

        return self.current_enemy

    # ================================================================================================

    def handle_enemy_selection(self, wanted: str) -> str:
        wanted_enemy = load_enemy(wanted)
        available = [
            enemy_name
            for enemy_name in self.enemies
            if enemy_name not in self.enemies_seen
        ]

        if not available:
            self.enemies_seen.clear()
            available = [
                enemy_name
                for enemy_name in self.enemies
                if enemy_name not in self.enemies_seen
            ]

        enemy_name = random.choice(available)

        if self.enemies_seen:
            seen_enemy_chance = min(0.15, 0.01 * len(self.enemies_seen))

            if random.random() < seen_enemy_chance:
                enemy_name = random.choice(tuple(self.enemies_seen))

        # --- if Sherlock Tench, 15% chance of wanted if correct area ---
        if perk_is_active(SHERLOCK_TENCH):
            if self.name in wanted_enemy.areas and random.random() < 0.15:
                enemy_name = wanted

        return enemy_name

# ================================================================================================

    @staticmethod
    def handle_stat_adjustments(enemy: Enemy, player_level: int) -> str | None:
        enemy.hp += random.randint(-2, 2)
        enemy.hp += round((enemy.hp * 0.03) * max(player_level - 1, 0))
        enemy.max_hp = enemy.hp

        enemy.strength += random.uniform(-0.03, 0.03)
        enemy.acc += random.uniform(-0.03, 0.03)

        enemy.coins = max(0, enemy.coins + random.randint(-10, 20))

        if random.random() < 0.20:
            enemy.coins += round(enemy.coins * random.uniform(0.05, 0.25))

        return enemy.get_enemy_encounter_line()

    @staticmethod
    def handle_trait_transformation(enemy: Enemy, time: str, moon: str) -> Enemy:
        if has_trait(enemy, NIGHT_OWL) and time == NIGHT:
            enemy = create_night_owl(enemy)

        if has_trait(enemy, WEREWOLF) and time == NIGHT and moon == FULL:
            enemy = create_werewolf(enemy)

        return enemy

    @staticmethod
    def handle_elite_chance(enemy: Enemy, player_level: int) -> bool:
        elite_chance = min(0.15, max(0.0, (player_level - 1) * 0.03))

        if random.random() < elite_chance:
            enemy.name = f"Elite {enemy.name}"
            enemy.hp = int(enemy.hp * 1.5)
            enemy.max_hp = int(enemy.max_hp * 1.5)
            enemy.strength += 0.1

            if not has_trait(enemy, WEREWOLF):
                enemy.acc += 0.1

            enemy.coins = int(enemy.coins * 1.5)
            return True

        return False

    def handle_final_trait_initialization(self, time: str) -> None:
        if WEREWOLF in self.current_enemy.name:
            self.current_enemy.current_weapon = load_weapon(CLAWS)
            play_sound(WEREWOLF_SFX)
        elif has_trait(self.current_enemy, NIGHT_OWL) and time == NIGHT:
            play_sound(OWL_SFX)

    def handle_elite_weapon(self) -> None:
        if self.current_enemy.current_weapon.type not in [BLIND, SPECIAL] and random.random() < 0.15:
            base_weapon = self.current_enemy.current_weapon
            self.current_enemy.current_weapon = make_elite_weapon(base_weapon)

# ================================================================================================

    def spawn_special_boss(self, name: str, time: str, gs) -> SpecialBoss:
        special_boss = load_special_boss(name)
        self.enemies_seen.add(name)

        # --- assign Trait ---
        if special_boss.trait:
            if isinstance(special_boss.trait, str):
                trait_dict = next(
                    (trait for trait in Traits if trait["name"] == special_boss.trait),
                    None,
                )

                if trait_dict:
                    special_boss.trait = load_trait(trait_dict)

            # --- traits and illness ---
            if has_trait(special_boss, CONTAGIOUS):
                special_boss = handle_trait_and_illness(special_boss)

            # --- night owl logic ---
            if has_trait(special_boss, NIGHT_OWL) and time == NIGHT:
                special_boss = create_night_owl(special_boss)
                play_sound(OWL_SFX)

        self.current_enemy = special_boss
        self.log_encounter(self.current_enemy, gs)

        # --- elite weapon logic ---
        if self.current_enemy.current_weapon.type not in [BLIND, SPECIAL] and random.random() < 0.15:
            base_weapon = self.current_enemy.current_weapon
            self.current_enemy.current_weapon = make_elite_weapon(base_weapon)

        return self.current_enemy

    @staticmethod
    def log_encounter(enemy: Enemy | SpecialBoss, game_state) -> None:
        area = game_state.current_area.name
        game_state.encountered_enemies.append({"area": area, "enemy": enemy})

# ================================================================================================

    def set_boss_to_current_enemy(self, name: str) -> Boss:
        self.current_enemy = load_boss(name)

        if self.current_enemy.name != HOHKKEN:
            self.current_enemy.current_weapon = make_elite_weapon(
                self.current_enemy.current_weapon
            )

        return self.current_enemy

    def summon_boss(self) -> Boss:
        self.current_enemy = self.boss
        self.current_enemy.current_weapon = make_elite_weapon(
            self.current_enemy.current_weapon
        )

        return self.current_enemy

    def summon_final_boss(self) -> Boss:
        self.current_enemy = load_final_boss()
        self.current_enemy.current_weapon = make_elite_weapon(
            self.current_enemy.current_weapon
        )

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

def has_trait(enemy: Enemy, trait_name: str) -> bool:
    return bool(enemy.trait and enemy.trait.name == trait_name)


def create_night_owl(enemy: Enemy) -> Enemy:
    enemy.max_hp += random.randint(5, 10)
    enemy.hp = enemy.max_hp
    enemy.strength += round(random.uniform(0.01, 0.1), 2)
    enemy.acc += round(random.uniform(0.01, 0.1), 2)

    return enemy


def create_werewolf(enemy: Enemy) -> Enemy:
    enemy.name = WEREWOLF
    enemy.hp += random.randint(10, 25)
    enemy.max_hp = enemy.hp
    enemy.strength = 1.50
    enemy.acc = 1.25
    enemy.coins = 0

    return enemy

def handle_trait_and_illness(enemy: Enemy) -> Enemy:
    if enemy.type == NORMAL:
        valid = [trait["name"] for trait in Traits]
        traits = load_traits(valid)
        enemy.trait = random.choice(traits)

    if has_trait(enemy, CONTAGIOUS):
        valid = [
            illness["name"]
            for illness in Illnesses
            if illness["name"] != LATE_ONSET_SIDS
        ]
        illness_name = random.choice(valid)
        illness_list = load_illnesses([illness_name])
        enemy.illness = next(iter(illness_list))

    return enemy

# ================================================================================================

def load_areas() -> list[Area]:
    areas = []

    for area_data in Areas:
        data = copy.deepcopy(area_data)
        data["shop"] = Shop(data["name"])

        if "actions_menu" in data:
            data["actions_menu"] = AreaActions(**data["actions_menu"])

        if "encounters" in data:
            data["encounters"] = [
                AreaEncounter(**encounter)
                for encounter in data["encounters"]
            ]

        areas.append(Area(**data))

    return areas
