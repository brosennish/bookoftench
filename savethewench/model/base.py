import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict

from savethewench import event_logger
from savethewench.audio import play_sound
from savethewench.data.audio import WEAPON_BROKE
from savethewench.model.events import HitEvent, CritEvent, MissEvent
from savethewench.ui import red, yellow
from savethewench.util import print_and_sleep


@dataclass
class Buyable:
    cost: int


@dataclass
class WeaponBase:
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

    def play_sound(self):
        if len(self.sound) > 0:
            play_sound(self.sound)

    def use(self):
        if self.uses < 0:
            return
        self.uses -= 1

    def is_broken(self):
        return self.uses == 0


@dataclass
class NPC:
    name: str


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

    def __post_init__(self):
        self.blind = False
        self.blinded_by = ""
        self.blind_effect = 0.0
        self.blind_turns = 0

    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, damage: int) -> int:
        self.hp -= damage
        return damage

    def calculate_accuracy(self) -> float:
        return self.current_weapon.accuracy

    def get_crit_chance(self) -> float:
        return self.current_weapon.crit

    def handle_miss(self):
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
    def handle_broken_weapon(self):
        pass

    def handle_hit(self, other: "Combatant", damage_inflicted: int) -> None:
        self.current_weapon.use()
        if isinstance(other, NPC):
            print_and_sleep(f"You attacked {other.name} with your {self.current_weapon.name} for "
                            f"{red(damage_inflicted)} damage!", 1)
            event_logger.log_event(HitEvent())
        else:
            print_and_sleep(f"{self.name} attacked you with their {self.current_weapon.name} for "
                            f"{red(damage_inflicted)} damage!", 1)
        if self.current_weapon.is_broken():
            play_sound(WEAPON_BROKE)
            print_and_sleep(yellow(f"{self.current_weapon.name} broke!"), 1)
            self.handle_broken_weapon()

    def attack(self, other: "Combatant") -> None:
        if random.random() > self.calculate_accuracy():
            self.handle_miss()
        else:
            base_damage = self.current_weapon.calculate_base_damage()
            crit = random.random() < self.get_crit_chance()
            dmg = base_damage * 2 if crit else base_damage  # 2x damage if crit, otherwise dmg after spread
            self.handle_hit(other, other.take_damage(dmg))
            self.handle_crit(crit)
