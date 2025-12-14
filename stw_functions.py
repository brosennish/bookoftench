import os.path
import pickle
import random
import time as t
import sys

import stw_constants as const
from stw_data import Weapons, Items, Enemies, Areas, Perks, Results, Achievements
from stw_classes import GameState, Player, Enemy, Shop, SaveGameState
from stw_colors import red as r, green as g, blue as b, purple as p, yellow as y, cyan as c, orange as o
from stw_colors import dim as d, reset as rst
from stw_audio import play_sound, play_music, get_current_music, stop_music


# FUNCTIONS: Record Kill, Win Game

def record_kill(gs, player):     # accesses GameState/player and returns T/F
    # Decrement area enemy count and increase kills per area count
    area = player.current_area    # define area to be where player is when enemy killed

    # updating area kill counts
    gs.area_kills[player.current_area] += 1

    # decrement & clamp
    gs.area_enemies[area] = max(0, gs.area_enemies[area] - 1)

    # first kill check
    if Results[const.Events.KILL] == 1:
        unlock_achievement(player, const.Achievements.KRILL_OR_BE_KRILLED)

    if Results[const.Events.KILL] == 10:
        unlock_achievement(player, const.Achievements.TENCH_KILLS)


def win_game(gs): 
    gs.rescued = True     # wench has been rescued
    print(f"\nYou defeated the evil Denny Biltmore and rescued the wench!\n\n{g}You win!")
    play_sound('great_job')
    t.sleep(3)   
    if play_again():
        run_game()
    else:
        sys.exit()


def play_again():
    while True:
        choice = input(f"\nWould you like to play again? (y/n):{b}\n>{rst} ").strip().lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            return False
        else:
            print("Invalid choice.")


# ==================================================================================================
# HELPER FUNCTIONS
# ==================================================================================================

# --- UNLOCK ACHIEVEMENT ---

def unlock_achievement(player, ach_id):
    if ach_id in player.achievements:
        return

    player.achievements.add(ach_id)
    ach = next(a for a in Achievements if a['id'] == ach_id)

    # award perk
    if ach['reward_type'] == 'perk':
        filtered = [i for i in Perks if i['name'] not in player.perks and i['name'] != const.Perks.WENCH_LOCATION]
        if filtered:
            reward = random.choice(filtered)
            print(f"{o}ACHIEVEMENT UNLOCKED: {ach['name']}"
                  f"\nReward: {reward['name']} | {reward['description']}{rst}")
            player.add_perk(reward['name'])
        else:
            return

        t.sleep(3)
        return

    # award XP
    elif ach['reward_type'] == 'xp':
        player.xp += ach['reward_value']

    # award coins
    elif ach['reward_type'] == 'coins':
        player.coins += ach['reward_value']

    print(f"{o}ACHIEVEMENT UNLOCKED: {ach['name']}"
          f"\nReward: +{ach['reward_value']} {ach['reward_type'].upper()}{rst}")
    t.sleep(3)


# --- MUSIC ---
def play_area_theme(player):
    area = player.current_area
    if area == const.Areas.CITY and get_current_music() != 'city_theme':
        play_music('city_theme')
    elif area == const.Areas.FOREST and get_current_music() != 'forest_theme':
        play_music('forest_theme')
    elif area == const.Areas.SWAMP and get_current_music() != 'swamp_theme':
        play_music('swamp_theme')
    elif area == const.Areas.CAVE and get_current_music() != 'cave_theme':
        play_music('cave_theme')

# --- GET DATA ---

def get_weapon_data(name: str) -> dict:     # enter name, return dict
    # enter the weapon name to return the full weapon dict
    return next((w for w in Weapons if w['name'] == name), None)


def get_item_data(name: str) -> dict:
    # enter the item name to return the full item dict
    return next((i for i in Items if i['name'] == name), None)


def get_perk_data(name: str) -> dict:
    # enter the perk name to return the full perk dict
    return next((i for i in Perks if i['name'] == name), None)


def get_ach_data(ach: str) -> dict:
    # enter the achievement id to return the full ach dict
    return next((a for a in Achievements if a['id'] == ach), None)


# --- BATTLE ---
def battle_header(player, enemy):
    # Weapon use variables with color indicators
    p_weapon_data, p_uses_left = p_uses(player)
    e_weapon_data, e_uses_left = e_uses(enemy)
    
    # HP color indicators
    pc = p_color(player)
    ec = e_color(enemy)

    # Player battle header
    print(f"\n{o}{player.name}{rst} {d}-{rst} {pc}{int(player.hp)} HP {rst}\n{c}{p_weapon_data['name']}{rst}\n{d}Damage: {rst}{r}{p_weapon_data['damage']}{rst} {d}| Accuracy: {rst}{y}{p_weapon_data['accuracy']}{rst} {d}| Uses: {rst}{p_uses_left}")
    # Enemy battle header
    print(f"\n{p}{enemy.name}{rst} {d}-{rst} {ec}{int(enemy.hp)} HP{rst}\n{c}{e_weapon_data['name']}{rst}\n{d}Damage: {rst}{r}{e_weapon_data['damage']}{rst} {d}| Accuracy: {rst}{y}{e_weapon_data['accuracy']}{rst} {d}| Uses: {rst}{e_uses_left}")


def bayou_bill_intro():
    print(f"{r}What do we have here?{rst}")
    t.sleep(2)
    print(f"{r}Looks like anotha one a dem riverboat bad boys right heuh uh huh.{rst}")
    t.sleep(2)
    print(f"{r}Bill's had a hankerin' for some a dat riverboat gumbo, mmhm.{rst}")
    t.sleep(2)
    print(f"{r}We gonna cook up some riverboat gumbo with some stuffin' with that mmhm riverboat boy.{rst}")
    t.sleep(2)


def is_boss(gs, player, enemy):
    if enemy.type == 'boss':
        gs.boss_defeated[player.current_area]['defeated'] = True
    if enemy.type == 'boss_final':
        win_game(gs)


def do_boss_battle(gs, player, shop):
    area = player.current_area

    # Get the boss dict for this area 
    boss_data = next(
        (e for e in Enemies
        if e.get('type') == 'boss' and e.get('area') == area),
        None
    )

    # Convert boss dict into an Enemy instance (same way you spawn normal enemies)
    enemy = Enemy.spawn_boss(boss_data)

    # Run the battle like normal
    battle(player, enemy, gs, shop)


