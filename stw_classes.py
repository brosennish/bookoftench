from dataclasses import dataclass, field
from typing import List, Dict, Union, Tuple, Optional
import random
import time as t
import sys

from stw_data import Weapons, Items, Enemies, Areas, Perks
from stw_colors import red as r, green as g, blue as b, purple as p, yellow as y, cyan as c, orange as o
from stw_colors import dim as d, reset as rst
from stw_audio import play_sound, play_music


# --- GS CLASS ---

@dataclass
class GameState:
    day: int = 1
    wench_area: str = field(default_factory=lambda: random.choice([a['name'] for a in Areas]))
    rescued: bool = False
    wanted_data: Dict[str, Union[str, int]] = field(
        default_factory=lambda: random.choice(
            [e for e in Enemies if e.get('type') not in ('boss', 'boss_final')]
        ).copy()
    )   

    boss_defeated: Dict[str, dict] = field(
    default_factory=lambda: {
        'Cave':   {'name': 'Captain Hole',  'defeated': False},
        'City':   {'name': 'The Mayor',     'defeated': False},
        'Forest': {'name': 'Sledge Hammond', 'defeated': False},
        'Swamp':  {'name': 'Bayou Bill',    'defeated': False},
        }
    )



    area_enemies: Dict[str, int] = field(
        default_factory=lambda:
        {'Cave': random.randint(10, 15),
        'City': random.randint(10, 15),
        'Forest': random.randint(10, 15),
        'Swamp': random.randint(10, 15),
        }
    )

    area_kills: Dict[str, int] = field(
        default_factory=lambda: 
        {'Cave': 0,
        'City': 0,
        'Forest': 0,
        'Swamp': 0
        }
    )
    
    wanted: str = field(init=False)
    bounty: int = field(init=False)

    def __post_init__(self):
            # Copy the values from wanted_data when the GameState is created
            self.wanted = self.wanted_data['name']
            self.bounty = self.wanted_data['bounty'] 

# --- PLAYER CLASS ---

@dataclass
class Player:
    name: str = ''
    lvl: int = 1
    hp: int = 100
    max_hp: int = 100
    xp: int = 0

    coins: int = 0
    bank: int = 0
    bank_interest_rate: float = 0.10
    interest: int = 0
    casino_won: int = 0
    casino_lost: int = 0
    plays: int = 10

    blind: bool = False
    blinded_by: str = ''
    blind_effect: float = 0.0
    blind_turns: int = 0

    current_weapon: str = 'Bare Hands'
    perks: List[str] = field(default_factory=list)
    cheat_death_ready: bool = False
    max_weapons: int = 5
    max_items: int = 5
    weapons: List[str] = field(default_factory=lambda: ['Bare Hands','Knife'])
    # no helper function used here, direct lookup from Weapons table:
    weapon_uses: Dict[str, int] = field(    # creates new list of dicts for player
        default_factory=lambda: {           # resets each game
            'Bare Hands': next(w for w in Weapons if w['name'] == 'Bare Hands')['uses'],
            'Knife': next(w for w in Weapons if w['name'] == 'Knife')['uses']
        }
    )
    
    # player starts in City with a Tench and 3 lives
    current_area: str = 'City'   
    items: List[str] = field(default_factory=lambda: ['Tench Filet'])
    alive: bool = True
    lives: int = 3

