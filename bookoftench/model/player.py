from __future__ import annotations

import random
from dataclasses import asdict, dataclass, field

from bookoftench import event_logger
from bookoftench.audio import play_sound
from bookoftench.data import audio as a
from bookoftench.data import items as i
from bookoftench.data import perks as p
from bookoftench.data.areas import CAVE
from bookoftench.data.enemies import EMPATH
from bookoftench.data.environment import DAY, DRYING, FULL, NIGHT, WETTING
from bookoftench.data.weapons import (
    BARE_HANDS,
    BLADED,
    CLAWS,
    KNIFE,
    LASER_BEAMS,
    MELEE,
    RANGED,
    VOODOO_STAFF,
)
from bookoftench.event_logger import subscribe_function
from bookoftench.model.bait import Bait
from bookoftench.model.illness import Illness, load_illness
from bookoftench.ui import cyan, dim, green, purple, red, yellow
from bookoftench.util import print_and_sleep
from .base import Buyable, Combatant
from .build import Build
from .enemy import Enemy
from .events import (
    BuyItemEvent,
    BuyPerkEvent,
    BuyWeaponEvent,
    GenericStealEvent,
    HitEvent,
    ItemSoldEvent,
    ItemUsedEvent,
    LevelUpEvent,
    PlayerDeathEvent,
    StealItemEvent,
    StealPerkEvent,
    StealWeaponEvent,
    SwapWeaponEvent,
    WeaponBrokeEvent,
)
from .fish import Fish
from .fishing_item import FishingItem
from .investment import Investment
from .item import Item, load_items
from .perk import Perk, activate_perk_print, attach_perk, attach_perks, perk_is_active
from .trait import Trait
from .weapon import Weapon, load_weapons
from ..data.audio import GOLF_CLAP, GREAT_JOB, XP
from ..data.illnesses import Illnesses

# ================================================================================================

@dataclass
class PlayerWeapon(Weapon):
    def calculate_base_damage(self) -> int:
        base_damage = self.calculate_base_damage_no_perk()

        @attach_perk(
            p.ROSETTI_THE_GYM_RAT,
            value_description="melee damage",
            condition=lambda: self.type == MELEE,
        )
        @attach_perk(
            p.AMBROSE_BLADE,
            value_description="blade damage",
            condition=lambda: self.subtype == BLADED,
        )
        @attach_perks(
            p.KARATE_LESSONS,
            p.MARTIAL_ARTS_TRAINING,
            value_description="bare hands damage",
            condition=lambda: self.name == BARE_HANDS,
        )
        def apply_perks() -> int:
            return base_damage

        return int(apply_perks())

    def get_accuracy(self) -> float:
        @attach_perk(
            p.TENCH_EYES,
            value_description="projectile accuracy",
            condition=lambda: self.type == RANGED,
        )
        def apply_perks() -> float:
            return self.accuracy

        return apply_perks()

    @classmethod
    def from_weapon(cls, weapon: Weapon) -> PlayerWeapon:
        return cls.from_dict(asdict(weapon))

    def __repr__(self) -> str:
        return dim(" | ").join([
            cyan(f"{self.name:<24}"),
            f"Dmg: {red(f'{self.damage:<3}')}",
            f"Acc: {yellow(f'{self.accuracy:<4}')}",
            f"Var: {red(self.var)}",
            f"Crit: {yellow(f'{self.crit:<4}')}",
            f"Uses: {self.format_uses()}",
        ])


def item_defaults() -> dict[str, Item]:
    return {
        item.name: item
        for item in load_items([i.TENCH_FILET])
    }


def weapon_defaults() -> dict[str, PlayerWeapon]:
    return {
        weapon.name: PlayerWeapon.from_weapon(weapon)
        for weapon in load_weapons([BARE_HANDS, KNIFE])
    }


def build_weapon_defaults(build: Build | None) -> dict[str, PlayerWeapon]:
    build.weapons = [
        weapon
        for weapon in build.weapons
        if hasattr(weapon, "name")
    ]

    filtered = [
        weapon.name
        for weapon in build.weapons
        if weapon.name in [BARE_HANDS, CLAWS, LASER_BEAMS, VOODOO_STAFF]
    ]

    if filtered:
        build.weapons.extend(load_weapons(filtered))
    else:
        build.weapons = load_weapons([BARE_HANDS])

    return {
        weapon.name: PlayerWeapon.from_weapon(weapon)
        for weapon in build.weapons
    }