def calculate_flee(player):
    if const.Perks.USED_SNEAKERS in player.perks:
        flee = 0.55
    elif const.Perks.NEW_SNEAKERS in player.perks:
        flee = 0.60
    elif const.Perks.USED_SNEAKERS and const.Perks.NEW_SNEAKERS in player.perks:
        flee = 0.65
    else:
        flee = 0.5

    return int(flee * 100)

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

def casino_color(player):
    # Enemy color (ec)
    if player.plays >= 10:
        cc = g
    elif player.plays >= 3:
        cc = y
    else:
        cc = r
    
    return cc


# --- REMAINING WEAPON USES ---
def p_uses(player):
    p_weapon_data = get_weapon_data(player.current_weapon)
    p_uses_left = player.weapon_uses.get(player.current_weapon, p_weapon_data['uses'])
    
    if p_uses_left == -1:
        p_uses_left = f"{c}∞{rst}"
    elif p_uses_left == 1:
        p_uses_left = f"{r}{p_uses_left}{rst}"
    elif p_uses_left in (2, 3):
        p_uses_left = f"{y}{p_uses_left}{rst}"
    else:
        p_uses_left = f"{p_uses_left}{rst}"   

    return p_weapon_data, p_uses_left


def p_uses_weapons(player, weapon: str):
    data = get_weapon_data(weapon)
    uses_left = player.weapon_uses.get(weapon, data['uses'])

    if uses_left == -1:
        uses_display = f"{c}∞{rst}"
    elif uses_left == 1:
        uses_display = f"{r}{uses_left}{rst}"
    elif uses_left in (2, 3):
        uses_display = f"{y}{uses_left}{rst}"
    else:
        uses_display = f"{uses_left}{rst}"

    return data, uses_display


def e_uses(enemy):
    e_weapon_data = get_weapon_data(enemy.current_weapon)
    e_uses_left = enemy.weapon_uses.get(enemy.current_weapon, e_weapon_data['uses'])
    if e_uses_left == -1:
        e_uses_left = f"{c}∞{rst}"
    elif e_uses_left == 1:
        e_uses_left = f"{r}{e_uses_left}{rst}"
    elif e_uses_left in (2,3):
        e_uses_left = f"{y}{e_uses_left}{rst}"
    else:
        e_uses_left = f"{e_uses_left}{rst}"

    return e_weapon_data, e_uses_left


# --- BOUNTY ---
def bounty_update(gs, player):
    if const.Perks.TENCH_THE_BOUNTY_HUNTER in player.perks:
            bounty = (gs.bounty + 25)
    else:
        bounty = gs.bounty

    return bounty

def refresh_wanted(gs):
    valid = [e for e in Enemies if e.get('type', 'normal') not in ('boss', 'boss_final')]
    gs.wanted_data = random.choice(valid).copy()
    gs.wanted = gs.wanted_data['name']
    gs.bounty = gs.wanted_data['bounty']


# --- BANK ---
def visit_bank_manual(player):
    play_music('bank_theme')

    print(f"Welcome to the Off-Shore Bank of Shebokken.\n"
          f"We do not accept deposits between level-ups.\n"
          f"Withdrawals will incur a 10% fee.")

    while True:
        print(f"\nPlayer: {g}{player.coins} {rst}{d}|{rst} Bank: {g}{player.bank}{rst}")

        choice = input(f"\nWhat would you like to do?\n"
                       f"[w] Withdraw\n"
                       f"[q] Leave\n{b}>{rst} ").strip().lower()

        if choice == 'w':
            selection = input(f"\nHow much would you like to withdraw?\n{b}>{rst} ").strip().lower()

            if selection.isdigit():
                num = int(selection)
            else:
                print(f"{y}Invalid choice.")
                continue

            if num <= player.bank:
                player.bank -= num
                amount = int(num * 0.9)
                player.coins += amount
                print(f'You withdrew {g}{amount}{rst} coins from the bank.')
                log_event(const.Events.WITHDRAW)
                t.sleep(1)
                continue
            elif num > player.bank:
                print(f"{y}Insufficient funds for withdrawal.")
                t.sleep(1)
                continue
            else:
                print(f"{y}Invalid choice.")
                continue

        elif choice == 'q':
            print(f"{b}Very well...")
            t.sleep(1)
            stop_music()
            return

        else:
            print(f"{y}Invalid choice.")
            continue


# --- WEAPONS ---
def find_weapon(player):
    weapon_dict = random.choice(Weapons)
    while weapon_dict['name'] in (const.Weapons.BARE_HANDS,const.Weapons.CLAWS,const.Weapons.VOODOO_STAFF):
        weapon_dict = random.choice(Weapons)
    max_uses = weapon_dict['uses']
    found_uses = random.randint(1, max_uses) if max_uses >= 1 else max_uses
    weapon = weapon_dict['name']
    if weapon not in player.weapons:
        print(f"{c}You found a {weapon}!")
        player.add_weapon(weapon, remaining_uses = found_uses)
        added = True
    else:
        added = False

    return weapon, found_uses, added


# --- PERKS ---
def do_view_perks(player, gs):

    if not player.perks:
        print(f"{y}Your perks are dry.")
        t.sleep(1)
    else:
        print(f"Your Perks:")
        if const.Perks.WENCH_LOCATION in player.perks:
            print(f'\nWench Location: {b}{gs.wench_area}{rst}')

        for perk in sorted(player.perks):
            perk_data = get_perk_data(perk)
            if not perk_data:
                print(f"\n{y}Perk: {perk:<22}\nDescription: [Missing data!]")
                continue
            print(f"\n{p}{perk_data['name']:<22} | {perk_data['description']}")
        input(f'\n{b}>{rst} ')


# --- ACHIEVEMENTS ---
def do_view_achievements(player):

    if not player.achievements:
        print(f"{y}Your achievements are dry.")
        t.sleep(1)
    else:
        print(f"Your Achievements:")
        for ach in sorted(player.achievements):
            ach_data = get_ach_data(ach)

            if not ach_data:
                print(f"\n{o}{ach:<22}\n[Missing data!]")
                continue

            print(f"\n{o}{ach_data['name']:<22} | {ach_data['description']}")

        input(f'\n{b}>{rst} ')


# --- COUNTER ---
def log_event(event: str):
    if event not in Results:
        return
    Results[event] += 1


# --------------------------------------------------------------------------------------------------
# GAME LOOP FUNCTIONS
# --------------------------------------------------------------------------------------------------