# ---------- Life & Health ----------
    
    def gain_hp(self, amount: int):
        self.hp = min(self.max_hp, self.hp + amount) # clamp on max_hp
        t.sleep(1)


    def take_damage(self, amount: int, enemy=None) -> bool:
        train_chance = 0.1

        # Apply Leather Skin first
        if 'Leather Skin' in self.perks:
            dmg = int(amount * 0.9)
        else:
            dmg = amount

        # Solomon Train: 10% chance to reverse a fatal blow
        if enemy is not None and 'Solomon Train' in self.perks:
            if self.hp - dmg <= 0:  # this hit would kill you
                if random.random() < train_chance:
                    print(f'{p}You were saved by Solomon Train!{rst}')
                    play_sound('rifle')
                    t.sleep(1)
                    enemy.take_damage(enemy.hp)  # kill the enemy instead
                    return True  # you take no damage

        # Normal damage handling
        self.hp = max(0, self.hp - dmg)  # clamp at 0

        if self.hp > 0:
            t.sleep(1)
            return True  # player survived / continue battle
        else:
            if self.cheat_death_ready:
                self.hp = 1
                print(f'{p}You survived the attack with Death Can Wait!{rst}')
                self.cheat_death_ready = False
                t.sleep(1)
                return True

        self.handle_death()
        return False  # player died / end battle
    

    def handle_death(self):
        from stw_functions import play_again

        self.lives -= 1
        print(f"\n{r}You died.{rst} Lives remaining: {y}{self.lives}")
        t.sleep(2)

        # Death penalties 
        if 'Wallet Chain' in self.perks:
            self.coins = int(self.coins * 0.25)
        else:
            self.coins = 0
        self.items = ['Tench Filet']
        self.weapons = ['Bare Hands','Knife']
        self.weapon_uses = {
            'Bare Hands': next(w for w in Weapons if w['name'] == 'Bare Hands')['uses'],
            'Knife': next(w for w in Weapons if w['name'] == 'Knife')['uses']
        }
        self.current_weapon = 'Bare Hands'
        if 'Death Can Wait' in self.perks:
            self.cheat_death_ready = True

        # Remaining lives check
        if self.lives > 0:
            self.hp = self.max_hp
            print(f"""\n{r}You wake up in a dumpster behind Showgirls 3.
You're buried beneath a pile of detritus and covered in slime...
There are parts of another man or men scattered around you.{rst}""")
            t.sleep(3)
            if self.bank > 0:
                
                self.visit_bank()
        else:
            print(f"\n{r}Game Over.")
            play_sound('devil_thunder')
            t.sleep(3)
            print(f"\n{r}You are now in Hell.")
            t.sleep(10)
            if play_again():
                return
            else:
                sys.exit()


    # ---------- Combat ----------
    
    # sound effects
    def play_weapon_sfx(self): 
        w = self.current_weapon
        if w in ('Pistol','Revolver'):
            play_sound('pistol')
        elif w in ('Bare Hands','Brass Knuckles','Claws'):
            play_sound('punch')
        elif w in ('Knife','Broken Bottle','Hatchet','Machete'):
            play_sound('blade')
        elif w in ('Axe','Fire Axe'):
            play_sound('axe')
        elif w in ('Bat','Crowbar','Pickaxe','Sledgehammer','Shovel'):
            play_sound('blunt')
        elif w == 'Chainsaw':
            play_sound('chainsaw')
        elif w == 'Rifle':
            play_sound('rifle')
        elif w == 'Shotgun':
            play_sound('shotgun')
        elif w in ('Crossbow','Harpoon'):
            play_sound('arrow')
        elif w == 'Voodoo Staff':
            play_sound('magic')

    
    def attack(self, enemy):
        from stw_functions import get_weapon_data, log_event

        # choose a valid weapon; fall back to Bare Hands
        weapon_name = self.current_weapon if self.current_weapon in self.weapons else 'Bare Hands'
        self.current_weapon = weapon_name
        weapon_data = get_weapon_data(weapon_name) # use helper to define weapon_data variable
        if not weapon_data:
            print(f"{y}{weapon_name} not found, resorting to Bare Hands.")
            t.sleep(1)
            weapon_name = 'Bare Hands'
            weapon_data = get_weapon_data('Bare Hands') # use helper to return Bare Hands weapon
            self.current_weapon = 'Bare Hands'

        # accuracy & damage
        base_accuracy = weapon_data['accuracy']

        if weapon_data['name'] in ('Pistol','Revolver','Rifle','Shotgun','Crossbow') and 'Tench Eyes' in self.perks:
            base_accuracy += 0.05
            print(f"\n{p}Accuracy increased by 5% with Tench Eyes.")
            t.sleep(1)

        if self.blind:
            base_accuracy *= (1 - self.blind_effect)
            reduction = int(self.blind_effect * 100)
            print(f"\n{p}Your accuracy is down {reduction}% from {self.blinded_by}!{rst}")
            t.sleep(1)

        if random.random() <= base_accuracy: # if float 0-1 is less than the decimal accuracy value
            spread = weapon_data.get('spread', 10)     # spread set to value (default 10 if none)
            base = weapon_data['damage'] + random.randint(-spread, spread) # base set to damage + random int within spread range
            base_floor = max(5, base) # clamp min damage to 5

            if "Lucky Tench's Fin" in self.perks:
                crit = random.random() < (weapon_data['crit'] + 0.05)
            else:
                crit = random.random() < weapon_data['crit']
            dmg = base_floor * 2 if crit else base_floor # damage determination before PERKS
            if weapon_data['name'] == 'Bare Hands':    
                if 'Karate Lessons' in self.perks:
                    print(f'\n{p}Karate Lessons increased damage by 5!')
                    dmg += 5
                    t.sleep(1)
                if 'Martial Arts Training' in self.perks:
                    print(f'\n{p}Martial Arts Training increased damage by 10!')
                    dmg += 10
                    t.sleep(1)
            if weapon_data['type'] == 'melee':
                if 'Rosetti the Gym Rat' in self.perks:
                    amount = int(weapon_data['damage']*0.1)
                    print(f'\n{p}Rosetti the Gym Rat increased damage by {amount}!{rst}')
                    dmg += amount
                    t.sleep(1)
                if weapon_data['name'] in ('Knife','Machete','Axe','Fire Axe'):
                    if 'Ambrose Blade' in self.perks:
                        print(f'\n{p}Ambrose Blade increased damage by 3!{rst}')
                        dmg += 3
                        t.sleep(1)
            if weapon_data['name'] == 'Pepper Spray':
                enemy.blind = True
                enemy.blinded_by = 'Pepper Spray'
                enemy.blind_effect = 0.50
                reduction = int(enemy.blind_effect * 100)
                enemy.blind_turns = 1
                print(f'\n{p}{enemy.name} has been pepper sprayed! Accuracy down {reduction}% for one turn.{rst}')
                t.sleep(1)
            if weapon_data['name'] == 'Bear Spray':
                enemy.blind = True
                enemy.blinded_by = 'Bear Spray'
                enemy.blind_effect = 0.75
                reduction = int(enemy.blind_effect * 100)
                enemy.blind_turns = 1
                print(f'\n{p}{enemy.name} has been bear sprayed! Accuracy down {reduction}% for one turn.{rst}')
                t.sleep(1)
            if weapon_data['name'] == 'Chili Powder':
                enemy.blind = True
                enemy.blinded_by = 'Chili Powder'
                enemy.blind_effect = 0.15
                reduction = int(enemy.blind_effect * 100)
                enemy.blind_turns = random.randint(3,5)
                print(f'\n{p}{enemy.name} has been blinded by chili powder! Accuracy down {reduction}% for {enemy.blind_turns} turns.{rst}')
                t.sleep(1)
            if weapon_data['name'] == 'Pocket Sand':
                enemy.blind = True
                enemy.blinded_by = 'Pocket Sand'
                enemy.blind_effect = 0.10
                reduction = int(enemy.blind_effect * 100)
                enemy.blind_turns = random.randint(2,4)
                print(f'\n{p}{enemy.name} has been blinded by pocket sand! Accuracy down {reduction}% for {enemy.blind_turns} turns.{rst}')
                t.sleep(1)

            print(f'\nYou attacked {enemy.name} with your {self.current_weapon} for {r}{dmg} {rst}damage!')
            if crit:
                print(f"\n{r}***Critical Hit***{rst}")
                self.play_weapon_sfx()
                log_event('crit')
            if 'Vampiric Sperm' in self.perks and weapon_data['type'] == 'melee':
                if self.hp < self.max_hp:
                    diff = self.max_hp - self.hp
                    gain = min(3, diff)
                    self.hp += gain
                    t.sleep(1)
                    print(f"\n{p}Restored {gain} HP with Vampiric Sperm!")
            t.sleep(1)
        
            # Consume THIS PLAYER'S uses (not the global template)
            uses = self.weapon_uses.get(weapon_name, weapon_data['uses'])

            if uses == -1:
                pass  # infinite: skip decrement for Bare Hands
            else:
                uses = max(0, uses - 1) # clamp min uses to 0
                self.weapon_uses[weapon_name] = uses  # update player inventory with correct uses
                if uses == 0:
                    print(f"\n{y}{weapon_name} broke!")
                    play_sound('weapon_broke')
                    t.sleep(1)
                    self.weapons.remove(weapon_name) 
                    if self.current_weapon == weapon_name:
                        self.current_weapon = 'Bare Hands'
                    if 'Bare Hands' not in self.weapons:
                        self.weapons.append('Bare Hands')
            enemy.take_damage(dmg)
            self.blind_reset()
    
        else:
            print(f'\n{y}You missed.')
            self.blind_reset()
            t.sleep(1)


    def blind_reset(self):
        if self.blind_turns > 0:
            self.blind_turns -= 1
            if self.blind_turns == 0:
                self.blind = False
                self.blinded_by = ''
                self.blind_effect = 0.0
                print(f"\n{p}You are no longer blinded!{rst}")
                t.sleep(1)


    def use_item(self):
        from stw_functions import get_item_data, p_color

        if not self.items:
            print(f"\n{y}Your inventory is dry...")
            t.sleep(1)
            return

        while True:
            print(f"\nItems {d}({len(self.items)}/{self.max_items}){rst}\n")
            item_list = list(self.items)  # snapshot so removing doesn't break indexing

            for idx, item in enumerate(item_list, 1):
                data = get_item_data(item)
                if not data:
                    print(f"[{idx}] {y}{item}{rst} {d}|{rst} {y}[missing item data]{rst}")
                    continue
                print(f"[{idx}] {c}{data['name']:<20}{rst} {d}|{rst} {g}+{data['hp']} HP")

            choice = input(f"\nWhich item would you like to use? (q to exit):\n{b}>{rst} ").strip().lower()

            if choice == "q":
                return

            if not choice.isdigit():
                print(f"{y}Invalid choice.")
                continue

            choice_idx = int(choice)

            if not (1 <= choice_idx <= len(item_list)):
                print(f"{y}Invalid choice.")
                continue

            selected_item = item_list[choice_idx - 1]
            item_data = get_item_data(selected_item)

            # Apply heal
            self.gain_hp(item_data['hp'])

            base = item_data['hp']
            has_nut = 'Health Nut' in self.perks
            has_fish = 'Doctor Fish' in self.perks

            bonus = 0
            if has_nut and has_fish:
                bonus = int(base * 0.25) + 2
                label = "Health Nut and Doctor Fish"
            elif has_nut:
                bonus = int(base * 0.25)
                label = "Health Nut"
            elif has_fish:
                bonus = 2
                label = "Doctor Fish"

            if bonus > 0:
                gain = min(self.max_hp - self.hp, bonus)
                self.gain_hp(gain)
                print(f"\n{p}You gained {gain} HP from {label}!")

            # Remove from actual inventory
            self.items.remove(selected_item)

            pc = p_color(self)

            print(f"You used {item_data['name']}:{rst} Your current HP is {pc}{self.hp}/{self.max_hp}{rst}")

            # Loop again to allow another use before taking a hit
            if not self.items:
                print(f"{y}Your inventory is dry.")
                t.sleep(1)
                return

        
    def flee(self) -> bool:
        if 'Used Sneakers' and 'New Sneakers' in self.perks:
            return random.random() < 0.65
        elif 'Used Sneakers' in self.perks:
            return random.random() < 0.55
        elif 'New Sneakers' in self.perks:
            return random.random() < 0.60
        else:
            return random.random() < 0.5
    
        
