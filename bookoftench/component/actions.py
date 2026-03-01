import random
from functools import partial
from typing import List

from bookoftench import event_logger
from bookoftench.audio import play_music, play_sound, stop_music
from bookoftench.component.base import TextDisplayingComponent, functional_component, Component, \
    ColoredNameSelectionBinding, BinarySelectionComponent, \
    NoOpComponent, LinearComponent, RandomChoiceComponent, ProbabilityBinding, GatekeepingComponent, ReprBinding
from bookoftench.data.audio import BATTLE_THEME, DEVIL_THUNDER, PISTOL
from bookoftench.data.components import SEARCH, USE_ITEM, EQUIP_WEAPON, ACHIEVEMENTS, PERKS, STATS, TRAVEL, \
    AREA_BOSS_FIGHT, FINAL_BOSS_FIGHT, DISCOVER_ITEM, SPAWN_ENEMY, DISCOVER_WEAPON, DISCOVER_DISCOVERABLE, \
    DISCOVER_PERK, \
    OVERVIEW, INFO, BUILD
from bookoftench.data.enemies import CAPTAIN_HOLE, FINAL_BOSS
from bookoftench.data.items import TENCH_FILET
from bookoftench.data.perks import WENCH_LOCATION, DEATH_CAN_WAIT
from bookoftench.event_logger import subscribe_function
from bookoftench.model.discoverable import load_discoverables, search_discoverable_rarity, rarity_color
from bookoftench.model.enemy import ENEMY_SWITCH_WEAPON_CHANCE
from bookoftench.model.events import KillEvent, FleeEvent, PlayerDeathEvent, BountyCollectedEvent, DiscoveryEvent
from bookoftench.model.game_state import GameState
from bookoftench.model.item import load_items
from bookoftench.model.perk import load_perks, Perk, perk_is_active, activate_perk
from bookoftench.model.util import get_battle_status_view, display_player_achievements, \
    display_game_stats, calculate_flee, display_active_perks, display_battle_info
from bookoftench.model.weapon import load_discoverable_weapons, load_weapons
from bookoftench.ui import green, purple, yellow, dim, red, cyan, blue
from bookoftench.util import print_and_sleep
from .base import LabeledSelectionComponent, SelectionBinding
from .encounters import PostKillEncounters
from .menu import OverviewMenu
from .registry import register_component, get_registered_component
from ..data.discoverables import COMMON, UNCOMMON, LEGENDARY, RARE
from ..event_base import EventType
from ..model.build import Build
from ..model.player import PlayerWeapon


@register_component(BUILD)
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
        print_and_sleep("What be your build?")

        for component in self.selection_components:
            component.display_options()

    @staticmethod
    def _make_selection_component(build: Build) -> type[Component]:
        @functional_component(state_dependent=True)
        def selection_component(game_state: GameState):
            player = game_state.player
            player.build = build
            player.hp = build.hp
            player.strength = build.str
            player.acc = build.acc
            player.coins = build.coins
            player.items = dict((it.name, it) for it in build.items)
            player.weapon_dict = {it.name: PlayerWeapon.from_weapon(it) for it in build.weapons}
            for p in build.perks:
                activate_perk(p.name)

            print_and_sleep(f"You selected {build.name}."), 2

        return selection_component


