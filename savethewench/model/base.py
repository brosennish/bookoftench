import random
from dataclasses import dataclass

from savethewench import event_logger
from savethewench.audio import play_sound
from savethewench.model.events import HitEvent, CritEvent, MissEvent
from savethewench.ui import red, yellow
from savethewench.util import print_and_sleep


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


@dataclass
class NPC:
    name: str


@dataclass
class Combatant:
    name: str
    hp: int
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

    def display_miss(self):
        print_and_sleep(yellow(f"{self.name if isinstance(self, NPC) else "You"} missed!"), 1)

    def display_hit(self, other: "Combatant", damage_inflicted: int) -> None:
        if isinstance(other, NPC):
            print_and_sleep(f"You attacked {other.name} with your {self.current_weapon.name} for "
                            f"{red(damage_inflicted)} damage!", 1)
        else:
            print_and_sleep(f"{self.name} attacked you with their {self.current_weapon.name} for "
                            f"{red(damage_inflicted)} damage!", 1)

    def display_crit(self):
        self.current_weapon.play_sound()
        print_and_sleep(red("*** Critical hit ***"), 1)

    def attack(self, other: "Combatant") -> None:
        if random.random() > self.calculate_accuracy():
            event_logger.log_event(MissEvent(self.display_miss))
        else:
            base_damage = self.current_weapon.calculate_base_damage()
            crit = random.random() < self.get_crit_chance()
            dmg = base_damage * 2 if crit else base_damage  # 2x damage if crit, otherwise dmg after spread
            damage_inflicted = other.take_damage(dmg)
            event_logger.log_event(HitEvent(lambda: self.display_hit(other, damage_inflicted)))
            if crit:
                event_logger.log_event(CritEvent(self.display_crit))