# ---------- XP & Leveling ----------
    @property # specifically made for returning a calculated value: print(player.xp_needed)
    def xp_needed(self):
        return 100 + (self.lvl - 1) * 10
    
    def level_up(self):
        # ---- core level-up effects live here ----
        self.lvl += 1
        cash_reward = 10 * self.lvl
        self.coins += cash_reward
        
        # casino
        if "Gramblin' Man" in self.perks and "Grambling Addict" in self.perks:
            self.plays = 20
        elif "Gramblin' Man" in self.perks:
            self.plays = 15
        elif "Grambling Addict" in self.perks:
            self.plays = 15
        
        # reset xp
        self.xp = 0

        if self.bank > 0:
            self.interest += int(self.bank * self.bank_interest_rate)
            self.bank += int(self.bank * self.bank_interest_rate)

        old_max = self.max_hp
        if self.max_hp < 150:
            self.max_hp += 5

        self.hp = self.max_hp

        if len(self.items) < self.max_items:
            reward = random.choice(Items)
            self.items.append(reward['name'])
        else:
            reward = None

        print(f"\n{g}You have reached Level {self.lvl}!\n")
        play_sound('great_job')
        t.sleep(2)
        print(f"{g}MAX HP: {old_max} -> {self.max_hp}{rst}")
        if reward != None:
            print(f"\n{c}Reward: {reward['name']}{rst}")
        print(f"\n{g}You were awarded {cash_reward} coins.{rst}")
        t.sleep(2)

    def gain_xp(self, enemy) -> bool:
        amount = enemy.max_hp // 3
        self.xp += amount
        print(f"\n{g}You gained {amount} XP!")
        t.sleep(1)

        leveled_up = False

        # handles cases where a big XP chunk might give multiple levels
        while self.xp >= self.xp_needed:
            self.level_up()
            leveled_up = True

        return leveled_up

     # ---------- Money ----------
    def gain_coins(self, amount: int):

        self.coins += amount
        print(f'\n{g}You gained {amount} coins. {rst}You now have {self.coins} coins.')
        t.sleep(2)

    def lose_coins(self, amount: int):

        loss = min(self.coins, amount)
        self.coins -= loss
        print(f'\n{y}You lost {loss} coins. {rst}You have {self.coins} coins remaining.')
        t.sleep(2)

    def visit_bank(self):
        from stw_functions import log_event
        
        play_music('bank_theme')
        
        visiting = True
        while visiting:
            choice = input(f"\nWould you like to visit the bank? (y or n):\n{b}>{rst} ").strip().lower()
            
            if choice == 'y':
                print('You may visit the bank each time you level up.\nDuring each visit, you may deposit or withdraw coins.'
                '\nEach time you level up, your bank value will increase by 10% + your current level.')
                
                banking = True
                while banking:
                    print(f"\nPlayer: {g}{self.coins} {rst}{d}|{rst} Bank: {g}{self.bank}{rst}")
                    
                    choice = input(f"\nWhat would you like to do? (d: deposit, w: withdraw: q: exit):\n{b}>{rst} ").strip().lower()
                    if choice == 'd':
                        selection = input(f"\nHow much would you like to deposit?\n{b}>{rst} ")
                        
                        if selection.isdigit():
                            num = int(selection)
                        else:
                            print(f"{y}Invalid amount.")
                            t.sleep(1)
                            continue

                        if num <= self.coins:
                            self.bank += num
                            self.coins -= num
                            print(f'\nYou successfully deposited {g}{num}{rst} coins into the bank.')
                            log_event('deposit')
                            t.sleep(1)
                            continue
                        elif num > self.coins:
                            print(f"{y}You don't have that many coins")
                            t.sleep(1)
                            continue
                        else:
                            print(f"{y}Invalid choice.")
                            continue
                    elif choice == 'w':
                        selection = input(f"\nHow much would you like to withdraw?\n{b}>{rst} ").strip().lower()
                        
                        if selection.isdigit():
                            num = int(selection)
                        else:
                            print(f"{y}Invalid choice.")
                            continue 
                        
                        if num <= self.bank:
                            self.bank -= num
                            self.coins += num
                            print(f'\nYou successfully withdrew {g}{num}{rst} coins from the bank.')
                            log_event('withdraw')
                            t.sleep(1)
                            continue
                        elif num > self.bank:
                            print(f"{y}Insufficient funds for withdrawal.")
                            t.sleep(1)
                            continue
                        else:
                            print(f"{y}Invalid choice.")
                            continue
                    
                    elif choice == 'q':
                        print(f"{b}Very well...")
                        t.sleep(1)
                        banking = False
                        return
                    else:
                        print(f"{y}Invalid choice.")
                        continue
            elif choice == 'n':
                print(f"{b}Very well...")
                t.sleep(1)
                return
            else:
                print(f"{y}Invalid choice.")
                continue


    # ---------- Weapons ----------
    def add_weapon(self, weapon_name: str, remaining_uses: int = None):
        from stw_functions import get_weapon_data

        if weapon_name in self.weapons: # enforce max 1 per item type
            print(f"{y}You already have this weapon.")
            t.sleep(1)
            return 
        elif len(self.weapons) >= self.max_weapons: # inventory space check
            print(f"{y}Your weapon sack is full.")
            t.sleep(1)
            return
        # add to list if new and room in sack
        elif weapon_name not in self.weapons and weapon_name not in ('Bare Hands', 'Claws', 'Voodoo Staff'):
            self.weapons.append(weapon_name)
            if remaining_uses is not None:
                self.weapon_uses[weapon_name] = remaining_uses
                print(f'{c}{weapon_name} added to weapons. Uses: {remaining_uses}{rst}')
                t.sleep(1)
            elif weapon_name not in self.weapon_uses:
                data = get_weapon_data(weapon_name)
                if data:
                    uses = data['uses']
                else:
                    data = get_weapon_data('Bare Hands')
                    uses = data['uses']
                self.weapon_uses[weapon_name] = uses
                print(f"{c}{data['name']} added to weapons. Uses: {uses}{rst}")
                t.sleep(1)
    

    def p_uses_weapons(self, weapon: str):
        from stw_functions import get_weapon_data

        weapon_data = get_weapon_data(weapon)
        uses_left = self.weapon_uses.get(weapon, weapon_data['uses'])

        if uses_left == -1:
            uses_display = f"{c}∞{rst}"
        elif uses_left == 1:
            uses_display = f"{r}{uses_left}{rst}"
        elif uses_left in (2, 3):
            uses_display = f"{y}{uses_left}{rst}"
        else:
            uses_display = f"{uses_left}{rst}"

        return weapon_data, uses_display


    def switch_weapon(self):

        if not self.weapons:
            print('\nYou have no weapons...')
            t.sleep(2)
            return

        print(f"\nWeapons {d}({len(self.weapons)}/{self.max_weapons}){rst}\n")
        for idx, weapon in enumerate(self.weapons, 1):
            weapon_data, uses_display = self.p_uses_weapons(weapon)

            print(
                f"[{idx}]{rst} {c}{weapon_data['name']:<20}{rst} {d}|{rst} "
                f"Damage: {r}{weapon_data['damage']:<3}{rst} {d}|{rst} "
                f"Accuracy: {y}{weapon_data['accuracy']:<4}{rst} {d}|{rst} "
                f"Uses: {uses_display}"
            )

        choice = input(f"\nWhich weapon would you like to equip? (q to exit): \n{b}>{rst} ").strip().lower()

        if choice == 'q':
            return

        if choice.isdigit():
            num = int(choice)

            if 1 <= num <= len(self.weapons):
                weapon = self.weapons[num - 1]
                self.current_weapon = weapon
                print(f"{c}\n{weapon} successfully equipped.{rst}")
                return
        
        else:
            print(f"{y}Invalid choice.")
            t.sleep(1)
            return

        
