from dataclasses import dataclass, field
from typing import Dict, List

from savethewench import event_logger
from savethewench.data.items import TENCH_FILET
from savethewench.data.perks import DOCTOR_FISH, HEALTH_NUT
from savethewench.data.weapons import BARE_HANDS, KNIFE
from . import Achievement
from .events import ItemUsedEvent
from .item import Item, load_items
from .weapon import load_weapons, Weapon
from savethewench.ui import yellow, cyan, dim
from savethewench.util import print_and_sleep


@dataclass
class Player:
    name: str = ''
    lives: int = 3
    lvl: int = 1
    hp: int = 100
    max_hp: int = 100
    xp: int = 0

    coins: int = 0
    bank: int = 0
    bank_interest_rate: float = 0.10
    interest: int = 0
    casino_won: int = 0
    casino_lost: int = 0
    plays: int = 10

    max_items: int = 5
    max_weapons: int = 5
    # TODO maybe add starting items/weapons to config file
    items: Dict[str, Item] = field(default_factory=lambda: dict((it.name, it) for it in load_items([TENCH_FILET])))
    weapons: Dict[str, Weapon] = field(
        default_factory=lambda: dict((it.name, it) for it in load_weapons([BARE_HANDS, KNIFE])))
    perks: List[str] = field(default_factory=list)
    achievements: List[Achievement] = field(default_factory=list)
    current_weapon: Weapon = None

    blind: bool = False
    blinded_by: str = ''
    blind_effect: float = 0.0
    blind_turns: int = 0

    def __post_init__(self):
        self.current_weapon = self.weapons[BARE_HANDS]

    @property  # specifically made for returning a calculated value: print(player.xp_needed)
    def xp_needed(self):
        return 100 + (self.lvl - 1) * 10

    def get_items(self) -> List[Item]:
        return list(self.items.values())

    def add_item(self, item: Item):
        if item.name in self.items:
            print_and_sleep(yellow(f"You already have {item.name}!"), 1)
        elif len(self.items) >= self.max_items:
            print_and_sleep(yellow("Your item sack is full."), 1)
        else:
            self.items[item.name] = item
            print_and_sleep(cyan(f"{item.name} added to sack."), 1)

    def use_item(self, name: str):
        item = self.items[name]
        self.gain_hp(item.hp)

        base = item.hp
        has_nut = HEALTH_NUT in self.perks
        has_fish = DOCTOR_FISH in self.perks

        bonus = 0
        active_perks = []
        if has_nut and has_fish:
            bonus = int(base * 0.25) + 2
            active_perks = [DOCTOR_FISH, HEALTH_NUT]
        elif has_nut:
            bonus = int(base * 0.25)
            active_perks = [HEALTH_NUT]
        elif has_fish:
            bonus = 2
            active_perks = [DOCTOR_FISH]

        gain = 0
        if bonus > 0:
            gain = min(self.max_hp - self.hp, bonus)
            self.gain_hp(gain)

        # Remove from actual inventory
        del self.items[item.name]
        event_logger.log_event(ItemUsedEvent(item, len(self.items), self.hp, self.max_hp, gain, active_perks))

    def gain_hp(self, amount: int):
        self.hp = min(self.max_hp, self.hp + amount)  # clamp on max_hp

    def get_weapons(self) -> List[Weapon]:
        return list(self.weapons.values())

    def add_weapon(self, weapon: Weapon):
        print_and_sleep(cyan(f"You found a {weapon.name}!"), 1)
        if weapon.name in self.weapons:
            print_and_sleep(yellow(dim("You already have this weapon.")), 1)
        elif len(self.weapons) >= self.max_weapons:
            print_and_sleep(yellow("Your weapon sack is full."), 1)
        else:
            self.weapons[weapon.name] = weapon
            print_and_sleep(cyan(f"{weapon.name} added to sack."), 1)

    def equip_weapon(self, name: str):
        self.current_weapon = self.weapons[name]

    def add_perk(self, perk: str):
        self.perks.append(perk)


