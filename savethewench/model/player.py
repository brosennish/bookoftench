import random
from dataclasses import dataclass, field
from typing import Dict, List

from savethewench import event_logger
from savethewench.data.items import TENCH_FILET
from savethewench.data.perks import DOCTOR_FISH, HEALTH_NUT, LUCKY_TENCHS_FIN, GRAMBLIN_MAN, GRAMBLING_ADDICT, \
    VAGABONDAGE, NOMADS_LAND, BEER_GOGGLES, WALLET_CHAIN, INTRO_TO_TENCH
from savethewench.data.weapons import BARE_HANDS, KNIFE
from savethewench.ui import yellow, dim, green, cyan
from savethewench.util import print_and_sleep
from .achievement import Achievement
from .base import Combatant, Buyable
from .events import ItemUsedEvent, ItemSoldEvent, BuyWeaponEvent, BuyItemEvent, BuyPerkEvent, LevelUpEvent, \
    SwapWeaponEvent, WeaponBrokeEvent
from .item import Item, load_items
from .perk import attach_perk, perk_is_active, Perk, activate_perk
from .weapon import load_weapons, Weapon


def item_defaults() -> Dict[str, Item]:
    return dict((it.name, it) for it in load_items([TENCH_FILET]))


def weapon_defaults() -> Dict[str, Weapon]:
    return dict((it.name, it) for it in load_weapons([BARE_HANDS, KNIFE]))


