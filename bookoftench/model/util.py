from typing import Callable, Any

from bookoftench import event_logger
from bookoftench.data.perks import WENCH_LOCATION, USED_SNEAKERS, NEW_SNEAKERS, CROWS_NEST
from bookoftench.event_base import EventType
from bookoftench.model.achievement import load_achievements
from bookoftench.model.base import Combatant
from bookoftench.model.enemy import Enemy
from bookoftench.model.perk import load_perks, perk_is_active, attach_perks
from bookoftench.model.player import Player
from bookoftench.ui import blue, cyan, green, orange, purple, red, yellow, dim, white
from bookoftench.util import print_and_sleep
from .discoverable import rarity_color
from .game_state import GameState
from ..data.areas import CAVE, CITY, FOREST, SWAMP
from ..data.enemies import CONTAGIOUS, BOSS, SPECIAL_BOSS, FINAL_BOSS, NORMAL
from ..data.enviroment import DAY
from ..data.fish import AGITATED, SPOOKED, CALM, SHALLOWS, BAY, OCEAN, Fish_Species, MALE, FEMALE, COMMON, UNCOMMON, \
    RARE, LEGENDARY
from ..data.fishing_areas import WET_SEASON, DRY_SEASON


# ================================================================================================

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

# ================================================================================================

def display_coffee_header(game_state: GameState) -> None:
    player = game_state.player
    player_color = p_color(player.hp, player.max_hp)

    print_and_sleep(f"{dim(' | ').join([
        f"HP: {player_color(f"{player.hp}/{player.max_hp}")}",
        f"Coins: {green(f"{player.coins}")}",
        f"Lives: {yellow(f"{player.lives}")}\n"
        "\nMenu:"
    ])}")

# ================================================================================================

def get_fish_stamina_label(game_state: GameState) -> str:
    fish = game_state.current_fish
    ratio = fish.stamina / fish.max_stamina

    if ratio >= 0.75:
        return "Strong"
    elif ratio >= 0.50:
        return "Tiring"
    elif ratio >= 0.25:
        return "Weary"
    else:
        return "Exhausted"

# ================================================================================================

def display_fishmonger_header(game_state: GameState) -> None:
    player = game_state.player
    season = game_state.season
    season_color = blue if season == WET_SEASON else yellow

    top_row = f"{season_color(f"{season}")}"

    second_row = dim(' | ').join([
        f"Lvl: {cyan(f"{player.fishing_lvl}")}",
        f"XP: {cyan(f"{player.fishing_xp}/{player.fishing_xp_needed}")}",
        f"Rod: {cyan(f"{player.rod_lvl}")}",
        f"Coins: {green(f"{player.coins}")}",
    ])

    print_and_sleep("\n".join([
        top_row,
        second_row,
    ]))

# ================================================================================================

def display_tackle_box_header(game_state: GameState) -> None:
    player = game_state.player
    bait = player.current_bait
    if player.current_bait:
        bait_name = bait.name
        casts = bait.casts
        b_color = cyan
    else:
        bait_name = "None"
        casts = "N/A"
        b_color = yellow

    print_and_sleep(
        f"Current: {b_color(f"{bait_name}")} | Casts: {b_color(f"{casts}")}"
    )

# ================================================================================================

def display_fishing_item_box_header(game_state: GameState) -> None:
    player = game_state.player
    active = player.active_fishing_items

    if not active:
        print_and_sleep("Active: None")
        return

    effects = []

    for item in active:
        if item.spit_hook_prevention:
            effects.append(
                f"{blue(item.name)} {purple(f'({item.turns})')}"
            )
        elif item.rage_reduction:
            effects.append(
                f"{red(item.name)} {purple(f'({item.turns})')}"
            )
        elif item.stamina_reduction:
            effects.append(
                f"{yellow(item.name)} {purple(f'({item.turns})')}"
            )
        elif item.speed_reduction:
            effects.append(
                f"{cyan(item.name)} {purple(f'({item.turns})')}"
            )
        elif item.strength_reduction:
            effects.append(
                f"{orange(item.name)} {purple(f'({item.turns})')}"
            )

    print_and_sleep(
        f"Active: {dim(' | ').join(effects)}"
    )

# ================================================================================================

def display_fish_log_header(game_state: GameState) -> None:
    player = game_state.player

    print_and_sleep(f"* {player.name}'s Fishing Log *")

# ================================================================================================

def display_compendium_header(game_state: GameState) -> None:
    player = game_state.player

    print_and_sleep(f"* Compendium *")

# ================================================================================================

def display_bait_shop_header(game_state: GameState) -> None:
    player = game_state.player
    season = game_state.season
    season_color = blue if season == WET_SEASON else yellow
    tod = game_state.time_of_day
    tod_display = "Day" if tod == DAY else "Night"
    moon = game_state.moon

    print_and_sleep(f"{dim(' | ').join([
        f"{season_color(f"{season}")}",
        f"{yellow(tod_display) if tod == DAY else purple(tod_display)}",
        f"{moon} Moon",
        f"Coins: {green(f"{player.coins}")}",
    ])}")

