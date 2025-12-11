import time as t
from typing import Callable

from savethewench.data.perks import WENCH_LOCATION
from savethewench.model import Enemy
from savethewench.model import GameState
from savethewench.model import Player
from savethewench.model.perk import load_perks
from savethewench.ui import blue, cyan, green, orange, purple, red, yellow, dim


# --- HP COLOR CODING ---
def p_color(hp: int, max_hp: int) -> Callable[[str], str]:
    # Player color (pc)
    p_ratio = hp / max_hp
    if p_ratio >= 0.7:
        return green
    elif p_ratio >= 0.3:
        return yellow
    else:
        return red


def get_player_status_view(game_state: GameState) -> str:
    player = game_state.player
    player_color = p_color(player.hp, player.max_hp)
    return (f"\n{dim(' | ').join([
        f"Area: {blue(game_state.current_area.name)}",
        f"Killed: {red(f"{game_state.current_area.enemies_killed}")}",
        f"Wanted: {purple(game_state.wanted)}",
        f"Bounty: {purple(f"{game_state.bounty} coins")}"])}"
            f"\n{dim(' | ').join([
                f"\n{orange(player.name)} {dim('-')} Level: {cyan(f"{player.lvl}")}",
                f"XP: {cyan(f"{player.xp}/{player.xp_needed}")}",
                f"HP: {player_color(f"{player.hp}/{player.max_hp}")}",
                f"Coins: {green(f"{player.coins}")}",
                f"Lives: {yellow(f"{player.lives}")}\n"
            ])}")


def get_battle_status_view(game_state: GameState) -> str:
    player: Player = game_state.player
    enemy: Enemy = game_state.current_area.current_enemy

    def format_uses(weapon) -> str:
        if weapon.uses == -1:
            return cyan('∞')
        elif weapon.uses == 1:
            return red(f"{weapon.uses}")
        elif weapon.uses in (2, 3):
            return yellow(f"{weapon.uses}")
        else:
            return f"{weapon.uses}"

    def format_combatant_data(name, name_color, combatant_color, hp, weapon, uses_left) -> str:
        return (f"\n{name_color(name)} {dim('-')} {combatant_color(f"{hp} HP")}"
                f"\n{cyan(weapon.name)}"
                f"\n{dim(' | ').join([
                    f"{dim("Damage:")} {red(f"{weapon.damage}")}"
                    f"Accuracy: {yellow(f"{weapon.accuracy}")}"
                    f"Uses: {uses_left}"
                ])}\n")

    return (f"{format_combatant_data(player.name, orange, p_color(player.hp, player.max_hp),
                                     player.hp, player.current_weapon, format_uses(player.current_weapon))}"
            f"{format_combatant_data(enemy.name, purple, p_color(enemy.hp, enemy.max_hp),
                                     enemy.hp, enemy.current_weapon, format_uses(enemy.current_weapon))}")


def display_bank_balance(game_state: GameState) -> None:
    player: Player = game_state.player
    if not player.bank:
        print(yellow("Your bank account is dry."))
        t.sleep(1)
    else:
        print(f"\nPlayer coins: {green(f"{player.coins}")} coins\n\nBank coins: {green(f"{player.bank}")} coins")


def display_player_perks(game_state: GameState) -> None:
    player: Player = game_state.player
    if not player.perks:
        print(yellow("Your perks are dry."))
        t.sleep(1)
    else:
        print(f"\nYour Perks:")
        if WENCH_LOCATION in player.perks:
            print(f'\nWench Location: {blue(game_state.wench_area)}')

        for perk in load_perks(sorted(player.perks)):
            print(purple(f"\n{perk.name} | {perk.description}"))
        print()