# ================================================================================================

@dataclass
class Player(Combatant):
    name: str = ""
    build: Build | None = None
    lives: int = 3
    lvl: int = 1
    coins: int = 0
    max_hp: int = 100
    hp: int = 100
    xp: int = 0
    strength: float = 1
    acc: float = 1
    luck: float = 1
    trait: Trait | None = None

    # --- fishing ---
    fishing_xp: int = 0
    fishing_xp_needed: int = 10
    fishing_lvl: int = 1
    rod_lvl: int = 1
    max_active_fishing_items: int = 3
    caught_fish: list[Fish] = field(default_factory=list)
    tackle_box: dict[str, Bait] = field(default_factory=dict)
    fishing_item_box: dict[str, FishingItem] = field(default_factory=dict)
    current_bait: Bait | None = None
    active_fishing_items: list[FishingItem] = field(default_factory=list)

    illness: Illness | None = None
    illness_death_lvl: int | None = None

    can_flee: bool = False
    double_damage_active: bool = False
    crit_active: bool = False
    cheat_death_enabled: bool = False

    casino_won: int = 0
    casino_lost: int = 0
    games_played: int = 0

    sum_of_bribes: int = 0

    _max_plays: int = 10
    _max_items: int = 5
    _max_weapons: int = 4

    _blind: bool = False

    items: dict[str, Item] = field(default_factory=item_defaults)
    weapon_dict: dict[str, PlayerWeapon] = field(default_factory=weapon_defaults)
    current_weapon: Weapon | None = None

    investments: list[Investment] = field(default_factory=list)
    expired_investment_opportunities: list[str] = field(default_factory=list)

# ================================================================================================

    def __post_init__(self) -> None:
        self.current_weapon = self.weapon_dict[BARE_HANDS]
        self._subscribe_listeners()

# ================================================================================================

    @property
    @attach_perk(p.GRAMBLIN_MAN, silent=True)
    @attach_perk(p.GRAMBLING_ADDICT, p.WrapperIndices.GramblingAddict.PLAYS, silent=True)
    def max_plays(self) -> int:
        return self._max_plays

    @property
    @attach_perks(p.NOMADS_LAND, p.VAGABONDAGE, silent=True)
    def max_items(self) -> int:
        return self._max_items

    @property
    @attach_perks(p.NOMADS_LAND, p.VAGABONDAGE, silent=True)
    def max_weapons(self) -> int:
        return self._max_weapons

# ================================================================================================

    @property
    def xp_needed(self) -> int:
        return 100 + (self.lvl - 1) * 10

    @property
    def remaining_plays(self) -> int:
        return self.max_plays - self.games_played

# ================================================================================================

    @property
    def blind(self) -> bool:
        return self._blind

    @blind.setter
    def blind(self, blind: bool) -> None:
        if blind and perk_is_active(p.BEER_GOGGLES):
            print_and_sleep(purple(f"{p.BEER_GOGGLES} prevented blindness."), 1)
        else:
            self._blind = blind

    def is_sick(self) -> bool:
        return self.illness is not None

# ================================================================================================

    def get_items(self) -> list[Item]:
        return list(self.items.values())

    def display_item_count(self) -> None:
        item_count = dim(f"({len(self.items)}/{self.max_items})")
        print_and_sleep(f"Items {item_count}")

    def add_item(self, item: Item) -> bool:
        if item.name in self.items:
            print_and_sleep(yellow(f"You already have {item.name}!"), 1)
            return False

        if len(self.items) >= self.max_items:
            print_and_sleep(yellow("Your item sack is full."), 1)
            return False

        self.items[item.name] = item
        return True

# ================================================================================================

    @staticmethod
    @attach_perks(p.HEALTH_NUT, p.DOCTOR_FISH, value_description="hp gained")
    def _apply_hp_bonus(base: int) -> int:
        return base