@register_component(SEARCH)
class Search(RandomChoiceComponent):
    def __init__(self, game_state: GameState):
        ep = game_state.current_area.search_probabilities
        super().__init__(game_state, bindings=[ProbabilityBinding(prob, get_registered_component(name))
                                               for name, prob in ep.items()])

    @staticmethod
    @register_component(DISCOVER_DISCOVERABLE)
    @functional_component(state_dependent=True)
    def _discover_discoverable(game_state: GameState):
        player = game_state.player
        rarity = search_discoverable_rarity()
        color = rarity_color(rarity)
        available = [d for d in load_discoverables() if game_state.current_area.name
                     in d.areas and d.rarity == rarity]

        find = random.choice(available)

        # log event for stats
        if rarity == COMMON:
            event_logger.log_event(DiscoveryEvent(EventType.DISCOVERY_COMMON))
        elif rarity == UNCOMMON:
            event_logger.log_event(DiscoveryEvent(EventType.DISCOVERY_UNCOMMON))
        elif rarity == RARE:
            event_logger.log_event(DiscoveryEvent(EventType.DISCOVERY_RARE))
        elif rarity == LEGENDARY:
            event_logger.log_event(DiscoveryEvent(EventType.DISCOVERY_LEGENDARY))
        else:
            event_logger.log_event(DiscoveryEvent(EventType.DISCOVERY_MYTHIC))

        # take damage if find.hp < 0
        if find.hp < 0:
            original_hp = player.hp
            player.lose_hp(abs(find.hp - random.randint(0, 3)))
            print_and_sleep(
                f"You{f' {find.pre} ' if find.pre else ' '}{yellow(find.name)} "
                f"{color(f"({find.rarity})")} and lost {red(original_hp - player.hp)} hp.",
                2)
            if player.hp == 0:
                player.lives -= 1
                event_logger.log_event(PlayerDeathEvent(player.lives))
            return

        # heal if discoverable.hp and player.hp < max_hp
        if player.hp < player.max_hp:
            if find.hp > 0:
                original_hp = player.hp
                player.gain_hp(find.hp + random.randint(0, 3))
                print_and_sleep(
                    f"You found{f' {find.pre} ' if find.pre else ' '}{cyan(find.name)} "
                    f"{color(f"({find.rarity})")} and restored {green(player.hp - original_hp)} hp.",
                    2)
                return

        # gain coin if value greater than 0
        if find.value > 0:
            print_and_sleep(
                f"You found{f' {find.pre} ' if find.pre else ' '}{cyan(find.name)} "
                f"{color(f'({find.rarity})')} worth {green(find.value)} of coin.",
                2)
            player.gain_coins(find.value)
            return

        # print found message if neutral
        print_and_sleep(
            f"You found{f' {find.pre} ' if find.pre else ' '}{cyan(find.name)} "
            f"{color(f'({find.rarity})')}!", 2)
        return

    @staticmethod
    @register_component(DISCOVER_ITEM)
    @functional_component(state_dependent=True)
    def _discover_item(game_state: GameState):
        available = [i for i in load_items()
                     if i.name not in game_state.player.items
                     and game_state.current_area in i.areas]
        if available:
            item = random.choice(available)
        else:
            all_unowned_items = [i for i in load_items()
                                 if i.name not in game_state.player.items]
            item = random.choice(all_unowned_items)

        game_state.found_item = item
        print_and_sleep(cyan(f"You found {item.name}!"), 1)

        if game_state.player.add_item(item):
            print_and_sleep(cyan(f"{item.name} added to sack."), 1)
            return game_state
        else:
            return SwapFoundItemYN(game_state).run()

    @staticmethod
    @register_component(DISCOVER_WEAPON)
    @functional_component(state_dependent=True)
    def _discover_weapon(game_state: GameState):
        available = [w for w in load_discoverable_weapons() if game_state.current_area.name in w.areas
                    and w.name not in game_state.player.weapon_dict]

        if len(available) == 0:  # shouldn't ever be the case in actual gameplay, but need this in debug mode
            available = load_discoverable_weapons()
        weapon = random.choice(available)
        game_state.found_weapon = weapon
        print_and_sleep(cyan(f"You found {'an' if weapon.name[0].lower() in 'aeiou' else 'a'} {weapon.name}!"),
                        1)

        if game_state.player.add_weapon(weapon):
            print_and_sleep(cyan(f"{weapon.name} added to sack."), 1)
            return game_state
        else:
            return SwapFoundWeaponYN(game_state).run()

    @staticmethod
    @register_component(DISCOVER_PERK)
    @functional_component()
    def _discover_perk():
        filtered: List[Perk] = load_perks(lambda p: not (p.active or p.name == WENCH_LOCATION))
        if len(filtered) > 0:
            reward = random.choice(filtered)
            print_and_sleep(purple("You sense a noble presence..."), 2)
            print_and_sleep(purple("It's a mensch!"), 2)
            print_and_sleep(purple(f"He's gifted you the {reward.name} perk!\n{reward.description}"), 2)
            reward.activate()
        else:
            print_and_sleep(yellow(dim("You came up dry.")), 1)


@register_component(TRAVEL)
class Travel(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         bindings=[
                             ColoredNameSelectionBinding(key=str(i), name=area.name, color=blue,
                                                         component=functional_component()(
                                                             partial(game_state.update_current_area, area.name)))
                             for i, area in enumerate(
                                 sorted([a for a in game_state.areas if a.name != game_state.current_area.name],
                                        key=lambda a: a.name), 1)], quittable=True)


