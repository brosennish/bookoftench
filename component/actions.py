from api import FunctionExecutingComponent, \
    FunctionalSelectionBinding, FunctionalSelectionComponent, NoOpComponent
from functools import partial
from model.game_state import GameState


class Explore(NoOpComponent): pass


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
    def _update_current_area(name: str, gs: GameState):
        gs.update_current_area(name)


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

class Achievements(NoOpComponent): pass

class BankBalance(NoOpComponent): pass

class DisplayPerks(NoOpComponent): pass

class Overview(NoOpComponent): pass