def get_choice_from_dict(prompt: str, options: dict) -> str:    # prompt is a str and options are a dict, return a str
    print("" + prompt)                              # print a new line and the prompt (MAIN MENU, etc.)
    for key, label in options.items():                # for the key/label for each dict pair in options
        print(f"[{key}] {label}")                   # print the key in caps and the label as is
    while True:
        choice = input(f"{b}>{rst} ").strip().lower()          # take the input, strip end spaces, and make lowercase
        if choice in options:
            return choice                             # if the choice is good, return it for use
        print(f"\n{y}Invalid choice.") 
        t.sleep(1)        


def get_choice_from_list(prompt: str, options: list) -> str:
    print("\n" + prompt)
    for option in options:
        print(option)
    options_lower = [option.lower() for option in options]
    while True:
        choice = input(f"{b}>{rst} ").strip().lower()
        if choice in options_lower:
            return choice
        print(f"\n{y}Invalid choice.")
        t.sleep(1)

def main_menu():
    while True:
        choice = get_choice_from_dict(f"\n{rst}MAIN MENU", {"n": "New Game", "l": "Load Game", "q": "Quit"})
        
        if choice == "n":
            run_game()
        elif choice == "l":
            load_game()
        elif choice == "q":
            sys.exit()
        else: 
            continue


def actions_main_menu(gs, player, shop):
    while True:
        choice = get_choice_from_dict(f"{rst}MAIN MENU",
                                      {"n": "New Game", "s": "Save Game", "l": "Load Game", "r": "Return", "q": "Quit"})
        
        if choice == "n":
            run_game()
        elif choice == "s":
            save_game(SaveGameState(gs, player, shop))
        elif choice == "l":
            load_game()
        elif choice == "r":
            return
        elif choice == "q":
            print(f"{r}You'll be back.\nOh... yes.\nYou'll be back.")
            t.sleep(1)
            sys.exit()
        else: 
            continue


def run_game(gs=GameState(), player=Player(), shop=Shop(), name=True, tutorial=True):

    play_music('intro_theme')
    while name:
        choice = input(f"\nWhat is your name?:\n{b}>{rst} ")
        if choice != '':
            player.name = choice
            name = False
        else:
            continue

    while tutorial:
        choice = input(f"\nDo you need a tutorial? (y/n):\n{b}>{rst} ").strip().lower()
        if choice == 'n':
            tutorial = False
        elif choice == 'y':
            print("""\nSAVE THE WENCH - HOW TO PLAY

            1. Explore areas to find enemies, loot, perks, and events
            2. Fight enemies in turn-based combat to earn XP and coins
            3. Buy and sell items and weapons in the shop
            4. Use items freely during your turn or between battles
            5. Gain perks that permanently affect combat, coins, or luck
            6. Play casino games to risk coins for big rewards
            7. Store coins in the bank to earn interest upon level-up
            8. Each area has a boss and a hidden number of enemies
            9. Clear the wench’s area to unlock the final showdown
            10. Defeat the final boss to save the wench and win the game
            """)
            input(f'{b}>{rst} ')
            tutorial = False
        else:
            print('Invalid choice.')
            continue

    print(f"\n{r}You wash up on a beach outside of Shebokken.")
    print(f"{r}The champion feels it in his jines that his wench is in danger.")
    print(f"{r}Find her before her life runs dry...\n")
    input(f"{b}>{rst} ")
    

    # Core loop: ends if player runs out of lives or the wench is rescued
    while player.lives > 0 and not gs.rescued:
        player.alive = True
        actions_menu(gs, player, shop)

    if play_again():
        run_game()


def actions_menu(gs, player, shop):
    get_current_music()
    play_area_theme(player)

    while player.lives > 0 and not gs.rescued:
        c_area = player.current_area
        player.alive = True
        
        # Enemies killed and remaining 
        remaining = gs.area_enemies.get(c_area, 0)
        killed = gs.area_kills[c_area]
        victory = gs.boss_defeated[c_area]['defeated']

        # Variable HP color coding
        pc = p_color(player)

        # Apply perks to update bounty
        bounty = bounty_update(gs, player)

        # Overview and Status menu
        if const.Perks.CROWS_NEST in player.perks:
            print(f"\nArea: {b}{c_area} {rst}{d}|{rst} Killed: {r}{killed}{rst} {d}|{rst} Remaining: {y}{remaining} {rst}{d}|{rst} Wanted: {p}{gs.wanted} {rst}{d}|{rst} Bounty: {p}{bounty} {rst}coins")
        else:
            print(f"\nArea: {b}{c_area} {rst}{d}|{rst} Killed: {r}{killed} {rst}{d}|{rst} Wanted: {p}{gs.wanted} {rst}{d}|{rst} Bounty: {p}{gs.bounty} {rst}coins")
        print(f"\n{o}{player.name}{rst} {d}-{rst} Level: {c}{player.lvl} {rst}{d}|{rst} XP: {c}{player.xp}/{player.xp_needed} {rst}{d}|{rst} HP: {rst}{pc}{player.hp}/{player.max_hp} {rst}{d}|{rst} Coins: {g}{int(player.coins)} {rst}{d}|{rst} Lives: {y}{player.lives}")
        
        # List choices
        if remaining > 0:
            choice = get_choice_from_dict(f"{rst}", {
                "e": "Explore",
                "i": "Use Item",
                "w": "Equip Weapon",
                "s": "Shop",
                "t": "Travel",
                "m": "More Options",
                "q": "Main Menu",
            })
        elif remaining == 0 and not victory:
            choice = get_choice_from_dict("", {
                "b": "Fight Boss",
                "i": "Use Item",
                "w": "Equip Weapon",
                "s": "Shop",
                "t": "Travel",
                "m": "More Options",
                "q": "Main Menu",
            })
        elif remaining == 0 and victory:
            print(f"{d}The {player.current_area} is dry.{rst}")
            choice = get_choice_from_dict("", {
                "i": "Use Item",
                "w": "Equip Weapon",
                "s": "Shop",
                "t": "Travel",
                "m": "More Options",
                "q": "Main Menu",
            })
        
        # action functions
        if choice == "e":
            do_explore(gs, player, shop)
        elif choice == "i": 
            player.use_item()
        elif choice == "w":
            do_equip_weapon(player)
        elif choice == "s":
            do_shop(player, shop, gs)
        elif choice == "t":
            do_travel(player)
        elif choice == "m":
            page_two = True
            while page_two:
                choice = get_choice_from_dict("", {
                "a": "Achievements",
                "b": "Bank",
                "c": "Casino",
                "p": "Perks",
                "o": "Overview",
                "r": "Return"
            })
                if choice == "a":
                    do_view_achievements(player)
                elif choice == "b":
                    visit_bank_manual(player)
                elif choice == "c":
                    do_casino(player)
                    play_area_theme(player)
                elif choice == "p":
                    do_view_perks(player, gs)
                elif choice == "o":
                    overview(gs, player)
                elif choice == "r":
                    page_two = False
        elif choice == "q":
            actions_main_menu(gs, player, shop)
        elif choice == "b" and remaining == 0 and not victory:
            do_boss_battle(gs, player, shop)
        else:
            continue

