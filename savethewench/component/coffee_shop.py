from savethewench.audio import play_music
from savethewench.component.registry import register_component
from savethewench.component.base import LabeledSelectionComponent, ReprBinding, SelectionBinding, \
    functional_component, GatekeepingComponent
from savethewench.data.audio import SHOP_THEME
from savethewench.data.components import COFFEE_SHOP
from savethewench.model import GameState
from savethewench.model.base import Buyable
from savethewench.model.coffee_shop import CoffeeShop
from savethewench.model.util import display_coffee_header
from savethewench.ui import blue, yellow
from savethewench.util import print_and_sleep


@register_component(COFFEE_SHOP)
class CoffeeBouncer(GatekeepingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, decision_function=lambda: game_state.player.illness is None,
                         accept_component=CoffeeShopComponent,
                         deny_component=functional_component()(lambda: print_and_sleep(
                             blue("Get *cough cough* lost. No sickos allowed.\n"), 1.5)))


class CoffeeShopComponent(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        shop = CoffeeShop()
        shop_options = shop.coffee_inventory

        item_bindings = [ReprBinding(str(i + 1), item.name, self._make_purchase_component(item), item) for
                         i, item in enumerate(shop_options)]
        return_binding = SelectionBinding('R', "Return", functional_component()(lambda: self._return()))
        super().__init__(game_state, refresh_menu=True,
                         bindings=[*item_bindings, return_binding])
        self.selection_components = [
            LabeledSelectionComponent(
                game_state,
                item_bindings,
                top_level_prompt_callback=lambda gs: print(display_coffee_header(gs)),
            ),
            LabeledSelectionComponent(
                game_state,
                [return_binding]
            ),
        ]
        self.exit_shop = False

    def play_theme(self):
        play_music(SHOP_THEME)

    def _return(self):
        self.exit_shop = True
        print_and_sleep((
            f"\n{blue('Until')} "
            f"{yellow('*cough cough*')} "
            f"{blue('next time!\n')} "
        ), 1)

    def can_exit(self):
        return (self.exit_shop
                or not self.game_state.player.is_alive()
                or self.game_state.player.is_sick())

    def display_options(self):
        print(
            f"\n{blue('Welcome to ')} "
            f"{yellow('*cough cough* ')} "
            f"{blue('Coughy\'s Coffee!\n')} "
        )
        for component in self.selection_components:
            component.display_options()

    @staticmethod
    def _make_purchase_component(buyable: Buyable):
        @functional_component(state_dependent=True)
        def purchase_component(game_state: GameState):
            game_state.make_coffee_purchase(buyable)

        return purchase_component
