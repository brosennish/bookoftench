from typing import Callable, Any

from savethewench import event_logger
from savethewench.data.perks import WENCH_LOCATION, USED_SNEAKERS, NEW_SNEAKERS, CROWS_NEST
from savethewench.event_base import EventType
from .game_state import GameState
from savethewench.model.achievement import load_achievements
from savethewench.model.base import Combatant
from savethewench.model.enemy import Enemy
from savethewench.model.perk import load_perks, attach_perk, perk_is_active
from savethewench.model.player import Player
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


def display_coffee_header(game_state: GameState) -> None:
    player = game_state.player
    player_color = p_color(player.hp, player.max_hp)

    print_and_sleep(f"{dim(' | ').join([
        f"HP: {player_color(f"{player.hp}/{player.max_hp}")}",
        f"Coins: {green(f"{player.coins}")}",
        f"Lives: {yellow(f"{player.lives}")}\n"
        "\nMenu:"
        ])}")


def display_hospital_header(game_state: GameState) -> None:
    player = game_state.player
    print_and_sleep("Welcome to The Free Range Children's Hospital of Shebokken.")
    print_and_sleep(f"{dim(' | ').join([
        f"Illness: {yellow(f"{player.illness.name}")}",
        f"Cost: {orange(f"{player.illness.cost}")}",
        f"Coins: {green(f"{player.coins}")}",
        f"Chance of Success: {cyan(f"{int(player.illness.success_rate * 100)}%")}\n"
        ])}")


def get_player_status_view(game_state: GameState) -> str:
    player = game_state.player
    player_color = p_color(player.hp, player.max_hp)
    killed_remaining = [f"Killed: {red(f"{game_state.current_area.enemies_killed}")}"]
    if perk_is_active(CROWS_NEST):
        killed_remaining.append(f"Remaining: {yellow(f"{game_state.current_area.enemies_remaining}")}")

    player_status = (f"{dim(' | ').join([
            f"Area: {blue(game_state.current_area.name)}",
            *killed_remaining,
            f"Wanted: {purple(game_state.wanted)}",
            f"Bounty: {purple(f"{game_state.bounty} coins")}"])}"
                f"\n{dim(' | ').join([
                    f"\n{orange(player.name)} {dim('-')} Level: {cyan(f"{player.lvl}")}",
                    f"XP: {cyan(f"{player.xp}/{player.xp_needed}")}",
                    f"HP: {player_color(f"{player.hp}/{player.max_hp}")}",
                    f"Coins: {green(f"{player.coins}")}",
                    f"Lives: {yellow(f"{player.lives}")}"])}")

    if game_state.player.illness:
        illness_status = (f"{dim(' | ').join([
            f"\nIllness: {red(f"{game_state.player.illness.name}")}",
            f"Death Level: {red(f"{game_state.player.illness_death_lvl}")}",
        ])}\n")

        return "\n".join([
            player_status,
            illness_status,
        ])
    else:
        return player_status


def get_battle_status_view(game_state: GameState) -> str:
    player: Player = game_state.player
    enemy: Enemy = game_state.current_area.current_enemy

    def format_combatant_data(cmbt: Combatant, name_color) -> str:
        blind_turns = f"{cmbt.blind_turns} turn{'s' if cmbt.blind_turns > 1 else ''}"
        return (f"\n{name_color(cmbt.name)}"
                f"{red(f' (blinded {int(cmbt.blind_effect*100)}% for {blind_turns})') if cmbt.blind else ''}"
                f"{orange(' (wanted)') if game_state.is_wanted(cmbt) else ''} {dim('-')} "
                f"{p_color(cmbt.hp, cmbt.max_hp)(f"{cmbt.hp} HP")}"
                f"\n{cmbt.current_weapon.get_simple_format()}")

    return f"{format_combatant_data(player, orange)}\n{format_combatant_data(enemy, purple)}\n"


def display_bank_balance(game_state: GameState) -> None:
    print_and_sleep(f"{dim(' | ').join([
        f"Player: {green(f"{game_state.player.coins}")}",
        f"Bank: {green(f"{game_state.bank.balance}")}"])}\n")


def display_game_overview(game_state: GameState):
    player = game_state.player
    player_color = p_color(player.hp, player.max_hp)

    width = 18  # adjust if you want wider/narrower labels

    def display_stat(title: str, value: Any, value_color: Callable[[str], str]) -> None:
        print(f"{title:<{width}} {dim('|')} {value_color(value)}")

    display_stat("Current Level", player.lvl, cyan)
    display_stat("Current HP", player.hp, player_color)

    display_stat("Coins", player.coins, green)
    display_stat("Bank", game_state.bank.balance, green)
    display_stat("Deposits", event_logger.get_count(EventType.DEPOSIT), orange)
    display_stat("Withdrawals", event_logger.get_count(EventType.WITHDRAW), orange)
    display_stat("Interest Earned", game_state.bank.interest, green)

    display_stat("Casino Won", player.casino_won, green)
    display_stat("Casino Lost", player.casino_lost, red)

    display_stat("Hits", event_logger.get_count(EventType.HIT), cyan)
    display_stat("Misses", event_logger.get_count(EventType.MISS), cyan)
    display_stat("Critical Hits", event_logger.get_count(EventType.CRIT), cyan)

    display_stat("Enemies Killed", event_logger.get_count(EventType.KILL), red)
    display_stat("Bounties Claimed", event_logger.get_count(EventType.BOUNTY_COLLECTED), purple)

    display_stat("Areas Cleared", sum(1 for a in game_state.areas if a.enemies_remaining == 0), blue)
    display_stat("Bosses Defeated", sum(1 for a in game_state.areas if a.boss_defeated), red)

    display_stat("Items Purchased", event_logger.get_count(EventType.BUY_ITEM), cyan)
    display_stat("Items Used", event_logger.get_count(EventType.USE_ITEM), cyan)
    display_stat("Weapons Purchased", event_logger.get_count(EventType.BUY_WEAPON), cyan)
    display_stat("Perks Owned", event_logger.get_count(EventType.BUY_PERK), cyan)

    display_stat("Times Traveled", event_logger.get_count(EventType.TRAVEL), blue)


def display_player_achievements(_: GameState):
    achievements = [a for a in load_achievements() if a.active]
    if len(achievements) == 0:
        print_and_sleep(yellow("Your achievements are dry."), 1)
    else:
        print(f"Your Achievements:")
        for ach in sorted(achievements, key=lambda a: a.name):
            print(orange(f"\n{ach.name} | {ach.description}"))


def display_active_perks(game_state: GameState) -> None:
    active_perks = [p for p in load_perks() if p.active]
    if len(active_perks) == 0:
        print_and_sleep(yellow("Your perks are dry."), 1)
    else:
        print_and_sleep(f"Your Perks:")
        if perk_is_active(WENCH_LOCATION):
            print_and_sleep(f'Wench Location: {blue(game_state.wench_area.name)}')

        for perk in sorted(active_perks, key=lambda a: a.name):
            print_and_sleep(purple(f"{perk.name} | {perk.description}"))


def display_active_perk_count():
    print_and_sleep(f"Perks {dim(f"({len(load_perks(lambda p: p.active))})")}")


@attach_perk(USED_SNEAKERS, NEW_SNEAKERS, silent=True)
def calculate_flee() -> float:
    return 0.5