# ==================
#      CASINO
# ==================

def do_casino(player):
    play_music('casino_theme')
    if player.plays == 0:
        print(f"{b}Buy a perk or level up, bozo.{rst}")
        t.sleep(3)
        return
    
    if player.coins == 0:
        print(f"{b}Your paper's no good here.\nCome back with some coins.{rst}")
        t.sleep(3)
        return
    
    print(f"{b}Welcome to Riverbroat Crasino.{rst}\n")
    t.sleep(3)
    while True:
        choice = input("[1] Krill or Cray\n"
                       "[2] Above or Below\n"
                       "[3] Wet or Dry (WIP)\n"
                       "[4] Fish Bones (WIP)\n"
                       "[5] Mystery Box (WIP)\n"
                       "[r] Return\n"
                       f"{b}>{rst} ")
        if choice == "r":
            return
        elif choice == "1":
            krill_or_cray(player)
        elif choice == "2":
            above_or_below(player)
        elif choice == "3":
            print("Work in progress!")
            continue
        elif choice == "4":
            print("Work in progress!")
            continue
        elif choice == "5":
            print("Work in progress!")
            continue
        else:
            print("Invalid choice.")
            continue

def casino_check(player):
    if player.plays == 0:
        print(f"{b}You're out of plays. Buy a perk or level up, bozo.{rst}\n")
        t.sleep(2)
        get_current_music()
        play_area_theme(player)
        return True
    elif player.coins == 0:
        print(f"{b}You're out of coins. Get lost, bozo.{rst}\n")
        t.sleep(2)
        get_current_music()
        play_area_theme(player)
        return True
    else:
        return None


def krill_or_cray(player):
    if casino_check(player):
        return
    else:
        print(f"{b}One to one bets. Classic Riverbroat Grambling.\n")

    while True:
        print(f"Coins: {g}{player.coins}{rst} {d}|{rst} Plays: {c}{player.plays}{rst}\n")
        choice = input(f"[#] Wager\n"
                       f"[q] Leave\n{b}>{rst} ").strip().lower()

        if choice == "q":
            print(f"{b}Later bozo.{rst}")
            t.sleep(1)
            return
        
        elif choice.isdigit():
            wager = int(choice)
            if wager > player.coins:
                print(f"{b}If you ain't got it, don't bet it, bozo.{rst}")
                t.sleep(1)
                continue
            elif wager <= 0:
                print(f"{b}Gotta bet something, bozo.{rst}")
                t.sleep(1)
                continue
            else: 
                pick = input(f"You bet {g}{wager}{rst} coins.\n\nWhat's the call? {o}k for krill {rst}{d}|{rst} {o}c for cray{rst}\n{b}>{rst} ").strip().lower()
                winner = random.choice(['k','c'])
                if pick not in ('k','c'):
                    print(f"{y}Invalid choice.")
                    t.sleep(1)
                    continue
                elif pick == winner:
                    if const.Perks.GRAMBLING_ADDICT in player.perks:
                        print(f"{p}Payout increased 5% with Grambling Addict!{rst}\n")
                        payout = int((wager * 1.05) * 0.9)
                        player.coins += payout
                        player.casino_won += payout
                    else:
                        payout = int(wager * 0.9)
                        player.coins += payout
                        player.casino_won += payout
                    print(f"{g}Lucky guess, bozo! You won {payout} coins.{rst}")
                    play_sound('golf_clap')
                    if const.Perks.AP_TENCH_STUDIES in player.perks:
                        leveled_up = player.gain_xp_other(2)
                    else:
                        leveled_up = player.gain_xp_other(1)
                    if leveled_up:
                        player.visit_bank()
                    player.plays -= 1
                    print()
                    if casino_check(player):
                        return
                    else:
                        continue
                else: 
                    print(f"{b}Bozo's blunder. Classic. Could've seen that coming from six or eight miles away.{rst}\n")
                    player.coins -= wager
                    player.casino_lost += wager
                    player.plays -= 1
                    if casino_check(player):
                        return
                    else:
                        continue
        else:
            print(f"{y}Invalid choice.{rst}")
            continue


