import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from savethewench import event_logger
from savethewench.audio import play_sound
from savethewench.data.audio import RIFLE
from savethewench.data.items import TENCH_FILET
from savethewench.data.perks import DOCTOR_FISH, HEALTH_NUT, LUCKY_TENCHS_FIN, GRAMBLIN_MAN, GRAMBLING_ADDICT, \
    VAGABONDAGE, NOMADS_LAND, BEER_GOGGLES, WALLET_CHAIN, INTRO_TO_TENCH, AP_TENCH_STUDIES, AMBROSE_BLADE, \
    ROSETTI_THE_GYM_RAT, KARATE_LESSONS, MARTIAL_ARTS_TRAINING, TENCH_EYES, SOLOMON_TRAIN, VAMPIRIC_SPERM, TENCH_GENES
from savethewench.data.weapons import BARE_HANDS, KNIFE, MELEE, PROJECTILE, MACHETE, FIRE_AXE, AXE
from savethewench.event_logger import subscribe_function
from savethewench.model.illness import Illness
from savethewench.ui import yellow, dim, green, cyan, purple, red
from savethewench.util import print_and_sleep
from .base import Combatant, Buyable
from .events import ItemUsedEvent, ItemSoldEvent, BuyWeaponEvent, BuyItemEvent, BuyPerkEvent, LevelUpEvent, \
    SwapWeaponEvent, WeaponBrokeEvent, HitEvent, PlayerDeathEvent
from .item import Item, load_items
from .perk import attach_perk, perk_is_active, Perk, activate_perk, attach_perk_conditional, load_perks
from .weapon import load_weapons, Weapon


@dataclass
class PlayerWeapon(Weapon):

    def _is_bladed(self) -> bool:
        return self.name in (KNIFE, MACHETE, AXE, FIRE_AXE)

    def calculate_base_damage(self) -> int:
        base_damage = self.calculate_base_damage_no_perk()

        @attach_perk_conditional(ROSETTI_THE_GYM_RAT, value_description="melee damage",
                                 condition=lambda: self.type == MELEE)
        @attach_perk_conditional(AMBROSE_BLADE, value_description="blade damage",
                                 condition=lambda: self._is_bladed())
        @attach_perk_conditional(KARATE_LESSONS, MARTIAL_ARTS_TRAINING, value_description="bare hands damage",
                                 condition=lambda: self.name == BARE_HANDS)
        def apply_perks():
            return base_damage

        return int(apply_perks())

    def get_accuracy(self) -> float:
        @attach_perk_conditional(TENCH_EYES, value_description="projectile accuracy",
                                 condition=lambda: self.type == PROJECTILE)
        def apply_perks():
            return self.accuracy

        return apply_perks()

    @classmethod
    def from_weapon(cls, weapon: Weapon):
        return cls(**weapon.__dict__)


def item_defaults() -> Dict[str, Item]:
    return dict((it.name, it) for it in load_items([TENCH_FILET]))


def weapon_defaults() -> Dict[str, PlayerWeapon]:
    return dict((it.name, PlayerWeapon.from_weapon(it)) for it in load_weapons([BARE_HANDS, KNIFE]))


