from __future__ import annotations

import random
from functools import partial

from savethewench.audio import play_music
from savethewench.component.base import LabeledSelectionComponent, ReprBinding, SelectionBinding, \
    functional_component, Component, RandomChoiceComponent, ProbabilityBinding, GatekeepingComponent
from savethewench.component.officer import OfficerEncounter
from savethewench.component.registry import register_component
from savethewench.data.audio import SHOP_THEME
from savethewench.data.components import SHOP
from savethewench.model import GameState
from savethewench.model.base import Buyable
from savethewench.model.util import display_active_perk_count
from savethewench.ui import green, blue
from savethewench.util import print_and_sleep

_MAX_STEAL_CHANCE = 75
_STEAL_SPREAD = 5


@register_component(SHOP)
class ShopBouncer(GatekeepingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, decision_function=self._player_can_enter_shop,
                         accept_component=ShopComponent,
                         deny_component=functional_component()(lambda: print_and_sleep(
                             blue("You're banned, bozo. Come back when you level up."), 1.5)))

    def _player_can_enter_shop(self) -> bool:
        return not self.game_state.shop.player_is_banned


class ShopComponent(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        item_bindings = [ReprBinding(str(i + 1), item.name, self._make_buy_or_steal_component(item), item) for
                         i, item in enumerate(game_state.shop.item_inventory)]
        weapon_bindings = [ReprBinding(str(i + 1), weapon.name, self._make_buy_or_steal_component(weapon), weapon) for
                           i, weapon in enumerate(game_state.shop.weapon_inventory, len(item_bindings))]
        perk_bindings = [ReprBinding(str(i + 1), perk.name, self._make_buy_or_steal_component(perk), perk) for
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

    def play_theme(self) -> None:
        play_music(SHOP_THEME)

    def _return(self):
        self.exit_shop = True
        print_and_sleep(blue("Until next time!"), 1)

    def can_exit(self) -> bool:
        return self.game_state.shop.player_is_banned or self.exit_shop

    def display_options(self) -> None:
        print(f"\n{blue("Welcome! You have")} {green(self.game_state.player.coins)} {blue("coins.")}\n")
        for component in self.selection_components:
            component.display_options()

    @staticmethod
    def _make_buy_or_steal_component(buyable: Buyable):
        @functional_component(state_dependent=True)
        def buy_or_steal_component(game_state: GameState):
            BuyOrStealDecision(game_state, buyable).run()

        return buy_or_steal_component


class BuyOrStealDecision(LabeledSelectionComponent):
    def __init__(self, game_state: GameState, buyable: Buyable):
        success_chance = self.calculate_success_chance(buyable)
        super().__init__(game_state, bindings=[
            SelectionBinding('B', f"Buy ({buyable.cost} of coin)", self._make_purchase_component(buyable)),
            SelectionBinding('S', f"Steal ({success_chance}% chance of success)",
                             self._make_steal_component(buyable, success_chance))
        ], quittable=True)

    @staticmethod
    def calculate_success_chance(buyable: Buyable) -> int:
        upper_bound = max(_MAX_STEAL_CHANCE - buyable.cost, _STEAL_SPREAD)
        return random.randint(max(1, upper_bound - _STEAL_SPREAD), upper_bound)

    @staticmethod
    def _make_purchase_component(buyable: Buyable):
        @functional_component(state_dependent=True)
        def purchase_component(game_state: GameState):
            if game_state.player.make_purchase(buyable):
                game_state.shop.remove_listing(buyable)

        return purchase_component

    @staticmethod
    def _make_steal_component(buyable: Buyable, success_chance: int) -> type[Component]:
        @functional_component(state_dependent=True)
        def steal_component(game_state: GameState):
            StealItem(game_state, buyable, success_chance).run()

        return steal_component


class StealItem(RandomChoiceComponent):
    def __init__(self, game_state: GameState, buyable: Buyable, success_chance: int):
        super().__init__(game_state, bindings=[
            ProbabilityBinding(success_chance, self._make_steal_component(buyable)),
            ProbabilityBinding(100 - success_chance, self.busted_component)
        ])

    @staticmethod
    def _make_steal_component(buyable: Buyable):
        @functional_component(state_dependent=True)
        def steal_component(game_state: GameState):
            if game_state.player.steal_buyable(buyable):
                game_state.player.gain_xp_other(1)
                game_state.shop.remove_listing(buyable)

        return steal_component

    @staticmethod
    @functional_component(state_dependent=True)
    def busted_component(game_state: GameState):
        game_state.shop.ban_player()
        OfficerEncounter(game_state).run()


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