# ---------- Items and Perks ----------

    def add_item(self, item: str):
       
        if item in self.items:
            print(f"{y}You already have {item}!")
            t.sleep(1)
            return
        elif len(self.items) >= self.max_items:
            print(f"{y}Your item sack is full.")
            t.sleep(1)
            return
        else: 
            self.items.append(item)

    
    def add_perk(self, perk: str):

        if perk not in self.perks:
            self.perks.append(perk)
        else:
            print(f"{y}You already have {perk}!")
            t.sleep(2)

# === ENEMY CLASS ===

@dataclass
class Enemy:
    # === Core Identity & State ===
    name: str
    hp: int
    max_hp: int
    weapons: List[str]
    items: List[str]
    current_weapon: str
    type: str
    coins: int
    current_area: str
    blind: bool = False
    blinded_by: str = ''
    blind_effect: float = 0.0
    blind_turns: int = 0
    alive: bool = True
    weapon_uses: Dict[str, int] = field(
    default_factory=lambda: {
        'Bare Hands': next(w for w in Weapons if w['name'] == 'Bare Hands')['uses']
    })

    # === Spawning / Construction ===
    @classmethod # tells python this belongs to the Class itself, not an instance
    def spawn_enemy_for_area(cls, area_name: str) -> "Enemy":  # Only spawning enemies that match the current area
        from stw_functions import get_weapon_data

        ENEMY_BY_NAME = {e['name']: e for e in Enemies}
        AREA_BY_NAME  = {a['name']: a for a in Areas}
        
        area = AREA_BY_NAME[area_name]                   # KeyError if typo -> good for catching bugs
        candidates = area['enemies']                     # list of enemy names for that area
        enemy_name = random.choice(candidates)           # equal chance for now
        enemy_data = ENEMY_BY_NAME[enemy_name]
        hp_spread = 5

        return cls(
            name = enemy_data['name'],
            hp = random.randint(enemy_data['hp'] - hp_spread, enemy_data['hp'] + hp_spread),
            max_hp = enemy_data['hp'],
            weapons = list(enemy_data['weapon']),        # copy names
            weapon_uses = {
                w: random.randint(1, max(get_weapon_data(w)['uses'], 1))
                for w in enemy_data['weapon']
            },                                        
            current_weapon = random.choice(enemy_data['weapon']), # assigns random weapon from their list
            items = [],
            type = enemy_data['type'],
            coins = random.randint(5, 50),
            current_area = area_name
        )
    
    @classmethod
    def spawn_boss(cls, boss_data: dict) -> "Enemy":
        from stw_functions import get_weapon_data

        # boss_data is one of the dicts from Enemies with type 'boss' or 'boss_final'
        weapon_names = boss_data['weapon']          # <-- this is the list of weapon strings

        # pick starting weapon
        start_weapon = random.choice(weapon_names)

        # build weapon_uses safely from the Weapons table
        weapon_uses = {}
        for w in weapon_names:
            data = get_weapon_data(w)
            if data is None:
                # if you ever see this printed, it means the weapon name doesn't exist in Weapons
                print(f"\nDEBUG: No weapon data found for boss weapon '{w}'")
                t.sleep(1)
                continue
            weapon_uses[w] = data['uses']

        return cls(
            name=boss_data['name'],
            hp=boss_data['hp'],
            max_hp=boss_data['hp'],
            weapons=list(weapon_names),
            weapon_uses=weapon_uses,
            current_weapon=start_weapon,
            items=['Tench Filet'],
            type=boss_data['type'],
            coins=boss_data['bounty'],
            current_area=boss_data['area'],
        )

    
    # === Combat: Taking & Dealing Damage ===
    def denny_biltmore_dialogue(self):
        if self.name != 'Denny Biltmore':
            return
        if self.hp <= 0:
            return

        roll = random.random()

        if roll < 0.08:
            print(f"{r}Solomon.{rst}")
            t.sleep(2)
            print(f"{r}Bring a plate of drinks for me and the boy...{rst}")
            t.sleep(2)
        elif 0.08 < roll <= 0.16:
            print(f"{r}Yes, yes...{rst}")
            t.sleep(2)
            print(f"{r}Let me just place a quick phone call...{rst}")
            t.sleep(2)

    
    def bayou_bill_dialogue(self):
        if self.name != 'Bayou Bill':
            return
        if self.hp <= 0:
            return

        roll = random.random()

        if roll < 0.08:
            print(f"{r}Riverboat... riverboat... we cookin' today, boy.{rst}")
            t.sleep(2)
            print(f"{r}Gonna toss some crawdad in dat pot, mmhm.{rst}")
            t.sleep(2)
            print(f"{r}Alligator gumbo! Now we talkin'.{rst}")
            t.sleep(2)
        elif 0.08 < roll <= 0.16:
            print(f"{r}When you livin' in the swamp, ain't nobody come round lessen dey askin' for trouble...{rst}")
            t.sleep(2)

    
    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        
        if self.hp == 0:
            print(f"\n{r}{self.name} is now in Hell.{rst}\n")
            play_sound('devil_thunder')
            if self.name in ('The Mayor','Denny Biltmore'):
                play_sound('welcome_to_hell')
                t.sleep(2)
            t.sleep(2)
            return self.alive == False
        else:
            self.bayou_bill_dialogue()
            self.denny_biltmore_dialogue()
            return
        
    # sound effects
    def play_weapon_sfx(self): 
        w = self.current_weapon
        if w in ('Pistol','Revolver'):
            play_sound('pistol')
        elif w in ('Bare Hands','Brass Knuckles','Claws'):
            play_sound('punch')
        elif w in ('Knife','Broken Bottle','Hatchet','Machete'):
            play_sound('blade')# slash
        elif w in ('Axe','Fire Axe'):
            play_sound('axe')# chop
        elif w in ('Bat','Crowbar','Pickaxe','Sledgehammer','Shovel'):
            play_sound('blunt')# thud
        elif w == 'Chainsaw':
            play_sound('chainsaw')# chainsaw
        elif w == 'Rifle':
            play_sound('rifle')# rifle
        elif w == 'Shotgun':
            play_sound('shotgun')# shotgun
        elif w in ('Crossbow','Harpoon'):
            play_sound('arrow')# thunk
        elif w == 'Voodoo Staff':
            play_sound('magic')# magic whoosh


    def attack(self, player):
        from stw_functions import get_weapon_data, log_event

        # Find weapon data from global Weapons list
        weapon_data = get_weapon_data(self.current_weapon) # Next weapon is current
        if not weapon_data: 
            print(f"\n{self.current_weapon} not found, resorting to Bare Hands.")
            t.sleep(2)
            weapon_data = get_weapon_data('Bare Hands')
            self.current_weapon = 'Bare Hands'

        if self.blind:
            accuracy = weapon_data['accuracy'] * (1 - self.blind_effect)
            reduction = int(self.blind_effect * 100)
            print(f"\n{p}Accuracy down {reduction}% from {self.blinded_by}!{rst}")
            t.sleep(1)
        else:
            accuracy = weapon_data['accuracy']

        if random.random() <= accuracy:
            spread = weapon_data.get('spread', 10) # Weapon spread, default 10 if no value
            base = weapon_data['damage'] + random.randint(-spread, spread) # Base damage +/- 10
            base_floor = max(5, base) # Damage >= 5
            crit = random.random() < weapon_data['crit']
            dmg = base_floor * 2 if crit else base_floor # 2x damage if crit, otherwise dmg after spread
            if weapon_data['name'] in ('Pistol','Rifle','Revolver','Shotgun') and 'Bulletproof' in player.perks:
                print(f"\n{p}Bulletproof absorbs 10% of the damage!{rst}")
                dmg = int(dmg * 0.9)
                t.sleep(1)

            # blind effects on player
            if weapon_data['name'] == 'Pepper Spray':
                player.blind = True
                player.blinded_by = 'Pepper Spray'
                player.blind_effect = 0.50
                reduction = int(self.blind_effect * 100)
                player.blind_turns = 1
                print(f'\n{y}You have been pepper sprayed! Accuracy down {reduction}% for one turn.{rst}')
                t.sleep(1)
            if weapon_data['name'] == 'Bear Spray':
                player.blind = True
                player.blinded_by = 'Bear Spray'
                player.blind_effect = 0.75
                reduction = int(self.blind_effect * 100)
                player.blind_turns = 1
                print(f'\n{y}You have been bear sprayed! Accuracy down {reduction}% for one turn.{rst}')
                t.sleep(1)
            if weapon_data['name'] == 'Chili Powder':
                player.blind = True
                player.blinded_by = 'Chili Powder'
                player.blind_effect = 0.15
                reduction = int(self.blind_effect * 100)
                player.blind_turns = random.randint(3,5)
                print(f'\nYou have been blinded by chili powder! Accuracy down {reduction}% for {player.blind_turns} turns.{rst}')
                t.sleep(1)
            if weapon_data['name'] == 'Pocket Sand':
                player.blind = True
                player.blinded_by = 'Pocket Sand'
                player.blind_effect = 0.10
                reduction = int(self.blind_effect * 100)
                player.blind_turns = random.randint(2,4)
                print(f'\n{r}You have been blinded by pocket sand! Accuracy down {reduction}% for {player.blind_turns} turns.{rst}')
                t.sleep(1)

            if self.name == 'The Mayor' and player.hp > 0:
                coke = random.random() < 0.10
                if coke:
                    dmg *= 1.1
                    print(f"{p}The Mayor snorted something and increased damage by 10%!{rst}")
                    t.sleep(1)

            if self.name == 'Bayou Bill' and player.hp > 0:
                gator = random.random() < 0.10
                if gator:
                    bite = random.randint(3,5)
                    player.hp -= bite
                    print(f"{p}Mama Gator attacked you causing {bite} damage!{rst}")
                    play_sound('gator')
                    t.sleep(2)

            if player.alive:
                print(f"\n{self.name} attacked you with their {self.current_weapon} for {r}{dmg}{rst} damage!")
                if crit:
                    print(f"\n{r}*** Critical hit ***{rst}")
                    self.play_weapon_sfx()
                    log_event('crit')
                    t.sleep(1)
                                
                self.switch_weapon()
                alive = player.take_damage(dmg)  # T/F if the player survived or died 
                
                # blind reset logic 
                self.blind_reset()
                return alive

            return False 
        
        else:
            print(f"\n{y}{self.name} missed!")
            t.sleep(1)
            self.blind_reset()
            return True # missed, player still alive
        
    
    def blind_reset(self):
        if self.blind_turns > 0:
            self.blind_turns -= 1
            if self.blind_turns == 0:
                self.blind = False
                self.blinded_by = ''
                self.blind_effect = 0.0
                print(f"\n{p}{self.name} is no longer blinded!{rst}")
                t.sleep(1)
        

    # === Weapons: Selection & Switching ===
    def choose_weapon(self, weapons):
        self.current_weapon = random.choice(weapons)

    def switch_weapon(self):
        from stw_functions import get_weapon_data

        weapon_data = get_weapon_data(self.current_weapon)
        uses = self.weapon_uses.get(self.current_weapon, weapon_data['uses'])

        if uses == -1:
            return  # infinite: skip decrement for Bare Hands
        else:
            uses = max(0, uses - 1)
            self.weapon_uses[self.current_weapon] = uses
            if uses == 0:
                print(f"{y}\n{self.current_weapon} broke!{rst}")
                play_sound('weapon_broke')
                t.sleep(1)
                self.weapons.remove(self.current_weapon)
                if self.weapons:
                    self.current_weapon = self.weapons[0]
                else:
                    self.weapons.append('Bare Hands')
                    self.current_weapon = 'Bare Hands'
                    self.weapon_uses['Bare Hands'] = -1
            elif weapon_data['type'] == 'blind':
                # For blind weapons, switch to a different weapon if available
                available_weapons = [w for w in self.weapons if w != self.current_weapon]
                if available_weapons:
                    self.current_weapon = random.choice(available_weapons)
                else:
                    self.weapons.append('Bare Hands')
                    self.current_weapon = 'Bare Hands'
                    self.weapon_uses['Bare Hands'] = -1


    # === Loot / Rewards ===
    def drop_loot(self, player):
        from stw_functions import get_weapon_data
            
        weapon_data = get_weapon_data(self.current_weapon)
        uses = self.weapon_uses.get(self.current_weapon, weapon_data['uses'])

        player.coins += self.coins
        if 'Rickety Pickpocket' in player.perks:
            bonus = random.randint(20,30)
            player.coins += bonus
            print(f"{p}You scrounged {bonus} extra coins with Rickety Pickpocket!{rst}")

        if self.current_weapon not in ('Claws', 'Voodoo Staff', 'Bare Hands'):
            if self.current_weapon in player.weapons:
                return
            elif len(player.weapons) >= player.max_weapons:        
                return
            else:
                player.add_weapon(self.current_weapon, remaining_uses=uses)