def above_or_below(player):
    if casino_check(player):
        return
    else:
        print(f"{b}Welcome to Above or Below!\n\n"
              f"{rst}Rules:\n"
              f"1. Place a wager and roll a die.\n"
              f"2. Guess if the next roll will be above or below the previous roll and roll once more.\n"
              f"3. Your payout increases by a higher percentage with each correct guess.\n"
              f"4. If you're incorrect, you lose your wager and forfeit the payout.\n"
              f"5. Play up to 4 rounds and cash out before you run dry.{rst}\n")

    while True:
        if casino_check(player):
            return
        print(f"Coins: {g}{player.coins}{rst} {d}|{rst} Plays: {c}{player.plays}{rst}\n")
        choice = input(f"[#] Wager\n"
                       f"[q] Leave\n{b}>{rst} ").strip().lower()
        if choice == "q":
            print(f"{b}Later bozo.{rst}\n")
            return
        elif not choice.isdigit():
            print(f"{y}Invalid choice.\n")
            continue
        elif int(choice) > player.coins:
            print(f"{b}You don't have enough coins, bozo.\n")
            continue
        else:
            wager = int(choice)
            player.plays -= 1
            turn = 1
            payout = wager
            ladder = [1.5, 2.0, 2.8, 4.0]

            while True:
                mult = ladder[turn-1]
                if const.Perks.GRAMBLING_ADDICT in player.perks:
                    print(f"Round: {c}{turn}{rst} {d}|{rst} Wager: {g}{wager}{rst} {d}|{rst} Mult: {p}{mult}{rst} {d}|{rst} Payout: {g}{int(payout*1.05)}{rst}\n")
                else:
                    print(f"Round: {c}{turn}{rst} {d}|{rst} Wager: {g}{wager}{rst} {d}|{rst} Mult: {p}{mult}{rst} {d}|{rst} Payout: {g}{int(payout)}{rst}\n")
                input(f"Roll the die\n{b}>{rst} ")
                roll1 = random.randint(1, 6)
                print(f"{b}You rolled a {roll1}.\n")

                while True:
                    call = input(f"[A] Above\n"
                                 f"[B] Below\n{b}>{rst} ").strip().lower()
                    if call not in ('a', 'b'):
                        print(f"{y}Invalid choice.")
                        continue
                    else:
                        break

                input(f"\nRoll the die.\n{b}>{rst} ")
                roll2 = random.randint(1, 6)
                print(f"{b}You rolled a {roll2}.\n")

                if call == 'a' and roll2 > roll1:
                    payout = wager * ladder[turn-1]
                    print(f"{g}Lucky guess!\n"
                          f"Payout increased to {int(payout)} coins.\n")
                elif call == 'a' and roll2 <= roll1:
                    print(f"{y}Your guess was dry.\n")
                    player.coins -= wager
                    player.casino_lost += wager
                    break
                elif call == 'b' and roll2 < roll1:
                    payout = wager * ladder[turn-1]
                    print(f"{g}Lucky guess!\n"
                          f"Payout increased to {int(payout)} coins.\n")
                else:
                    print(f"{y}Your guess was dry.\n")
                    player.coins -= wager
                    player.casino_lost += wager
                    break

                turn += 1
                if turn == 5:
                    if const.Perks.GRAMBLING_ADDICT in player.perks:
                        final_payout = int(payout * 1.05)
                    else:
                        final_payout = int(payout)

                    player.coins += final_payout
                    print(f"{b}You completed the final round.{rst}\n"
                          f"{g}You cashed out {final_payout} coins!\n")
                    if const.Perks.AP_TENCH_STUDIES in player.perks:
                        leveled_up = player.gain_xp_other(4)
                    else:
                        leveled_up = player.gain_xp_other(3)
                    if leveled_up:
                        player.visit_bank()
                    player.casino_won += final_payout
                    print()
                    return

                while True:
                    choice = input(f"[c] Continue\n"
                                   f"[q] Cash Out\n"
                                   f"{b}>{rst} ")
                    if choice == 'c':
                        break
                    elif choice == 'q':
                        if const.Perks.GRAMBLING_ADDICT in player.perks:
                            final_payout = int(payout * 1.05)
                            print(f"{p}Payout increase 5% with Grambling Addict!\n")
                        else:
                            final_payout = int(payout)

                        player.coins += final_payout
                        print(f"{g}You cashed out {final_payout} coins!\n")
                        player.casino_won += final_payout
                        return
                    else:
                        continue

# ==================
#    CASINO END
# ==================

def overview(gs, player):
    from stw_data import Results
    pc = p_color(player)

    width = 18  # adjust if you want wider/narrower labels

    print(f"{'Current Level':<{width}} {d}|{rst} {c}{player.lvl}{rst}")
    print(f"{'Current HP':<{width}} {d}|{rst} {pc}{player.hp}/{player.max_hp}{rst}")

    print(f"{'Coins':<{width}} {d}|{rst} {g}{player.coins}{rst}")
    print(f"{'Bank':<{width}} {d}|{rst} {g}{player.bank}{rst}")
    print(f"{'Deposits':<{width}} {d}|{rst} {o}{Results[const.Events.DEPOSIT]}{rst}")
    print(f"{'Withdrawals':<{width}} {d}|{rst} {o}{Results[const.Events.WITHDRAW]}{rst}")
    print(f"{'Interest Earned':<{width}} {d}|{rst} {g}{player.interest}{rst}")

    print(f"{'Casino Won':<{width}} {d}|{rst} {g}{player.casino_won}{rst}")
    print(f"{'Casino Lost':<{width}} {d}|{rst} {r}{player.casino_lost}{rst}")

    print(f"{'Hits':<{width}} {d}|{rst} {c}{Results[const.Events.HIT]}{rst}")
    print(f"{'Misses':<{width}} {d}|{rst} {c}{Results[const.Events.MISS]}{rst}")
    print(f"{'Critical Hits':<{width}} {d}|{rst} {c}{Results[const.Events.CRIT]}{rst}")

    print(f"{'Enemies Killed':<{width}} {d}|{rst} {r}{Results[const.Events.KILL]}{rst}")
    print(f"{'Bounties Claimed':<{width}} {d}|{rst} {p}{Results[const.Events.BOUNTY_COLLECTED]}{rst}")

    areas_cleared = sum(1 for count in gs.area_enemies.values() if count == 0)
    print(f"{'Areas Cleared':<{width}} {d}|{rst} {b}{areas_cleared}{rst}")

    bosses_defeated = sum(1 for data in gs.boss_defeated.values() if data['defeated'])
    print(f"{'Bosses Defeated':<{width}} {d}|{rst} {r}{bosses_defeated}{rst}")

    print(f"{'Items Purchased':<{width}} {d}|{rst} {c}{Results[const.Events.BUY_ITEM]}{rst}")
    print(f"{'Items Used':<{width}} {d}|{rst} {c}{Results[const.Events.USE_ITEM]}{rst}")
    print(f"{'Weapons Purchased':<{width}} {d}|{rst} {c}{Results[const.Events.BUY_WEAPON]}{rst}")
    print(f"{'Perks Owned':<{width}} {d}|{rst} {c}{len(player.perks)}{rst}")

    print(f"{'Times Traveled':<{width}} {d}|{rst} {b}{Results[const.Events.TRAVEL]}{rst}")
    input(f"{b}>{rst} ")


