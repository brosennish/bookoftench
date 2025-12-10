from functools import partial

from api import FunctionExecutingComponent, \
    FunctionalSelectionBinding, FunctionalSelectionComponent, RandomThresholdComponent, ThresholdBinding, \
    TextDisplayingComponent
from api import NoOpComponent, LinearComponent, LabeledSelectionComponent, SelectionBinding
from model.game_state import GameState
from .util import get_battle_status_view, display_bank_balance, display_player_perks


class Explore(RandomThresholdComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         bindings=[
                             ThresholdBinding(0.5, SpawnEnemy),
                             ThresholdBinding(0.6, DiscoverItem),
                             ThresholdBinding(0.68, DiscoverWeapon),
                             ThresholdBinding(0.88, DiscoverCoin),
                             ThresholdBinding(0.89, DiscoverPerk)
                         ])


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


class Achievements(NoOpComponent): pass


class BankBalance(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, display_callback=display_bank_balance, should_proceed=False)


class DisplayPerks(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, display_callback=display_player_perks, should_proceed=False)


class Overview(NoOpComponent): pass
