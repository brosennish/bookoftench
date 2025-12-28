import random
from functools import partial
from typing import List

from savethewench import event_logger
from savethewench.audio import play_music, play_sound, stop_music
from savethewench.component.base import RandomThresholdComponent, ThresholdBinding, \
    TextDisplayingComponent, functional_component, Component, ColoredNameSelectionBinding, BinarySelectionComponent, \
    NoOpComponent, LinearComponent
from savethewench.data.audio import BATTLE_THEME, DEVIL_THUNDER, PISTOL
from savethewench.data.enemies import CAPTAIN_HOLE, FINAL_BOSS
from savethewench.data.items import TENCH_FILET
from savethewench.data.perks import METAL_DETECTIVE, WENCH_LOCATION, DEATH_CAN_WAIT
from savethewench.event_logger import subscribe_function
from savethewench.model.events import KillEvent, FleeEvent, PlayerDeathEvent, BountyCollectedEvent
from savethewench.model.game_state import GameState
from savethewench.model.item import load_items
from savethewench.model.perk import load_perks, Perk, attach_perk, perk_is_active
from savethewench.model.util import get_battle_status_view, display_player_achievements, \
    display_game_overview, calculate_flee, display_active_perks
from savethewench.model.weapon import load_discoverable_weapons
from savethewench.ui import green, purple, yellow, dim, red, cyan, blue
from savethewench.util import print_and_sleep
from .bank import BankVisitDecision
from .base import LabeledSelectionComponent, SelectionBinding
from ..data.weapons import BARE_HANDS
from ..model.player import Player


class Explore(RandomThresholdComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         bindings=[
                             ThresholdBinding(0, SpawnEnemy),
                             ThresholdBinding(0, self._discover_item),
                             ThresholdBinding(1, self._discover_weapon),
                             ThresholdBinding(0, self._discover_coin),
                             ThresholdBinding(0, self._discover_perk)
                         ])

    @staticmethod
    @functional_component(state_dependent=True)
    def _discover_item(game_state: GameState):
        item = random.choice(load_items())
        if game_state.player.add_item(item):
            print_and_sleep(cyan(f"{item.name} added to sack."), 1)



    @staticmethod
    @functional_component(state_dependent=True)
    def _discover_weapon(game_state: GameState):
        available = [w for w in load_discoverable_weapons()
                     if w.name not in game_state.player.weapon_dict]

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
    @functional_component(state_dependent=True)
    def _discover_coin(game_state: GameState):
        @attach_perk(METAL_DETECTIVE, value_description="coin")
        def find(): return random.randint(10, 25)

        coins = find()
        print_and_sleep(green(f"You found {coins} of coin!"), 1)
        game_state.player.coins += coins

    @staticmethod
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


class UseItem(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         bindings=[SelectionBinding(key=str(i),
                                                    name=item.get_simple_format(),
                                                    component=functional_component()(
                                                        partial(game_state.player.use_item, item.name)))
                                   for (i, item) in enumerate(game_state.player.get_items(), 1)],
                         top_level_prompt_callback=lambda gs: gs.player.display_item_count(), quittable=True)


class EquipWeapon(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         bindings=[SelectionBinding(
                             key=str(i),
                             name=weapon.get_simple_format(),
                             component=functional_component()(
                                 partial(game_state.player.equip_weapon, weapon.name)))
                             for (i, weapon) in enumerate(game_state.player.get_weapons(), 1)],
                         top_level_prompt_callback=lambda gs: gs.player.display_weapon_count(), quittable=True)


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
                    name=weapon.get_simple_format(),
                    component=functional_component()(
                        partial(game_state.player.swap_found_weapon, weapon.name, found)
                    )
                )
                for i, weapon in enumerate(valid, 1)
            ],
            top_level_prompt_callback=lambda gs: (
                print_and_sleep(dim(gs.found_weapon.get_simple_format()), 0),
            )[-1],
            quittable=True
        )



class Attack(Component):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)
        self.failed_flee = False

    def handle_enemy_death(self, player, enemy):
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
            if player.add_weapon(enemy_weapon):
                print_and_sleep(cyan(f"{enemy_weapon.name} added to sack."), 1)
        player.gain_coins(enemy.drop_coins())
        if player.gain_xp_from_enemy(enemy):
            BankVisitDecision(self.game_state).run()  # TODO figure out a way to not call this in so many places
        event_logger.log_event(KillEvent())
        self.game_state.current_area.kill_current_enemy()

    def run(self) -> GameState:
        player, enemy = self.game_state.player, self.game_state.current_area.current_enemy
        if not self.failed_flee:
            player.attack(enemy)
        if enemy.is_alive():
            enemy.attack(player)
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
    def format(self):
        return f"Flee ({int(calculate_flee() * 100)}%)"


class TryFlee(RandomThresholdComponent):
    def __init__(self, game_state: GameState):
        self.flee_chance = calculate_flee()
        super().__init__(game_state, bindings=[
            ThresholdBinding(self.flee_chance, self._flee_success),
            ThresholdBinding(1.0, FailedFlee)
        ])

    @staticmethod
    @functional_component(state_dependent=True)
    def _flee_success(game_state: GameState):
        event_logger.log_event(FleeEvent(game_state.current_area.current_enemy.name))
        if game_state.player.gain_xp_other(1):
            BankVisitDecision(game_state).run()  # TODO figure out a way to not call this in so many places

class SpawnEnemy(LinearComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, next_component=Battle)

    def execute_current(self) -> GameState:
        self.game_state.current_area.spawn_enemy(self.game_state.player.lvl)
        return self.game_state


class Battle(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, top_level_prompt_callback=lambda gs: print_and_sleep(get_battle_status_view(gs)),
                         bindings=[
                             SelectionBinding('A', "Attack", Attack),
                             SelectionBinding('I', "Use Item", UseItem),
                             SelectionBinding('S', "Switch Weapon", EquipWeapon),
                             FleeSelectionBinding('F', "Flee (50%)", TryFlee),
                             SelectionBinding('P', "Perks", DisplayPerks)
                         ])
        self.player = self.game_state.player
        if perk_is_active(DEATH_CAN_WAIT):
            self.player.cheat_death_enabled = True
        self.enemy = self.game_state.current_area.current_enemy
        self.fled = False
        self._subscribe_listeners()

    def play_theme(self):
        play_music(BATTLE_THEME)

    def can_exit(self):
        return self.fled or not (self.player.is_alive() and self.enemy.is_alive())

    def _subscribe_listeners(self):
        @subscribe_function(FleeEvent)
        def handle_flee(_: FleeEvent):
            self.fled = True


class FightBoss(Battle):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)
        self.enemy = self.game_state.current_area.summon_boss()

    def play_theme(self):
        play_music(self.enemy.theme)

    @staticmethod
    @functional_component(state_dependent=True)
    # TODO generalize this and get it out of component
    def captain_hole_action(game_state: GameState):
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


class FightFinalBoss(FightBoss):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)
        self.enemy = self.game_state.current_area.summon_final_boss()

class Achievements(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, display_callback=display_player_achievements)


class DisplayPerks(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, display_callback=display_active_perks)


class Overview(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, display_callback=display_game_overview)