# --- INVENTORY CLASS ---

@dataclass
class Inventory:
    bag: Dict[str, int] = field(default_factory=dict)        # e.g., {"Tench": 2, "Krill": 1}

    def add(self, name: str, qty: int = 1) -> None:          # add() to add an item
        self.bag[name] = self.bag.get(name, 0) + qty         # for bag, add the item name + qty

    def remove(self, name: str, qty: int = 1) -> bool:       # remove() to remove or decrease an item's qty
        have = self.bag.get(name, 0)                         # have equals the current qty of an item
        if have >= qty:                                   
            left = have - qty
            if left:
                self.bag[name] = left
            else:
                self.bag.pop(name)                           # remove the item from bag if there is no qty left after remove()
            return True
        return False

    def has(self, name: str, qty: int = 1) -> bool:
        return self.bag.get(name, 0) >= qty                  # checks if you have an item by whether its qty is >= 1
    

# --- SHOP CLASS ---

@dataclass
class Shop:
    item_inventory: List[Dict[str, Union [str, int]]] = field(
        default_factory=lambda: random.sample(Items, k=min(3, len(Items))
    )
)
    
    weapon_inventory: List[Dict] = field(
    default_factory=lambda: random.sample(
        [w for w in Weapons if w['name'] not in ('Bare Hands', 'Claws', 'Voodoo Staff')],
        k=3
    )
) 
    
    perk_inventory: List[Dict] = field(
    default_factory=lambda: random.sample(
        [p for p in Perks],
        k=3
    )
)

    def reset_inventory(self, player): # shop inventory resets upon level up, used in player.gain_xp
        listings = 3
        if 'Brown Friday' in player.perks:
            listings = 4
        self.item_inventory = random.sample(Items, k=listings)
        
        self.weapon_inventory = random.sample(
        [w for w in Weapons if w['name'] not in ('Bare Hands', 'Claws', 'Voodoo Staff')],
        k=listings
        )

        unsold_perks = [p for p in Perks if p['name'] not in player.perks]
        if len(unsold_perks) > 0: 
            self.perk_inventory = random.sample(
            unsold_perks, k=min(len(unsold_perks), listings)
            )
        else: 
            self.perk_inventory = []


    def view_shop_inventory(self, player):
        # figure out discount once
        perks = set(player.perks)
        discount = 1.0

        if 'Barter Sauce' in perks and 'Trade Ship' in perks:
            print(f"{p}Prices down 30% with Barter Sauce and Trade Ship!{rst}")
            discount = 0.7
        elif 'Trade Ship' in perks:
            print(f"{p}Prices down 20% with Trade Ship!{rst}")
            discount = 0.8
        elif 'Barter Sauce' in perks:
            print(f"{p}Prices down 10% with Barter Sauce!{rst}")
            discount = 0.9
    
       # ITEMS
        print(f"Items {d}({len(player.items)}/{player.max_items}){rst}\n")
        filtered_items = [i for i in self.item_inventory if i['name'] not in player.items]

        if filtered_items:
            for idx, item in enumerate(filtered_items, 1):
                print(
                    f"[{idx}] "
                    f"{c}{item['name']:<24}{rst} {d}|{rst} "
                    f"Cost: {o}{item['cost']:<3}{rst} {d}|{rst} "
                    f"HP: {g}+{item['hp']:<3}"
                )
        else:
            print(f"{d}No items available at the moment.{rst}")

        # WEAPONS
        print(f"\nWeapons {d}({len(player.weapons)}/{player.max_weapons}){rst}\n")
        filtered_weapons = [w for w in self.weapon_inventory if w['name'] not in player.weapons]

        base_index = len(filtered_items)
        if filtered_weapons:
            for idx, weapon in enumerate(filtered_weapons, 1):
                acc = weapon['accuracy']
                uses = weapon['uses']
                actual = base_index + idx

                print(
                    f"[{actual}] "
                    f"{c}{weapon['name']:<24}{rst} {d}|{rst} "
                    f"Cost: {o}{weapon['cost']:<3}{rst} {d}|{rst} "
                    f"DMG: {r}{weapon['damage']:<2}{rst} {d}|{rst} "
                    f"ACC: {y}{acc:<3}{rst} {d}|{rst} "
                    f"Uses: {uses} "
                )
        else:
            print(f"{d}No weapons available at the moment.{rst}")

        # PERKS
        print(f"\nPerks {d}({len(player.perks)}){rst}\n")
        if self.perk_inventory:
            perks_index = base_index + len(filtered_weapons) + 1
            for idx, perk in enumerate(self.perk_inventory, perks_index):
                perk_cost = int(perk['cost'] * discount)
                print(
                    f"[{idx}] "
                    f"{c}{perk['name']:<24}{rst} {d}|{rst} "
                    f"Cost: {o}{perk_cost:<3}{rst} {d}|{rst} "
                    f"{perk['description']}{rst}"
                )
        else:
            print(f"{d}No perks available at the moment.")


    def buy_item(self, item_name, player): # player buys item
        from stw_functions import get_item_data, log_event
        
        item_data = get_item_data(item_name)
        if not item_data:
            print(f'\n{y}Item not found.')
            t.sleep(1)
            return

        cost = item_data['cost']  

        if len(self.item_inventory) >= player.max_items:
            print(f"{y}Your item sack is full.")
            t.sleep(1)
            return
        
        if cost > player.coins:
            print(f"\n{y}Need more coins")
            t.sleep(1)
            return

        player.coins -= cost
        player.add_item(item_name)
        self.item_inventory.remove(item_data)
        print(f'{rst}{g}You purchased {item_name} for {cost} coins.')
        play_sound('purchase')
        t.sleep(1)
        log_event('buy_item')

    def buy_weapon(self, weapon_name: str, player): # player buys weapon
        from stw_functions import get_weapon_data, log_event
        
        weapon_data = get_weapon_data(weapon_name)
        if not weapon_data or weapon_data not in self.weapon_inventory:
            print(f'\n{y}{d}Weapon not found.')
            t.sleep(1)
            return
        
        cost = weapon_data['cost']

        if len(player.weapons) >= player.max_weapons:
            print(f"{y}Your weapon sack is full.")
            t.sleep(1)
            return

        if cost > player.coins:
            print(f'\n{y}Need more coins')
            t.sleep(1)
            return
        
        player.coins -= cost
        print(f'{g}You purchased {weapon_name} for {cost} coins.')
        play_sound('purchase')
        player.add_weapon(weapon_name)
        self.weapon_inventory.remove(weapon_data)
        log_event('buy_weapon')

    def buy_perk(self, perk_name: str, player): # player buys perk
        from stw_functions import get_perk_data, log_event
        
        perk_data = get_perk_data(perk_name)
        if not perk_data:
            print(f'\n{y}{d}Perk not found.')
            t.sleep(1) 
            return
        
        if perk_data not in self.perk_inventory:
            print(f'\n{y}{d}Perk not in shop inventory.')
            t.sleep(1)
            return
        
        if perk_data['name'] in player.perks:
            print(f'\n{y}{d}You already own this perk.')
            t.sleep(1)
            return
        
        cost = perk_data['cost']

        if cost > player.coins:
            print(f'\n{y}Need more coins')
            t.sleep(1)
            return

        player.coins -= cost
        player.add_perk(perk_data['name'])
        self.perk_inventory.remove(perk_data)
        print(f"{g}You purchased {perk_data['name']} for {cost} coins.")
        play_sound('purchase')
        log_event('buy_perk')
        
        if perk_data['name'] == 'Vagabondage':
            player.max_weapons += 1; player.max_items += 1
        if perk_data['name'] == "Nomad's Land":
            player.max_weapons += 1; player.max_items += 1
        if perk_data['name'] == 'Sledge Fund':
            player.bank_interest_rate += 0.05
        if perk_data['name'] == 'Death Can Wait':
            player.cheat_death_ready = True
        
        t.sleep(1)
        return True

    def sell_item(self, item_name, player): # player sells item
        from stw_functions import get_item_data, log_event
        
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
        log_event('sell_item')


    def calculate_sell_price(self, weapon_name, current_uses):
        from stw_functions import get_weapon_data

        data = get_weapon_data(weapon_name)
        base = data['sell_value']
        max_uses = data['uses']

        # Infinite-use weapons: always sell for base value
        if max_uses == -1:
            return base

        proportion = current_uses / max_uses
        price = base * proportion
        return max(int(price), 1)


    def sell_weapon(self, weapon_name, player):  # player sells weapon
        from stw_functions import get_weapon_data, log_event

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

        sell_value = self.calculate_sell_price(weapon_name, current_uses)

        player.coins += sell_value

        # Remove from inventory
        player.weapons.remove(weapon_name)
        player.weapon_uses.pop(weapon_name, None)

        print(f"\n{g}You sold {weapon_name} ({current_uses} uses left) for {sell_value} coins.")
        play_sound('purchase')
        t.sleep(1)
        log_event('sell_weapon')


@dataclass
class SaveGameState:
    game_state: GameState
    player: Player
    shop: Shop

