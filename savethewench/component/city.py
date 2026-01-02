from savethewench.component.base import Component
from savethewench.component.registry import register_component
from savethewench.data.components import COFFEE_SHOP
from savethewench.model import GameState
from savethewench.ui import orange
from savethewench.util import print_and_sleep


@register_component(COFFEE_SHOP)
class CoffeeShopComponent(Component):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)

    def run(self) -> GameState:
        print_and_sleep(orange("Coughy's Coffee...Opening Soon."), 2)
        return self.game_state