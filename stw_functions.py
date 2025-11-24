import random
import time as t
import sys

from stw_data import Weapons, Items, Enemies, Areas, Perks, Results
from stw_classes import GameState, Player, Enemy, Shop
from stw_colors import red as r, green as g, blue as b, purple as p, yellow as y, cyan as c, orange as o
from stw_colors import dim as d, reset as rst
from stw_audio import play_sound, play_music, get_current_music, stop_music


# FUNCTIONS: Record Kill, Win Game

def record_kill(gs, player) -> bool:     # accesses GameState/player and returns T/F
    '''Decrement area enemy count and check win; return True if game won'''
    area = player.current_area    # define area to be where player is when enemy killed

    # updating area kill counts
    gs.area_kills[player.current_area] += 1

    # decrement & clamp
    gs.area_enemies[area] = max(0, gs.area_enemies[area] - 1)

    if 'Death Can Wait' in player.perks:
        player.cheat_death_ready = True


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
        choice = input(f"\nWould you like to play again? (y or n):{b}\n> ").strip().lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            return False
        else:
            print("Invalid choice.")


# --------------------------------------------------------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------------------------------------------------------

# --- MUSIC ---
def play_area_theme(player):
    area = player.current_area
    if area == 'City' and get_current_music() != 'city_theme':
        play_music('city_theme')
    elif area == 'Forest' and get_current_music() != 'forest_theme':
        play_music('forest_theme')
    elif area == 'Swamp' and get_current_music() != 'swamp_theme':
        play_music('swamp_theme')
    elif area == 'Cave' and get_current_music() != 'cave_theme':
        play_music('cave_theme')

# --- GET DATA ---

def get_weapon_data(name: str) -> dict:     # enter name, return dict
    '''enter the weapon name to return the full weapon dict'''
    return next((w for w in Weapons if w['name'] == name), None)


def get_item_data(name: str) -> dict:
    '''enter the item name to return the full item dict'''
    return next((i for i in Items if i['name'] == name), None)


def get_perk_data(name: str) -> dict:
    '''enter the perk name to return the full perk dict'''
    return next((p for p in Perks if p['name'] == name), None)


# --- BATTLE ---
def battle_header(player, enemy):
    # Weapon use variables with color indicators
    p_weapon_data, p_uses_left = p_uses(player)
    e_weapon_data, e_uses_left = e_uses(enemy)
    
    # HP color indicators
    pc = p_color(player)
    ec = e_color(enemy)

    # Player battle header
    print(f"\n{o}{player.name}{rst} {d}-{rst} {pc}{player.hp} HP {rst}\n{c}{p_weapon_data['name']}{rst}\n{d}Damage: {rst}{r}{p_weapon_data['damage']}{rst} {d}| Accuracy: {rst}{y}{p_weapon_data['accuracy']}{rst} {d}| Uses: {rst}{p_uses_left}")
    # Enemy battle header
    print(f"\n{p}{enemy.name}{rst} {d}-{rst} {ec}{enemy.hp} HP{rst}\n{c}{e_weapon_data['name']}{rst}\n{d}Damage: {rst}{r}{e_weapon_data['damage']}{rst} {d}| Accuracy: {rst}{y}{e_weapon_data['accuracy']}{rst} {d}| Uses: {rst}{e_uses_left}")


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
    if 'Used Sneakers' in player.perks:
        flee = 0.55
    elif 'New Sneakers' in player.perks:
        flee = 0.60
    elif 'Used Sneakers' and 'New Sneakers' in player.perks:
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
    from stw_functions import get_weapon_data

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
    if 'Tench the Bounty Hunter' in player.perks:
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
def do_bank_balance(player):

    if not player.bank:
        print(f"{y}Your bank account is dry.")
        t.sleep(1)
        return
    else:
        print(f"\nPlayer coins: {g}{player.coins}{rst} coins\n\nBank coins: {g}{player.bank}{rst} coins")

    input(f'\n{b}>{rst} ')
    return


# --- WEAPONS ---
def find_weapon(player):
    weapon_dict = random.choice(Weapons)
    while weapon_dict['name'] in ('Bare Hands','Claws','Voodoo Staff'):
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
        print(f"Your Perks:\n")
        if 'Wench Location' in player.perks:
            print(f'Wench Location: {b}{gs.wench_area}{rst}')

        for perk in player.perks:
            perk_data = get_perk_data(perk)
            if not perk_data:
                print(f"\n{y}Perk: {perk}\nDescription: [Missing data!]")
                continue
            print(f"\nPerk: {p}{perk_data['name']}{rst}\nDescription: {perk_data['description']}")
        input(f'\n{b}>{rst} ')


