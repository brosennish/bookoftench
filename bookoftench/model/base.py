from __future__ import annotations

import copy
import random
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, fields
from typing import Dict, List, Self

from bookoftench import event_logger
from bookoftench.audio import play_sound
from bookoftench.data.audio import WEAPON_BROKE, WHIFF
from bookoftench.data.enemies import SLEDGE_HAMMOND, BUTTERFINGERS, INVESTOR, PLANT, PREPARED, JUNKIE, ORACLE, It_Its
from bookoftench.data.weapons import MELEE, RANGED, BLIND
from bookoftench.model.events import HitEvent, CritEvent, MissEvent
from bookoftench.model.illness import Illness
from bookoftench.model.trait import Trait
from bookoftench.ui import red, yellow, color_text, purple, cyan, dim, green
from bookoftench.util import print_and_sleep

# ================================================================================================

@dataclass
class Buyable:
    name: str
    cost: int

    def __post_init__(self) -> None:
        self._original_cost = self.cost

    @property
    def original_cost(self) -> int:
        return self._original_cost

    @classmethod
    def from_dict(cls, data: dict):
        init_fields = {f.name for f in fields(cls) if f.init}
        return cls(**{k: v for k, v in data.items() if k in init_fields})

# ================================================================================================

@dataclass
class WeaponBase(ABC):
    name: str
    damage: int
    uses: int
    acc: float
    var: int
    crit: float
    sound: str
    type: str
    stun: float = 0
    base_name: str = None
    subtype: str = MELEE
    areas: list[str] | None = None
    is_elite: bool = False

    def __post_init__(self):
        if self.base_name is None:
            self.base_name = self.name

    def calculate_base_damage(self) -> int:
        base = self.damage + random.randint(-self.var, self.var)
        return max(0, base)

    def get_accuracy(self) -> float:
        return self.acc

    def play_sound(self) -> None:
        if len(self.sound) > 0:
            play_sound(self.sound)

    def use(self) -> None:
        if self.uses < 0:
            return
        self.uses -= 1

    def is_broken(self) -> bool:
        return self.uses == 0

    def format_uses(self) -> str:
        if self.uses == -1:
            return cyan('∞')
        elif self.uses == 1:
            return red(f"{self.uses}")
        elif self.uses in (2, 3):
            return yellow(f"{self.uses}")
        else:
            return f"{self.uses}"

    def get_build_format(self, strength: float | None, acc: float | None) -> str:
        crit_chance = round(self.crit + max(self.acc - 1, 0) * 0.10, 2)
        crit_chance = min(crit_chance, 0.35)

        return f"{cyan(self.name)}\n{dim(' | ').join([
            f"{dim("Dmg:")} {red(f"{round(self.damage * strength if strength and self.type == MELEE else self.damage):<2}")}",
            f"{dim("Acc:")} {yellow(f"{round(self.acc * acc if acc and self.type == RANGED else self.acc, 2):<4}")}",
            f"{dim("Var:")} {f"{red(f"{self.var}")}"}",
            f"{dim("Crit:")} {yellow(f"{crit_chance:<4}")}",
            f"{dim("Stun:")} {yellow(f"{self.stun:<4}")}",
            f"{dim("Uses:")} {self.format_uses()}",
        ])}"

    def get_complete_format(self, strength: float | None, acc: float | None) -> str:
        crit_chance = round(self.crit + max((acc or 1) - 1, 0) * 0.10, 2)
        crit_chance = min(crit_chance, 0.35)

        return f"{cyan(self.name)}\n{dim(' | ').join([
            f"{dim("Dmg:")} {red(f"{round(self.damage * strength if strength and self.type == MELEE else self.damage):<2}")}",
            f"{dim("Acc:")} {yellow(f"{round(self.acc * acc if acc and self.type == RANGED else self.acc, 2):<4}")}",
            f"{dim("Var:")} {red(f"{self.var}")}",
            f"{dim("Crit:")} {yellow(f"{crit_chance:<4}")}",
            f"{dim("Uses:")} {self.format_uses()}",
        ])}"

    def get_simple_format(self, strength: float | None, acc: float | None) -> str:
        return f"{cyan(self.name)}\n{dim(' | ').join([
            f"{dim("Dmg:")} {red(f"{round(self.damage * strength if strength and self.type == MELEE else self.damage):<2}")}",
            f"{dim("Acc:")} {yellow(f"{round(self.acc * acc if acc and self.type == RANGED else self.acc, 2):<4}")}",
            f"{dim("Uses:")} {self.format_uses()}",
        ])}"

    @abstractmethod
    def get_blind_effect(self) -> float:
        pass

    @abstractmethod
    def get_blind_turns(self) -> int:
        pass

# ================================================================================================

@dataclass
class DisplayableText:
    text: str
    color: str = None
    sleep: int = 0

    def display(self) -> None:
        print_and_sleep(color_text(self.color, self.text) if self.color is not None else self.text, seconds=self.sleep)