# ================================================================================================

def fishing_state_color(game_state: GameState) -> Callable[[str], str]:
    fish = game_state.current_fish

    if fish.state == CALM:
        return cyan
    elif fish.state == AGITATED:
        return yellow
    elif fish.state == SPOOKED:
        return purple
    else:
        return red

def fishing_distance_color(game_state: GameState) -> Callable[[str], str]:
    fishing_area = game_state.current_fishing_area
    remaining = fishing_area.escape_distance
    ratio = remaining / fishing_area.escape_distance

    if ratio < 0.15:
        return red
    elif ratio < 0.35:
        return orange
    elif ratio < 0.60:
        return yellow
    else:
        return green

# ================================================================================================

def display_fishing_battle_header(game_state: GameState) -> None:
    fish = game_state.current_fish
    player = game_state.player
    fishing_area = game_state.current_fishing_area

    if fish is None:
        return

    name = fish.name if fish.species_known else "Unknown Creature"
    stamina_percentage = round((fish.stamina / fish.max_stamina) * 100)

    state_color = fishing_state_color(game_state)
    distance_color = fishing_distance_color(game_state)

    top_row = dim(' | ').join([
        blue(name),
        state_color(fish.state),
    ])

    second_row = dim(' | ').join([
        f"Distance: {distance_color(f'{fish.distance}/{fishing_area.escape_distance}')}",
        f"Stamina: {yellow(f'{stamina_percentage}%')}",
        f"Rage: {red(f'{fish.rage}%')}",
    ])

    rows = [top_row, second_row]

    if player.active_fishing_items:
        active_items = []

        for item in player.active_fishing_items:
            if item.spit_hook_prevention:
                item_color = blue
            elif item.rage_reduction:
                item_color = red
            elif item.stamina_reduction:
                item_color = yellow
            elif item.speed_reduction:
                item_color = cyan
            elif item.strength_reduction:
                item_color = orange
            else:
                item_color = white

            active_items.append(
                f"{item_color(item.name)} {purple(f'({item.turns})')}"
            )

        rows.append(dim(' | ').join(active_items))

    print_and_sleep("\n".join(rows))

# ================================================================================================

# --- CASTS REMAINING COLOR CODING ---
def c_color(casts: int) -> Callable[[str], str]:
    if casts == 1:
        return red
    elif casts <= 3:
        return yellow
    else:
        return green

def display_boat_header(game_state: GameState):
    player = game_state.player
    tod = game_state.time_of_day
    tod_display = "Day" if tod == DAY else "Night"
    moon = game_state.moon
    season = game_state.season
    season_color = blue if season == WET_SEASON else yellow
    bait = player.current_bait.name if player.current_bait else "None"
    bait_color = yellow if bait == "None" else cyan
    casts = game_state.current_fishing_area.casts
    casts_color = c_color(casts)
    if game_state.all_fish:
        pref_text = "All"
    else:
        pref_text = "New"

    # --- top row ---
    top_row = f"{dim(' | ').join([
        f"{season_color(f"{season}")}",
        f"{blue(f"{game_state.current_fishing_area.name}")}",
        f"{yellow(tod_display) if tod == DAY else purple(tod_display)}",
        f"{moon} Moon",
        f"{purple(pref_text)}",
    ])}\n"

    # --- bottom row ---
    bottom_row = f"{dim(' | ').join([
        f"Lvl: {cyan(f"{player.fishing_lvl}")}",
        f"XP: {cyan(f"{player.fishing_xp}/{player.fishing_xp_needed}")}",  
        f"Bait: {bait_color(f"{bait}")}",
        f"Casts: {casts_color(f"{game_state.current_fishing_area.casts}")}",
    ])}"

    print_and_sleep("\n".join([
        top_row,
        bottom_row,
    ]))

# ================================================================================================

def display_blacksmith_header(game_state: GameState) -> None:
    player = game_state.player

    print_and_sleep(f"{dim(' | ').join([
        f"Coins: {green(f"{player.coins}")}",
        f"Melee: {orange(f"125")}",
        f"Ranged: {orange(f"150")}",
        f"Special (∞): {orange(f"400")}\n",
    ])}\n")

# ================================================================================================

def display_occultist_header(game_state: GameState) -> None:
    player = game_state.player

    print_and_sleep(f"{dim(' | ').join([
        f"Coins: {green(f"{player.coins}")}",
        f"Lives: {yellow(f"{player.lives}")}\n",
    ])}")

# ================================================================================================

def display_wizard_header(game_state: GameState) -> None:
    player = game_state.player

    print_and_sleep(f"{dim(' | ').join([
        f"Coins: {green(f"{player.coins}")}",
        f"Items: {cyan(f"{len(player.items)}/{player.max_items}")}",
        f"Weapons: {cyan(f"{len(player.get_weapons())}/{player.max_weapons}")}"
    ])}\n")