def do_explore(gs, player, shop):
    # 45% chance of enemy (10% for elite), 10% for item, 10% weapon, 20% coins, 1% perk, 14% dry

    if player.lives > 0:
        player.alive = True
    roll = random.random()
    if roll < 0.45:
        enemy = Enemy.spawn_enemy_for_area(player.current_area)
        while enemy.type in ('boss', 'boss_final'):
            enemy = Enemy.spawn_enemy_for_area(player.current_area)

        # enemy hp scaling
        level_bonus = max(0, player.lvl - 1)
        enemy.max_hp += level_bonus
        enemy.hp = enemy.max_hp

        if random.random() < 0.10:  
            enemy.name = f"Elite {enemy.name}"
            enemy.max_hp = int(enemy.max_hp * 1.5)
            enemy.hp = enemy.max_hp
            enemy.coins = int(enemy.coins * 1.5)
            print(f"{y}An enemy appears!{rst} {p}(Elite enemy!)")
        else:
            print(f"{y}An enemy appears!{rst}")
        t.sleep(1)
        battle(player, enemy, gs, shop)
    elif roll < 0.55:
        if len(player.items) < player.max_items:
            item_dict = random.choice(Items)
            item = item_dict['name']
            player.add_item(item)
            t.sleep(1)
            return
        else:
            print(f"{y}Your item sack is full.")
            t.sleep(1)
            return
    elif roll < 0.65:
        if len(player.weapons) < player.max_weapons:
            added = find_weapon(player)
            if added:
                return
            else:
                print(f"{y}{d}You already have this weapon.")
                t.sleep(1)
                return
        else:
            print(f"{y}Your weapon sack is full.")
            t.sleep(1)
            return
    elif roll < 0.85:
        if const.Perks.METAL_DETECTIVE in player.perks:
            coins = random.randint(25, 50)
        else:
            coins = random.randint(10, 25)
        print(f'{g}You found {coins} coins!')
        t.sleep(1)
        player.coins += coins
    elif roll < 0.86:
        filtered = [i for i in Perks if i['name'] not in player.perks and i['name'] != const.Perks.WENCH_LOCATION]
        if filtered:
            reward = random.choice(filtered)
            print(f"{p}You sense a noble presence...\n")
            t.sleep(2)
            print(f"{p}It's a mensch!\n")
            t.sleep(2)
            print(f"{p}He's gifted you the {reward['name']} perk!\n"
                  f"{p}{reward['description']}")
            player.add_perk(reward['name'])
            t.sleep(3)
        else:
            return
    else:
        print(f'{d}You came up dry.')
        t.sleep(1)
        return 


def do_equip_weapon(player):
    while True:
        print(f"\nWeapons {d}({len(player.weapons)}/{player.max_weapons}){rst}")

        for idx, weapon in enumerate(player.weapons, 1):
            p_weapon_data, p_uses_left = p_uses_weapons(player, weapon)

            print(
                f"[{idx}] {c}{p_weapon_data['name']}{rst}\n"
                f"{d}Damage:{rst} {r}{p_weapon_data['damage']:<2}{rst} {d}| "
                f"Accuracy:{rst} {y}{p_weapon_data['accuracy']:<3}{rst} {d}| "
                f"Uses:{rst} {p_uses_left}"
            )

        choice = input(f"\n[#] Equip weapon\n"
                       f"[r] Return\n{b}>{rst} ").strip().lower()
        if choice == 'r':
            return
        
        if choice.isdigit():
            num = int(choice)

            # Weapon range
            if 1 <= num <= len(player.weapons):
                weapon = player.weapons[num - 1] # python zero index correction
                player.current_weapon = weapon 
                print(f"{c}{weapon} equipped.")
                t.sleep(1)
                return
    
            else:
                print("Invalid choice.")
                t.sleep(1)

# ===================
#       SHOP
# ===================

def get_shop_discount(player):
    perks = set(player.perks)
    discount = 1.0

    if const.Perks.BARTER_SAUCE in perks and const.Perks.TRADE_SHIP in perks:
        print(f"{p}Prices down 30% with Barter Sauce and Trade Ship!{rst}\n")
        discount = 0.7
    elif const.Perks.TRADE_SHIP in perks:
        print(f"{p}Prices down 20% with Trade Ship!{rst}\n")
        discount = 0.8
    elif const.Perks.BARTER_SAUCE in perks:
        print(f"{p}Prices down 10% with Barter Sauce!{rst}\n")
        discount = 0.9
    else:
        discount = 1

    return discount

# --- DO SHOP ---

def do_shop(player, shop, gs):
    play_music('shop_theme')
    while True:
        print(f'\n{b}Welcome! You have {rst}{g}{player.coins} {rst}{b}coins.\n')
        shop.view_shop_inventory(player)

        choice = input(f"\n[#] Purchase\n"
                       f"[s] Sell\n"
                       f"[r] Return\n{b}>{rst} ").strip().lower()

        if choice == "r":
            print(f"{b}Until next time!{rst}")
            t.sleep(2)
            get_current_music()
            play_area_theme(player)
            return

        if choice.isdigit():
            num = int(choice)

            filtered_items = [i for i in shop.item_inventory if i['name'] not in player.items]
            filtered_weapons = [w for w in shop.weapon_inventory if w['name'] not in player.weapons]

            item_count = len(filtered_items)
            weapon_count = len(filtered_weapons)
            perk_count = len(shop.perk_inventory)

            # --- ITEMS ---
            if 1 <= num <= item_count:
                item = filtered_items[num - 1]
                shop.buy_item(item['name'], player)
                continue

            # --- WEAPONS ---
            weapon_start = item_count + 1
            weapon_end = weapon_start + weapon_count - 1

            if weapon_start <= num <= weapon_end:
                index = num - weapon_start
                weapon = filtered_weapons[index]
                shop.buy_weapon(weapon['name'], player)
                continue

            # --- PERKS ---
            perk_start = weapon_end + 1
            perk_end = perk_start + perk_count - 1

            if perk_start <= num <= perk_end:
                index = num - perk_start
                if 0 <= index < perk_count:
                    perk = shop.perk_inventory[index]
                    shop.buy_perk(perk['name'], player)
                    if perk['name'] == const.Perks.WENCH_LOCATION and perk['name'] in player.perks:
                        print(f"\n{y}Shopkeeper: The wench is in the {gs.wench_area}. Don't ask me how I know.")
                        t.sleep(3)
                    if perk['name'] in (const.Perks.GRAMBLIN_MAN,const.Perks.GRAMBLING_ADDICT):
                        player.plays += 5
                else:
                    print(f"\n{y}Perk not found.")
                continue

            print(f"\n{y}Invalid choice.")
            t.sleep(1)

        elif choice == 's':

            # --- PRINT PLAYER INVENTORY WITH NUMBERS ---
            print(f"\nYour Inventory (sell menu): ")

            entries = []  # holds ("item", name) or ("weapon", name)

            # List items first
            for item in player.items:
                entries.append(("item", item))  # for items in inventory, append them to new entries list
            # Then weapons
            sellable = [w for w in player.weapons if w != const.Weapons.BARE_HANDS]
            for weapon in sellable:
                entries.append(("weapon", weapon))

            if not entries:
                print(f"\n{y}You have nothing to sell.")
                t.sleep(1)
                continue

            # Print numbered list
            for i, (kind, name) in enumerate(entries, 1):
                if kind == "item":
                    data = get_item_data(name)
                    print(f"[{i}] {c}{name:<24}{rst} {d}|{rst} Value:{rst} {g}{data['sell_value']:<3}{rst} {d}|{rst} HP: {g}+{data['hp']}")
                else:
                    data, uses_display = p_uses_weapons(player, name)
                    current_uses = player.weapon_uses.get(name, data['uses'])
                    sell_value = calculate_sell_price(name, current_uses)
                
                    print(
                        f"[{i}] {c}{name:<24}{rst} {d}|{rst} "
                        f"Value: {g}{sell_value:<3}{rst} {d}|{rst} "
                        f"DMG: {r}{data['damage']:<3}{rst} {d}|{rst} "
                        f"Accuracy: {y}{data['accuracy']:<4}{rst} {d}|{rst} "
                        f"Uses: {uses_display}"
                    )

            # --- CHOICE ---
            choice = input(f"\n[#] Sell item\n"
                           f"[r] Return\n{b}>{rst} ").strip().lower()
            if choice == "r":
                continue
            if not choice.isdigit():
                print(f"{y}Invalid choice. Try again.")
                t.sleep(1)
                continue

            num = int(choice)
            if not (1 <= num <= len(entries)):
                print(f"{y}Invalid choice. Try again.")
                t.sleep(1)
                continue

            # Extract what the number corresponds to
            kind, name = entries[num - 1]

            # --- SELL LOGIC ---
            if kind == "item":
                sell_item(name, player)
            else:
                sell_weapon(name, player)

        else:
            print(f"{y}Invalid choice.")
            t.sleep(1)