@register_component(USE_ITEM)
class UseItem(GatekeepingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         decision_function=lambda: len(game_state.player.items) > 0,
                         accept_component=ItemSelectionComponent,
                         deny_component=functional_component()(
                             lambda: print_and_sleep(yellow(f"Your inventory is dry."), 1)))


class ItemSelectionComponent(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        self.length = 0
        for i in game_state.player.items.keys():
            if len(i) > self.length:
                self.length = len(i) + 1

        super().__init__(game_state,
                         bindings=[SelectionBinding(key=str(i),
                                                    name=item.get_simple_format(self.length),
                                                    component=functional_component()(
                                                        partial(game_state.player.use_item, item.name)))
                                   for (i, item) in enumerate(game_state.player.get_items(), 1)],
                         top_level_prompt_callback=lambda gs: gs.player.display_item_count(), quittable=True)


@register_component(EQUIP_WEAPON)
class EquipWeapon(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         bindings=[SelectionBinding(
                             key=str(i),
                             name=weapon.get_complete_format(),
                             component=functional_component()(
                                 partial(game_state.player.equip_weapon, weapon.name)))
                             for (i, weapon) in enumerate(game_state.player.get_weapons(), 1)],
                         top_level_prompt_callback=lambda gs: gs.player.display_equip_header(), quittable=True)


class SwapFoundItemYN(BinarySelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         query="Swap for one of your current items",
                         yes_component=SwapFoundItemMenu,
                         no_component=NoOpComponent)


# TODO Clean Up
class SwapFoundItemMenu(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        found = game_state.found_item
        valid = list(i for i in game_state.player.items.values())
        length = 0
        for i in game_state.player.items.keys():
            if len(i) > length:
                length = len(i) + 1

        super().__init__(
            game_state,
            bindings=[
                SelectionBinding(
                    key=str(i),
                    name=item.get_simple_format(length),
                    component=functional_component()(
                        partial(game_state.player.swap_found_item, item.name, found)
                    )
                )
                for i, item in enumerate(valid, 1)
            ],
            top_level_prompt_callback=lambda gs: (
                print_and_sleep(dim(gs.found_item.get_found_format()), 0),
            )[-1],
            quittable=True
        )


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
                    name=weapon.get_complete_format(),
                    component=functional_component()(
                        partial(game_state.player.swap_found_weapon, weapon.name, found)
                    )
                )
                for i, weapon in enumerate(valid, 1)
            ],
            top_level_prompt_callback=lambda gs: (
                print_and_sleep(dim(gs.found_weapon.get_complete_format()), 0),
            )[-1],
            quittable=True
        )


class Attack(Component):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)
        self.failed_flee = False

    def handle_enemy_death(self, player, enemy) -> None:
        if enemy.type == FINAL_BOSS:
            self.game_state.victory = True
            return
        # TODO maybe put the next 3 lines in an event callback
        stop_music()
        play_sound(DEVIL_THUNDER)
        print_and_sleep(red(f"{enemy.name} is now in Hell."), 2)
        if self.game_state.is_wanted(enemy):
            event_logger.log_event(BountyCollectedEvent(enemy.name))
        enemy_weapon = enemy.drop_weapon()
        if enemy_weapon is not None:
            player.obtain_enemy_weapon(enemy_weapon)

        coins = enemy.drop_coins()
        coins *= min(1.25, 1 + ((player.lvl - 1) * 0.025))
        player.gain_coins(round(coins))
        player.gain_xp_from_enemy(enemy)

        event_logger.log_event(KillEvent())
        self.game_state.current_area.kill_current_enemy()
        PostKillEncounters(self.game_state).run()

    def run(self) -> GameState:
        player, enemy = self.game_state.player, self.game_state.current_area.current_enemy
        if not self.failed_flee:
            player.attack(enemy)
        if enemy.is_alive():
            enemy.attack(player)
            if player.is_alive() and random.random() < ENEMY_SWITCH_WEAPON_CHANCE:
                enemy.current_weapon = enemy.enemy_switch_weapon()
        if not enemy.is_alive():
            self.handle_enemy_death(player, enemy)
        if not player.is_alive():
            player.lives -= 1
            event_logger.log_event(PlayerDeathEvent(player.lives))
        return self.game_state


class FailedFlee(Attack):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)
        self.failed_flee: bool = True

    def run(self) -> GameState:
        print_and_sleep(yellow("Couldn't escape!"), 0.5)
        return super().run()


