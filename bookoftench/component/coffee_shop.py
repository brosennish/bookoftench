import random

from bookoftench import event_logger
from bookoftench.audio import play_music
from bookoftench.component.base import LabeledSelectionComponent, ReprBinding, SelectionBinding, \
    functional_component, GatekeepingComponent, Component
from bookoftench.component.registry import register_component
from bookoftench.data.audio import SHOP_THEME
from bookoftench.data.components import COFFEE_SHOP
from bookoftench.model import GameState
from bookoftench.model.coffee_item import CoffeeItem
from bookoftench.model.coffee_shop import CoffeeShop
from bookoftench.model.events import PlayerDeathEvent
from bookoftench.model.illness import load_illnesses
from bookoftench.model.player import Player
from bookoftench.model.util import display_coffee_header
from bookoftench.ui import blue, yellow, green, red
from bookoftench.util import print_and_sleep


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
        shop_options = shop.apply_discounts(shop.coffee_inventory)

        item_bindings = [ReprBinding(str(i + 1), item.name, self._make_purchase_component(item), item) for
                         i, item in enumerate(shop_options)]
        return_binding = SelectionBinding('R', "Return", functional_component()(lambda: self._return()))
        super().__init__(game_state, refresh_menu=True,
                         bindings=[*item_bindings, return_binding])
        self.selection_components = [
            LabeledSelectionComponent(
                game_state,
                item_bindings,
                top_level_prompt_callback=display_coffee_header,
            ),
            LabeledSelectionComponent(
                game_state,
                [return_binding]
            ),
        ]
        self.exit_shop = False

    def play_theme(self) -> None:
        play_music(SHOP_THEME)

    def _return(self):
        self.exit_shop = True
        print_and_sleep((
            f"{blue('Until')} "
            f"{yellow('*cough cough*')} "
            f"{blue('next time!')}\n"
        ), 1)

    def can_exit(self) -> bool:
        return (self.exit_shop
                or not self.game_state.player.is_alive()
                or self.game_state.player.is_sick())

    def display_options(self) -> None:
        print_and_sleep(
            f"{blue('Welcome to ')} "
            f"{yellow('*cough cough* ')} "
            f"{blue('Coughy\'s Coffee!')} "
        )
        for component in self.selection_components:
            component.display_options()

    @staticmethod
    def _make_purchase_component(coffee_item: CoffeeItem) -> type[Component]:
        @functional_component(state_dependent=True)
        def purchase_component(game_state: GameState):
            player = game_state.player
            if player.coins < coffee_item.cost:
                print_and_sleep(yellow(f"Need more coin"), 1)
            else:
                player.coins -= coffee_item.cost
                apply_coffee_effect(coffee_item, player)

        return purchase_component


def apply_coffee_effect(item: CoffeeItem, player: Player):
    original_hp = player.hp
    player.gain_hp(item.hp)
    print_and_sleep(f"You restored {green(player.hp - original_hp)} hp!", 1)

    illness = random.choice(load_illnesses())

    if random.random() < item.risk:
        if illness.causes_instant_death:
            print_and_sleep(yellow(f"Coughy coughed on your coffee and now you're just a worthless bag of bones."),
                            2)
            print_and_sleep(f"Cause of Death: {red(f'{illness.name}')}", 2)
            print_and_sleep(f"{red(f'{illness.description}')}", 3)
            player.hp = 0
            player.lives -= 1
            event_logger.log_event(PlayerDeathEvent(player.lives))
        else:
            player.illness = illness
            player.illness_death_lvl = player.lvl + illness.levels_until_death

            print_and_sleep(yellow(f"Coughy coughed on your coffee and now you're sicker than Hell."), 2)
            print_and_sleep(f"Illness: {yellow(f'{illness.name}')}", 2)
            print_and_sleep(f"{yellow(f'{illness.description}')}", 2)
            print_and_sleep(
                f"Seek treatment or die at level {red(f'{player.illness_death_lvl}')}\n",
                3
            )