# ================================================================================================

def display_shaman_header(game_state: GameState) -> None:
    player = game_state.player
    player_color = p_color(player.hp, player.max_hp)

    player_status = dim(' | ').join([
        f"{orange(player.name)} {dim('-')} Level: {cyan(player.lvl)}",
        f"HP: {player_color(f'{player.hp}/{player.max_hp}')}",
        f"Coins: {green(player.coins)}",
        f"Lives: {yellow(player.lives)}",
    ])

    status_line_two = dim(' | ').join([
        f"\nIllness: {yellow(player.illness.name) if player.illness else "None"}",
        f"Death Level: {red(player.illness_death_lvl) if player.illness_death_lvl else "N/A"}",
        f"Blind Turns: {red(player.blind_turns) if player.blind_turns else "0"}",
    ])

    print(player_status, "\n", status_line_two, "\n")

# ================================================================================================

def display_hospital_header(game_state: GameState) -> None:
    player = game_state.player

    print_and_sleep(f"{blue(f'Welcome to The Free Range Children\'s Hospital of Shebokken.')}", 2)
    print_and_sleep(f"{dim(' | ').join([
        f"Illness: {yellow(f"{player.illness.name}")}",
        f"Cost: {orange(f"{player.illness.cost}")}",
        f"Coins: {green(f"{player.coins}")}",
    ])}")
    print_and_sleep(f"Chance of Success: {cyan(f'{int(player.illness.success_rate * 100)}%')}\n")

# ================================================================================================

def display_shop_header(game_state: GameState):
    player = game_state.player
    player_color = p_color(player.hp, player.max_hp)

    print_and_sleep(
        dim(" | ").join([
            f"Coins: {green(player.coins)}",
            f"HP: {player_color(f'{player.hp}/{player.max_hp}')}",
            f"Lives: {yellow(player.lives)}",
        ])
    )

# ================================================================================================

# --- standard view ---
def get_player_status_view_1(game_state: GameState) -> str:
    player = game_state.player
    player_color = p_color(player.hp, player.max_hp)

    tod = game_state.time_of_day
    tod_display = "Day" if tod == DAY else "Night"
    moon = game_state.moon

    killed_remaining = [
        f"Killed: {red(game_state.current_area.enemies_killed)}"
    ]

    if perk_is_active(CROWS_NEST):
        killed_remaining.append(
            f"Left: {yellow(game_state.current_area.enemies_remaining)}"
        )

    hp_display = (
        f"HP: {player_color(f'{player.hp}/{player.max_hp}' if player.hp != player.max_hp else player.hp)}"
    )

    player_status = (
        f"{dim(' | ').join([
            blue(game_state.current_area.name),
            *killed_remaining,
            yellow(tod_display) if tod == DAY else purple(tod_display),
            f'{moon} Moon',
            f'Wanted: {purple(game_state.wanted)}',
            f'Bounty: {purple(game_state.bounty)}',
        ])}"
        f"\n"
        f"{dim(' | ').join([
            f'\n{orange(player.name)} {dim("-")} Lvl: {cyan(player.lvl)}',
            f'XP: {cyan(f"{player.xp}/{player.xp_needed}")}',
            hp_display,
            f'Coins: {green(player.coins)}',
            f'Lives: {yellow(player.lives)}',
        ])}"
    )

    if player.illness:
        illness_status = dim(' | ').join([
            f"\nIllness: {yellow(player.illness.name)}",
            f"Death Lvl: {red(player.illness_death_lvl)}",
        ])

        return "\n".join([
            player_status,
            illness_status,
        ])

    return player_status

# ================================================================================================

# --- detailed view ---
def get_player_status_view_2(game_state: GameState) -> str:
    player = game_state.player
    player_color = p_color(player.hp, player.max_hp)

    tod = game_state.time_of_day
    moon = game_state.moon
    season = game_state.season

    hp_display = (
        f"HP: {player_color(f'{player.hp}/{player.max_hp}' if player.hp != player.max_hp else player.hp)}"
    )

    player_status = (
        f"{dim(' | ').join([
            blue(game_state.current_area.name),
            yellow(season) if season == DRY_SEASON else blue(season),
            yellow(tod) if tod == DAY else purple(tod),
            f'{moon} Moon',
            f'Wanted: {purple(game_state.wanted)}',
            f'Bounty: {purple(game_state.bounty)}',
        ])}"
        f"\n"
        f"{dim(' | ').join([
            f'\n{orange(player.name)} {dim("-")} Lvl: {cyan(player.lvl)}',
            f'XP: {cyan(f"{player.xp}/{player.xp_needed}")}',
            hp_display,
            f'Coins: {green(player.coins)}',
            f'Lives: {yellow(player.lives)}',
            f'Str: {red(player.strength)}',
            f'Acc: {yellow(player.acc)}',
            f'Luck: {purple(player.luck)}',
        ])}"
    )

    if player.illness:
        illness_status = dim(' | ').join([
            f"\nIllness: {yellow(player.illness.name)}",
            f"Death Lvl: {red(player.illness_death_lvl)}",
        ])

        return "\n".join([
            player_status,
            illness_status,
        ])

    return player_status

