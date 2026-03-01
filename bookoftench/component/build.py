from __future__ import annotations

from bookoftench.component.base import LabeledSelectionComponent, ReprBinding
from bookoftench.component.registry import register_component
from bookoftench.data.components import BUILD
from bookoftench.model import GameState, build
from bookoftench.util import print_and_sleep


@register_component(BUILD)
class BuildComponent(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        build_bindings = [ReprBinding(str(i + 1), build.name, self._make_buy_or_steal_component(item), item) for
                         i, item in enumerate(game_state.shop.item_inventory)]
        # todo add list of build objects to game_state
        super().__init__(game_state, refresh_menu=True,
                         bindings=[*build_bindings])
        self.selection_components = [
            LabeledSelectionComponent(game_state, build_bindings, lambda gs: gs.player.display_item_count()),
        ]
        self.can_exit = False

    def can_exit(self) -> bool:
        return self.game_state.player.build

    def display_options(self) -> None:
        print_and_sleep("What be your build?")

        for component in self.selection_components:
            component.display_options()
