from typing import List

from savethewench.audio import play_music
from savethewench.component.base import LabeledSelectionComponent, ReprBinding, SelectionBinding, \
    functional_component
from savethewench.data.audio import SHOP_THEME
from savethewench.data.coffee_items import Coffee_Items
from savethewench.model import GameState
from savethewench.model.base import Buyable
from savethewench.ui import green, blue
from savethewench.util import print_and_sleep

class CoffeeShopComponent(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        item_bindings = [ReprBinding(str(i + 1), item['name'], self._make_purchase_component(item), item) for
                         i, item in enumerate(Coffee_Items)]
        return_binding = SelectionBinding('R', "Return", functional_component()(lambda: self._return()))
        super().__init__(game_state, refresh_menu=True,
                         bindings=[*item_bindings, return_binding])
        self.selection_components = [
            LabeledSelectionComponent(game_state, item_bindings, lambda gs: gs.player.display_item_count()),
            LabeledSelectionComponent(game_state, [return_binding]),
        ]
        self.exit_shop = False

    def play_theme(self):
        play_music(SHOP_THEME)

    def _return(self):
        self.exit_shop = True
        print_and_sleep(blue("Until *cough cough* next time!"), 1)

    def can_exit(self):
        return self.exit_shop

    def display_options(self):
        print(f"\n{blue("Welcome! You have *cough cough*")} {green(self.game_state.player.coins)} {blue("coins.")}\n")
        for component in self.selection_components:
            component.display_options()

    @staticmethod
    def _make_purchase_component(buyable: Buyable):
        @functional_component(state_dependent=True)
        def purchase_component(game_state: GameState):
            game_state.make_coffee_purchase(buyable)

        return purchase_component