# ================================================================================================

# --- simple view ---
def get_player_status_view_3(game_state: GameState) -> str:
    player = game_state.player
    player_color = p_color(player.hp, player.max_hp)

    tod = game_state.time_of_day
    moon = game_state.moon
    season = game_state.season

    hp_display = (
        f"HP: {player_color(f'{player.hp}/{player.max_hp}' if player.hp != player.max_hp else player.hp)}"
    )

    player_status = (
        f"{dim(' | ').join([
            blue(game_state.current_area.name),
            yellow(season) if season == DRY_SEASON else blue(season),
            yellow(tod) if tod == DAY else purple(tod),
            f'{moon} Moon',
            f'{purple(game_state.wanted)}',
            f'{purple(game_state.bounty)}',
        ])}"
        f"\n"
        f"{dim(' | ').join([
            f'\n{orange(player.name)} {dim("-")} Lvl: {cyan(player.lvl)}',
            f'XP: {cyan(f"{player.xp}/{player.xp_needed}")}',
            hp_display,
            f'Coins: {green(player.coins)}',
            f'Lives: {yellow(player.lives)}',
        ])}"
    )

    if player.illness:
        illness_status = dim(' | ').join([
            f"\nIllness: {yellow(player.illness.name)}",
            f"Death Lvl: {red(player.illness_death_lvl)}",
        ])

        return "\n".join([
            player_status,
            illness_status,
        ])

    return player_status

# ================================================================================================

# --- fishing view ---
def get_player_status_view_4(game_state: GameState) -> str:
    player = game_state.player
    player_color = p_color(player.hp, player.max_hp)

    tod = game_state.time_of_day
    moon = game_state.moon
    season = game_state.season

    player_status = (
        f"{dim(' | ').join([
            blue(game_state.current_area.name),
            yellow(season) if season == DRY_SEASON else blue(season),
            yellow(tod) if tod == DAY else purple(tod),
            f'{moon} Moon',
        ])}"
        f"\n"
        f"{dim(' | ').join([
            f'\n{orange(player.name)} {dim("-")} Fishing Lvl: {cyan(player.fishing_lvl)}',
            f'XP: {cyan(f"{player.fishing_xp}/{player.fishing_xp_needed}")}',
            f'Rod: {orange(player.rod_lvl)}',
            f'Caught: {blue(len(player.caught_fish))}',
            f'Bait: {cyan(sum(i.casts for i in player.tackle_box.values()))}',
            f'Items: {purple(sum(i.count for i in player.fishing_item_box.values()))}'
        ])}"
    )

    if player.illness:
        illness_status = dim(' | ').join([
            f"\nIllness: {yellow(player.illness.name)}",
            f"Death Lvl: {red(player.illness_death_lvl)}",
        ])

        return "\n".join([
            player_status,
            illness_status,
        ])

    return player_status

# ================================================================================================

def get_battle_status_view(game_state: GameState) -> str:
    player: Player = game_state.player
    enemy: Enemy = game_state.current_area.current_enemy
    enemy_name_color = red if enemy.type in [SPECIAL_BOSS, BOSS] else purple

    def format_combatant_data(cmbt: Combatant, name_color) -> str:
        blind_turns = f"{cmbt.blind_turns} turn{'s' if cmbt.blind_turns > 1 else ''}"
        return (f"\n{name_color(cmbt.name)}"
                f"{red(f' (blinded {int(cmbt.blind_effect * 100)}% for {blind_turns})') if cmbt.blind else ''}"
                f"{red(f' (2x)') if cmbt.double_damage_active else ''}"
                f"{red(f' (crit)') if cmbt.crit_active else ''}"
                f"{orange(' (wanted)') if game_state.is_wanted(cmbt) else ''} {dim('-')} "
                f"{p_color(cmbt.hp, cmbt.max_hp)(f"{cmbt.hp} HP")}"
                f"\n{cmbt.current_weapon.get_complete_format(cmbt.strength, cmbt.acc)}")

    return f"{format_combatant_data(player, orange)}\n{format_combatant_data(enemy, enemy_name_color)}\n"

# ================================================================================================

def display_bank_balance(game_state: GameState) -> None:
    print_and_sleep(f"{dim(' | ').join([
        f"Player: {green(f"{game_state.player.coins}")}",
        f"Bank: {green(f"{game_state.bank.balance}")}"])}")

# ================================================================================================

def display_player_attributes(game_state: GameState) -> None:
    player: Player = game_state.player

    print_and_sleep(f"\n{dim('Strength |')} {red(round(player.strength, 2))}"
        f"\n{dim('Accuracy |')} {yellow(round(player.acc, 2))}"
        f"\n{dim('Luck     |')} {purple(round(player.luck, 3))}")