# ================================================================================================

    def equip_bait(self, bait: Bait) -> None:
        self.current_bait = bait

    @property
    def has_usable_bait(self) -> bool:
        return any(bait.casts > 0 for bait in self.tackle_box.values())

    def use_fishing_item(self, fish: Fish, item: FishingItem) -> None:
        if item.spit_hook_prevention:
            fish.barb_hook_active = True

        if item.speed_reduction:
            fish.speed_multiplier *= 1 - item.speed_reduction

        if item.stamina_reduction:
            fish.stamina_multiplier *= 1 + item.stamina_reduction

        if item.rage_reduction:
            fish.rage_multiplier *= 1 - item.rage_reduction

        if item.strength_reduction:
            fish.strength_multiplier *= 1 - item.strength_reduction

        item.count -= 1
        self.active_fishing_items.append(item)

        if item.count <= 0:
            self.fishing_item_box.pop(item.name, None)

# ================================================================================================

    def use_item(self, name: str, enemy: Enemy | None, game_state) -> None:
        item = self.items[name]
        sfx = item.sound
        time = game_state.time_of_day
        moon = game_state.moon

        # --- retrieve gain amount and/or activate special item ---
        if item.type in [i.NORMAL, i.BOSS] and item.hp > 0:  # normal hp gain
            play_sound(sfx)
            gain = int(min(self.max_hp - self.hp, self._apply_hp_bonus(item.hp)))
        else:
            if item.type == i.BOSS:
                print_and_sleep(yellow("Sell this at the shop, bozo."), 1.5)
                return

            gain = self.handle_special_item(item, enemy, time, moon, game_state)

        # --- Gain hp and activate enemy's empath trait if applicable ---
        if gain:
            self.gain_hp(gain)

            if enemy and enemy.trait and enemy.trait.name == EMPATH:
                heal = min(gain, enemy.max_hp - enemy.hp)

                if heal > 0:
                    enemy.hp += heal
                    print_and_sleep(green(f"The empathic {enemy.name} gained {heal} HP."), 1.5)

        # --- Remove from actual inventory ---
        del self.items[item.name]
        event_logger.log_event(
            ItemUsedEvent(
                item.name,
                item.type,
                len(self.items),
                self.hp,
                self.max_hp,
                gain,
            )
        )

# ================================================================================================

    def handle_special_item(
            self,
            item: Item,
            enemy: Enemy | None,
            time: str,
            moon: str,
            game_state,
    ) -> int | None:
        if item.type == i.FLEE:  # used to escape from battle
            play_sound(a.WHIFF)
            self.can_flee = True
            return None

        if item.type == i.STAT:  # used to mutate stats
            self.handle_stat_item(item)
            return None

        if item.type == i.DMG:  # used to alter your damage output
            play_sound(a.DISCOVERABLE)
            self.double_damage_active = True
            return None

        if item.type == i.CRIT:  # used to alter your critical hit odds
            play_sound(a.DISCOVERABLE)
            self.crit_active = True
            return None

        if item.type == i.HEALTH:  # used to heal in an abnormal way
            return self.handle_health_item(item, time, game_state)

        if item.type == i.ENEMY:  # used to do damage to enemy or mutate their stats
            self.handle_enemy_item(enemy, item, time, game_state, moon)
            return None

        return None

# ================================================================================================

    def handle_stat_item(self, item: Item) -> None:
        if item.name == i.ACCURACY_SEARUM:
            old = round(self.acc, 2)
            self.acc = round(self.acc + 0.03, 2)
            play_sound(a.DRINK)
            print_and_sleep(green(f"Accuracy: {old} -> {self.acc}"), 1)

        elif item.name == i.HTH:
            old = round(self.strength, 2)
            self.strength = round(self.strength + 0.03, 2)
            play_sound(a.DRINK)
            print_and_sleep(green(f"Strength: {old} -> {self.strength}"), 1)