@dataclass
class Player(Combatant):
    name: str = ''
    lives: int = 3
    lvl: int = 1
    hp: int = 100
    max_hp: int = 100
    xp: int = 0

    coins: int = 0
    interest: int = 0
    casino_won: int = 0
    casino_lost: int = 0
    games_played: int = 0

    _max_plays: int = 10
    _max_items: int = 5
    _max_weapons: int = 5

    _blind = False
    # TODO maybe add starting items/weapons to config file
    items: Dict[str, Item] = field(default_factory=item_defaults)
    weapon_dict: Dict[str, Weapon] = field(default_factory=weapon_defaults)
    achievements: List[Achievement] = field(default_factory=list)
    current_weapon: Weapon = None

    def __post_init__(self):
        self.current_weapon = self.weapon_dict[BARE_HANDS]

    @property
    @attach_perk(GRAMBLIN_MAN, GRAMBLING_ADDICT, silent=True)
    def max_plays(self):
        return self._max_plays

    @property
    @attach_perk(NOMADS_LAND, VAGABONDAGE, silent=True)
    def max_items(self):
        return self._max_items

    @property
    @attach_perk(NOMADS_LAND, VAGABONDAGE, silent=True)
    def max_weapons(self):
        return self._max_weapons

    @property  # specifically made for returning a calculated value: print(player.xp_needed)
    def xp_needed(self):
        return 100 + (self.lvl - 1) * 10

    @property
    def remaining_plays(self):
        return self.max_plays - self.games_played

    @property
    @attach_perk(BEER_GOGGLES)
    def blind(self) -> bool:
        return self._blind

    @blind.setter
    def blind(self, blind: bool) -> None:
        self._blind = blind

    def get_items(self) -> List[Item]:
        return list(self.items.values())

    def display_item_count(self):
        print(f"Items {dim(f"({len(self.items)}/{self.max_items})")}")

    def add_item(self, item: Item) -> bool:
        if item.name in self.items:
            print_and_sleep(yellow(f"You already have {item.name}!"), 1)
            return False
        elif len(self.items) >= self.max_items:
            print_and_sleep(yellow("Your item sack is full."), 1)
            return False
        else:
            self.items[item.name] = item
            return True

    def use_item(self, name: str):
        item = self.items[name]
        self.gain_hp(item.hp)

        base = item.hp
        has_nut = perk_is_active(HEALTH_NUT)
        has_fish = perk_is_active(DOCTOR_FISH)

        bonus = 0
        if has_nut and has_fish:
            bonus = int(base * 0.25) + 2
        elif has_nut:
            bonus = int(base * 0.25)
        elif has_fish:
            bonus = 2

        gain = 0
        if bonus > 0:
            gain = min(self.max_hp - self.hp, bonus)
            self.gain_hp(gain)

        # Remove from actual inventory
        del self.items[item.name]
        event_logger.log_event(ItemUsedEvent(item.name, len(self.items), self.hp, self.max_hp, gain))

    def make_purchase(self, buyable: Buyable) -> bool:
        if self.coins <= buyable.cost:
            print_and_sleep(yellow(f"Need more coin"), 1)
            return False
        if isinstance(buyable, Item) and self.add_item(buyable):
            event_logger.log_event(BuyItemEvent(buyable.name, buyable.cost))
        elif isinstance(buyable, Weapon) and self.add_weapon(buyable):
            event_logger.log_event(BuyWeaponEvent(buyable.name, buyable.cost, buyable.uses))
        elif isinstance(buyable, Perk) and self.add_perk(buyable):
            event_logger.log_event(BuyPerkEvent(buyable.name, buyable.cost))
        else:
            return False
        self.coins -= buyable.cost
        return True

    def sell_item(self, name: str):
        item = self.items[name]
        self.coins += item.sell_value
        del self.items[name]
        event_logger.log_event(ItemSoldEvent(item.name, item.sell_value))

    def gain_hp(self, amount: int):
        self.hp = min(self.max_hp, self.hp + amount)  # clamp on max_hp

    def display_weapon_count(self):
        print(f"Weapons {dim(f"({len(self.weapon_dict)}/{self.max_weapons})")}")

    def get_weapons(self) -> List[Weapon]:
        return list(self.weapon_dict.values())

    def add_weapon(self, weapon: Weapon) -> bool:
        if weapon.name in self.weapon_dict:
            print_and_sleep(yellow(dim("You already have this weapon.")), 1)
            return False
        elif len(self.weapon_dict) >= self.max_weapons:
            print_and_sleep(yellow("Your weapon sack is full."), 1)
            return False
        else:
            self.weapon_dict[weapon.name] = weapon
            return True

    def sell_weapon(self, name: str):
        weapon = self.weapon_dict[name]
        self.coins += weapon.sell_value
        del self.weapon_dict[name]
        event_logger.log_event(ItemSoldEvent(weapon.name, weapon.sell_value))

    def equip_weapon(self, name: str):
        if name != self.current_weapon.name:
            event_logger.log_event(SwapWeaponEvent())
            self.current_weapon = self.weapon_dict[name]
            print_and_sleep(cyan(f"{name} equipped."), 1)

    @attach_perk(LUCKY_TENCHS_FIN, value_description="crit chance")
    def get_crit_chance(self) -> float:
        return super().get_crit_chance()

    @staticmethod
    def add_perk(perk: Perk) -> bool:
        if perk_is_active(perk.name):
            print_and_sleep(yellow(f"You already have this perk."), 1)
            return False
        activate_perk(perk.name)
        return True

    def gain_coins(self, amount: int):
        self.coins += amount
        print_and_sleep(green(f"You gained {amount} coins!"), 1)

    @staticmethod
    @attach_perk(INTRO_TO_TENCH) # AP_TENCH_STUDIES won't work as is, but there might be a way
    def _calculate_xp_from_enemy(enemy: Combatant) -> int:
        return int(enemy.max_hp / 2.8)

    def gain_xp_from_enemy(self, enemy: Combatant) -> bool:
        amount = self._calculate_xp_from_enemy(enemy)
        return self.gain_xp(amount)

    def gain_xp(self, amount: int) -> bool:
        self.xp += amount
        print_and_sleep(green(f"You gained {amount} XP!"), 1)

        leveled_up = False

        # handles cases where a big XP chunk might give multiple levels
        while self.xp >= self.xp_needed:
            self.level_up()
            leveled_up = True

        return leveled_up

    def level_up(self):
        # ---- core level-up effects live here ----
        self.xp -= self.xp_needed
        self.lvl += 1
        cash_reward = random.randint(100, 200)
        self.coins += cash_reward
        self.games_played = 0

        old_max = self.max_hp
        if self.max_hp < 150:
            self.max_hp += 5
        self.hp = self.max_hp

        item_reward = None
        if len(self.items) < self.max_items:
            filtered: List[Item] = [item for item in load_items() if item.name not in self.items]
            if filtered:
                item_reward = random.choice(filtered)
                self.items[item_reward.name] = item_reward
                item_reward = str(item_reward.to_sellable_item())

        event_logger.log_event(LevelUpEvent(self.lvl, old_max, self.max_hp, item_reward, cash_reward))

    def apply_death_penalties(self):
        self.coins = int(self.coins * 0.25) if perk_is_active(WALLET_CHAIN) else 0  # TODO use the framework for this
        self.items = item_defaults()
        self.weapon_dict = weapon_defaults()
        self.current_weapon = self.weapon_dict[BARE_HANDS]
        self.hp = self.max_hp
        self.xp = 0

    def handle_broken_weapon(self):
        event_logger.log_event(WeaponBrokeEvent())
        del self.weapon_dict[self.current_weapon.name]
        self.current_weapon = self.weapon_dict[BARE_HANDS]