# ================================================================================================

def display_game_stats(game_state: GameState) -> None:
    player = game_state.player
    player_build = player.build

    width = 18  # adjust if you want wider/narrower labels

    def display_stat(title: str, value: Any, value_color: Callable[[str], str]) -> None:
        print(f"{title:<{width}} {(white(dim('|')))} {value_color(value)}")

    display_stat("Name", str(player.name), cyan)
    display_stat("Build", str(player_build.name), orange)
    display_stat("Level", player.lvl, cyan)
    display_stat("Strength", player.strength, red)
    display_stat("Accuracy", player.acc, yellow)
    display_stat("Luck", player.luck, green)
    display_stat("Perks", len([p for p in load_perks() if p.active]), purple)
    display_stat("Achievements", len([a for a in load_achievements() if a.active]), orange)
    display_stat("Deaths", event_logger.get_count(EventType.PLAYER_DEATH), red)

    display_stat("Coins", player.coins, green)
    display_stat("Bank Balance", game_state.bank.balance, green)
    display_stat("Interest Earned", game_state.bank.interest, green)

    display_stat("Casino Won", player.casino_won, green)
    display_stat("Casino Lost", player.casino_lost, red)

    display_stat("Hits", event_logger.get_count(EventType.HIT), red)
    display_stat("Misses", event_logger.get_count(EventType.MISS), blue)
    display_stat("Critical Hits", event_logger.get_count(EventType.CRIT), red)
    display_stat("Flees", event_logger.get_count(EventType.FLEE), cyan)
    display_stat("Failed Flees", event_logger.get_count(EventType.FAILED_FLEE), yellow)

    display_stat("Enemies Killed", event_logger.get_count(EventType.KILL), red)
    display_stat("Bounties Claimed", event_logger.get_count(EventType.BOUNTY_COLLECTED), purple)
    display_stat("Shoplifts", event_logger.get_count(EventType.STEAL), cyan)
    display_stat("Sum of Bribes", player.sum_of_bribes, green)
    display_stat("Police Brutalities", event_logger.get_count(EventType.OFFICER_UNPAID), red)

    display_stat("Areas Cleared", sum(1 for a in game_state.areas if a.enemies_remaining == 0), blue)
    display_stat("Bosses Defeated", len([a for a in game_state.liberated_enemies if a.type in
                                        [SPECIAL_BOSS, BOSS, FINAL_BOSS]]), red)

    display_stat("Coffees Purchased", event_logger.get_count(EventType.COFFEE_EVENT), green)

    display_stat("Common Finds", event_logger.get_count(EventType.DISCOVERY_COMMON), yellow)
    display_stat("Uncommon Finds", event_logger.get_count(EventType.DISCOVERY_UNCOMMON), green)
    display_stat("Rare Finds", event_logger.get_count(EventType.DISCOVERY_RARE), blue)
    display_stat("Legendary Finds", event_logger.get_count(EventType.DISCOVERY_LEGENDARY), orange)
    display_stat("Mythic Finds", event_logger.get_count(EventType.DISCOVERY_MYTHIC), purple)

    display_stat("Times Traveled", event_logger.get_count(EventType.TRAVEL), blue)

# ================================================================================================

def display_player_achievements(_: GameState) -> None:
    achievements = [a for a in load_achievements() if a.active]
    if len(achievements) == 0:
        print_and_sleep(yellow("Your achievements are dry."), 1)
    else:
        print(f"Your Achievements:")
        for ach in sorted(achievements, key=lambda a: a.name):
            print(orange(f"\n{ach.name} | {ach.description}"))

# ================================================================================================

def display_active_perks(game_state: GameState) -> None:
    active_perks = sorted(
        [p for p in load_perks() if p.active],
        key=lambda p: p.name.lower()
    )

    if not active_perks:
        print_and_sleep(yellow("Your perks are dry."), 1)
        return

    print_and_sleep("Your Perks:\n")

    for perk in active_perks:
        print_and_sleep(purple(perk.name))
        print_and_sleep(dim(perk.description))
        print()

    if perk_is_active(WENCH_LOCATION):
        print_and_sleep(f"Wench Location: {blue(game_state.wench_area.name)}")

# ================================================================================================

def display_encountered(game_state: GameState) -> None:
    encountered = game_state.encountered_enemies
    if not encountered:
        print_and_sleep(yellow("Go find some enemies fool."), 1)
        return
    else:
        cave_encounters = [i for i in encountered if i["area"] == CAVE]
        city_encounters = [i for i in encountered if i["area"] == CITY]
        forest_encounters = [i for i in encountered if i["area"] == FOREST]
        swamp_encounters = [i for i in encountered if i["area"] == SWAMP]

    print_and_sleep(blue("Cave"))
    for i in cave_encounters:
        enemy = i["enemy"]
        display_encountered_enemy(enemy)

    print_and_sleep(blue("City"))
    for i in city_encounters:
        enemy = i["enemy"]
        display_encountered_enemy(enemy)

    print_and_sleep(blue("Forest"))
    for i in forest_encounters:
        enemy = i["enemy"]
        display_encountered_enemy(enemy)

    print_and_sleep(blue("Swamp"))
    for i in swamp_encounters:
        enemy = i["enemy"]
        display_encountered_enemy(enemy)