# ================================================================================================

    def handle_health_item(self, item: Item, time: str, game_state) -> int | None:
        if item.name == i.nPnG:
            original_max = self.max_hp
            amount = random.randint(1, 5)
            self.max_hp += amount
            play_sound(a.POSITIVE)
            print_and_sleep(green(f"Max HP: {original_max} -> {self.max_hp}"), 1)

            original_hp = self.hp
            self.hp -= min(amount, original_hp)
            print_and_sleep(red(f"You lost {original_hp - self.hp} HP."), 1)
            return None

        if item.name == i.PHOTOSYNTHOPHYL:
            if time == DAY and game_state.current_area.name != CAVE:
                amount = self.max_hp - self.hp
                self.hp = self.max_hp
                play_sound(a.POSITIVE)
                print_and_sleep(green(f"You used Photosynthophyl to restore {amount} HP!"), 1)
                return amount

        return None

# ================================================================================================

    def handle_enemy_item(
            self,
            enemy: Enemy,
            item: Item,
            time: str,
            game_state,
            moon: str,
    ) -> None:
        if item.name == i.BOOMERANG:
            damage = random.randint(5, 25)
            half = damage // 2
            self.hp -= min(self.hp, half)
            enemy.hp -= min(enemy.hp, damage)
            play_sound(a.BOOMERANG_SFX)
            print_and_sleep(purple("..."), 2)
            play_sound(a.PUNCH)
            print_and_sleep(purple(f"Boomerang did {damage} damage and you lost {half} HP!"), 1)

        elif item.name == i.FLACCID_ACID:
            original = round(enemy.strength, 2)
            decrement = round(enemy.strength * 0.25, 2)
            enemy.strength = round(original - decrement, 2)
            play_sound(a.SPRAY)
            print_and_sleep(
                purple(
                    f"You doused {enemy.name} with Flaccid Acid! Strength: "
                    f"{original} -> {enemy.strength}"
                ),
                1,
            )

        elif item.name == i.MOON_RUNE and time == NIGHT and game_state.current_area.name != CAVE:
            damage = 10  # dry moon

            if moon == DRYING:
                damage = 25
            elif moon == WETTING:
                damage = 50
            elif moon == FULL:
                damage = 100

            enemy.hp -= min(enemy.hp, damage)
            play_sound(a.MAGIC)
            print_and_sleep(purple(f"Moon Rune did {damage} damage!"), 1)

# ================================================================================================

    def make_purchase(self, buyable: Buyable) -> bool:
        if self.coins < buyable.cost:
            print_and_sleep(yellow("Need more coin."), 1)
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

# ================================================================================================

    def steal_buyable(self, buyable: Buyable) -> bool:
        if isinstance(buyable, Item) and self.add_item(buyable):
            event_logger.log_event(StealItemEvent(buyable.name, buyable.cost))
        elif isinstance(buyable, Weapon) and self.add_weapon(buyable):
            event_logger.log_event(StealWeaponEvent(buyable.name, buyable.cost))
        elif isinstance(buyable, Perk) and self.add_perk(buyable):
            event_logger.log_event(StealPerkEvent(buyable.name, buyable.cost))
        else:
            return False

        event_logger.log_event(GenericStealEvent())
        return True

# ================================================================================================

    def sell_item(self, name: str) -> None:
        item = self.items[name]
        play_sound(a.COINS)
        self.coins += item.sell_value
        del self.items[name]
        event_logger.log_event(ItemSoldEvent(item.name, item.sell_value))

# ================================================================================================

    def gain_hp(self, amount: int) -> None:
        self.hp = min(self.max_hp, self.hp + amount)

    def lose_hp(self, amount: int) -> None:
        self.hp = max(0, self.hp - amount)

# ================================================================================================

    def display_weapon_count(self) -> None:
        weapon_count = dim(f"({len(self.weapon_dict)}/{self.max_weapons})")
        print_and_sleep(f"Weapons {weapon_count}")

    def display_equip_header(self) -> None:
        self.display_weapon_count()
        print_and_sleep(
            f"{cyan(self.current_weapon.name)} {dim('(Equipped)')}",
            newline_prefix=False,
        )

    def get_weapons(self) -> list[Weapon]:
        return list(self.weapon_dict.values())