# =================================
#   SELL PRICE, SELL ITEM/WEAPON
# =================================

def calculate_sell_price(weapon_name, current_uses):
    data = get_weapon_data(weapon_name)
    base = data['sell_value']
    max_uses = data['uses']

    # Infinite-use weapons: always sell for base value
    if max_uses == -1:
        return base

    proportion = current_uses / max_uses
    price = base * proportion
    return max(int(price), 1)

def sell_item(item_name, player):  # player sells item
    item_data = get_item_data(item_name)
    if not item_data or item_name not in player.items:
        print(f'\n{y}{d}Item not found.')
        t.sleep(2)
        return

    sell_value = item_data['sell_value']

    player.coins += sell_value
    player.items.remove(item_name)
    print(f'{g}You sold {item_name} for {sell_value} coins.')
    play_sound('purchase')
    t.sleep(1)
    log_event(const.Events.SELL_ITEM)

def sell_weapon(weapon_name, player):  # player sells weapon
    # Must own the weapon
    if weapon_name not in player.weapons:
        print(f"\n{y}Can't sell what you don't have!")
        t.sleep(1)
        return

    weapon_data = get_weapon_data(weapon_name)
    if not weapon_data:
        print(f"\n{y}{d}Weapon not found.")
        t.sleep(1)
        return

    # Get current uses from player.weapon_uses
    current_uses = player.weapon_uses.get(weapon_name, weapon_data['uses'])

    sell_value = calculate_sell_price(weapon_name, current_uses)

    player.coins += sell_value

    # Remove from inventory
    player.weapons.remove(weapon_name)
    player.weapon_uses.pop(weapon_name, None)

    print(f"{g}You sold {weapon_name} for {sell_value} coins.")
    if weapon_name == player.current_weapon:
        player.current_weapon = const.Weapons.BARE_HANDS
    play_sound('purchase')
    t.sleep(1)
    log_event(const.Events.SELL_WEAPON)

# ================================================

def do_travel(player):
    areas = [a['name'] for a in Areas]

    if not areas:
        print(f'\n{y}Nowhere left to go...')
        t.sleep(2)
        return

    print("\nYou can travel to the following areas: ")
    for idx, area in enumerate(areas, 1):
        print(f"[{idx}] {b}{area}")
                
    choice = input(f"\n[#] Travel\n"
                   f"[r] Return\n{b}>{rst} ").strip().lower()

    if choice == 'r':
        return
    
    if choice.isdigit():
        num = int(choice)

        if 1 <= num <= len(areas):
            area = areas[num - 1] # for python 0 index
            player.current_area = area
            print(f'\n{c}Traveling by six by eight to the {area}...')
            play_music('travel_theme')
            log_event(const.Events.TRAVEL)
            t.sleep(5)
            # stop travel music, then start the new area's theme
            stop_music()
            play_area_theme(player)
            
        else:
            print(f"\n{y}Invalid choice.")
            t.sleep(1)
    else:
        print(f"\n{y}Invalid choice.")
        t.sleep(1)

# =====================================
#             BATTLE
# =====================================

def do_final_boss_battle(gs, player, shop):
    """Spawn and fight Denny Biltmore as the final boss."""

    # Find Denny's data (boss_final) from Enemies
    denny_data = next(
        e for e in Enemies
        if e.get('type') == 'boss_final'
    )

    weapon_names = denny_data['weapon']
    start_weapon = random.choice(weapon_names)

    # Build weapon_uses similar to spawn_enemy_for_area
    weapon_uses = {
        w: random.randint(1, max(get_weapon_data(w)['uses'], 1))
        for w in weapon_names
    }

    # Build the Enemy instance for Denny
    enemy = Enemy(
        name=denny_data['name'],
        hp=denny_data['hp'],
        max_hp=denny_data['hp'],
        weapons=list(weapon_names),
        items=[const.Items.TENCH_FILET],
        current_weapon=start_weapon,
        type=denny_data['type'],
        coins=denny_data['bounty'],
        current_area=player.current_area,
        weapon_uses=weapon_uses,
    )

    play_music('final_boss_theme')
    t.sleep(4)
    print(f"\n{r}You look through the corpse's phone...{rst}")
    t.sleep(4)
    print(f"\n{r}Its last location was the Biltmore Estate...{rst}")
    t.sleep(4)
    print(f"\n{r}You travel there and enter the grand corridor...{rst}")
    t.sleep(4)
    print(f"\n{r}Denny Biltmore stands before you...{rst}")
    t.sleep(4)
    print(f"\n{r}\"I've waited a long, long time to put you down...\"{rst}")
    t.sleep(4)
    print(f"\n{r}\"I knew if I captured the champion's beloved Meg Craig, he would send you to her rescue...\"{rst}")
    t.sleep(4)
    print(f"\n{r}\"Well, let's have at it then.\"{rst}")
    t.sleep(4)

    # When this battle ends and Denny dies, is_boss() will call win_game(gs)
    battle(player, enemy, gs, shop)


