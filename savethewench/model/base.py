from __future__ import annotations

import copy
import random
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List

from savethewench import event_logger
from savethewench.audio import play_sound
from savethewench.data.audio import WEAPON_BROKE
from savethewench.data.enemies import SLEDGE_HAMMOND
from savethewench.model.events import HitEvent, CritEvent, MissEvent
from savethewench.ui import red, yellow, color_text, purple, cyan, dim
from savethewench.util import print_and_sleep


@dataclass
class Buyable:
    name: str
    cost: int


@dataclass
class WeaponBase(ABC):
    name: str
    damage: int
    uses: int
    accuracy: float
    spread: int
    crit: float
    sound: str

    def calculate_base_damage(self) -> int:
        base = self.damage + random.randint(-self.spread, self.spread)  # Base damage +/- 10
        return max(5, base)  # Damage >= 5

    def get_accuracy(self) -> float:
        return self.accuracy

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

    def get_simple_format(self) -> str:
        return f"{cyan(self.name)}\n{dim(' | ').join([
            f"{dim("Damage:")} {red(f"{self.damage}")}",
            f"{dim("Accuracy:")} {yellow(f"{self.accuracy}")}",
            f"{dim("Uses:")} {self.format_uses()}"
        ])}"

    @abstractmethod
    def get_blind_effect(self) -> float:
        pass

    @abstractmethod
    def get_blind_turns(self) -> int:
        pass


@dataclass
class DisplayableText:
    text: str
    color: str = None
    sleep: int = 0

    def display(self) -> None:
        print_and_sleep(color_text(self.color, self.text) if self.color is not None else self.text, seconds=self.sleep)


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
    def from_dict(cls, data: dict) -> NPC:
        data = copy.deepcopy(data)
        if 'random_dialogue' in data:
            data['random_dialogue'] = [RandomDisplayableText.from_dict(d) for d in data['random_dialogue']]
        return cls(**data)


@dataclass
class Combatant(ABC):
    weapon_dict: Dict[str, WeaponBase]
    name: str
    hp: int
    max_hp: int
    current_weapon: WeaponBase

    blind: bool = False
    blinded_by: str = ''
    blind_effect: float = 0.0
    blind_turns: int = 0

    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, damage: int, other: "Combatant") -> int:
        self.hp -= damage
        if isinstance(self, NPC):
            self.do_random_dialogue()
        # TODO generalize, get specific logic out of components
        if self.name == SLEDGE_HAMMOND:
            self.hp += 3
            print_and_sleep(purple("Sledge Hammond took steroids and restored 3 HP!"), 1)
        return damage

    def reset_blindness(self) -> None:
        self.blind: bool = False
        self.blinded_by: str = ''
        self.blind_effect: float = 0.0
        self.blind_turns: int = 0

    def calculate_accuracy(self) -> float:
        if self.blind:
            self.blind_turns -= 1
            if self.blind_turns == 0:
                self.reset_blindness()
            return self.current_weapon.get_accuracy() * (1 - self.blind_effect)
        return self.current_weapon.get_accuracy()

    def get_crit_chance(self) -> float:
        return self.current_weapon.crit

    def handle_miss(self) -> None:
        if isinstance(self, NPC):
            print_and_sleep(yellow(f"{self.name} missed!"), 1)
        else:
            print_and_sleep(yellow(f"You missed!"), 1)
            event_logger.log_event(MissEvent())

    def handle_crit(self, is_crit: bool) -> None:
        if not is_crit:
            return
        self.current_weapon.play_sound()
        print_and_sleep(red("*** Critical hit ***"), 1)
        if not isinstance(self, NPC):
            event_logger.log_event(CritEvent())

    @abstractmethod
    def handle_broken_weapon(self) -> None:
        pass

    def set_blind_effect(self, blinded_by: str, blind_effect: float, blind_turns: int) -> None:
        self.blind = True
        self.blinded_by = blinded_by
        self.blind_effect = blind_effect
        self.blind_turns = blind_turns

    def handle_blinding(self, other: "Combatant") -> None:
        blind_effect = self.current_weapon.get_blind_effect()
        if blind_effect > 0:
            blind_turns = self.current_weapon.get_blind_turns()
            other.set_blind_effect(self.current_weapon.name, blind_effect, blind_turns)
            if other.blind:  # skip if beer goggles prevents blindness
                prefix = f"{other.name} has been" if isinstance(other, NPC) else "You have been"
                print_and_sleep(
                    purple(
                        f"{prefix} blinded by {self.current_weapon.name}. Accuracy down {int(blind_effect * 100)}% for "
                        f"{blind_turns} turns"), 1)

    def handle_hit(self, other: "Combatant") -> None:
        self.current_weapon.use()
        if not self.is_alive():  # solomon train
            return
        base_damage = self.current_weapon.calculate_base_damage()
        crit = random.random() < self.get_crit_chance()
        damage_inflicted = base_damage * 2 if crit else base_damage  # 2x damage if crit, otherwise dmg after spread
        other.take_damage(damage_inflicted, self)
        if isinstance(other, NPC):
            print_and_sleep(f"You attacked {other.name} with your {self.current_weapon.name} for "
                            f"{red(damage_inflicted)} damage!", 1)
            event_logger.log_event(HitEvent(self.current_weapon.name))
        else:
            print_and_sleep(f"{self.name} attacked you with their {self.current_weapon.name} for "
                            f"{red(damage_inflicted)} damage!", 1)
        self.handle_crit(crit)
        self.handle_blinding(other)
        if self.current_weapon.is_broken():
            play_sound(WEAPON_BROKE)
            print_and_sleep(yellow(f"{self.current_weapon.name} broke!"), 1)
            self.handle_broken_weapon()

    def attack(self, other: "Combatant") -> None:
        if random.random() > self.calculate_accuracy():
            self.handle_miss()
        else:
            self.handle_hit(other)