# ================================================================================================

    def add_weapon(self, weapon: Weapon) -> bool:
        if weapon.base_name in self.weapon_dict:
            print_and_sleep(yellow(dim("You already have this weapon.")), 1)
            return False

        if len(self.weapon_dict) >= self.max_weapons:
            print_and_sleep(yellow("Your weapon sack is full."), 1)
            return False

        self.weapon_dict[weapon.base_name] = PlayerWeapon.from_weapon(weapon)
        return True

    def sell_weapon(self, name: str) -> None:
        sellable_weapon = self.weapon_dict[name].to_sellable_weapon()
        self.coins += sellable_weapon.sell_value
        del self.weapon_dict[name]

        if name == self.current_weapon.base_name:
            selection = next((weapon for weapon in self.weapon_dict.values()))
            self.current_weapon = PlayerWeapon.from_weapon(selection)

        play_sound(a.COINS)
        event_logger.log_event(ItemSoldEvent(sellable_weapon.name, sellable_weapon.sell_value))

    def equip_weapon(self, name: str, base_name: str) -> None:
        if base_name != self.current_weapon.base_name:
            event_logger.log_event(SwapWeaponEvent())
            self.current_weapon = self.weapon_dict[base_name]
            play_sound(a.EQUIP_WEAPON)
            print_and_sleep(cyan(f"{name} equipped."), 1)

    def swap_found_item(self, old_name: str, found_item: Item, game_state) -> None:
        if self.hp < self.max_hp:
            self.use_item(old_name, None, game_state)
            print_and_sleep(cyan(f"{found_item.name} added to sack."), 1)
        else:
            del self.items[old_name]
            print_and_sleep(cyan(f"{old_name} discarded. {found_item.name} added to sack."), 1)

        self.items[found_item.name] = found_item

    def swap_found_weapon(self, old_name: str, found_weapon: Weapon) -> None:
        del self.weapon_dict[old_name]
        self.weapon_dict[found_weapon.base_name] = PlayerWeapon.from_weapon(found_weapon)
        self.current_weapon = self.weapon_dict[found_weapon.base_name]
        print_and_sleep(cyan(f"{old_name} discarded. {found_weapon.name} equipped."), 1)

    def obtain_enemy_weapon(self, enemy_weapon: Weapon) -> None:
        match = next(
            (
                weapon
                for weapon in self.weapon_dict.values()
                if weapon.name == enemy_weapon.base_name
            ),
            None,
        )

        if match:
            if match.uses < enemy_weapon.uses:
                self.weapon_dict[enemy_weapon.base_name] = PlayerWeapon.from_weapon(enemy_weapon)
                self.current_weapon = self.weapon_dict[enemy_weapon.base_name]
                print_and_sleep(cyan(f"{enemy_weapon.name} added to sack."), 1)
        else:
            if self.add_weapon(enemy_weapon):
                print_and_sleep(cyan(f"{enemy_weapon.name} added to sack."), 1)

# ================================================================================================

    @attach_perk(p.LUCKY_TENCHS_FIN, value_description="crit chance")
    def get_crit_chance(self) -> float:
        return super().get_crit_chance()

    @staticmethod
    def add_perk(perk: Perk) -> bool:
        if perk_is_active(perk.name):
            print_and_sleep(yellow("You already have this perk."), 1)
            return False

        activate_perk_print(perk.name)
        return True

    def gain_coins(self, amount: int) -> None:
        play_sound(a.COINS)
        self.coins += amount
        print_and_sleep(green(f"You gained {amount} of coin!"), 1)

    def gain_strength(self, amount: float) -> None:
        amount = round(amount, 2)
        self.strength += amount
        print_and_sleep(cyan(f"Your strength increased by {amount}!"), 1)

    def gain_accuracy(self, amount: float) -> None:
        amount = round(amount, 2)
        self.acc += amount
        print_and_sleep(cyan(f"Your accuracy increased by {amount}!"), 1)

    def gain_or_lose_luck(self, amount: float) -> None:
        old_luck = self.luck

        new_luck = round(old_luck + amount, 2)
        new_luck = max(0.0, min(new_luck, 7.0))

        actual_change = round(new_luck - old_luck, 2)

        if actual_change < 0:
            print_and_sleep(yellow(f"Your luck decreased by {abs(actual_change)}."), 1)
        elif actual_change > 0:
            print_and_sleep(green(f"Your luck increased by {actual_change}!"), 1)

        self.luck = new_luck

    def acquire_illness(self, illness_name: str) -> None:
        illness_data = next(
            illness
            for illness in Illnesses
            if illness["name"] == illness_name
        )
        self.illness = load_illness(illness_data)
        self.illness_death_lvl = self.lvl + self.illness.levels_until_death

