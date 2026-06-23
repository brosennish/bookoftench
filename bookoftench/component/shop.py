from __future__ import annotations

import random

from bookoftench.audio import play_music, play_sound
from bookoftench.component.base import LabeledSelectionComponent, ReprBinding, SelectionBinding, \
    functional_component, Component, RandomChoiceComponent, ProbabilityBinding, GatekeepingComponent
from bookoftench.component.officer import OfficerEncounter
from bookoftench.component.registry import register_component
from bookoftench.data.audio import SHOP_THEME, WHIFF
from bookoftench.data.components import SHOP
from bookoftench.data.perks import CATFISH_BURGLAR
from bookoftench.model import GameState
from bookoftench.model.base import Buyable
from bookoftench.model.perk import attach_perk
from bookoftench.model.util import display_active_perk_count, display_shop_header
from bookoftench.ui import blue, yellow, orange
from bookoftench.util import print_and_sleep

# ================================================================================================

_max_steal_chance = 75
_steal_spread = 5

# ================================================================================================

# --- check if player is banned ---

@register_component(SHOP)
class ShopBouncer(GatekeepingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         decision_function=self._player_can_enter_shop,
                         accept_component=ShopComponent,
                         deny_component=player_banned_from_shop)

    def _player_can_enter_shop(self) -> bool:
        return not self.game_state.shop.player_is_banned


@functional_component(state_dependent=True)
def player_banned_from_shop(game_state: GameState) -> GameState:
    print_and_sleep(blue("You're banned, bozo. Come back when you level up."), 1.5)
    return game_state

# ================================================================================================