def battle(player, enemy, gs, shop):
    # Death Can Wait check
    if 'Death Can Wait' in player.perks:
        player.cheat_death_ready = True

    if enemy.name in (const.Enemies.SLEDGE_HAMMOND,const.Enemies.BAYOU_BILL,const.Enemies.CAPTAIN_HOLE,const.Enemies.DENNY_BILTMORE):
        if enemy.name == const.Enemies.BAYOU_BILL:
            bayou_bill_intro()
        get_current_music()
        play_music('area_boss_theme')
    elif enemy.name == const.Enemies.THE_MAYOR:
        play_music('final_boss_theme')
    elif enemy.type not in ('boss','boss_final'):
        get_current_music()
        play_music('battle_theme')

    while True:

        # Captain Hole event
        if enemy.name == const.Enemies.CAPTAIN_HOLE and const.Items.TENCH_FILET in player.items:
            print("Captain Hole has offered to shoot himself in the jines in exchange for your Tench Filet.")
            t.sleep(4)
            filet = input(f"Do you accept? (y/n):\n{b}>{rst} ").strip().lower()
            if filet == 'y':
                stop_music()
                player.items.remove(const.Items.TENCH_FILET)
                injury = random.randint(25,50)
                enemy.hp -= injury
                print('You hand your filet over to Captain Hole.\n')
                t.sleep(2)
                print(f'He shoots himself in the jines, losing {injury} HP as a result.')
                play_sound('pistol')
                get_current_music()
                play_music('area_boss_theme')
                t.sleep(3)

        player_turn = True
        while player_turn:
            battle_header(player, enemy)
            flee = calculate_flee(player)
            choice = input(f"\n[a] attack\n[i] use item\n[s] switch weapon\n[f] flee ({flee}%)\n[p] perks\n{b}>{rst} ").strip().lower()

            if choice == 'a':
                player.attack(enemy)   # attack the enemy
                player_turn = False    # change turn

            elif choice == 'i':
                player.use_item()      # use item
                continue               # continue turn

            elif choice == 's':        # switch weapon
                player.switch_weapon() # continue turn
                continue

            elif choice == 'f':        # try to flee
                fled = player.flee()   # T/F
                if enemy.name == const.Enemies.DENNY_BILTMORE:
                    print("There's no turning back now!")
                    t.sleep(2)
                    continue
                elif fled:
                    print(f'{c}You ran away from {enemy.name}!')
                    log_event(const.Events.FLEE)
                    if const.Perks.AP_TENCH_STUDIES in player.perks:
                        leveled_up = player.gain_xp_other(2)
                    else:
                        leveled_up = player.gain_xp_other(1)
                    if leveled_up:
                        player.visit_bank()
                    t.sleep(1)
                    stop_music()
                    play_area_theme(player)
                    return None
                else:
                    print(f"{y}Couldn't escape!")
                    t.sleep(1)
                    player_turn = False
            
            elif choice == 'p':          # view perks
                do_view_perks(player,gs) 
                continue

            else:
                print(f'{y}Invalid choice.')
                continue
    
        if enemy.hp <= 0:
            log_event(const.Events.KILL)
            if enemy.name == const.Enemies.THE_MAYOR:
                play_sound('kids_cheer')
            if enemy.name == gs.wanted:
                bounty = bounty_update(gs, player)
                if 'Elite' in enemy.name:
                    bounty *= 1.5
                player.coins += bounty
                print(f"{g}You killed {enemy.name} and collected a bounty of {bounty} coins!{rst}")
                log_event(const.Events.BOUNTY_COLLECTED)
                refresh_wanted(gs) # ONLY refresh wanted if the wanted enemy is killed
                t.sleep(1)
            
            is_boss(gs, player, enemy)
            record_kill(gs, player)
            
            if enemy.type != 'boss_final':
                enemy.drop_loot(player)
                leveled_up = player.gain_xp(enemy) # runs it and returns boolean for level_up
                if leveled_up:
                    player.visit_bank()

            if enemy.type == 'boss' and player.current_area == gs.wench_area:
                player.hp = player.max_hp
                do_final_boss_battle(gs, player, shop)

            stop_music()
            play_area_theme(player)
            return False # battle over, enemy dead

        else:
            if enemy.name == const.Enemies.SLEDGE_HAMMOND:
                enemy.hp += 3
                print(f"\n{p}Sledge Hammond took steroids and restored 3 HP!{rst}")
                t.sleep(1)
            alive = enemy.attack(player)
            if not alive:
                if player.cheat_death_ready:
                    player.hp = 1
                    print(f'{p}You survived the attack with Death Can Wait!{rst}')
                    player.cheat_death_ready = False
                    t.sleep(1)
                else:
                    shop.reset_inventory(player)
                    stop_music()
                    play_area_theme(player)
                    return False # battle over, player dead

# =====================================
#           BATTLE END
# =====================================

# ----- SAVE/LOAD GAME LOGIC -----

def load_game():
    save_dir = "saves"

    saves = dict((str(i), n) for (i, n) in enumerate(set(fn.split(".")[0] for fn in os.listdir(save_dir))))
    if len(saves) == 0:
        print(f"\n{r}No saved games exist.")
        t.sleep(1)
        return

    name = saves[get_choice_from_dict("Select a save: ", saves)]
    save_file = f"{name}.tench"

    with open(f"{save_dir}/{save_file}", "rb") as f:
        save_state: SaveGameState = pickle.load(f)

    run_game(save_state.game_state, save_state.player, save_state.shop, False, False)


def save_game(save_state: SaveGameState):
    save_dir = "saves"
    save_file = f"{save_state.player.name}.tench"

    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)
    with open(f"{save_dir}/{save_file}", "wb") as f:
        pickle.dump(save_state, f)

    print(f"\n{c}Game saved.\n")


# ----- MAIN: START GAME LOGIC -----
def main():
    main_menu()


if __name__ == "__main__":
    main()