# ================================================================================================

def display_encountered_enemy(enemy):
    color = purple if enemy.type == NORMAL else red
    print_and_sleep(f"{color(f'{enemy.name}')}")

# ================================================================================================

def display_liberated(game_state: GameState) -> None:
    liberated = game_state.liberated_enemies
    pipe = dim(" | ")

    if liberated:
        for i in liberated:
            color = orange if i.type in [BOSS, SPECIAL_BOSS] else purple
            print_and_sleep(f"{color(f'{i.name}')}"
                f"\n{green(f'{i.max_hp}{white(f'{pipe}')}')}"
                f"{red(f'{round(i.strength, 2)}{white(f'{pipe}')}')}"
                f"{yellow(f'{round(i.acc, 2)}{white(f'{pipe}')}')}"
                f"{purple(f'{i.trait.name if i.trait else ''}')}\n")
    else:
        print_and_sleep(yellow("Go liberate some enemies fool."), 1)

# ================================================================================================

def display_discoveries(game_state: GameState) -> None:
    discoveries = game_state.discoveries

    if discoveries:
        abc = sorted(discoveries, key=lambda a: a.name)
        for i in abc:
            color = rarity_color(i.rarity)
            print_and_sleep(f"{color(f'{i.name}')}"
                f"\n{color(f'{i.desc}')}"
                f"\nCount: {i.count}")
    else:
        print_and_sleep(yellow("Go make some discoveries fool."), 1)

# ================================================================================================

def get_battle_info_view(game_state: GameState) -> str:
    player: Player = game_state.player
    enemy: Enemy = game_state.current_area.current_enemy
    tod = game_state.time_of_day
    moon = game_state.moon

    def format_world_data() -> str:
        color = yellow if tod == DAY else purple
        word = "Day" if tod == DAY else "Night"
        return f"\n{color(word)} {dim('|')} {moon} Moon"


    def format_combatant_data(cmbt: Player | Enemy, name_color) -> str:
        if cmbt.trait in ['', None]:
            return (f"\n{name_color(cmbt.name)}"
                    f"\n{dim('Strength |')} {red(round(cmbt.strength, 2))}"
                    f"\n{dim('Accuracy |')} {yellow(round(cmbt.acc, 2))}"
                    f"\n{dim('Coins    |')} {green(cmbt.coins)}")
        elif cmbt.trait.name == CONTAGIOUS:
            return (f"\n{name_color(cmbt.name)}"
                    f"\n{dim('Strength |')} {red(round(cmbt.strength, 2))}"
                    f"\n{dim('Accuracy |')} {yellow(round(cmbt.acc, 2))}"
                    f"\n{dim('Coins    |')} {green(cmbt.coins)}"
                    f"\n{dim('Illness  |')} {yellow(cmbt.illness.name)}"
                    f"\n{dim('Trait    |')} {purple(cmbt.trait.name)}"
                    f"\n{dim('Ability  |')} {purple(cmbt.trait.desc)}"
                    )
        else:
            return (f"\n{name_color(cmbt.name)}"
                    f"\n{dim('Strength |')} {red(round(cmbt.strength, 2))}"
                    f"\n{dim('Accuracy |')} {yellow(round(cmbt.acc, 2))}"
                    f"\n{dim('Coins    |')} {green(cmbt.coins)}"
                    f"\n{dim('Trait    |')} {purple(cmbt.trait.name)}"
                    f"\n{dim('Ability  |')} {purple(cmbt.trait.desc)}"
                    )

    return (f"{format_world_data()}\n{format_combatant_data(player, orange)}\n"
            f"{format_combatant_data(enemy, purple)}")

# ================================================================================================

def display_battle_info(game_state: GameState) -> None:
    print_and_sleep(get_battle_info_view(game_state))

# ================================================================================================

def display_active_perk_count() -> None:
    print_and_sleep(f"Perks {dim(f"({len(load_perks(lambda p: p.active))})")}")

# ================================================================================================

@attach_perks(USED_SNEAKERS, NEW_SNEAKERS, silent=True)
def calculate_flee() -> float:
    return 0.5

# ================================================================================================
# ================================================================================================

