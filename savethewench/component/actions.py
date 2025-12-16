import random
from functools import partial
from typing import List

from savethewench import event_logger
from savethewench.audio import play_music
from savethewench.component.base import RandomThresholdComponent, ThresholdBinding, \
    TextDisplayingComponent, anonymous_component, Component, ColoredNameSelectionBinding
from savethewench.component.util import get_battle_status_view, display_bank_balance, display_player_achievements, \
    display_game_overview, calculate_flee, display_active_perks
from savethewench.data.audio import BATTLE_THEME
from savethewench.data.perks import METAL_DETECTIVE, WENCH_LOCATION
from savethewench.model.events import KillEvent, BankWithdrawalEvent, FleeEvent, PlayerDeathEvent
from savethewench.model.game_state import GameState
from savethewench.model.item import load_items
from savethewench.model.perk import load_perks, Perk, attach_perk
from savethewench.model.weapon import load_discoverable_weapons
from savethewench.ui import green, purple, yellow, dim, red, cyan, blue
from savethewench.util import print_and_sleep, safe_input
from .base import LabeledSelectionComponent, SelectionBinding


class Explore(RandomThresholdComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         bindings=[
                             ThresholdBinding(0.5, Battle),
                             ThresholdBinding(0.6, self._discover_item),
                             ThresholdBinding(0.68, self._discover_weapon),
                             ThresholdBinding(0.88, self._discover_coin),
                             ThresholdBinding(0.89, self._discover_perk)
                         ])

    @staticmethod
    @anonymous_component(state_dependent=True)
    def _discover_item(game_state: GameState):
        item = random.choice(load_items())
        if game_state.player.add_item(item):
            print_and_sleep(cyan(f"{item.name} added to sack."), 1)

    @staticmethod
    @anonymous_component(state_dependent=True)
    def _discover_weapon(game_state: GameState):
        weapon = random.choice(load_discoverable_weapons())
        print_and_sleep(cyan(f"You found a {weapon.name}!"), 1)
        if game_state.player.add_weapon(weapon):
            print_and_sleep(cyan(f"{weapon.name} added to sack."), 1)

    @staticmethod
    @anonymous_component(state_dependent=True)
    def _discover_coin(game_state: GameState):
        @attach_perk(METAL_DETECTIVE, value_description="coin")
        def find(): return random.randint(10, 25)

        coins = find()
        print_and_sleep(green(f"You found {coins} of coin!"), 1)
        game_state.player.coins += coins

    @staticmethod
    @anonymous_component()
    def _discover_perk():
        filtered: List[Perk] = load_perks(lambda p: not (p.active or p.name == WENCH_LOCATION))
        if len(filtered) > 0:
            reward = random.choice(filtered)
            reward.activate()
            print_and_sleep(purple(f"You found the {reward.name} perk!\n{reward.description}"), 1)
        else:
            print_and_sleep(yellow(dim("You came up dry.")), 1)


class Travel(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         bindings=[
                             ColoredNameSelectionBinding(key=str(i), name=area.name, color=blue,
                                                         component=anonymous_component()(
                                                             partial(game_state.update_current_area, area.name)))
                             for i, area in enumerate(
                                 sorted([a for a in game_state.areas if a.name != game_state.current_area.name],
                                        key=lambda a: a.name), 1)], quittable=True)


class UseItem(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         bindings=[SelectionBinding(key=str(i),
                                                    name=item.name,
                                                    component=anonymous_component()(
                                                        partial(game_state.player.use_item, item.name)))
                                   for (i, item) in enumerate(game_state.player.get_items(), 1)],
                         top_level_prompt_callback=lambda gs: gs.player.display_item_count(), quittable=True)


class EquipWeapon(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state,
                         bindings=[SelectionBinding(key=str(i),
                                                    name=weapon.name,
                                                    component=anonymous_component()(
                                                        partial(game_state.player.equip_weapon, weapon.name)))
                                   for (i, weapon) in enumerate(game_state.player.get_weapons(), 1)],
                         top_level_prompt_callback=lambda gs: gs.player.display_weapon_count(), quittable=True)


class Attack(Component):
    def __init__(self, game_state: GameState):
        super().__init__(game_state)

    def run(self) -> GameState:
        player, enemy = self.game_state.player, self.game_state.current_area.current_enemy
        player.attack(enemy)
        if not enemy.is_alive():
            print_and_sleep(red(f"{enemy.name} is now in Hell."), 1)
            enemy_weapon = enemy.drop_weapon()
            if enemy_weapon is not None:
                if player.add_weapon(enemy_weapon):
                    print_and_sleep(cyan(f"{enemy_weapon.name} added to sack."), 1)
            player.gain_coins(enemy.drop_coins())
            player.gain_xp(enemy)
            event_logger.log_event(KillEvent())
            self.game_state.current_area.kill_current_enemy()
            return self.game_state
        enemy.attack(player)
        if not player.is_alive():
            player.lives -= 1
            event_logger.log_event(PlayerDeathEvent(player.lives))
        return self.game_state


class FleeSelectionBinding(SelectionBinding):
    def format(self):
        return f"Flee ({int(calculate_flee() * 100)}%)"


class Battle(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, top_level_prompt_callback=lambda gs: print(get_battle_status_view(gs)),
                         bindings=[
                             SelectionBinding('A', "Attack", Attack),
                             SelectionBinding('I', "Use Item", UseItem),
                             SelectionBinding('S', "Switch Weapon", EquipWeapon),
                             FleeSelectionBinding('F', "Flee (50%)", anonymous_component()(self._try_flee)),
                             SelectionBinding('P', "Perks", DisplayPerks)
                         ])
        self.player = self.game_state.player
        self.enemy = self.game_state.current_area.spawn_enemy()
        self.fled = False

    def play_theme(self):
        play_music(BATTLE_THEME)

    def can_exit(self):
        return self.fled or not (self.player.is_alive() and self.enemy.is_alive())

    def _try_flee(self):
        flee_chance = calculate_flee()
        if random.random() < flee_chance:
            event_logger.log_event(FleeEvent(self.enemy.name))
            self.fled = True
            self.game_state.current_area.reset_current_enemy()
        else:
            print(yellow("Couldn't escape!"))


class FightBoss(Battle):
    def run(self) -> GameState:
        print("TODO - Boss Fight")
        return self.game_state


class InGameBank(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, bindings=[
            SelectionBinding('W', 'Withdraw', self._make_withdrawal),
            SelectionBinding('Q', 'Leave', anonymous_component()(self._return))
        ], top_level_prompt_callback=display_bank_balance)
        self.leave_bank = False

    def _return(self):  # TODO stop duplicating this pattern
        print_and_sleep(blue("Very well..."), 1)
        self.leave_bank = True

    def can_exit(self):
        return self.leave_bank

    @staticmethod
    @anonymous_component(state_dependent=True)
    def _make_withdrawal(game_state: GameState):
        raw_amount = safe_input("\nHow much would you like to withdraw?")
        if raw_amount.isdigit():
            amount = int(raw_amount)
            if game_state.bank.make_withdrawal(amount):
                game_state.player.coins += amount
                event_logger.log_event(BankWithdrawalEvent(amount))
        else:
            print(yellow("Invalid choice."))


class Achievements(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, display_callback=display_player_achievements)


class DisplayPerks(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, display_callback=display_active_perks)


class Overview(TextDisplayingComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, display_callback=display_game_overview)
