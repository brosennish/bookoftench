from typing import Callable

from savethewench.component.base import LabeledSelectionComponent, Component, SelectionBinding, functional_component, \
    BinarySelectionComponent, NoOpComponent
from savethewench.component.menu import ActionMenu
from savethewench.component.registry import register_component
from savethewench.data.components import SAVE_GAME, LOAD_GAME
from savethewench.event_base import Listener
from savethewench.event_logger import subscribe_listener
from savethewench.model import GameState
from savethewench.model.game_state import SaveGameDecisionTriggerEvent
from savethewench.persistence import SaveSlot, load_save_slots
from savethewench.ui import blue, yellow
from savethewench.util import print_and_sleep


def _your_funeral():
    print_and_sleep(blue("Your funeral..."), 1)


class SavedGameInteractingComponent(LabeledSelectionComponent):
    def __init__(self, game_state: GameState, action: Callable[[SaveSlot], type[Component]]):
        super().__init__(game_state, bindings=[
            SelectionBinding(str(slot.slot_id),
                             slot.get_displayable_format(),
                             action(slot))
            for slot in load_save_slots()], quittable=True)


@register_component(SAVE_GAME)
class SaveGame(SavedGameInteractingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, action=self.save_with_overwrite_check)

    @staticmethod
    def save_with_overwrite_check(slot: SaveSlot) -> type[Component]:
        save_game = functional_component(state_dependent=True)(slot.save_game)
        if slot.is_empty:
            return save_game

        class OverwriteCheck(BinarySelectionComponent):
            def __init__(self, gs: GameState):
                super().__init__(gs,
                                 query=f"A saved game already exists in slot {slot.slot_id}.\n\nDo you wish to proceed?",
                                 yes_component=save_game,
                                 no_component=NoOpComponent)

        return OverwriteCheck


class SaveGameDecision(BinarySelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, query="Would you like to save the game?",
                         yes_component=SaveGame, no_component=functional_component()(_your_funeral))


@subscribe_listener(SaveGameDecisionTriggerEvent)
class SaveGameDecisionListener(Listener):
    @staticmethod
    def handle_event(event: SaveGameDecisionTriggerEvent) -> None:
        SaveGameDecision(event.game_state).run()


@register_component(LOAD_GAME)
class LoadGame(SavedGameInteractingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, action=self.load_to_action_menu)

    @staticmethod
    def load_to_action_menu(slot: SaveSlot) -> type[Component]:
        if slot.is_empty:
            return functional_component()(
                lambda: print_and_sleep(yellow(f"No saved game exists in slot {slot.slot_id}.")))

        class GameStateInjectedActionMenu(ActionMenu):
            def __init__(self, _: GameState):
                super().__init__(slot.load_game())

        return GameStateInjectedActionMenu