@dataclass
class Player(Combatant):
    name: str = ''
    lives: int = 3
    lvl: int = 1
    hp: int = 100
    max_hp: int = 100
    xp: int = 0

    illness: Optional[Illness] = None
    illness_death_lvl: Optional[int] = None

    coins: int = 0
    casino_won: int = 0
    casino_lost: int = 0
    games_played: int = 0

    _max_plays: int = 10
    _max_items: int = 5
    _max_weapons: int = 5

    _blind = False
    # TODO maybe add starting items/weapons to config file
    items: Dict[str, Item] = field(default_factory=item_defaults)
    weapon_dict: Dict[str, PlayerWeapon] = field(default_factory=weapon_defaults)
    current_weapon: Weapon = None

    cheat_death_enabled: bool = False

    def __post_init__(self):
        self.current_weapon = self.weapon_dict[BARE_HANDS]
        self._subscribe_listeners()

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
    def blind(self) -> bool:
        return self._blind

    @blind.setter
    def blind(self, blind: bool) -> None:
        if blind and perk_is_active(BEER_GOGGLES):
            print_and_sleep(purple(f"{BEER_GOGGLES} prevented blindness."), 1)
        else:
            self._blind = blind

    def is_sick(self) -> bool:
        return self.illness is not None

    def get_items(self) -> List[Item]:
        return list(self.items.values())

    def display_item_count(self):
        print_and_sleep(f"Items {dim(f"({len(self.items)}/{self.max_items})")}")

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

    @attach_perk(HEALTH_NUT, DOCTOR_FISH, value_description="hp gained")
    def _apply_hp_bonus(self, base: int) -> int:
        return base

    def use_item(self, name: str):
        item = self.items[name]
        gain = int(min(self.max_hp - self.hp, self._apply_hp_bonus(item.hp)))
        self.gain_hp(gain)

        # Remove from actual inventory
        del self.items[item.name]
        event_logger.log_event(ItemUsedEvent(item.name, len(self.items), self.hp, self.max_hp, gain))

    def make_purchase(self, buyable: Buyable) -> bool:
        if self.coins < buyable.cost:
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
        print_and_sleep(f"Weapons {dim(f"({len(self.weapon_dict)}/{self.max_weapons})")}")

    def display_equip_header(self):
        self.display_weapon_count()
        print_and_sleep(f"{cyan(self.current_weapon.name)} {dim('(Equipped)')}", newline_prefix=False)

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
            self.weapon_dict[weapon.name] = PlayerWeapon.from_weapon(weapon)
            return True

    def sell_weapon(self, name: str):
        sellable_weapon = self.weapon_dict[name].to_sellable_weapon()
        self.coins += sellable_weapon.sell_value
        del self.weapon_dict[name]
        if name == self.current_weapon.name:
            selection = next((w for w in self.weapon_dict.values()))
            self.current_weapon = PlayerWeapon.from_weapon(selection)
        event_logger.log_event(ItemSoldEvent(sellable_weapon.name, sellable_weapon.sell_value))

    def equip_weapon(self, name: str):
        if name != self.current_weapon.name:
            event_logger.log_event(SwapWeaponEvent())
            self.current_weapon = self.weapon_dict[name]
            print_and_sleep(cyan(f"{name} equipped."), 1)

    def swap_found_item(self, old_name: str, found_item: Item):
        del self.items[old_name]
        self.items[found_item.name] = found_item
        print_and_sleep(cyan(f"{old_name} discarded. {found_item.name} added to sack."), 1)

    def swap_found_weapon(self, old_name: str, found_weapon: Weapon):
        del self.weapon_dict[old_name]
        self.weapon_dict[found_weapon.name] = PlayerWeapon.from_weapon(found_weapon)
        self.current_weapon = self.weapon_dict[found_weapon.name]
        print_and_sleep(cyan(f"{old_name} discarded. {found_weapon.name} equipped."), 1)

    def obtain_enemy_weapon(self, enemy_weapon: Weapon):
        match = next((w for w in self.weapon_dict.values()
                      if w.name == enemy_weapon.name), None)
        if match:
            if match.uses < enemy_weapon.uses:
                self.weapon_dict[enemy_weapon.name] = PlayerWeapon.from_weapon(enemy_weapon)
                self.current_weapon = self.weapon_dict[enemy_weapon.name]
                print_and_sleep(cyan(f"{enemy_weapon.name} added to sack."), 1)
        else:
            if self.add_weapon(enemy_weapon):
                print_and_sleep(cyan(f"{enemy_weapon.name} added to sack."), 1)


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
    @attach_perk(AP_TENCH_STUDIES, INTRO_TO_TENCH, value_description="xp gained")
    def _calculate_xp_from_enemy(enemy: Combatant) -> int:
        return int(enemy.max_hp / 2.8)

    def gain_xp_from_enemy(self, enemy: Combatant) -> bool:
        amount = self._calculate_xp_from_enemy(enemy)
        return self._gain_xp(amount)

    def gain_xp_other(self, amount: int) -> bool:
        return self._gain_xp(amount + 1) if perk_is_active(AP_TENCH_STUDIES) else self._gain_xp(amount)

    def _gain_xp(self, amount: int) -> bool:
        self.xp += amount
        print_and_sleep(green(f"You gained {amount} XP!"), 1)

        leveled_up = False

        # handles cases where a big XP chunk might give multiple levels
        while self.xp >= self.xp_needed:
            self.level_up()
            leveled_up = True

        return leveled_up

    @property
    def has_tench_genes(self) -> bool:
        has_tench_genes = any(p.name for p in load_perks() if p.active and p.name == TENCH_GENES)
        return has_tench_genes

    def level_up(self):
        # ---- core level-up effects live here ----
        self.xp -= self.xp_needed
        self.lvl += 1
        cash_reward = 80 + (self.lvl * 10)
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

        # check for illness death level match
        if self.lvl == self.illness_death_lvl:
            if self.has_tench_genes and random.random() < 0.10:
                self.illness_death_lvl += 1
                print_and_sleep(purple("You survived death with Tench Genes!"), 1)
                print_and_sleep(f"New Death Level: {red(f'{str(self.illness_death_lvl)}')}", 1)
            else:
                self.hp = 0
                self.lives -= 1
                event_logger.log_event(PlayerDeathEvent(self.lives))
                self.illness = None
                self.illness_death_lvl = None

    def apply_death_penalties(self):
        self.coins = int(self.coins * 0.25) if perk_is_active(WALLET_CHAIN) else 0  # TODO use the framework for this
        self.items = item_defaults()
        self.weapon_dict = weapon_defaults()
        self.current_weapon = self.weapon_dict[BARE_HANDS]
        self.hp = self.max_hp
        self.xp = 0
        self.blind = False
        self.blind_turns = 0
        self.illness = None
        self.illness_death_lvl = None


    def handle_broken_weapon(self):
        event_logger.log_event(WeaponBrokeEvent())
        del self.weapon_dict[self.current_weapon.name]
        self.current_weapon = self.weapon_dict[BARE_HANDS]

    def take_damage(self, damage: int, other: Combatant) -> int:
        if damage >= self.hp:
            if perk_is_active(SOLOMON_TRAIN) and random.random() < 0.10:
                play_sound(RIFLE)
                print_and_sleep(purple("You were saved by Solomon Train!"), 1)
                return other.take_damage(other.hp, other)
            elif self.cheat_death_enabled:
                print_and_sleep(purple("You survived the attack with Death Can Wait!"), 1)
                self.cheat_death_enabled = False
                return super().take_damage(self.hp - 1, other)
        return super().take_damage(damage, other)

    def _subscribe_listeners(self):
        @subscribe_function(HitEvent)
        def handle_hit(event: HitEvent):
            if event.weapon_type == MELEE and perk_is_active(VAMPIRIC_SPERM):
                if self.hp < self.max_hp:
                    gain = min(3, self.max_hp - self.hp)
                    self.gain_hp(gain)
                    print_and_sleep(purple(f"Restored {gain} HP with Vampiric Sperm!"), 1)

            # for loading from save file
    def __setstate__(self, state):
        self.__dict__.update(state)
        self._subscribe_listeners()