class ShopComponent(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        item_bindings = [
            ReprBinding(
                str(index + 1),
                item.name,
                self._make_buy_or_steal_component(item),
                item,
            )
            for index, item in enumerate(game_state.shop.item_inventory)
        ]

        weapon_bindings = [
            ReprBinding(
                str(index + 1),
                weapon.base_name,
                self._make_buy_or_steal_component(weapon),
                weapon,
            )
            for index, weapon in enumerate(
                game_state.shop.weapon_inventory,
                len(item_bindings),
            )
        ]

        perk_bindings = [
            ReprBinding(
                str(index + 1),
                perk.name,
                self._make_buy_or_steal_component(perk),
                perk,
            )
            for index, perk in enumerate(
                game_state.shop.perk_inventory,
                len(item_bindings) + len(weapon_bindings),
            )
        ]

        sell_binding = SelectionBinding("S", "Sell", SellItem)
        refresh_binding = SelectionBinding(
            "U",
            refresh_cost(game_state),
            functional_component()(lambda: self._refresh()),
        )
        return_binding = SelectionBinding(
            "R",
            "Return",
            functional_component()(lambda: self._return()),
        )

        super().__init__(
            game_state,
            refresh_menu=True,
            bindings=[
                *item_bindings,
                *weapon_bindings,
                *perk_bindings,
                sell_binding,
                refresh_binding,
                return_binding,
            ],
        )

        self.selection_components = [
            LabeledSelectionComponent(
                game_state,
                item_bindings,
                lambda gs: gs.player.display_item_count(),
            ),
            LabeledSelectionComponent(
                game_state,
                weapon_bindings,
                lambda gs: gs.player.display_weapon_count(),
            ),
            LabeledSelectionComponent(
                game_state,
                perk_bindings,
                lambda _: display_active_perk_count(),
            ),
            LabeledSelectionComponent(
                game_state,
                [sell_binding, refresh_binding, return_binding],
            ),
        ]
        self.exit_shop = False

    def play_theme(self) -> None:
        play_music(SHOP_THEME)

    def _return(self) -> GameState:
        self.exit_shop = True
        print_and_sleep(blue("Until next time!"), 1)
        return self.game_state

    def can_exit(self) -> bool:
        return self.game_state.shop.player_is_banned or self.exit_shop

    def display_options(self) -> None:
        area = self.game_state.current_area.name

        print_and_sleep(blue(f"Welcome to the {area} Shop!"))
        display_shop_header(self.game_state)

        for component in self.selection_components:
            component.display_options()

    def _refresh(self) -> GameState:
        player = self.game_state.player
        cost = min(4 + player.lvl, 10)

        if player.coins < cost:
            print_and_sleep(yellow("Need more coin."), 2)
            return self.game_state

        player.coins -= cost
        play_sound(WHIFF)
        self.game_state.current_area.shop.reset_inventory()

        return self.game_state

    @staticmethod
    def _make_buy_or_steal_component(buyable: Buyable) -> type[Component]:
        @functional_component(state_dependent=True)
        def buy_or_steal_component(game_state: GameState) -> GameState:
            return BuyOrStealDecision(game_state, buyable).run()

        return buy_or_steal_component

# ================================================================================================

def refresh_cost(game_state: GameState) -> str:
    player = game_state.player
    cost = min(4 + player.lvl, 10)

    return f"Refresh ({orange(cost)})"

# ================================================================================================

class BuyOrStealDecision(LabeledSelectionComponent):
    def __init__(self, game_state: GameState, buyable: Buyable):
        luck = min(game_state.player.luck, 7)

        success_chance = self.calculate_success_chance(buyable, luck)
        success_chance = max(0, min(100, success_chance))

        buy_binding = SelectionBinding(
            "B",
            f"Buy ({buyable.cost})",
            self._make_purchase_component(buyable),
        )
        steal_binding = SelectionBinding(
            "S",
            f"Steal ({success_chance}% chance)",
            self._make_steal_component(buyable, success_chance),
        )

        super().__init__(
            game_state,
            bindings=[buy_binding, steal_binding],
            quittable=True,
        )

    @staticmethod
    @attach_perk(CATFISH_BURGLAR, value_description="shoplifting odds")
    def calculate_success_chance(buyable: Buyable, luck: float) -> int:
        upper_bound = max(_max_steal_chance - buyable.cost, _steal_spread)
        lower_bound = max(1, upper_bound - _steal_spread + int(luck))
        lower_bound = min(lower_bound, upper_bound)

        return random.randint(lower_bound, upper_bound)

    @staticmethod
    def _make_purchase_component(buyable: Buyable) -> type[Component]:
        @functional_component(state_dependent=True)
        def purchase_component(game_state: GameState) -> GameState:
            if game_state.player.make_purchase(buyable):
                game_state.shop.remove_listing(buyable)

            return game_state

        return purchase_component

    @staticmethod
    def _make_steal_component(buyable: Buyable, success_chance: int) -> type[Component]:
        @functional_component(state_dependent=True)
        def steal_component(game_state: GameState) -> GameState:
            return StealItem(game_state, buyable, success_chance).run()

        return steal_component

# ================================================================================================

class StealItem(RandomChoiceComponent):
    def __init__(self, game_state: GameState, buyable: Buyable, success_chance: int):
        super().__init__(game_state, bindings=[
            ProbabilityBinding(success_chance, self._make_steal_component(buyable)),
            ProbabilityBinding(100 - success_chance, self.busted_component)
        ])

    @staticmethod
    def _make_steal_component(buyable: Buyable) -> type[Component]:
        @functional_component(state_dependent=True)
        def steal_component(game_state: GameState) -> GameState:
            player = game_state.player

            if player.steal_buyable(buyable):
                player.gain_xp_other(1)
                player.gain_or_lose_luck(0.1)
                game_state.shop.remove_listing(buyable)

            return game_state

        return steal_component

    @staticmethod
    @functional_component(state_dependent=True)
    def busted_component(game_state: GameState) -> GameState:
        game_state.shop.ban_player()
        game_state.player.gain_or_lose_luck(-0.1)

        return OfficerEncounter(game_state).run()

# ================================================================================================

class SellItem(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        item_bindings = [
            ReprBinding(
                str(index),
                item.name,
                self._make_sell_item_component(item.name),
                item.to_sellable_item(),
            )
            for index, item in enumerate(game_state.player.items.values(), 1)
        ]

        weapon_bindings = [
            ReprBinding(
                str(index),
                weapon.base_name,
                self._make_sell_weapon_component(weapon.base_name),
                weapon.to_sellable_weapon(),
            )
            for index, weapon in enumerate(
                [weapon for weapon in game_state.player.weapon_dict.values() if weapon.sell_value > 0],
                len(item_bindings) + 1,
            )
        ]

        super().__init__(
            game_state,
            bindings=[*item_bindings, *weapon_bindings],
            top_level_prompt_callback=lambda _: print("\nYour Inventory (Sell Menu):"),
            refresh_menu=True,
            quittable=True,
        )

    @staticmethod
    def _make_sell_item_component(item_name: str) -> type[Component]:
        @functional_component(state_dependent=True)
        def sell_item_component(game_state: GameState) -> GameState:
            game_state.player.sell_item(item_name)
            return game_state

        return sell_item_component

    @staticmethod
    def _make_sell_weapon_component(weapon_name: str) -> type[Component]:
        @functional_component(state_dependent=True)
        def sell_weapon_component(game_state: GameState) -> GameState:
            game_state.player.sell_weapon(weapon_name)
            return game_state

        return sell_weapon_component

