import random
from functools import partial
from typing import List

from savethewench.component.base import FunctionExecutingComponent, \
    FunctionalSelectionBinding, FunctionalSelectionComponent, RandomThresholdComponent, ThresholdBinding, \
    TextDisplayingComponent, anonymous_component, Component
from savethewench.component.util import get_battle_status_view, display_bank_balance, display_player_achievements, \
    display_game_overview, calculate_flee, display_active_perks
from savethewench.data.perks import METAL_DETECTIVE, WENCH_LOCATION
from savethewench.model.game_state import GameState
from savethewench.model.item import load_items
from savethewench.model.perk import load_perks, Perk, attach_perk
from savethewench.model.weapon import load_discoverable_weapons
from savethewench.ui import green, purple, yellow, dim, red
from savethewench.util import print_and_sleep
from .base import LabeledSelectionComponent, SelectionBinding
from .. import event_logger
from ..model.events import KillEvent


class Explore(RandomThresholdComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         bindings=[
                             ThresholdBinding(0.5, Battle),
                             ThresholdBinding(0.6, self._discover_item),
                             ThresholdBinding(0.68, self._discover_weapon),
                             ThresholdBinding(0.88, self._discover_coin),
                             ThresholdBinding(0.89, self._discover_perk)
                         ])

    @staticmethod
    @anonymous_component(state_dependent=True)
    def _discover_item(game_state: GameState):
        game_state.player.add_item(random.choice(load_items()))

    @staticmethod
    @anonymous_component(state_dependent=True)
    def _discover_weapon(game_state: GameState):
        game_state.player.add_weapon(random.choice(load_discoverable_weapons()))

    @staticmethod
    @anonymous_component(state_dependent=True)
    def _discover_coin(game_state: GameState):
        @attach_perk(METAL_DETECTIVE, value_description="coin")
        def find(): return random.randint(10, 25)

        coins = find()
        print_and_sleep(green(f"You found {coins} of coin!"), 1)
        game_state.player.coins += coins

    @staticmethod
    @anonymous_component()
    def _discover_perk():
        filtered: List[Perk] = load_perks(lambda p: not (p.is_active() or p.name == WENCH_LOCATION))
        if len(filtered) > 0:
            reward = random.choice(filtered)
            reward.activate()
            print_and_sleep(purple(f"You found the {reward.name} perk!\n{reward.description}"), 1)
        else:
            print_and_sleep(yellow(dim("You came up dry.")), 1)


class Travel(FunctionalSelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         bindings=[
                             FunctionalSelectionBinding(key=str(i),
                                                        name=area.name,
                                                        component=FunctionExecutingComponent,
                                                        function=partial(self._update_current_area, area.name))
                             for i, area in enumerate(
                                 reversed([a for a in game_state.areas if a.name != game_state.current_area.name]), 1)
                         ])

    @staticmethod
    def _update_current_area(name: str, gs: GameState) -> GameState:
        return gs.update_current_area(name)


class UseItem(FunctionalSelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         bindings=[FunctionalSelectionBinding(key=str(i),
                                                              name=item.name,
                                                              component=FunctionExecutingComponent,
                                                              function=partial(self._use_item, item.name))
                                   for (i, item) in enumerate(game_state.player.get_items(), 1)],
                         top_level_prompt_callback=lambda gs:
                         print(f"Items {dim(f"({len(gs.player.items)}/{gs.player.max_items})")}"))

    @staticmethod
    def _use_item(name: str, gs: GameState) -> GameState:
        gs.player.use_item(name)
        return gs


class EquipWeapon(FunctionalSelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         bindings=[FunctionalSelectionBinding(key=str(i),
                                                              name=weapon.name,
                                                              component=FunctionExecutingComponent,
                                                              function=partial(self._equip_weapon, weapon.name))
                                   for (i, weapon) in enumerate(game_state.player.get_weapons(), 1)])

    @staticmethod
    def _equip_weapon(name: str, gs: GameState) -> GameState:
        gs.player.equip_weapon(name)
        return gs


class Attack(Component):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)

    def run(self) -> GameState:
        player, enemy = self.game_state.player, self.game_state.current_area.current_enemy
        player.attack(enemy)
        if not enemy.is_alive():
            print(red(f"{enemy.name} is now in Hell."))
            event_logger.log_event(KillEvent())
            self.game_state.current_area.kill_current_enemy()
            # player.gain_enemy_weapon(enemy)
            return self.game_state
        enemy.attack(player)
        if not player.is_alive():
            # TODO handle player death
            print(red("You ded"))
        return self.game_state


class FleeSelectionBinding(SelectionBinding):
    def format(self):
        return f"Flee ({int(calculate_flee() * 100)}%)"


# TODO - a lot, but especially bounty stuff and handling player death
class Battle(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, top_level_prompt_callback=lambda gs: print(get_battle_status_view(gs)),
                         bindings=[
                             SelectionBinding('A', "Attack", Attack),
                             SelectionBinding('I', "Use Item", UseItem),
                             SelectionBinding('S', "Switch Weapon", EquipWeapon),
                             FleeSelectionBinding('F', "Flee (50%)", anonymous_component()(self._try_flee)),
                             SelectionBinding('P', "Perks", DisplayPerks)
                         ])
        self.player = self.game_state.player
        self.enemy = self.game_state.current_area.spawn_enemy()
        self.fled = False

    def can_exit(self):
        return self.fled or not (self.player.is_alive() and self.enemy.is_alive())

    def _try_flee(self):
        flee_chance = calculate_flee()
        if random.random() < flee_chance:
            print(dim(f"You ran away from {self.enemy.name}!"))
            self.fled = True
            self.game_state.current_area.reset_current_enemy()
        else:
            print(yellow("Couldn't escape!"))


class Achievements(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, display_callback=display_player_achievements, should_proceed=False)


class BankBalance(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, display_callback=display_bank_balance, should_proceed=False)


class DisplayPerks(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, display_callback=display_active_perks, should_proceed=False)


class Overview(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, display_callback=display_game_overview, should_proceed=False)
