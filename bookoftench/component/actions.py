import random
from functools import partial
from typing import List

from bookoftench import event_logger
from bookoftench.audio import play_music, play_sound, stop_music
from bookoftench.component.base import TextDisplayingComponent, functional_component, Component, \
    ColoredNameSelectionBinding, BinarySelectionComponent, \
    NoOpComponent, LinearComponent, RandomChoiceComponent, ProbabilityBinding, GatekeepingComponent, ReprBinding
from bookoftench.data.audio import BATTLE_THEME, DEVIL_THUNDER, PISTOL, MENSCH_THEME, POSITIVE, DISCOVERABLE, \
    DISCOVERABLE_2, HOHKKEN_THEME
from bookoftench.data.components import SEARCH, USE_ITEM, EQUIP_WEAPON, ACHIEVEMENTS, PERKS, STATS, TRAVEL, \
    AREA_BOSS_FIGHT, FINAL_BOSS_FIGHT, DISCOVER_ITEM, SPAWN_ENEMY, DISCOVER_WEAPON, DISCOVER_DISCOVERABLE, \
    DISCOVER_PERK, \
    OVERVIEW, INFO, BUILD, ATTRIBUTES, FIGHT_BOSS_OTHER, KILLS, DISCOVERIES, ENCOUNTERS, ENCOUNTER_SUB_BOSS, INVESTMENTS
from bookoftench.data.enemies import CAPTAIN_HOLE, FINAL_BOSS, ACHILLES, COWARD, CONTAGIOUS, CHEATER, HOHKKEN, \
    SPECIAL_BOSS
from bookoftench.data.items import TENCH_FILET, Items, NORMAL, BOSS
from bookoftench.data.perks import DEATH_CAN_WAIT, Perks, NEPTUNE
from bookoftench.event_logger import subscribe_function
from bookoftench.model.discoverable import load_discoverables, search_discoverable_rarity, rarity_color
from bookoftench.model.enemy import ENEMY_SWITCH_WEAPON_CHANCE, Enemy, SpecialBoss
from bookoftench.model.events import KillEvent, FleeEvent, PlayerDeathEvent, BountyCollectedEvent, DiscoveryEvent, \
    FailedFleeEvent, DefeatHohkkenEvent
from bookoftench.model.game_state import GameState
from bookoftench.model.item import load_items, load_boss_item
from bookoftench.model.perk import load_perks, Perk, perk_is_active, activate_perk_print, activate_perk_no_print
from bookoftench.model.util import get_battle_status_view, display_player_achievements, \
    display_game_stats, calculate_flee, display_active_perks, display_battle_info, display_player_attributes, \
    display_liberated, display_discoveries, display_encountered, display_investments
from bookoftench.model.weapon import load_discoverable_weapons, load_weapons, make_elite_weapon, make_autographed_weapon
from bookoftench.ui import green, purple, yellow, dim, red, cyan, blue
from bookoftench.util import print_and_sleep, safe_input
from .base import LabeledSelectionComponent, SelectionBinding
from .encounters import PostKillEncounters
from .menu import OverviewMenu
from .registry import register_component, get_registered_component
from bookoftench.data.builds import RANDOM, DENNY, BRO
from bookoftench.data.discoverables import COMMON, UNCOMMON, LEGENDARY, RARE, MYTHIC
from bookoftench.data.illnesses import Illnesses, LATE_ONSET_SIDS
from bookoftench.data.weapons import BARE_HANDS, Weapons, TENCH_CANNON, SPECIAL, BLIND
from bookoftench.event_base import EventType
from bookoftench.model.build import Build, load_builds
from bookoftench.model.illness import load_illnesses
from bookoftench.model.player import PlayerWeapon

# ================================================================================================

@register_component(BUILD)
class BuildTypeSelection(BinarySelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         query="Create a custom build",
                         yes_component=BuildNameSelection,
                         no_component=BuildComponent)

# ================================================================================================

# --- custom build path ---

class BuildNameSelection(LinearComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, BuildLevelSelection)

    def execute_current(self) -> None:
        preset = load_builds([DENNY])
        player = self.game_state.player
        player.build = next(i for i in preset)
        build = player.build
        build.name = ""
        while True:
            build.name = safe_input("Build Name:")
            if build.name:
                break
        return self.game_state

# ================================================================================================

class BuildLevelSelection(LinearComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, BuildFishingLevelSelection)

    def execute_current(self) -> None:
        player = self.game_state.player
        while True:
            level = safe_input("Level:")
            if not level.isdigit():
                print_and_sleep(yellow("Level must be a numeric value."))
            elif int(level) < 1:
                player.lvl = 1
                return self.game_state
            else:
                player.lvl = int(level)
                return self.game_state

# ================================================================================================

class BuildFishingLevelSelection(LinearComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, BuildRodLevelSelection)

    def execute_current(self) -> None:
        player = self.game_state.player
        while True:
            fishing_level = safe_input("Fishing Level [0-10]:")
            if not fishing_level.isdigit():
                print_and_sleep(yellow("Fishing Level must be a numeric value between 0 and 10."))
            elif int(fishing_level) < 0:
                player.fishing_lvl = 0
                return self.game_state
            elif int(fishing_level) > 10:
                player.fishing_lvl = 10
                return self.game_state
            else:
                player.fishing_lvl = int(fishing_level)
                return self.game_state

# ================================================================================================

class BuildRodLevelSelection(LinearComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, BuildLivesSelection)

    def execute_current(self) -> None:
        player = self.game_state.player

        while True:
            rod_level = safe_input("Fishing Rod Level [0-10]:")
            if not rod_level.isdigit():
                print_and_sleep(yellow("Fishing Rod Level must be a numeric value between 0 and 10."))
            elif int(rod_level) < 0:
                player.rod_lvl = 0
                return self.game_state
            elif int(rod_level) > 10:
                player.rod_lvl = 10
                return self.game_state
            else:
                player.rod_lvl = int(rod_level)
                return self.game_state

