import copy
import random
from dataclasses import dataclass, field
from typing import List, Optional, Dict

from savethewench.audio import play_sound
from savethewench.data import Enemies
from savethewench.data.audio import AREA_BOSS_THEME, GATOR
from savethewench.data.enemies import Bosses, Final_Boss, BAYOU_BILL
from savethewench.data.perks import RICKETY_PICKPOCKET
from savethewench.data.weapons import BARE_HANDS
from savethewench.ui import purple
from savethewench.util import print_and_sleep
from .base import Combatant, NPC, DisplayableText
from .perk import attach_perk
from .weapon import Weapon, load_weapon, load_weapons


@dataclass
class Enemy(Combatant, NPC):
    name: str = ''
    hp: int = 0
    weapons: List[str] = field(default_factory=list)
    bounty: int = 0
    type: str = ''
    items: List[str] = field(default_factory=list)
    coins: int = random.randint(5, 50)
    alive: bool = True

    current_weapon: Weapon = field(init=False)
    weapon_dict: Dict[str, Weapon] = field(init=False)
    max_hp: int = field(init=False)

    def __post_init__(self):
        self.weapon_dict = dict((w.name, w) for w in load_weapons(self.weapons))
        self.current_weapon = random.choice(list(self.weapon_dict.values()))
        self.max_hp = self.hp

    def drop_weapon(self) -> Optional[Weapon]:
        if self.current_weapon.sell_value > 0:
            return self.current_weapon
        return None

    @attach_perk(RICKETY_PICKPOCKET, value_description="coins dropped")
    def drop_coins(self) -> int:
        return self.coins

    def handle_broken_weapon(self):
        del self.weapon_dict[self.current_weapon.name]
        if len(self.weapon_dict) == 0:
            self.weapon_dict[BARE_HANDS] = load_weapon(BARE_HANDS)
        self.current_weapon = random.choice(list(self.weapon_dict.values()))


def load_enemy(name: str) -> Enemy:
    matches = load_enemies([name])
    if len(matches) == 0:
        raise ValueError(f"Could not find enemy data for {name}")
    return matches[0]


def load_enemies(restriction: List[str] = None) -> List[Enemy]:
    return [Enemy(**d) for d in Enemies if restriction is None or d['name'] in restriction]


@dataclass
class Boss(Enemy):
    theme: str = AREA_BOSS_THEME
    preamble: List[DisplayableText] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict):
        data = copy.deepcopy(data)
        if 'preamble' in data:
            data['preamble'] = [DisplayableText(**d) for d in data['preamble']]
        return super().from_dict(data)

    def do_preamble(self):
        for displayableText in self.preamble:
            displayableText.display()

    def handle_hit(self, other: "Combatant") -> None:
        super().handle_hit(other)
        if self.name == BAYOU_BILL:
            gator = random.random() < 0.10
            if gator:
                bite = random.randint(3, 5)
                play_sound(GATOR)
                print_and_sleep(purple(f"Mama Gator attacked you for {bite} damage!"), 2)
                other.take_damage(bite, self)


def load_boss(name: str) -> Boss:
    matches = [Boss.from_dict(d) for d in Bosses if d['name'] == name]
    if len(matches) == 0:
        raise ValueError(f"Could not find boss data for {name}")
    return matches[0]


def load_final_boss() -> Boss:
    return Boss.from_dict(Final_Boss)
