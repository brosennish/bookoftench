import time as t
from typing import Callable, Any

from savethewench import event_logger
from savethewench.data.perks import WENCH_LOCATION
from savethewench.event_base import EventType
from savethewench.model import Enemy
from savethewench.model import GameState
from savethewench.model import Player
from savethewench.model.perk import load_perks
from savethewench.ui import blue, cyan, green, orange, purple, red, yellow, dim
from savethewench.util import print_and_sleep


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


def display_game_overview(game_state: GameState):
    player = game_state.player
    player_color = p_color(player.hp, player.max_hp)

    width = 18  # adjust if you want wider/narrower labels

    def display_stat(title: str, value: Any, value_color: Callable[[str], str]) -> None:
        print(f"{title:<{width}} {dim('|')} {value_color(value)}")

    display_stat("Current Level", player.lvl, cyan)
    display_stat("Current HP", player.hp, player_color)

    display_stat("Coins", player.coins, green)
    display_stat("Bank", player.bank, green)
    display_stat("Deposits", event_logger.get_count(EventType.DEPOSIT), orange)
    display_stat("Withdrawals", event_logger.get_count(EventType.WITHDRAW), orange)
    display_stat("Interest Earned", player.interest, green)

    display_stat("Casino Won", player.casino_won, green)
    display_stat("Casino Lost", player.casino_lost, red)

    display_stat("Hits", event_logger.get_count(EventType.HIT), cyan)
    display_stat("Misses", event_logger.get_count(EventType.MISS), cyan)
    display_stat("Critical Hits", event_logger.get_count(EventType.CRIT), cyan)

    display_stat("Enemies Killed", event_logger.get_count(EventType.KILL), red)
    display_stat("Bounties Claimed", event_logger.get_count(EventType.BOUNTY_COLLECTED), purple)

    display_stat("Areas Cleared", sum(1 for a in game_state.areas if a.enemy_count == 0), blue)
    display_stat("Bosses Defeated", sum(1 for a in game_state.areas if a.boss_defeated), red)

    display_stat("Items Purchased", event_logger.get_count(EventType.BUY_ITEM), cyan)
    display_stat("Items Used", event_logger.get_count(EventType.USE_ITEM), cyan)
    display_stat("Weapons Purchased", event_logger.get_count(EventType.BUY_WEAPON), cyan)
    display_stat("Perks Owned", event_logger.get_count(EventType.BUY_PERK), cyan)

    display_stat("Times Traveled", event_logger.get_count(EventType.TRAVEL), blue)


def display_player_achievements(game_state: GameState):
    player: Player = game_state.player
    if not player.achievements:
        print_and_sleep(yellow("Your achievements are dry."), 1)
    else:
        print(f"Your Achievements:")
        for ach in sorted(player.achievements, key=lambda a: a.name):
            print(orange(f"\n{ach.name} | {ach.description}"))


def display_player_perks(game_state: GameState) -> None:
    player: Player = game_state.player
    if not player.perks:
        print_and_sleep(yellow("Your perks are dry."), 1)
    else:
        print(f"\nYour Perks:")
        if WENCH_LOCATION in player.perks:
            print(f'\nWench Location: {blue(game_state.wench_area)}')

        for perk in load_perks(sorted(player.perks)):
            print(purple(f"\n{perk.name} | {perk.description}"))