# ================================================================================================

class BuildLivesSelection(LinearComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, BuildMaxHPSelection)

    def execute_current(self) -> None:
        player = self.game_state.player
        while True:
            lives = safe_input("Lives:")
            if not lives.isdigit():
                print_and_sleep(yellow("Lives must be a numeric value."))
            elif int(lives) < 1:
                player.lives = 1
                return self.game_state
            else:
                player.lives = int(lives)
                return self.game_state

# ================================================================================================

class BuildMaxHPSelection(LinearComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, BuildHPSelection)

    def execute_current(self) -> None:
        player = self.game_state.player
        while True:
            max_hp = safe_input("Max HP:")
            if not max_hp.isdigit():
                print_and_sleep(yellow("Max HP must be a numeric value."))
            elif int(max_hp) < 1:
                player.max_hp = 1
                return self.game_state
            else:
                player.max_hp = int(max_hp)
                return self.game_state

# ================================================================================================

class BuildHPSelection(LinearComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, BuildStrengthSelection)

    def execute_current(self) -> None:
        player = self.game_state.player
        while True:
            hp = safe_input(f"HP:")
            if not hp.isdigit():
                print_and_sleep(yellow("HP must be a numeric value."))
            elif int(hp) < 1:
                player.hp = 1
                return self.game_state
            elif int(hp) > player.max_hp:
                player.hp = player.max_hp
                return self.game_state
            else:
                player.hp = int(hp)
                return self.game_state

# ================================================================================================

class BuildStrengthSelection(LinearComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, BuildAccuracySelection)

    def execute_current(self) -> None:
        player = self.game_state.player

        while True:
            strength = safe_input("Strength [0-125]:")
            if not strength.isdigit():
                print_and_sleep(yellow("Strength must be a numeric value between 0 and 125."))
            elif int(strength) < 0:
                player.strength = 0
                return self.game_state
            elif int(strength) > 125:
                player.strength = 1.25
                return self.game_state
            else:
                player.strength = round(int(strength) * 0.01, 2)
                return self.game_state

# ================================================================================================

class BuildAccuracySelection(LinearComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, BuildCoinsSelection)

    def execute_current(self) -> None:
        player = self.game_state.player

        while True:
            accuracy = safe_input("Accuracy [0-110]:")
            if not accuracy.isdigit():
                print_and_sleep(yellow("Accuracy must be a numeric value between 0 and 110."))
            elif int(accuracy) < 0:
                player.acc = 0
                return self.game_state
            elif int(accuracy) > 110:
                player.acc = 1.10
                return self.game_state
            else:
                player.acc = round(int(accuracy) * 0.01, 2)
                return self.game_state

# ================================================================================================

class BuildCoinsSelection(LinearComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, BuildLuckSelection)

    def execute_current(self) -> None:
        player = self.game_state.player
        while True:
            coins = safe_input("Coins:")
            if not coins.isdigit():
                print_and_sleep(yellow("Coins must be a numeric value."))
            elif int(coins) < 0:
                player.coins = 0
                return self.game_state
            else:
                player.coins = int(coins)
                return self.game_state

# ================================================================================================

class BuildLuckSelection(LinearComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, BuildIllnessSelection)

    def execute_current(self) -> None:
        player = self.game_state.player
        while True:
            luck = safe_input("Luck [0-7]:")
            if not luck.isdigit():
                print_and_sleep(yellow("Luck must be a numeric value between 0 and 7."))
            elif float(luck) < 0:
                player.luck = 0
                return self.game_state
            elif float(luck) > 7:
                player.luck = 7
                return self.game_state
            else:
                player.luck = round(float(luck), 2)
                return self.game_state

# ================================================================================================