# --- COUNTER ---
def log_event(event: str):
    if event not in Results:
        return
    Results[event] += 1


# --------------------------------------------------------------------------------------------------
# GAME LOOP FUNCTIONS
# --------------------------------------------------------------------------------------------------

def get_choice(prompt: str, options: dict) -> str:    # prompt is a str and options are a dict, return a str
    print("" + prompt)                              # print a new line and the prompt (MAIN MENU, etc.)
    for key, label in options.items():                # for the key/label for each dict pair in options
        print(f"[{key.upper()}] {label}")             # print the key in caps and the label as is
    while True:
        choice = input(f"{b}>{rst} ").strip().lower()          # take the input, strip end spaces, and make lowercase
        if choice in options:
            return choice                             # if the choice is good, return it for use
        print(f"\n{y}Invalid choice.") 
        t.sleep(1)        


def main_menu():
    while True:
        choice = get_choice("MAIN MENU", {"n": "New Game", "q": "Quit"})
        
        if choice == "n":
            run_game()  
        elif choice == "q":
            sys.exit()
        else: 
            continue


def actions_main_menu():
    while True:
        choice = get_choice("MAIN MENU", {"n": "New Game", "r": "Return", "q": "Quit"})
        
        if choice == "n":
            run_game()  
        elif choice == "r":
            return
        elif choice == "q":
            print("You'll be back.\nOh... yes.\nYou'll be back.")
            t.sleep(2)
            sys.exit()
        else: 
            continue