def display_fishing_actions(game_state: GameState) -> None:
    print_and_sleep("\n".join([
        cyan("Fishing Actions"),
        "",
        yellow("Pull Rod"),
        "An aggressive move.",
        "Brings the fish closer and drains stamina quickly.",
        "Also increases rage quickly.",
        "Best used when the fish is tired or when you want to end the fight.",
        "",
        green("Reel In"),
        "A safe and steady move.",
        "Makes progress while slowly wearing the fish down.",
        "Generates less rage than Pull Rod.",
        "Best used when the fish is calm and you want consistent progress.",
        "",
        blue("Give Line"),
        "A defensive move.",
        "Allows the fish to gain distance but lowers rage.",
        "Useful when the fish is becoming angry.",
        "Best used to prevent the fish from breaking free.",
        "",
        purple("Observe"),
        "A tactical move.",
        "Reveals information about the fish.",
        "May uncover its species, variant, strength, speed, or temperament.",
        "Best used when you are unsure how to approach the fight.",
        "",
        orange("General Strategy"),
        dim("Reel In to make safe progress."),
        dim("Pull Rod to finish the fight."),
        dim("Give Line when rage becomes dangerous."),
        dim("Observe to learn more about the fish."),
    ]), )

def display_fishing_info(game_state: GameState) -> None:
    print_and_sleep("\n".join([
        cyan("Understanding Fish"),
        "",
        green("Stamina"),
        "Represents how much energy the fish has left.",
        "Tired fish are easier to catch and do not fight as effectively.",
        "If a fish's stamina reaches 0, it can no longer continue the fight.",
        "",
        yellow("Distance"),
        "Represents how far the fish is from you.",
        "Bring the distance down to 0 to land the fish.",
        "If the fish reaches the area's escape distance, it escapes.",
        "",
        red("Rage"),
        "Represents how agitated the fish has become.",
        "Rage rises when pressure is applied and falls when you Give Line.",
        "If rage reaches 100%, the fish may break free and escape.",
        "",
        white("Spit Hook Chance"),
        "Some fish can shake the hook loose on their own.",
        "This chance is usually very small.",
        "Aggressive and energetic fish tend to have higher values.",
        "",
        cyan("Fish States"),
        "",
        blue("Calm"),
        "The fish is under control.",
        "It fights normally and is less dangerous.",
        "",
        yellow("Agitated"),
        "The fish is becoming annoyed.",
        "Its behavior becomes less predictable.",
        "",
        purple("Spooked"),
        "The fish senses danger.",
        "It may fight harder and become more difficult to manage.",
        "",
        red("Enraged"),
        "The fish is in a panic.",
        "It becomes much more dangerous and may break free if not calmed down.",
        "",
        orange("General Strategy"),
        dim("Wear the fish down while keeping rage under control."),
        dim("Bring distance to 0 before the fish reaches the escape distance."),
        dim("A tired fish is easier to catch."),
        dim("An angry fish is more likely to get away."),
    ]), )

# ================================================================================================

def display_fishing_stats(game_state: GameState) -> None:
    player = game_state.player
    if not player.caught_fish:
        print_and_sleep(yellow("No fish caught."), 1)
        return

    caught = player.caught_fish
    shallows_fish = [i for i in caught if i.catch_location == SHALLOWS]
    bay_fish = [i for i in caught if i.catch_location == BAY]
    ocean_fish = [i for i in caught if i.catch_location == OCEAN]

    largest = max(caught, key=lambda fish: fish.size)
    smallest = min(caught, key=lambda fish: fish.size)
    longest = max(caught, key=lambda fish: fish.length)
    heaviest = max(caught, key=lambda fish: fish.weight)
    valuable = max(caught, key=lambda fish: fish.value)
    fastest = max(caught, key=lambda fish: fish.speed)
    enraged = max(caught, key=lambda fish: fish.rage_factor)
    toughest = max(caught, key=lambda fish: fish.max_stamina)
    strongest = max(caught, key=lambda fish: fish.strength)

    stats_fish = [
        largest,
        smallest,
        longest,
        heaviest,
        valuable,
        fastest,
        enraged,
        toughest,
        strongest,
    ]

    space = max(len(fish.name) for fish in stats_fish)
    pipe = white('|')

    if not player.caught_fish:
        print_and_sleep(yellow("Go catch some fish fool."))
    else:
        print_and_sleep("\n".join([
            f"Total Caught:   {blue(len(caught))}",

            f"Shallows:       {blue(len(shallows_fish))}",
            f"Bay:            {(blue(len(bay_fish)))}",
            f"Ocean:          {(blue(len(ocean_fish)))}",
            "",
            f"Largest:        {blue(f'{largest.name:<{space}}')} {pipe} {yellow(largest.weight)} lbs, {yellow(largest.length)} in",
            f"Smallest:       {blue(f'{smallest.name:<{space}}')} {pipe} {yellow(smallest.weight)} lbs, {yellow(smallest.length)} in",
            f"Longest:        {blue(f'{longest.name:<{space}}')} {pipe} {yellow(longest.length)} in",
            f"Heaviest:       {blue(f'{heaviest.name:<{space}}')} {pipe} {yellow(heaviest.weight)} lbs",
            f"Most Valuable:  {blue(f'{valuable.name:<{space}}')} {pipe} {green(valuable.value)} coins",
            f"Fastest:        {blue(f'{fastest.name:<{space}}')} {pipe} Speed: {cyan(fastest.speed)}",
            f"Most Rage:      {blue(f'{enraged.name:<{space}}')} {pipe} Rage Factor: {red(enraged.rage_factor)}",
            f"Strongest:      {blue(f'{strongest.name:<{space}}')} {pipe} Strength: {yellow(strongest.strength)}",
            f"Toughest:       {blue(f'{toughest.name:<{space}}')} {pipe} Max Stamina: {orange(toughest.max_stamina)}",
        ]))