# ================================================================================================

    def gain_fishing_xp(self, xp: int) -> None:
        self.fishing_xp += xp
        fishing_xp = self.fishing_xp
        original_fishing_lvl = self.fishing_lvl

        play_sound(XP)
        print_and_sleep(cyan(f"You gained {xp} XP!"), 1)

        # todo - add conditional fishing xp display based on max lvl
        if fishing_xp >= 1000:
            fishing_lvl = 10
            xp_needed = self.fishing_xp
        elif fishing_xp >= 750:
            fishing_lvl = 9
            xp_needed = 1000
        elif fishing_xp >= 550:
            fishing_lvl = 8
            xp_needed = 750
        elif fishing_xp >= 360:
            xp_needed = 550
            fishing_lvl = 7
        elif fishing_xp >= 250:
            xp_needed = 360
            fishing_lvl = 6
        elif fishing_xp >= 160:
            xp_needed = 250
            fishing_lvl = 5
        elif fishing_xp >= 90:
            xp_needed = 160
            fishing_lvl = 4
        elif fishing_xp >= 40:
            xp_needed = 90
            fishing_lvl = 3
        elif fishing_xp >= 10:
            xp_needed = 40
            fishing_lvl = 2
        else:
            xp_needed = 10
            fishing_lvl = 1

        self.fishing_lvl = fishing_lvl
        self.fishing_xp_needed = xp_needed

        if original_fishing_lvl != fishing_lvl:
            play_sound(GOLF_CLAP)
            play_sound(GREAT_JOB)
            print_and_sleep(cyan(f"You have reached fishing level {self.fishing_lvl}!"), 1)

# ================================================================================================

    @staticmethod
    @attach_perk(p.INTRO_TO_TENCH, value_description="xp gained")
    @attach_perk(
        p.AP_TENCH_STUDIES,
        p.WrapperIndices.ApTenchStudies.BATTLE_XP,
        value_description="xp gained",
    )
    def _calculate_xp_from_enemy(enemy: Combatant) -> int:
        return round((enemy.max_hp / 2.75) * ((enemy.strength + enemy.acc) / 2))

    def gain_xp_from_enemy(self, enemy: Combatant) -> None:
        amount = self._calculate_xp_from_enemy(enemy)
        self._gain_xp(amount)

    @attach_perk(
        p.AP_TENCH_STUDIES,
        p.WrapperIndices.ApTenchStudies.OTHER_XP,
        value_description="xp gained",
    )
    def _calculate_xp_other(self, amount: int) -> int:
        return amount

    def gain_xp_other(self, amount: int) -> None:
        amount = self._calculate_xp_other(amount)
        self._gain_xp(amount)

    def _gain_xp(self, amount: int) -> None:
        play_sound(a.XP)
        self.xp += amount
        print_and_sleep(cyan(f"You gained {amount} XP!"), 1)

        # Handles cases where a big XP chunk might give multiple levels.
        while self.xp >= self.xp_needed:
            self.level_up()

# ================================================================================================

    def level_up(self) -> None:
        # ---- core level-up effects ----
        self.xp -= self.xp_needed
        self.lvl += 1
        cash_reward = 100
        self.coins += cash_reward
        self.games_played = 0

        if perk_is_active(p.AMBERJACKED):
            if self.strength < 1.25:
                self.gain_strength(self.strength * 0.03)

        if perk_is_active(p.CASTING_RANGE):
            if self.acc < 1.15:
                self.gain_accuracy(self.acc * 0.015)

        old_max = self.max_hp

        if self.max_hp < 150:
            self.max_hp += 5

        self.hp = self.max_hp

        event_logger.log_event(
            LevelUpEvent(self.lvl, old_max, self.max_hp, cash_reward)
        )

        # --- check for illness death level match ---
        if self.lvl == self.illness_death_lvl:
            if random.random() < self.get_illness_survival_probability():
                self.illness_death_lvl += 1
                print_and_sleep(purple("You survived death with Tench Genes!"), 1)
                print_and_sleep(f"New Death Level: {red(f'{self.illness_death_lvl}')}", 1)
            else:
                self.hp = 0
                self.lives -= 1
                event_logger.log_event(PlayerDeathEvent(self.lives))
                self.illness = None
                self.illness_death_lvl = None