class BuildIllnessSelection(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        illnesses = [i for i in Illnesses if i['name'] != LATE_ONSET_SIDS]
        illnesses_sorted = sorted(illnesses, key=lambda i: i['name'])

        illness_bindings = [
            ReprBinding(
                str(i + 1),
                illness['name'],
                self._handle_selection_component(illness['name']),
                yellow(illness['name'])
            )
            for i, illness in enumerate(illnesses_sorted)
        ]

        continue_binding = SelectionBinding(
            "C",
            "Continue",
            functional_component()(lambda: BuildBlindSelection(game_state).run())
        )

        super().__init__(
            game_state,
            refresh_menu=True,
            bindings=[*illness_bindings, continue_binding]
        )

        self.selection_components = [
            LabeledSelectionComponent(game_state, illness_bindings),
            LabeledSelectionComponent(game_state, [continue_binding]),
        ]

    def display_options(self) -> None:
        for component in self.selection_components:
            component.display_options()

    @staticmethod
    def _handle_selection_component(illness_name: str) -> type[Component]:
        @functional_component(state_dependent=True)
        def selection_component(game_state: GameState):
            valid_illness_names = [
                illness['name']
                for illness in Illnesses
                if illness['name'] != LATE_ONSET_SIDS
            ]

            if illness_name not in valid_illness_names:
                print_and_sleep(yellow("Illness not found - Please try again."))
                return game_state

            illness = load_illnesses([illness_name])
            player = game_state.player

            player.illness = next(i for i in illness)
            player.illness_death_lvl = player.lvl + player.illness.levels_until_death

            return BuildBlindSelection(game_state).run()

        return selection_component

# ================================================================================================

class BuildBlindSelection(BinarySelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         query="Are you blind?",
                         yes_component=BuildBlindEffectSelection,
                         no_component=BuildItemsSelection)

# ================================================================================================

class BuildBlindEffectSelection(LinearComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, BuildBlindTurnsSelection)

    def execute_current(self) -> None:
        player = self.game_state.player
        player.blind = True
        while True:
            effect = safe_input("Blindness [1-100]:")
            if not effect.isdigit():
                print_and_sleep(yellow("Effect must be a numeric value between 1 and 100."))
            elif int(effect) < 1:
                player.blind_effect = 1
                return self.game_state
            elif int(effect) > 100:
                player.blind_effect = 100
                return self.game_state
            else:
                player.blind_effect = int(effect) * 0.01
                return self.game_state

# ================================================================================================

class BuildBlindTurnsSelection(LinearComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, BuildItemsSelection)

    def execute_current(self) -> None:
        player = self.game_state.player
        player.blind = True
        while True:
            turns = safe_input("How many turns?")
            if not turns.isdigit():
                print_and_sleep(yellow("Turns must be a numeric value."))
            elif int(turns) < 1:
                player.blind_turns = 1
                return self.game_state
            else:
                player.blind_turns = int(turns)
                return self.game_state

# ================================================================================================

class BuildItemsSelection(LinearComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, BuildWeaponsSelection)

    def execute_current(self) -> None:
        player = self.game_state.player
        player.items.clear()
        items = random.sample([i for i in Items if i['type'] != BOSS], k=12)
        for i in items:
            if i['type'] == NORMAL:
                print_and_sleep(cyan(f"{i['name']:<24}") + (dim(' | ')) + "HP: +" + (green(i['hp'])))
            else:
                print_and_sleep(cyan(f"{i['name']:<24}") + (dim(' | ')) + (i['desc']))

        selections = []
        while True:
            item = safe_input(f"Add an item ({len(selections)}/4 selected) or c to continue:")
            if item == "c":
                if selections:
                    final_picks = load_items(selections)
                    player.items = dict((it.name, it) for it in final_picks)
                return self.game_state
            elif item in selections:
                print_and_sleep(yellow(f"You already have {item}."))
            elif item not in [i['name'] for i in items]:
                print_and_sleep(yellow("Item not found - Please try again (case-sensitive)."))
            else:
                selections.append(item)
                if len(selections) == 4:
                    final_picks = load_items(selections)
                    player.items = dict((it.name, it) for it in final_picks)
                    return self.game_state

# ================================================================================================

class BuildWeaponsSelection(LinearComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, BuildPerksSelection)

    def execute_current(self) -> None:
        player = self.game_state.player

        player.weapon_dict.clear()

        load = load_weapons([BARE_HANDS])
        weapon = next(i for i in load)
        player.weapon_dict[BARE_HANDS] = PlayerWeapon.from_weapon(weapon)
        player.current_weapon = player.weapon_dict[BARE_HANDS]

        weapons = random.sample([w['name'] for w in Weapons if w['uses'] >= 0], k=12)
        weapon_options = load_weapons(weapons)
        weapons_sorted = sorted(weapon_options, key=lambda w: w.damage)

        for w in weapons_sorted:
            print_and_sleep(w.get_complete_format(None, None))

        selections = []

        while True:
            weapon = safe_input(f"Add a weapon ({len(selections)}/3 selected) or c to continue:")

            if weapon == "c":
                if selections:
                    final_picks = load_weapons(selections)

                    for w in final_picks:
                        player.weapon_dict.update({w.name: PlayerWeapon.from_weapon(w)})

                    player.build.weapons.extend(final_picks)

                return self.game_state

            elif weapon in selections:
                print_and_sleep(yellow(f"You already have {weapon}."))

            elif weapon not in weapons:
                print_and_sleep(yellow("Weapon not found - Please try again (case-sensitive)."))

            else:
                selections.append(weapon)

                if len(selections) == 3:
                    final_picks = load_weapons(selections)

                    for w in final_picks:
                        player.weapon_dict.update({w.name: PlayerWeapon.from_weapon(w)})

                    player.build.weapons.extend(final_picks)

                    return self.game_state

# ================================================================================================

class BuildPerksSelection(LinearComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, NoOpComponent)

    def execute_current(self) -> None:
        perks = random.sample(Perks, k=12)
        perks_sorted = sorted(perks, key=lambda p: p['name'])
        for p in perks_sorted:
            print_and_sleep(purple(p['name']) + dim("\n") + p['description'])

        selections = []
        while True:
            perk = safe_input(f"Add a perk (a to add all) or c to continue:")
            if perk == "c":
                return self.game_state
            elif perk == "a":
                for p in perks:
                    if p not in selections:
                        activate_perk_print(p['name'])
                return self.game_state
            elif perk in selections: # if it's already been selected
                print_and_sleep(yellow(f"You already have {perk}."))
            elif perk not in [p['name'] for p in perks]: # if it's not a perk
                print_and_sleep(yellow("Perk not found - Please try again (case-sensitive)."))
            else:
                selections.append(perk)
                activate_perk_print(perk) # add to list for counting
                if len(selections) == len(perks):
                    return self.game_state

# ================================================================================================
# ================================================================================================

# --- standard build path ---
class BuildComponent(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        build_bindings = [ReprBinding(str(i + 1), build.name, self._make_selection_component(build), build) for
                         i, build in enumerate(game_state.build_inventory)]
        super().__init__(game_state, refresh_menu=True,
                         bindings=[*build_bindings])
        self.selection_components = [
            LabeledSelectionComponent(game_state, build_bindings),
        ]

    def display_options(self) -> None:
        print_and_sleep("What is your build?", 1.5)

        for component in self.selection_components:
            component.display_options()

# ================================================================================================

    # TODO - refactor
    @staticmethod
    def _make_selection_component(build: Build) -> type[Component]:
        @functional_component(state_dependent=True)
        def selection_component(game_state: GameState):
            player = game_state.player
            player.build = build

            print_and_sleep(f"You selected {cyan(build.name)}", 1.5)

            if build.name == RANDOM:
                player.lives = random.randint(1, 3)

                player.lvl = random.randint(1, 3)
                player.fishing_lvl = random.randint(1, 4)
                player.rod_lvl = random.randint(1, 4)

                player.max_hp = random.randint(80, 120)
                hp_deficit = random.randint(1, 40)
                player.hp = player.max_hp - hp_deficit if random.random() < 0.5 else player.max_hp

                player.strength = round(random.uniform(0.8, 1.2), 2)
                player.acc = round(random.uniform(0.9, 1.1), 2)

                player.coins = random.randint(0, 250)
                player.luck = random.randint(0, 5)

                player.weapon_dict.clear()
                bare_hands = next(iter(load_weapons([BARE_HANDS])))
                player.weapon_dict[BARE_HANDS] = PlayerWeapon.from_weapon(bare_hands)
                player.current_weapon = player.weapon_dict[BARE_HANDS]

                # --- illness ---
                if random.random() < 0.5:
                    illness_names = [
                        i['name']
                        for i in Illnesses
                        if i['name'] != LATE_ONSET_SIDS
                    ]

                    options = load_illnesses(illness_names)
                    player.illness = random.choice(options)
                    player.illness_death_lvl = player.lvl + player.illness.levels_until_death

                # --- items ---
                items_count = random.randint(0, 3)
                if items_count >= 1:
                    items = [
                        i['name']
                        for i in Items
                        if i['type'] != BOSS
                    ]

                    item_options = load_items(items)
                    selections = random.sample(item_options, k=items_count)
                    player.items = dict((it.name, it) for it in selections)

                # --- weapons ---
                weapons_count = random.randint(0, 3)
                if weapons_count >= 1:
                    weapons = [
                        i['name']
                        for i in Weapons
                        if i['name'] != BARE_HANDS
                    ]

                    weapon_options = load_weapons(weapons)
                    selections = random.sample(weapon_options, k=weapons_count)

                    for weapon in selections:
                        player.weapon_dict.update({
                            weapon.name: PlayerWeapon.from_weapon(weapon)
                        })

                # --- perks ---
                perks_count = random.randint(0, 4)
                if perks_count >= 1:
                    perks = [i['name'] for i in Perks]
                    selections = random.sample(perks, k=perks_count)

                    for perk in selections:
                        activate_perk_print(perk)

            else:
                player.lives = build.lives
                player.lvl = build.lvl
                player.max_hp = build.hp
                player.hp = build.hp
                player.strength = build.str
                player.acc = build.acc
                player.coins = build.coins
                player.luck = build.luck
                player.fishing_lvl = build.fishing_lvl
                player.rod_lvl = build.rod_lvl

                if build.illness:
                    player.illness = build.illness
                    player.illness_death_lvl = player.lvl + build.illness.levels_until_death

                player.items = dict((it.name, it) for it in build.items)
                player.weapon_dict.clear()

                for weapon in build.weapons:
                    player.weapon_dict[weapon.name] = PlayerWeapon.from_weapon(weapon)

                if player.weapon_dict:
                    player.current_weapon = next(iter(player.weapon_dict.values()))
                else:
                    bare_hands = next(iter(load_weapons([BARE_HANDS])))
                    player.weapon_dict[BARE_HANDS] = PlayerWeapon.from_weapon(bare_hands)
                    player.current_weapon = player.weapon_dict[BARE_HANDS]

                for p in build.perks:
                    if build.name == BRO:
                        activate_perk_no_print(p.name)
                    else:
                        activate_perk_print(p.name)

        return selection_component

# ================================================================================================

@register_component(SEARCH)
class Search(RandomChoiceComponent):
    def __init__(self, game_state: GameState):
        ep = game_state.current_area.search_probabilities
        super().__init__(game_state, bindings=[ProbabilityBinding(prob, get_registered_component(name))
                                               for name, prob in ep.items()])

# ================================================================================================

    # todo - refactor
    @staticmethod
    @register_component(DISCOVER_DISCOVERABLE)
    @functional_component(state_dependent=True)
    def _discover_discoverable(game_state: GameState):
        player = game_state.player

        rarity = search_discoverable_rarity(player)

        available = [
            d for d in load_discoverables()
            if game_state.current_area.name in d.areas
               and d.rarity == rarity
        ]

        if not available:
            available = [
                d for d in load_discoverables()
                if game_state.current_area.name in d.areas
            ]

        if not available:
            print_and_sleep(dim("You came up dry."), 1)
            return game_state

        find = random.choice(available)
        rarity = find.rarity
        color = rarity_color(rarity)

        if rarity == COMMON:
            time = 1
        elif rarity == UNCOMMON:
            time = 1.5
        else:
            time = 2

        # log event for stats
        if rarity == COMMON:
            play_sound(DISCOVERABLE)
            event_logger.log_event(DiscoveryEvent(EventType.DISCOVERY_COMMON))
        elif rarity == UNCOMMON:
            play_sound(DISCOVERABLE)
            event_logger.log_event(DiscoveryEvent(EventType.DISCOVERY_UNCOMMON))
        elif rarity == RARE:
            play_sound(DISCOVERABLE)
            event_logger.log_event(DiscoveryEvent(EventType.DISCOVERY_RARE))
        elif rarity == LEGENDARY:
            play_sound(DISCOVERABLE_2)
            event_logger.log_event(DiscoveryEvent(EventType.DISCOVERY_LEGENDARY))
        elif rarity == MYTHIC:
            play_sound(DISCOVERABLE_2)
            event_logger.log_event(DiscoveryEvent(EventType.DISCOVERY_MYTHIC))
        else:
            play_sound(DISCOVERABLE)
            print_and_sleep(yellow(f"Unknown discovery rarity: {rarity}"), 1)

        # add to discoveries and update count
        discovered = next(
            (d for d in game_state.discoveries if d.name == find.name),
            None
        )

        if discovered:
            discovered.count += 1
        else:
            find.count += 1
            game_state.discoveries.append(find)

        # take damage if find.hp < 0
        if find.hp < 0:
            original_hp = player.hp
            damage = abs(find.hp) + random.randint(0, 3)

            player.lose_hp(damage)

            print_and_sleep(
                f"You{f' {find.pre} ' if find.pre else ' '}{yellow(find.name)} "
                f"{color(f'({find.rarity})')} and lost {red(original_hp - player.hp)} hp.",
                time
            )

            if player.hp == 0:
                player.lives -= 1
                event_logger.log_event(PlayerDeathEvent(player.lives))

            return game_state

        # heal if discoverable.hp and player.hp < max_hp
        if player.hp < player.max_hp and find.hp > 0:
            original_hp = player.hp

            player.gain_hp(find.hp + random.randint(0, 3))

            print_and_sleep(
                f"You found{f' {find.pre} ' if find.pre else ' '}{cyan(find.name)} "
                f"{color(f'({find.rarity})')} and restored {green(player.hp - original_hp)} hp.",
                time
            )

            return game_state

        # gain coin if value greater than 0
        if find.value > 0:
            print_and_sleep(
                f"You found{f' {find.pre} ' if find.pre else ' '}{cyan(find.name)} "
                f"{color(f'({find.rarity})')} worth {green(find.value)} of coin.",
                time
            )

            player.gain_coins(find.value)
            return game_state

        # print found message if neutral
        print_and_sleep(
            f"You found{f' {find.pre} ' if find.pre else ' '}{cyan(find.name)} "
            f"{color(f'({find.rarity})')}!",
            time
        )

        return game_state

# ================================================================================================

    @staticmethod
    @register_component(DISCOVER_ITEM)
    @functional_component(state_dependent=True)
    def _discover_item(game_state: GameState):
        player = game_state.player

        available = [
            i for i in load_items()
            if i.name not in player.items
               and i.areas is not None
               and game_state.current_area.name in i.areas
        ]

        if not available:
            available = [
                i for i in load_items()
                if i.name not in player.items
            ]

        if not available:
            print_and_sleep(yellow("You found nothing new."), 1)
            return game_state

        item = random.choice(available)
        game_state.found_item = item

        play_sound(POSITIVE)
        print_and_sleep(cyan(f"You found {'an' if item.name[0].lower() in 'aeiou' else 'a'} {item.name}!"), 2)

        if player.add_item(item):
            print_and_sleep(cyan(f"{item.name} added to sack."), 1)
            return game_state

        return SwapFoundItemYN(game_state).run()

# ================================================================================================

    @staticmethod
    @register_component(DISCOVER_WEAPON)
    @functional_component(state_dependent=True)
    def _discover_weapon(game_state: GameState):
        player = game_state.player

        available = [
            w for w in load_discoverable_weapons()
            if game_state.current_area.name in w.areas
               and w.name not in player.weapon_dict
        ]

        if not available:
            available = [
                w for w in load_discoverable_weapons()
                if w.name not in player.weapon_dict
            ]

        if not available:
            print_and_sleep(yellow("You found nothing new."), 1)
            return game_state

        weapon = random.choice(available)

        if weapon.type not in [BLIND, SPECIAL]:
            if random.random() < 0.10:
                weapon = make_elite_weapon(weapon)
            if random.random() < 0.05:
                weapon = make_autographed_weapon(weapon)

        game_state.found_weapon = weapon

        play_sound(POSITIVE)
        print_and_sleep(
            cyan(f"You found {'an' if weapon.name[0].lower() in 'aeiou' else 'a'} {weapon.name}!"),
            2
        )

        if player.add_weapon(weapon):
            print_and_sleep(cyan(f"{weapon.name} added to sack."), 1)
            return game_state

        return SwapFoundWeaponYN(game_state).run()

# ================================================================================================

    @staticmethod
    @register_component(DISCOVER_PERK)
    @functional_component()
    def _discover_perk():
        filtered: List[Perk] = load_perks(lambda p: not p.active)
        if len(filtered) > 0:
            play_music(MENSCH_THEME)
            reward = random.choice(filtered)
            print_and_sleep(purple("You sense a noble presence..."), 3)
            print_and_sleep(purple("It's a mensch!"), 3)
            print_and_sleep(purple(f"He's gifted you the {reward.name} perk!\n{reward.description}"), 4)
            reward.activate_print()
        else:
            print_and_sleep(dim("You came up dry."), 1)

# ================================================================================================

@register_component(TRAVEL)
class Travel(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(
            game_state,
            bindings=[
                ColoredNameSelectionBinding(
                    key=str(i),
                    name=area.name,
                    color=blue,
                    component=self._make_travel_component(area.name)
                )
                for i, area in enumerate(
                    sorted(
                        [a for a in game_state.areas if a.name != game_state.current_area.name],
                        key=lambda a: a.name
                    ),
                    1
                )
            ],
            quittable=True
        )

    @staticmethod
    def _make_travel_component(area_name: str):
        @functional_component(state_dependent=True)
        def travel_component(game_state: GameState):
            game_state.update_current_area(area_name, game_state.season)

            if getattr(game_state, "pending_boss", False):
                game_state.pending_boss = False
                return FightBossOther(game_state).run()

            return game_state

        return travel_component

# ================================================================================================

@register_component(USE_ITEM)
class UseItem(GatekeepingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(
            game_state,
            decision_function=lambda: len(game_state.player.items) > 0,
            accept_component=ItemSelectionComponent,
            deny_component=self._no_items_component
        )

    @staticmethod
    @functional_component(state_dependent=True)
    def _no_items_component(game_state: GameState):
        print_and_sleep(yellow("Your inventory is dry."), 1)
        return game_state


class ItemSelectionComponent(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        self.length = 0
        enemy = game_state.current_area.current_enemy

        for i in game_state.player.items.keys():
            if len(i) > self.length:
                self.length = len(i) + 1

        super().__init__(
            game_state,
            bindings=[
                SelectionBinding(
                    key=str(i),
                    name=item.get_simple_format(self.length),
                    component=functional_component()(
                        lambda item=item: self._use_item_and_check(
                            item,
                            enemy if enemy else None,
                        )
                    )
                )
                for (i, item) in enumerate(game_state.player.get_items(), 1)
            ],
            top_level_prompt_callback=lambda gs: gs.player.display_item_count(),
            quittable=True
        )

    def _use_item_and_check(self, item, enemy: Enemy | None) -> GameState:
        self.game_state.player.use_item(
            item.name,
            enemy,
            self.game_state,
        )

        player = self.game_state.player
        current_enemy = self.game_state.current_area.current_enemy

        if not player.is_alive() or (current_enemy and not current_enemy.is_alive()):
            return BattleEnd(self.game_state).run()

        return self.game_state

# ================================================================================================

@register_component(EQUIP_WEAPON)
class EquipWeapon(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(
            game_state,
            bindings=[
                SelectionBinding(
                    key=str(i),
                    name=weapon.get_complete_format(None, None),
                    component=self._make_equip_component(weapon)
                )
                for i, weapon in enumerate(game_state.player.get_weapons(), 1)
            ],
            top_level_prompt_callback=lambda gs: gs.player.display_equip_header(),
            quittable=True
        )

    @staticmethod
    def _make_equip_component(weapon):
        @functional_component(state_dependent=True)
        def equip_component(game_state: GameState):
            game_state.player.equip_weapon(weapon.name, weapon.base_name)
            return game_state

        return equip_component

# ================================================================================================

class SwapFoundItemYN(BinarySelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         query="Swap for one of your current items",
                         yes_component=SwapFoundItemMenu,
                         no_component=NoOpComponent)


class SwapFoundItemMenu(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        found = game_state.found_item
        valid = list(game_state.player.items.values())

        length = 0
        for item_name in game_state.player.items.keys():
            if len(item_name) > length:
                length = len(item_name) + 1

        super().__init__(
            game_state,
            bindings=[
                SelectionBinding(
                    key=str(i),
                    name=item.get_simple_format(length),
                    component=self._make_swap_component(item.name, found)
                )
                for i, item in enumerate(valid, 1)
            ],
            top_level_prompt_callback=lambda gs: print_and_sleep(
                dim(gs.found_item.get_found_format()),
                0
            ),
            quittable=True
        )

    @staticmethod
    def _make_swap_component(item_name, found):
        @functional_component(state_dependent=True)
        def swap_component(game_state: GameState):
            game_state.player.swap_found_item(item_name, found, game_state)
            return game_state

        return swap_component


class SwapFoundWeaponYN(BinarySelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         query="Swap for one of your current weapons",
                         yes_component=SwapFoundWeaponMenu,
                         no_component=NoOpComponent)


class SwapFoundWeaponMenu(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        found = game_state.found_weapon
        valid = [
            w for w in game_state.player.get_weapons()
            if w.name != "Bare Hands"
        ]

        super().__init__(
            game_state,
            bindings=[
                SelectionBinding(
                    key=str(i),
                    name=weapon.get_complete_format(None, None),
                    component=self._make_swap_component(weapon.base_name, found)
                )
                for i, weapon in enumerate(valid, 1)
            ],
            top_level_prompt_callback=lambda gs: print_and_sleep(
                dim(gs.found_weapon.get_complete_format(None, None)),
                0
            ),
            quittable=True
        )

    @staticmethod
    def _make_swap_component(weapon_base_name, found):
        @functional_component(state_dependent=True)
        def swap_component(game_state: GameState):
            game_state.player.swap_found_weapon(weapon_base_name, found)
            return game_state

        return swap_component

# ================================================================================================

class Attack(Component):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)
        self.failed_flee = False

    def run(self) -> GameState:
        player, enemy = self.game_state.player, self.game_state.current_area.current_enemy

        if not self.failed_flee and player.is_alive() and enemy.is_alive():
            player.attack(enemy)

        if player.is_alive() and enemy.is_alive():
            enemy.attack(player)

        if player.is_alive() and enemy.is_alive():
            self.handle_trait_checks(player, enemy)

        if not player.is_alive() or not enemy.is_alive():
            return BattleEnd(self.game_state).run()

        return self.game_state

    def handle_trait_checks(self, player, enemy) -> None:
        if enemy.trait:
            trait_name = enemy.trait.name

            if trait_name == CHEATER and enemy.current_weapon.uses > 0 and random.random() < 0.15:
                enemy.attack(player)

                if not player.is_alive() or not enemy.is_alive():
                    return

            elif trait_name == CONTAGIOUS and random.random() < 0.15:
                EnemyInfect(self.game_state).run()

            elif trait_name == COWARD and random.random() < 0.15:
                print_and_sleep(yellow(f"{enemy.name} fled like a bozo baby coward!"), 1.5)
                player.can_flee = True
                return

            elif (
                    trait_name == ACHILLES
                    and enemy.current_weapon.base_name != TENCH_CANNON
                    and enemy.hp < 25
            ):
                enemy.current_weapon = enemy.enemy_switch_weapon(TENCH_CANNON)

        if random.random() < ENEMY_SWITCH_WEAPON_CHANCE and enemy.current_weapon.base_name != TENCH_CANNON:
            enemy.current_weapon = enemy.enemy_switch_weapon(None)

# ================================================================================================

class FailedFlee(Attack):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)
        self.failed_flee: bool = True

    def run(self) -> GameState:
        event_logger.log_event(FailedFleeEvent())
        return super().run()


class FleeSelectionBinding(SelectionBinding):
    def __init__(self, key: str, name: str, component, game_state: GameState):
        self.game_state = game_state
        super().__init__(key, name, component)

    def format(self) -> str:
        enemy = self.game_state.current_area.current_enemy
        calculation = int(round(calculate_flee() * enemy.flee, 2) * 100)
        calculation = max(0, min(100, calculation))

        return f"Flee ({calculation}%)"


class TryFlee(RandomChoiceComponent):
    def __init__(self, game_state: GameState):
        enemy = game_state.current_area.current_enemy
        self.flee_chance = int(round(calculate_flee() * enemy.flee, 2) * 100)
        self.flee_chance = max(0, min(100, self.flee_chance))

        super().__init__(game_state, bindings=[
            ProbabilityBinding(self.flee_chance, self._flee_success),
            ProbabilityBinding(100 - self.flee_chance, FailedFlee)
        ])

    @staticmethod
    @functional_component(state_dependent=True)
    def _flee_success(game_state: GameState):
        event_logger.log_event(FleeEvent(game_state.current_area.current_enemy.name))
        game_state.player.gain_xp_other(1)

        return game_state

# ================================================================================================

@register_component(ENCOUNTER_SUB_BOSS)
class EncounterBoss(GatekeepingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(
            game_state,
            decision_function=lambda: self.execute_current(),
            accept_component=Battle,
            deny_component=self._all_bosses_dead_component
        )

    def execute_current(self) -> bool:
        area = self.game_state.current_area

        liberated = [enemy.name for enemy in self.game_state.liberated_enemies]
        available = [
            boss_name for boss_name in area.special_bosses
            if boss_name not in liberated
        ]

        if not available:
            return False

        choice = random.choice(available)
        set_special_boss(self.game_state, choice)

        return True

    @staticmethod
    @functional_component(state_dependent=True)
    def _all_bosses_dead_component(game_state: GameState):
        print_and_sleep(yellow("All bosses in this area are currently in Hell.\n"), 1.5)
        return game_state

# ================================================================================================

def set_special_boss(game_state: GameState, name: str) -> GameState:
    time = game_state.time_of_day

    special_boss = game_state.current_area.spawn_special_boss(name, time, game_state)
    game_state.current_area.current_enemy = special_boss

    return game_state

# ================================================================================================

@register_component(SPAWN_ENEMY)
class SpawnEnemy(LinearComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, next_component=Battle)

    def execute_current(self) -> GameState:
        self.game_state.current_area.spawn_enemy(self.game_state,
                                                 self.game_state.player.lvl,
                                                 self.game_state.wanted,
                                                 self.game_state.time_of_day,
                                                 self.game_state.moon)

        return self.game_state

# ================================================================================================

class Battle(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(
            game_state,
            top_level_prompt_callback=lambda gs: print_and_sleep(get_battle_status_view(gs)),
            bindings=[
                SelectionBinding('A', "Attack", Attack),
                SelectionBinding('I', "Use Item", UseItem),
                SelectionBinding('S', "Switch Weapon", EquipWeapon),
                FleeSelectionBinding('F', "Flee", TryFlee, game_state),
                SelectionBinding('V', "View", DisplayInfo),
            ]
        )
        self.player = self.game_state.player
        self.player.can_flee = False
        if perk_is_active(DEATH_CAN_WAIT):
            self.player.cheat_death_enabled = True
        self.enemy = self.game_state.current_area.current_enemy
        self.fled = False
        self._subscribe_listeners()

    def play_theme(self) -> None:
        current_enemy = self.game_state.current_area.current_enemy
        theme = BATTLE_THEME

        if isinstance(current_enemy, SpecialBoss):
            theme = current_enemy.theme if current_enemy.theme else HOHKKEN_THEME

        play_music(theme)

    def can_exit(self) -> bool:
        return self.fled or self.player.can_flee or not (self.player.is_alive() and self.enemy.is_alive())

    def _subscribe_listeners(self):
        @subscribe_function(FleeEvent)
        def handle_flee(_: FleeEvent):
            self.fled = True

# ================================================================================================

class EnemyInfect(NoOpComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)

    def run(self):
        return self.execute()

    def execute(self):
        player = self.game_state.player
        enemy = self.game_state.current_area.current_enemy

        if not enemy or not enemy.illness:
            return self.game_state

        if not player.illness:
            illness_name = enemy.illness.name
            player.acquire_illness(illness_name)
            print_and_sleep(yellow(f"You caught {player.illness.name} from {enemy.name}!"), 2)

        return self.game_state

# ================================================================================================

class BattleEnd(NoOpComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)

    def run(self):
        return self.check_battle_end()

    def check_battle_end(self) -> GameState:
        player = self.game_state.player
        enemy = self.game_state.current_area.current_enemy
        current_area = self.game_state.current_area
        wench_area = self.game_state.wench_area

        if enemy and not enemy.is_alive():
            self.handle_enemy_death(player, enemy)
            self.game_state.current_area.kill_current_enemy(current_area, wench_area)
            self.game_state = PostKillEncounters(self.game_state).run()

        if not player.is_alive():
            player.lives -= 1
            event_logger.log_event(PlayerDeathEvent(player.lives))

        return self.game_state

    # TODO - refactor
    def handle_enemy_death(self, player, enemy) -> None:
        if enemy.type == FINAL_BOSS:
            self.game_state.victory = True
            return

        if self.game_state.pending_boss:
            self.game_state.pending_boss = False

        # TODO maybe put the next 3 lines in an event callback (Kill)
        stop_music()
        play_sound(DEVIL_THUNDER)
        print_and_sleep(red(f"{enemy.name} is now in Hell."), 2)

        # --- Hohkken ---
        if enemy.name == HOHKKEN:
            event_logger.log_event(DefeatHohkkenEvent())
            activate_perk_print(NEPTUNE)
            self.game_state.hohkken_is_alive = False

        # --- wanted / bounty ---
        if self.game_state.is_wanted(enemy):
            event_logger.log_event(BountyCollectedEvent(enemy.name))
        enemy_weapon = enemy.drop_weapon()
        if enemy_weapon is not None:
            player.obtain_enemy_weapon(enemy_weapon)

        # --- coins and xp ---
        coins = enemy.drop_coins(enemy)
        coins *= min(1.25, 1 + ((player.lvl - 1) * 0.025))
        if coins:
            player.gain_coins(round(coins))
        player.gain_xp_from_enemy(enemy)

        # --- special boss item drop ---
        # TODO - add swap item code eventually just in case (usually going to use an item to beat a boss)
        if enemy.type == SPECIAL_BOSS:
            if enemy.item:
                item = load_boss_item(enemy.item)
                if player.add_item(item):
                    print_and_sleep(cyan(f"{item.name} added to sack."), 1)

        # --- logging and updates ---
        event_logger.log_event(KillEvent())
        if event_logger.get_count(EventType.KILL) % 2 == 0:
            self.game_state.update_time_of_day()
        if event_logger.get_count(EventType.KILL) % 4 == 0:
            self.game_state.update_moon()

        # --- add enemy to list of liberated enemies ---
        self.game_state.liberated_enemies.append(enemy)

# ================================================================================================

@register_component(FIGHT_BOSS_OTHER)
class FightBossOther(Battle):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)
        self.enemy = self.game_state.current_area.current_enemy

    def play_theme(self) -> None:
        theme = self.enemy.theme if self.enemy.theme else BATTLE_THEME
        play_music(theme)

    def run(self) -> GameState:
        self.play_theme()
        self.enemy.do_preamble()
        self.game_state = super().run()
        return self.game_state

# ================================================================================================

@register_component(AREA_BOSS_FIGHT)
class FightBoss(Battle):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)
        self.enemy = self.game_state.current_area.current_enemy

    def play_theme(self) -> None:
        theme = self.enemy.theme if self.enemy.theme else BATTLE_THEME
        play_music(theme)

    @staticmethod
    @functional_component(state_dependent=True)
    # TODO generalize this and get it out of component
    def captain_hole_action(game_state: GameState) -> GameState:
        game_state.player.items.pop(TENCH_FILET, None)

        injury = random.randint(25, 50)
        game_state.current_area.current_enemy.hp -= injury

        print_and_sleep("You hand your filet over to Captain Hole.", seconds=2)
        stop_music()
        play_sound(PISTOL)
        print_and_sleep(f"He shoots himself in the jines, losing {injury} HP as a result.", 3)

        return game_state

    def run(self) -> GameState:
        self.play_theme()
        self.enemy.do_preamble()

        # TODO generalize this and get it out of component
        if self.enemy.name == CAPTAIN_HOLE and TENCH_FILET in self.player.items:
            self.game_state = BinarySelectionComponent(
                self.game_state,
                query="Do you accept?",
                yes_component=self.captain_hole_action,
                no_component=NoOpComponent
            ).run()

        self.game_state = super().run()

        if self.game_state.current_area.current_enemy is None and self.game_state.is_final_boss_available():
            return FightFinalBoss(self.game_state).run()

        return self.game_state

# ================================================================================================

@register_component(FINAL_BOSS_FIGHT)
class FightFinalBoss(FightBoss):
    def __init__(self, game_state: GameState):
        final_boss = game_state.current_area.summon_final_boss()
        game_state.current_area.current_enemy = final_boss

        super().__init__(game_state)

        self.enemy = final_boss

# ================================================================================================

# --- keep alphabetical ---

@register_component(ACHIEVEMENTS)
class Achievements(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, display_callback=display_player_achievements)


@register_component(ATTRIBUTES)
class Attributes(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, display_callback=display_player_attributes)


@register_component(DISCOVERIES)
class Discoveries(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, display_callback=display_discoveries)


@register_component(ENCOUNTERS)
class Encounters(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, display_callback=display_encountered)


@register_component(INFO)
class DisplayInfo(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, display_callback=display_battle_info)


@register_component(INVESTMENTS)
class Investments(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, display_callback=display_investments)


@register_component(KILLS)
class Liberated(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, display_callback=display_liberated)


@register_component(OVERVIEW)
class Overview(GatekeepingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, decision_function=lambda: game_state.player.is_alive(),
                         accept_component=OverviewMenu, deny_component=functional_component()(lambda:
                                                                                              print_and_sleep(yellow(
                                                                                                  f"You're a dang ghost."),

                                                                                                              1)))


@register_component(PERKS)
class DisplayPerks(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, display_callback=display_active_perks)


@register_component(STATS)
class Stats(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, display_callback=display_game_stats)