# ================================================================================================

def display_area_log(game_state: GameState, area: str) -> None:
    player = game_state.player

    all_catches_in_area = [
        fish for fish in player.caught_fish
        if fish.catch_location == area
    ]

    if not all_catches_in_area:
        print_and_sleep(yellow("Log is dry."))
        return

    print_and_sleep(cyan(f"=== {area.upper()} ==="))

    area_species = {i['name'] for i in Fish_Species if area in i['areas']}
    caught_species = {i.base_name for i in player.caught_fish if area in i.areas}

    total = len(area_species)
    caught = len(caught_species)
    percentage = round((caught / total) * 100)

    print_and_sleep(f"Caught: {caught}/{total} ({percentage}%)", 2)

    name_width = max(len(fish.name) for fish in all_catches_in_area)
    rarity_width = max(len(fish.get_rarity_text()) for fish in all_catches_in_area)

    length_width = max(len(str(fish.length)) for fish in all_catches_in_area)
    weight_width = max(len(str(fish.weight)) for fish in all_catches_in_area)

    for fish in sorted(all_catches_in_area, key=lambda fish: fish.base_name):
        sex_color = blue if fish.sex == MALE else purple if fish.sex == FEMALE else orange

        print_and_sleep(
            dim(" | ").join([
                blue(f"{fish.name:<{name_width}}"),
                f"{fish.get_rarity_text():<{rarity_width}}",
                f"{sex_color(fish.sex[0])}",
                f"{yellow(f'{fish.length:>{length_width}}')} in",
                f"{yellow(f'{fish.weight:>{weight_width}}')} lbs",
                f"{yellow(f'{get_percentile_text(fish.size_percentile)}')}",
            ])
        )

    print("")

# ================================================================================================

def get_percentile_text(percentile):
    if 10 <= percentile % 100 <= 20:
        end = "th"
    else:
        end = {
            1: "st",
            2: "nd",
            3: "rd"
        }.get(percentile % 10, "th")

    text = f"{percentile}{end} percentile"

    if percentile >= 90:
        return green(f"Trophy Specimen ({text})")
    elif percentile >= 50:
        return yellow(text)
    else:
        return red(text)

# ================================================================================================

def display_area_compendium(game_state: GameState, area: str) -> None:
    player = game_state.player

    print_and_sleep(cyan(f"=== {area.upper()} COMPENDIUM ==="))

    # --- filtering ---
    area_species = [
        species for species in Fish_Species
        if area in species['areas']
    ]

    caught_species = {
        fish.base_name for fish in player.caught_fish
        if area in fish.areas
    }

    total = len(area_species)
    caught = len(caught_species)
    percentage = round((caught / total) * 100) if total else 0

    print_and_sleep(f"Discovered: {caught}/{total} ({percentage}%)", 2)

    # --- spacing ---
    name_width = max(
        len(species['name']) if species['name'] in caught_species else len("Unknown Creature")
        for species in area_species
    )

    rarity_width = max(
        len(species['rarity'])
        for species in area_species
    )

    area_width = max(
        len(", ".join(species['areas']))
        for species in area_species
    )

    bait_width = max(
        len(", ".join(
            b.name if hasattr(b, "name") else str(b)
            for b in species['preferred_bait']
        ))
        for species in area_species
    )


    # --- iterate and print ---
    for species in sorted(area_species, key=lambda species: species['name']):
        discovered = species['name'] in caught_species

        name = species['name'] if discovered else "Unknown Creature"
        name_color = cyan if discovered else dim

        area_text = ", ".join(species['areas'])
        bait_text = ", ".join(
            b.name if hasattr(b, "name") else str(b)
            for b in species['preferred_bait']
        )

        rarity = species['rarity']

        print_and_sleep(
            dim(" | ").join([
                name_color(f"{name:<{name_width}}"),
                get_rarity_text(f"{rarity:<{rarity_width}}"),
                blue(f"{area_text:<{area_width}}"),
                cyan(f"{bait_text:<{bait_width}}"),
            ])
        )

    print("")

def get_rarity_text(rarity: str) -> str:
    raw = rarity.strip()

    if raw == COMMON:
        return yellow(rarity)
    elif raw == UNCOMMON:
        return green(rarity)
    elif raw == RARE:
        return blue(rarity)
    else:
        return orange(rarity)