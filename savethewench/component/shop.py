from functools import partial

from savethewench.component.base import LabeledSelectionComponent, ReprBinding, SelectionBinding, \
    functional_component
from savethewench.model import GameState
from savethewench.model.base import Buyable
from savethewench.model.util import display_active_perk_count
from savethewench.ui import green, blue
from savethewench.util import print_and_sleep


class ShopComponent(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        item_bindings = [ReprBinding(str(i + 1), item.name, self._make_purchase_component(item), item) for
                         i, item in enumerate(game_state.shop.item_inventory)]
        weapon_bindings = [ReprBinding(str(i + 1), weapon.name, self._make_purchase_component(weapon), weapon) for
                           i, weapon in enumerate(game_state.shop.weapon_inventory, len(item_bindings))]
        perk_bindings = [ReprBinding(str(i + 1), perk.name, self._make_purchase_component(perk), perk) for
                         i, perk in
                         enumerate(game_state.shop.perk_inventory, len(item_bindings) + len(weapon_bindings))]
        sell_binding = SelectionBinding('S', "Sell Item", SellItem)
        return_binding = SelectionBinding('R', "Return", functional_component()(lambda: self._return()))
        super().__init__(game_state, refresh_menu=True,
                         bindings=[*item_bindings, *weapon_bindings, *perk_bindings, sell_binding, return_binding])
        self.selection_components = [
            LabeledSelectionComponent(game_state, item_bindings, lambda gs: gs.player.display_item_count()),
            LabeledSelectionComponent(game_state, weapon_bindings, lambda gs: gs.player.display_weapon_count()),
            LabeledSelectionComponent(game_state, perk_bindings, lambda _: display_active_perk_count()),
            LabeledSelectionComponent(game_state, [sell_binding, return_binding]),
        ]
        self.exit_shop = False

    def _return(self):
        self.exit_shop = True
        print_and_sleep(blue("Until next time!"), 1)

    def can_exit(self):
        return self.exit_shop

    def display_options(self):
        print(f"\n{blue("Welcome! You have")} {green(self.game_state.player.coins)} {blue("coins.")}\n")
        for component in self.selection_components:
            component.display_options()

    @staticmethod
    def _make_purchase_component(buyable: Buyable):
        @functional_component(state_dependent=True)
        def purchase_component(game_state: GameState):
            if game_state.player.make_purchase(buyable):
                game_state.shop.remove_listing(buyable)

        return purchase_component


class SellItem(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        item_bindings = [ReprBinding(str(i), item.name,
                                     functional_component()(partial(game_state.player.sell_item, item.name)),
                                     item.to_sellable_item()) for
                         i, item in enumerate(game_state.player.items.values())]
        weapon_bindings = [ReprBinding(str(i), weapon.name,
                                       functional_component()(partial(game_state.player.sell_weapon, weapon.name)),
                                       weapon.to_sellable_weapon()) for
                           i, weapon in enumerate(
                [w for w in game_state.player.weapon_dict.values() if w.sell_value > 0], len(item_bindings))]
        super().__init__(game_state,
                         bindings=[*item_bindings, *weapon_bindings],
                         top_level_prompt_callback=lambda gs: print("\nYour Inventory (Sell Menu):"), quittable=True)