# ================================================================================================

@dataclass
class RandomDisplayableText:
    upper_threshold: float
    dialogue: List[DisplayableText]

    def display(self) -> None:
        for dt in self.dialogue:
            dt.display()

    @classmethod
    def from_dict(cls, data: dict) -> RandomDisplayableText:
        return cls(
            upper_threshold=data['upper_threshold'],
            dialogue=[DisplayableText(**d) for d in data['dialogue']],
        )

# ================================================================================================

@dataclass
class NPC:
    name: str
    random_dialogue: List[RandomDisplayableText] = field(default_factory=list)

    def __post_init__(self):
        self.random_dialogue.sort(key=lambda x: x.upper_threshold)

    def do_random_dialogue(self) -> None:
        roll = random.random()
        for rdt in self.random_dialogue:
            if roll <= rdt.upper_threshold:
                rdt.display()
                break

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        data = copy.deepcopy(data)
        if 'random_dialogue' in data:
            data['random_dialogue'] = [RandomDisplayableText.from_dict(d) for d in data['random_dialogue']]
        return cls(**data)

# ================================================================================================

@dataclass
class Combatant(ABC):
    weapon_dict: Dict[str, WeaponBase]
    name: str
    trait: Trait
    illness: Illness
    hp: int
    max_hp: int
    coins: int
    current_weapon: WeaponBase

    double_damage_active: bool = False
    crit_active: bool = False

    junkie_active: bool = True
    oracle_active: bool = True
    prepared_active: bool = True

    stunned: bool = False

    blind: bool = False
    blinded_by: str = ''
    blind_effect: float = 0.0
    blind_turns: int = 0

    def __init__(self):
        self.strength = None
        self.acc = None

    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, damage: int, other: "Combatant") -> int:
        self.hp -= damage
        if isinstance(self, NPC):
            self.do_random_dialogue()
        sledge_hammond_action(other)

        return damage

# ================================================================================================

    def calculate_accuracy(self) -> float:
        base = self.current_weapon.get_accuracy()
        accuracy = base * self.acc if self.current_weapon.type == RANGED else base
        if self.blind:
            self.blind_turns -= 1
            if self.blind_turns == 0:
                self.reset_blindness()
            return accuracy * (1 - self.blind_effect)
        return accuracy

    def handle_miss(self) -> None:
        play_sound(WHIFF)
        if isinstance(self, NPC):
            print_and_sleep(yellow(f"{self.name} missed!"), 1)
        else:
            print_and_sleep(yellow(f"You missed!"), 1)
            event_logger.log_event(MissEvent())

        if self.current_weapon.type == MELEE:
            if random.random() < 0.50:
                self.current_weapon.use()
        else:
            self.current_weapon.use()

        # --- handle broken weapon ---
        self.check_weapon_status()

# ================================================================================================

    def get_crit_chance(self) -> float:
        crit_chance = self.current_weapon.crit + max(self.acc - 1, 0) * 0.10
        return min(crit_chance, 0.35)

    def handle_crit(self, is_crit: bool) -> None:
        if not is_crit:
            return

        self.current_weapon.play_sound()
        print_and_sleep(red("*** Critical hit ***"), 1)

        if not isinstance(self, NPC):
            event_logger.log_event(CritEvent())

# ================================================================================================

    @abstractmethod
    def handle_broken_weapon(self) -> None:
        pass

    def check_weapon_status(self) -> None:
        if self.current_weapon.is_broken():
            play_sound(WEAPON_BROKE)
            print_and_sleep(yellow(f"{self.current_weapon.name} broke!"), 1)
            self.handle_broken_weapon()

# ================================================================================================

    def reset_blindness(self) -> None:
        self.blind: bool = False
        self.blinded_by: str = ''
        self.blind_effect: float = 0.0
        self.blind_turns: int = 0

    def set_blind_effect(self, blinded_by: str, blind_effect: float, blind_turns: int) -> None:
        self.blind = True
        self.blinded_by = blinded_by
        self.blind_effect = blind_effect
        self.blind_turns = blind_turns

    def handle_blinding(self, other: "Combatant") -> None:
        if self.current_weapon.type != BLIND:
            return

        if other.blind:
            print_and_sleep(yellow(f"{other.name} is already blinded!"), 1)
            return

        blind_effect = self.current_weapon.get_blind_effect()
        if blind_effect > 0:
            blind_turns = self.current_weapon.get_blind_turns()
            other.set_blind_effect(self.current_weapon.base_name, blind_effect, blind_turns)
            if other.blind:  # skip if beer goggles prevents blindness
                prefix = f"{other.name} has been" if isinstance(other, NPC) else "You have been"
                print_and_sleep(
                    purple(
                        f"{prefix} blinded by {self.current_weapon.name}. Accuracy down {round(blind_effect * 100)}% for "
                        f"{blind_turns} turns"), 1)