class FleeSelectionBinding(SelectionBinding):
    def format(self) -> str:
        return f"Flee ({int(calculate_flee() * 100)}%)"


class TryFlee(RandomChoiceComponent):
    def __init__(self, game_state: GameState):
        self.flee_chance = int(calculate_flee() * 100)
        super().__init__(game_state, bindings=[
            ProbabilityBinding(self.flee_chance, self._flee_success),
            ProbabilityBinding(100 - self.flee_chance, FailedFlee)
        ])

    @staticmethod
    @functional_component(state_dependent=True)
    def _flee_success(game_state: GameState):
        event_logger.log_event(FleeEvent(game_state.current_area.current_enemy.name))
        game_state.player.gain_xp_other(1)


@register_component(SPAWN_ENEMY)
class SpawnEnemy(LinearComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, next_component=Battle)

    def execute_current(self) -> GameState:
        wanted = self.game_state.wanted
        self.game_state.current_area.spawn_enemy(wanted, self.game_state.player.lvl)
        return self.game_state


class Battle(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, top_level_prompt_callback=lambda gs: print_and_sleep(get_battle_status_view(gs)),
                         bindings=[
                             SelectionBinding('A', "Attack", Attack),
                             SelectionBinding('I', "Use Item", UseItem),
                             SelectionBinding('S', "Switch Weapon", EquipWeapon),
                             FleeSelectionBinding('F', "Flee (50%)", TryFlee),
                             SelectionBinding('V', "View", DisplayInfo)
                         ])
        self.player = self.game_state.player
        self.player.can_flee = False
        if perk_is_active(DEATH_CAN_WAIT):
            self.player.cheat_death_enabled = True
        self.enemy = self.game_state.current_area.current_enemy
        self.fled = False
        self._subscribe_listeners()

    def play_theme(self) -> None:
        play_music(BATTLE_THEME)

    def can_exit(self) -> bool:
        return self.fled or self.player.can_flee or not (self.player.is_alive() and self.enemy.is_alive())

    def _subscribe_listeners(self):
        @subscribe_function(FleeEvent)
        def handle_flee(_: FleeEvent):
            self.fled = True


@register_component(AREA_BOSS_FIGHT)
class FightBoss(Battle):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)
        self.enemy = self.game_state.current_area.summon_boss()

    def play_theme(self) -> None:
        play_music(self.enemy.theme)

    @staticmethod
    @functional_component(state_dependent=True)
    # TODO generalize this and get it out of component
    def captain_hole_action(game_state: GameState) -> None:
        del game_state.player.items[TENCH_FILET]
        injury = random.randint(25, 50)
        game_state.current_area.boss.hp -= injury
        print_and_sleep('You hand your filet over to Captain Hole.', seconds=2)
        stop_music()
        play_sound(PISTOL)
        print_and_sleep(f'He shoots himself in the jines, losing {injury} HP as a result.', 3)

    def run(self) -> GameState:
        self.play_theme()
        self.enemy.do_preamble()
        # TODO generalize this and get it out of component
        if self.enemy.name == CAPTAIN_HOLE and TENCH_FILET in self.player.items:
            BinarySelectionComponent(self.game_state,
                                     query="Do you accept?",
                                     yes_component=self.captain_hole_action,
                                     no_component=NoOpComponent).run()
        self.game_state = super().run()
        if self.game_state.current_area.current_enemy is None and self.game_state.is_final_boss_available():
            return FightFinalBoss(self.game_state).run()
        return self.game_state


@register_component(FINAL_BOSS_FIGHT)
class FightFinalBoss(FightBoss):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)
        self.enemy = self.game_state.current_area.summon_final_boss()


@register_component(ACHIEVEMENTS)
class Achievements(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, display_callback=display_player_achievements)


@register_component(PERKS)
class DisplayPerks(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, display_callback=display_active_perks)


@register_component(INFO)
class DisplayInfo(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, display_callback=display_battle_info)


@register_component(STATS)
class Stats(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, display_callback=display_game_stats)


@register_component(OVERVIEW)
class Overview(GatekeepingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, decision_function=lambda: game_state.player.is_alive(),
                         accept_component=OverviewMenu, deny_component=functional_component()(lambda:
                                                                                              print_and_sleep(yellow(
                                                                                                  f"You're a dang ghost."),
                                                                                                              1)))
