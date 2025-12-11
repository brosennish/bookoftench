import random
from functools import partial
from typing import List

from savethewench.component.base import FunctionExecutingComponent, \
    FunctionalSelectionBinding, FunctionalSelectionComponent, RandomThresholdComponent, ThresholdBinding, \
    TextDisplayingComponent, NoOpComponent, anonymous_component
from savethewench.data.perks import METAL_DETECTIVE, WENCH_LOCATION
from savethewench.model import GameState
from savethewench.model.item import load_items
from savethewench.model.weapon import load_discoverable_weapons
from savethewench.ui import green, purple, yellow, dim
from savethewench.util import print_and_sleep
from .base import LinearComponent, LabeledSelectionComponent, SelectionBinding
from .util import get_battle_status_view, display_bank_balance, display_player_perks, display_player_achievements, \
    display_game_overview
from savethewench.model.perk import load_perks, Perk


class Explore(RandomThresholdComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         bindings=[
                             ThresholdBinding(0.5, SpawnEnemy),
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
        coins = random.randint(25, 50) if METAL_DETECTIVE in game_state.player.perks \
            else random.randint(10, 25)
        print_and_sleep(green(f"You found {coins} coins!"))
        game_state.player.coins += coins

    @staticmethod
    @anonymous_component(state_dependent=True)
    def _discover_perk(game_state: GameState):
        filtered: List[Perk] = [p for p in load_perks() if p.name not in [*game_state.player.perks, WENCH_LOCATION]]
        if len(filtered) > 0:
            reward = random.choice(filtered)
            game_state.player.add_perk(reward.name)
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
                                   for (i, item) in enumerate(game_state.player.get_items(), 1)])

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


class SpawnEnemy(LinearComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, next_component=Battle)

    def execute_current(self) -> GameState:
        self.game_state.current_area.spawn_enemy()
        return self.game_state


class Attack(NoOpComponent): pass


class Flee(NoOpComponent): pass


class Battle(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, top_level_prompt_callback=lambda gs: print(get_battle_status_view(gs)),
                         bindings=[
                             SelectionBinding('A', "Attack", Attack),
                             SelectionBinding('I', "Use Item", UseItem),
                             SelectionBinding('S', "Switch Weapon", EquipWeapon),
                             SelectionBinding('F', "Flee (50%)", Flee),  # TODO make percentage take perks into account
                             SelectionBinding('P', "Perks", DisplayPerks)
                         ])

    def can_exit(self):
        # TODO - where to check hp and such for player and enemy
        return False


class DiscoverItem(NoOpComponent): pass


class DiscoverWeapon(NoOpComponent): pass


class DiscoverCoin(NoOpComponent): pass


class DiscoverPerk(NoOpComponent): pass


class Achievements(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, display_callback=display_player_achievements, should_proceed=False)


class BankBalance(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, display_callback=display_bank_balance, should_proceed=False)


class DisplayPerks(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, display_callback=display_player_perks, should_proceed=False)


class Overview(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, display_callback=display_game_overview, should_proceed=False)