def run_game():
    gs = GameState()
    player = Player()
    shop = Shop()

    play_music('intro_theme')
    name = True
    while name:
        choice = input(f"What is your name?:\n{b}>{rst} ")
        if choice != '':
            player.name = choice
            name = False
        else:
            continue

    tutorial = True
    while tutorial:
        choice = input(f"\nDo you need a tutorial? (y or n):\n{b}>{rst} ").strip().lower()
        if choice == 'n':
            tutorial = False
        elif choice == 'y':
            print("""\n1. Explore areas to find enemies, items, weapons, and coins
2. Fight enemies in turn-based combat
3. Use items to restore HP
4. Weapons have limited uses and can break
5. Defeat enemies to earn XP, coins, and a chance to recover their weapons
6. Leveling up restores HP, boosts stats, and refreshes the shop
7. Visit the shop to buy weapons, items, and perks
8. Travel between areas to search for the wench's hidden location
9. Perks offer special rewards and permanent bonuses
10. Clear the enemies in the wench's area and defeat the final boss to save the wench and win the game""")
            exit = input('')
            if exit == '':
                tutorial = False
            else:
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

        # XP needed logic
        required = 100 + (player.lvl - 1) * 50

        # Variable HP color coding
        pc = p_color(player)

        # Apply perks to update bounty
        bounty = bounty_update(gs, player)

        # Overview and Status menu
        if "Crow's Nest" in player.perks:
            print(f"\nArea: {b}{c_area} {rst}{d}|{rst} Killed: {r}{killed}{rst} {d}|{rst} Remaining: {y}{remaining} {rst}{d}|{rst} Wanted: {p}{gs.wanted} {rst}{d}|{rst} Bounty: {p}{bounty} {rst}coins")
        else:
            print(f"\nArea: {b}{c_area} {rst}{d}|{rst} Killed: {r}{killed} {rst}{d}|{rst} Wanted: {p}{gs.wanted} {rst}{d}|{rst} Bounty: {p}{gs.bounty} {rst}coins")
        print(f"\n{o}{player.name}{rst} {d}-{rst} Level: {c}{player.lvl} {rst}{d}|{rst} XP: {c}{player.xp}/{required} {rst}{d}|{rst} HP: {rst}{pc}{player.hp}/{player.max_hp} {rst}{d}|{rst} Coins: {g}{player.coins} {rst}{d}|{rst} Lives: {y}{player.lives}")
        
        # List choices
        if remaining > 0:
            choice = get_choice(f"{rst}", {
                "e": "Explore",
                "i": "Use Item",
                "w": "Equip Weapon",
                "s": "Shop",
                "t": "Travel",
                "m": "More Options",
                "q": "Main Menu",
            })
        elif remaining == 0 and not victory:
            choice = get_choice("", {
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
            choice = get_choice("", {
                "i": "Use Item",
                "w": "Equip Weapon",
                "s": "Shop",
                "t": "Travel",
                "m": "More Options",
                "q": "Main Menu",
            })
        
        # action functions
        if choice == "e":
            do_explore(gs, player, Enemy, shop)
        elif choice == "i": 
            player.use_item()
        elif choice == "w":
            do_equip_weapon(player)
        elif choice == "s":
            do_shop(player, shop, gs)
        elif choice == "t":
            do_travel(gs, player)
        elif choice == "m":
            page_two = True
            while page_two:
                choice = get_choice("", {
                "c": "Casino",
                "p": "View Perks",
                "b": "Bank Balance",
                "o": "Overview",
                "r": "Return"
            })
                if choice == "c":
                    do_casino(player)
                    play_area_theme(player)
                elif choice == "p":
                    do_view_perks(player, gs)
                elif choice == "b":
                    do_bank_balance(player)
                elif choice == "o":
                    overview(gs, player)
                elif choice == "r":
                    page_two = False
        elif choice == "r":
            actions_main_menu()
        elif choice == "b" and remaining == 0 and not victory:
            do_boss_battle(gs, player, shop)
        else:
            continue


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
    print(f"{b}One-to-one bets.\nClassic riverbroat grambling.{rst}\n")
    t.sleep(2)

    while player.coins > 0 and player.plays > 0:    
        print(f"Coins: {g}{player.coins}{rst} {d}|{rst} Plays: {c}{player.plays}{rst}\n")
        choice = input(f"What's your wager? (q to exit):\n{b}>{rst} ").strip().lower()

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
                    print(f"\n{g}Lucky guess, bozo! You won {wager} coins.{rst}\n")
                    play_sound('golf_clap')
                    if 'Grambling Addict' in player.perks:
                        print(f"{p}Payout increased 5% with Grambling Addict!{rst}\n")
                        player.coins += int(wager * 1.05)
                        player.casino_won += int(wager * 1.05)
                    else:
                        player.coins += wager
                        player.casino_won += wager
                    player.plays -= 1
                    t.sleep(2)
                    continue
                else: 
                    print(f"\n{b}Bozo's blunder. Classic. Could've seen that coming from six or eight miles away.{rst}\n")
                    player.coins -= wager
                    player.casino_lost += wager
                    player.plays -= 1
                    t.sleep(2)
                    continue
                        
        else:
            print(f"{y}Invalid choice.{rst}")
            continue
    
    if player.plays == 0:
        print(f"{b}You're out of plays. Buy a perk or level up, bozo.{rst}")
        t.sleep(2)
        get_current_music()
        play_area_theme(player)
        return    
    elif player.coins == 0:
        print(f"{b}You're out of coins. Get lost, bozo.{rst}")
        t.sleep(2)
        get_current_music()
        play_area_theme(player)
        return  


def overview(gs, player):
    from stw_data import Results
    pc = p_color(player)

    width = 18  # adjust if you want wider/narrower labels

    print(f"{'Current Level':<{width}} {d}|{rst} {c}{player.lvl}{rst}")
    print(f"{'Current HP':<{width}} {d}|{rst} {pc}{player.hp}/{player.max_hp}{rst}")

    print(f"{'Coins':<{width}} {d}|{rst} {g}{player.coins}{rst}")
    print(f"{'Bank':<{width}} {d}|{rst} {g}{player.bank}{rst}")
    print(f"{'Deposits':<{width}} {d}|{rst} {o}{Results['deposit']}{rst}")
    print(f"{'Withdrawals':<{width}} {d}|{rst} {o}{Results['withdraw']}{rst}")
    print(f"{'Interest Earned':<{width}} {d}|{rst} {g}{player.interest}{rst}")

    print(f"{'Casino Won':<{width}} {d}|{rst} {g}+{player.casino_won}{rst}")
    print(f"{'Casino Lost':<{width}} {d}|{rst} {r}-{player.casino_lost}{rst}")

    print(f"{'Hits':<{width}} {d}|{rst} {c}{Results['hit']}{rst}")
    print(f"{'Misses':<{width}} {d}|{rst} {c}{Results['miss']}{rst}")
    print(f"{'Critical Hits':<{width}} {d}|{rst} {c}{Results['crit']}{rst}")

    print(f"{'Enemies Killed':<{width}} {d}|{rst} {r}{Results['kill']}{rst}")
    print(f"{'Bounties Claimed':<{width}} {d}|{rst} {p}{Results['bounty_collected']}{rst}")

    areas_cleared = sum(1 for count in gs.area_enemies.values() if count == 0)
    print(f"{'Areas Cleared':<{width}} {d}|{rst} {b}{areas_cleared}{rst}")

    bosses_defeated = sum(1 for data in gs.boss_defeated.values() if data['defeated'])
    print(f"{'Bosses Defeated':<{width}} {d}|{rst} {r}{bosses_defeated}{rst}")

    print(f"{'Items Purchased':<{width}} {d}|{rst} {c}{Results['buy_item']}{rst}")
    print(f"{'Items Used':<{width}} {d}|{rst} {c}{Results['use_item']}{rst}")
    print(f"{'Weapons Purchased':<{width}} {d}|{rst} {c}{Results['buy_weapon']}{rst}")
    print(f"{'Perks Owned':<{width}} {d}|{rst} {c}{Results['buy_perk']}{rst}")

    print(f"{'Times Traveled':<{width}} {d}|{rst} {b}{Results['travel']}{rst}")
    input(f"{b}>{rst} ")



def do_explore(gs, player, Enemy, shop):
    # 40% chance of enemy (10% for elite), 15% for item, 15% weapon, 20% coins, 10% dry

    if player.lives > 0:
        player.alive = True
    roll = random.random()
    if roll < 0.4:
        enemy = Enemy.spawn_enemy_for_area(player.current_area)
        while enemy.type in ('boss', 'boss_final'):
            enemy = Enemy.spawn_enemy_for_area(player.current_area)
        if random.random() < 0.10:  
            enemy.name = f"Elite {enemy.name}"
            enemy.hp = int(enemy.hp * 1.5)
            enemy.max_hp = int(enemy.max_hp * 1.5)
            enemy.coins = int(enemy.coins * 1.5)
            print(f"{y}An enemy appears!{rst} {p}(Elite enemy!)")
        else:
            print(f"{y}An enemy appears!{rst}")
        t.sleep(1)
        battle(player, enemy, gs, shop)
    elif 0.4 <= roll < 0.55:
        if len(player.items) < player.max_items:
            item_dict = random.choice(Items)
            item = item_dict['name']
            player.add_item(item)
            print(f"{c}{item} added to sack!{rst}")
            t.sleep(1)
            return
        else:
            print('Your item sack is full!')
            t.sleep(1)
            return
    elif 0.55 <= roll < 0.7:
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
    elif 0.7 <= roll < 0.9:
        if 'Metal Detective' in player.perks:
            coins = random.randint(10, 50)
        else:
            coins = random.randint(10, 30)
        print(f'{g}You found {coins} coins!')
        t.sleep(1)
        player.coins += coins
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

        choice = input(f"\nWhich weapon would you like to equip? (q to exit): \n{b}>{rst} ").strip().lower()
        if choice == 'q':
            return
        
        if choice.isdigit():
            num = int(choice)

            # Weapon range
            if 1 <= num <= len(player.weapons):
                weapon = player.weapons[num - 1] # python zero index correction
                player.current_weapon = weapon 
                print(f"\n{c}{weapon} successfully equipped.")
                t.sleep(1)
                return
    
            else:
                print("\nInvalid choice.")
                t.sleep(1)


def do_shop(player, shop, gs):
    play_music('shop_theme')
    while True:
        print(f'\n{b}Welcome! You have {rst}{g}{player.coins} {rst}{b}coins.\n')
        shop.view_shop_inventory(player)

        choice = input(f"\nEnter the number you wish to buy or s to sell (q to exit):\n{b}>{rst} ").strip().lower()

        if choice == "q":
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
                    if perk['name'] == 'Wench Location' and perk['name'] in player.perks:
                        print(f"\n{y}Shopkeeper: The wench is in the {gs.wench_area}. Don't ask me how I know.")
                        t.sleep(3)
                    if perk['name'] in ("Gramblin' Man","Grambling Addict"):
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
            sellable = [w for w in player.weapons if w != 'Bare Hands']
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
                    print(f"[{i}] {c}{name:<24}{rst} {d}|{rst} Value:{rst} {g}{data['sell_value']:<3} {d}|{rst} HP: {g}+{data['hp']}")
                else:
                    data, uses_display = p_uses_weapons(player, weapon)

                    print(
                        f"[{i}] {c}{name:<24}{rst} {d}|{rst} "
                        f"Value: {g}{data['sell_value']:<3}{rst} {d}|{rst} "
                        f"DMG: {r}{data['damage']:<3}{rst} {d}|{rst} "
                        f"Accuracy: {y}{data['accuracy']:<4}{rst} {d}|{rst} "
                        f"Uses: {uses_display}"
                    )

            # --- CHOICE ---
            choice = input(f"\nEnter the number to sell (q to exit):\n{b}>{rst} ").strip().lower()
            if choice == "q":
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
                shop.sell_item(name, player)
            else:
                shop.sell_weapon(name, player)
            choice = 's'

        else:
            print(f"{y}Invalid choice.")
            t.sleep(1)  


def do_travel(gs, player):
    areas = [a['name'] for a in Areas]

    if not areas:
        print(f'\n{y}Nowhere left to go...')
        t.sleep(2)
        return

    print("\nYou can travel to the following areas: ")
    for idx, area in enumerate(areas, 1):
        print(f"[{idx}] {b}{area}")
                
    choice = input(f"\nEnter the number of where you'd like to go (q to exit):\n{b}>{rst} ").strip().lower()

    if choice == 'q':
        return
    
    if choice.isdigit():
        num = int(choice)

        if 1 <= num <= len(areas):
            area = areas[num - 1] # for python 0 index
            player.current_area = area
            print(f'\n{c}Traveling by six by eight to the {area}...')
            play_music('travel_theme')
            log_event('travel')
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
        items=['Tench Filet'],
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

    if enemy.name in ('Sledge Hammond','Bayou Bill','Captain Hole','Denny Biltmore'):
        if enemy.name == 'Bayou Bill':
            bayou_bill_intro()
        get_current_music()
        play_music('area_boss_theme')
    elif enemy.name == 'The Mayor':
        play_music('final_boss_theme')
    elif enemy.type not in ('boss','boss_final'):
        get_current_music()
        play_music('battle_theme')

    while player.hp > 0 and enemy.hp > 0:

        # Captain Hole event
        if enemy.name == 'Captain Hole' and 'Tench Filet' in player.items:
            print("Captain Hole has offered to shoot himself in the jines in exchange for your Tench Filet.")
            t.sleep(4)
            filet = input(f"Do you accept? (y or n):\n{b}> ").strip().lower()
            if filet == 'y':
                stop_music()
                player.items.remove('Tench Filet')
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
                if enemy.name == 'Denny Biltmore':
                    print("There's no turning back now!")
                    t.sleep(2)
                    continue
                elif fled:
                    print(f'\n{c}You ran away from {enemy.name}!')
                    t.sleep(1)
                    stop_music()
                    play_area_theme(player)
                    return
                else:
                    print(f"\n{y}Couldn't escape!")
                    t.sleep(1)
                    player_turn = False
            
            elif choice == 'p':          # view perks
                do_view_perks(player,gs) 
                continue

            else:
                print(f'{y}Invalid choice.')
                continue
    
        if enemy.hp <= 0:
            log_event('kill')
            if enemy.name == 'The Mayor':
                play_sound('kids_cheer')
            if enemy.name == gs.wanted:
                bounty = bounty_update(gs, player)
                if 'Elite' in enemy.name:
                    bounty *= 1.5
                player.coins += bounty
                print(f"{g}You killed {enemy.name} and collected a bounty of {bounty} coins!{rst}")
                log_event('bounty_collected')
                t.sleep(1)
            
            is_boss(gs, player, enemy)
            record_kill(gs, player)
            
            if enemy.type != 'boss_final':
                enemy.drop_loot(player)
                leveled_up = player.gain_xp(enemy) # runs it and returns boolean for level_up
                if leveled_up:
                    shop.reset_inventory(player)
                    player.visit_bank()
                refresh_wanted(gs)

            if enemy.type == 'boss' and player.current_area == gs.wench_area:
                player.hp = player.max_hp
                do_final_boss_battle(gs, player, shop)

            stop_music()
            play_area_theme(player)
            return False # battle over, enemy dead

        else:
            if enemy.name == 'Sledge Hammond':
                enemy.hp += 3
                print(f"\n{p}Sledge Hammond took steroids and restored 3 HP!{rst}")
                t.sleep(1)
            alive = enemy.attack(player)
            if not alive:
                refresh_wanted(gs)
                stop_music()
                play_area_theme(player)
                return False # battle over, player dead
                        

# ----- MAIN: START GAME LOGIC -----
def main():
    main_menu()

if __name__ == "__main__":
    main()
