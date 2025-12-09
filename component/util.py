from data.colors import blue as b, cyan as c, green as g, orange as o, purple as p, red as r, yellow as y, dim as d, \
    reset as rst
from model.game_state import GameState


# --- HP COLOR CODING ---
def p_color(player):
    # Player color (pc)
    p_ratio = player.hp / player.max_hp
    if p_ratio >= 0.7:
        pc = g
    elif p_ratio >= 0.3:
        pc = y
    else:
        pc = r

    return pc


def e_color(enemy):
    # Enemy color (ec)
    e_ratio = enemy.hp / enemy.max_hp
    if e_ratio >= 0.7:
        ec = g
    elif e_ratio >= 0.3:
        ec = y
    else:
        ec = r

    return ec


def get_player_status_view(game_state: GameState) -> str:
    player = game_state.player
    return f"\n{'|'.join([
        f"Area: {b}{game_state.current_area.name} {rst}{d}",
        f"{rst} Killed: {r}{game_state.current_area.enemies_killed} {rst}{d}",
        f"{rst} Wanted: {p}{game_state.wanted} {rst}{d}",
        f"{rst} Bounty: {p}{game_state.bounty} {rst}coins"])}\n{'|'.join([
        f"\n{o}{player.name}{rst} {d}-{rst} Level: {c}{player.lvl} {rst}{d}",
        f"{rst} XP: {c}{player.xp}/{player.xp_needed} {rst}{d}",
        f"{rst} HP: {rst}{p_color(player)}{player.hp}/{player.max_hp} {rst}{d}",
        f"{rst} Coins: {g}{player.coins} {rst}{d}",
        f"{rst} Lives: {y}{player.lives}{rst}\n"
    ])}"