# ================================================================================================

    def apply_death_penalties(self) -> None:
        self.coins = (
            round(self.coins * 0.25)
            if perk_is_active(p.WALLET_CHAIN)
            else 0
        )
        self.items = item_defaults()
        self.weapon_dict = build_weapon_defaults(self.build)

        if self.weapon_dict:
            current_weapon = next(weapon.name for weapon in self.weapon_dict.values())
        else:
            current_weapon = BARE_HANDS

        self.current_weapon = self.weapon_dict[current_weapon]
        self.hp = self.max_hp
        self.xp = 0
        self.blind = False
        self.blind_turns = 0
        self.illness = None
        self.illness_death_lvl = None
        self._max_plays = 10

# ================================================================================================

    @attach_perk(
        p.TENCH_GENES,
        p.WrapperIndices.TenchGenes.SURVIVAL,
        value_description="illness survival chance",
    )
    def get_illness_survival_probability(self) -> float:
        return 0.0

# ================================================================================================

    def handle_broken_weapon(self) -> None:
        event_logger.log_event(WeaponBrokeEvent())
        del self.weapon_dict[self.current_weapon.base_name]

        if self.weapon_dict:
            current = next(weapon for weapon in self.weapon_dict)
            self.current_weapon = self.weapon_dict[current]
        else:
            hands = load_weapons([BARE_HANDS])

            for weapon in hands:
                self.weapon_dict.update({weapon.name: PlayerWeapon.from_weapon(weapon)})
                self.current_weapon = self.weapon_dict[weapon.name]

    def take_damage(self, damage: int, other: Combatant) -> int:
        if damage >= self.hp:
            if perk_is_active(p.SOLOMON_TRAIN) and random.random() < 0.15:
                play_sound(a.RIFLE)
                print_and_sleep(purple("You were saved by Solomon Train!"), 1)
                return other.take_damage(other.hp, other)

            if self.cheat_death_enabled:
                print_and_sleep(purple("You survived the attack with Death Can Wait!"), 1)
                self.cheat_death_enabled = False
                return super().take_damage(self.hp - 1, other)

        return super().take_damage(damage, other)

# ================================================================================================

    def _subscribe_listeners(self) -> None:
        @subscribe_function(HitEvent)
        def handle_hit(event: HitEvent) -> None:
            if event.weapon_type == MELEE and perk_is_active(p.VAMPIRIC_SPERM):
                if self.hp < self.max_hp:
                    gain = min(3, self.max_hp - self.hp)
                    self.gain_hp(gain)
                    print_and_sleep(purple(f"Restored {gain} HP with Vampiric Sperm!"), 1)

        @subscribe_function(LevelUpEvent)
        def handle_investments(_: LevelUpEvent) -> None:
            investments = getattr(self, "investments", None)

            if not investments:
                return

            for investment in investments:
                if not investment.active:
                    continue

                if investment.maturity_lvl == self.lvl:
                    if random.random() < investment.success_rate:
                        payout = round(investment.value * investment.multiplier)
                        investment.value = payout
                        print_and_sleep(green(investment.success_text), 1.5)
                        self.gain_coins(payout)
                    else:
                        print_and_sleep(yellow(investment.failure_text), 1.5)
                        print_and_sleep(
                            yellow(f"Your investment of {investment.value} ran dry."),
                            1.5,
                        )
                        investment.value = 0

                    investment.active = False

    # For loading from save file.
    def __setstate__(self, state: dict) -> None:
        self.__dict__.update(state)
        self._subscribe_listeners()
