import time as t

from data.colors import blue as b, cyan as c, green as g, orange as o, purple as p, red as r, yellow as y, dim as d, \
    reset as rst
from data.perks import WENCH_LOCATION
from model.enemy import Enemy
from model.game_state import GameState
from model.perk import load_perks
from model.player import Player


# --- HP COLOR CODING ---
def p_color(hp: int, max_hp: int) -> int:
    # Player color (pc)
    p_ratio = hp / max_hp
    if p_ratio >= 0.7:
        pc = g
    elif p_ratio >= 0.3:
        pc = y
    else:
        pc = r

    return pc


def get_player_status_view(game_state: GameState) -> str:
    player = game_state.player
    return f"\n{'|'.join([
        f"Area: {b}{game_state.current_area.name} {rst}{d}",
        f"{rst} Killed: {r}{game_state.current_area.enemies_killed} {rst}{d}",
        f"{rst} Wanted: {p}{game_state.wanted} {rst}{d}",
        f"{rst} Bounty: {p}{game_state.bounty} {rst}coins"])}\n{'|'.join([
        f"\n{o}{player.name}{rst} {d}-{rst} Level: {c}{player.lvl} {rst}{d}",
        f"{rst} XP: {c}{player.xp}/{player.xp_needed} {rst}{d}",
        f"{rst} HP: {rst}{p_color(player.hp, player.max_hp)}{player.hp}/{player.max_hp} {rst}{d}",
        f"{rst} Coins: {g}{player.coins} {rst}{d}",
        f"{rst} Lives: {y}{player.lives}{rst}\n"
    ])}"


def get_battle_status_view(game_state: GameState) -> str:
    player: Player = game_state.player
    enemy: Enemy = game_state.current_area.current_enemy

    def format_uses(weapon) -> str:
        if weapon.uses == -1:
            return f"{c}∞{rst}"
        elif weapon.uses == 1:
            return f"{r}{weapon.uses}{rst}"
        elif weapon.uses in (2, 3):
            return f"{y}{weapon.uses}{rst}"
        else:
            return f"{weapon.uses}{rst}"

    def format_combatant_data(name, name_color, combatant_color, hp, weapon, uses_left) -> str:
        return (f"\n{name_color}{name}{rst} {d}-{rst} {combatant_color}{hp} HP {rst}"
                f"\n{c}{weapon.name}{rst}"
                f"\n{'|'.join([
                    f"{d}Damage: {rst}{r}{weapon.damage}{rst} {d}"
                    f" Accuracy: {rst}{y}{weapon.accuracy}{rst} {d}"
                    f" Uses: {rst}{uses_left}{rst}"
                ])}\n")

    return (f"{format_combatant_data(player.name, o, p_color(player.hp, player.max_hp),
                                     player.hp, player.current_weapon, format_uses(player.current_weapon))}"
            f"{format_combatant_data(enemy.name, p, p_color(enemy.hp, enemy.max_hp),
                                     enemy.hp, enemy.current_weapon, format_uses(enemy.current_weapon))}")


def display_bank_balance(game_state: GameState) -> None:
    player: Player = game_state.player
    if not player.bank:
        print(f"{y}Your bank account is dry.{rst}")
        t.sleep(1)
    else:
        print(f"\nPlayer coins: {g}{player.coins}{rst} coins\n\nBank coins: {g}{player.bank}{rst} coins")


def display_player_perks(game_state: GameState) -> None:
    player: Player = game_state.player
    if not player.perks:
        print(f"{y}Your perks are dry.{rst}")
        t.sleep(1)
    else:
        print(f"\nYour Perks:")
        if WENCH_LOCATION in player.perks:
            print(f'\nWench Location: {b}{game_state.wench_area}{rst}')

        for perk in load_perks(sorted(player.perks)):
            print(f"\n{p}{perk.name} | {perk.description}{rst}")
        print()