# ================================================================================================

    def handle_stun(self, other: "Combatant") -> None:
        if other.stunned:
            return

        stun_chance = self.current_weapon.stun / max(other.strength, 1)

        if random.random() >= stun_chance:
            return

        other.stunned = True

        stun_text = (
            f"{other.name} was stunned by your {self.current_weapon.name}!"
            if isinstance(other, NPC)
            else f"You were stunned by the enemy's {self.current_weapon.name}!"
        )

        print_and_sleep(yellow(stun_text), 1)

# ================================================================================================

    def handle_hit(self, other: "Combatant") -> None:
        self.current_weapon.use()

        if not self.is_alive():  # solomon train
            return

        # --- calculate base damage ---
        base_damage = self.current_weapon.calculate_base_damage()

        # apply strength to melee
        if self.current_weapon.type == MELEE:
            base_damage = round(base_damage * self.strength)

        # --- get calculated crit chance ---
        crit = random.random() < self.get_crit_chance()

        if self.crit_active:
            crit = True
            self.crit_active = False
        self.handle_crit(crit)

        # --- 1.5x damage if crit ---
        damage_inflicted = round(base_damage * 1.5) if crit else base_damage

        if isinstance(other, NPC):
            # --- double damage if item used ---
            if self.current_weapon.type == MELEE and self.double_damage_active == True:
                damage_inflicted *= 2
                self.double_damage_active = False
                print_and_sleep(red("*** Double damage ***"), 1)

            # --- print and log ---
            print_and_sleep(f"You attacked {other.name} with your {self.current_weapon.name} for "
                            f"{red(damage_inflicted)} damage!", 1)
            event_logger.log_event(HitEvent(self.current_weapon.type))

        else:
            pronoun = "its" if self.name in It_Its else "their"
            print_and_sleep(f"{self.name} attacked you with {pronoun} {self.current_weapon.name} for "
                            f"{red(damage_inflicted)} damage!", 1)

        other.take_damage(damage_inflicted, self)

        # --- handle weapon effects ---
        self.handle_blinding(other)
        self.handle_stun(other)

        # --- handle broken weapon ---
        self.check_weapon_status()

# ================================================================================================

    def attack(self, other: "Combatant") -> None:
        enemy_turn = not isinstance(other, NPC)

        if enemy_turn and self.stunned:
            print_and_sleep(yellow(f"{self.name} is stunned and unable to move!"), 1)
            self.stunned = False
            return

        if random.random() > self.calculate_accuracy():
            self.handle_miss()
        else:
            self.handle_hit(other)

        # trait handling after enemy turn
        if enemy_turn:
            if self.is_alive() and self.trait:
                self.handle_traits(other)

# ================================================================================================

    # todo - abstract trait logic and take time as parameter
    def handle_traits(self, other: "Combatant") -> None:
        time = 1

        if self.trait.name == BUTTERFINGERS:
            dropped = min(self.coins, random.randint(1, 10))
            self.coins -= dropped
            word = 'coin' if dropped == 1 else 'coins'
            if dropped > 0:
                print_and_sleep(yellow(f"{self.name} dropped {dropped} {word}."), time)

        elif self.trait.name == INVESTOR:
            change = random.randint(-10, 10)
            if change != 0:
                if change < 0 and self.coins < abs(change):
                    change = self.coins * -1
                self.coins += change

        elif self.trait.name == JUNKIE:
            if self.hp < 50 and self.junkie_active:
                amount = round(random.uniform(0.1, 0.25), 2)
                self.strength += amount
                print_and_sleep(green(f"{self.name} got yoked and increased strength by {amount}."), time)
                self.junkie_active = False

        elif other.current_weapon.type == BLIND and self.trait.name == ORACLE and self.oracle_active:
            self.strength += round(random.uniform(0.03, 0.12), 2)
            self.acc += round(random.uniform(0.03, 0.12), 2)
            print_and_sleep(green(f"{self.name}'s strength and accuracy increased."), time)
            other.oracle_active = False

        elif self.trait.name == PLANT and self.hp < self.max_hp:
            amount = random.randint(1, 5)
            if (self.max_hp - self.hp) < amount:
                amount = self.max_hp - self.hp
            self.hp += amount
            print_and_sleep(green(f"{self.name} regenerated {amount} HP."), time)

        elif self.trait.name == PREPARED:
            threshold = random.uniform(0.1, 0.5)
            if self.hp < (self.max_hp * threshold) and self.prepared_active:
                original = self.hp
                amount = random.randint(25, 50)
                self.hp += min(amount, self.max_hp - self.hp)
                print_and_sleep(green(f"{self.name} used an item and restored {self.hp - original} HP."), time)
                self.prepared_active = False

# ================================================================================================

def sledge_hammond_action(other: Combatant) -> None:
    if other.name == SLEDGE_HAMMOND:
        if other.hp > 0:
            other.hp += 5
            print_and_sleep(purple("Sledge Hammond took steroids and restored 5 HP!"), 1)
    return None