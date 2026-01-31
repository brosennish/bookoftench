import savethewench.data.audio as audio

# --------- #
# Constants #
# --------- #

# Names
AXE = "Axe"
BARE_HANDS = "Bare Hands"
BAT = "Bat"
BEAR_SPRAY = "Bear Spray"
BRASS_KNUCKLES = "Brass Knuckles"
BROKEN_BOTTLE = "Broken Bottle"
CHAINSAW = "Chainsaw"
CHILI_POWDER = "Chili Powder"
CLAWS = "Claws"
CROSSBOW = "Crossbow"
CROWBAR = "Crowbar"
FIRE_AXE = "Fire Axe"
HARPOON = "Harpoon"
HATCHET = "Hatchet"
KNIFE = "Knife"
MACHETE = "Machete"
PEPPER_SPRAY = "Pepper Spray"
PICKAXE = "Pickaxe"
PISTOL = "Pistol"
POCKET_SAND = "Pocket Sand"
REVOLVER = "Revolver"
RIFLE = "Rifle"
SHOTGUN = "Shotgun"
SHOVEL = "Shovel"
SLEDGEHAMMER = "Sledgehammer"
TENCH_CANNON = "Tench Cannon"
VOODOO_STAFF = "Voodoo Staff"

# Types
BLIND = 'blind'
MELEE = 'melee'
PROJECTILE = 'projectile'
SPECIAL = 'special'

Weapons = [
    # --- Default ---
    {'name': BARE_HANDS, 'damage': 10, 'uses': -1, 'accuracy': 0.90, 'spread': 3, 'crit': 0.10,
     'cost': 0, 'sell_value': 0, 'type': MELEE, 'sound': audio.PUNCH},

    # --- Blinding / Debuff ---
    {'name': PEPPER_SPRAY, 'damage': 6, 'uses': 3, 'accuracy': 0.85, 'spread': 2,
     'crit': 0.05, 'cost': 25, 'sell_value': 12, 'type': BLIND, 'sound': '',
     'blind_effect': 0.50, 'blind_turns_min': 2, 'blind_turns_max': 4},

    {'name': BEAR_SPRAY, 'damage': 0, 'uses': 1, 'accuracy': 0.85, 'spread': 0, 'crit': 0.00,
     'cost': 60, 'sell_value': 30, 'type': BLIND, 'sound': '',
     'blind_effect': 0.75, 'blind_turns_min': 2, 'blind_turns_max': 4},

    {'name': CHILI_POWDER, 'damage': 4, 'uses': 1, 'accuracy': 0.90, 'spread': 1,
     'crit': 0.02, 'cost': 30, 'sell_value': 15, 'type': BLIND, 'sound': '',
     'blind_effect': 0.15, 'blind_turns_min': 3, 'blind_turns_max': 5},

    {'name': POCKET_SAND, 'damage': 0, 'uses': 1, 'accuracy': 0.90, 'spread': 0, 'crit': 0.00,
     'cost': 20, 'sell_value': 8, 'type': BLIND, 'sound': '',
     'blind_effect': 0.10, 'blind_turns_min': 3, 'blind_turns_max': 5},

    # --- Tier 1 ---
    {'name': KNIFE, 'damage': 16, 'uses': 8, 'accuracy': 0.88, 'spread': 4, 'crit': 0.22,
     'cost': 25, 'sell_value': 12, 'type': MELEE, 'sound': audio.BLADE},

    {'name': BROKEN_BOTTLE, 'damage': 14, 'uses': 6, 'accuracy': 0.82, 'spread': 5, 'crit': 0.20,
     'cost': 20, 'sell_value': 8, 'type': MELEE, 'sound': audio.BLADE},

    {'name': HATCHET, 'damage': 18, 'uses': 8, 'accuracy': 0.82, 'spread': 5, 'crit': 0.16,
     'cost': 30, 'sell_value': 15, 'type': MELEE, 'sound': audio.BLADE},

    # --- Tier 2 ---
    {'name': BAT, 'damage': 20, 'uses': 9, 'accuracy': 0.80, 'spread': 6, 'crit': 0.14,
     'cost': 40, 'sell_value': 20, 'type': MELEE, 'sound': audio.BLUNT},

    {'name': CROWBAR, 'damage': 22, 'uses': 8, 'accuracy': 0.80, 'spread': 5, 'crit': 0.12,
     'cost': 45, 'sell_value': 22, 'type': MELEE, 'sound': audio.BLUNT},

    {'name': BRASS_KNUCKLES, 'damage': 22, 'uses': 9, 'accuracy': 0.90, 'spread': 4, 'crit': 0.25,
     'cost': 50, 'sell_value': 25, 'type': MELEE, 'sound': audio.PUNCH},

    {'name': SHOVEL, 'damage': 20, 'uses': 7, 'accuracy': 0.78, 'spread': 5, 'crit': 0.14,
     'cost': 38, 'sell_value': 19, 'type': MELEE, 'sound': audio.BLUNT},

    # --- Tier 3 ---
    {'name': PICKAXE, 'damage': 24, 'uses': 7, 'accuracy': 0.78, 'spread': 6, 'crit': 0.12,
     'cost': 55, 'sell_value': 28, 'type': MELEE, 'sound': audio.BLUNT},

    {'name': MACHETE, 'damage': 26, 'uses': 7, 'accuracy': 0.80, 'spread': 5, 'crit': 0.18,
     'cost': 60, 'sell_value': 30, 'type': MELEE, 'sound': audio.BLADE},

    {'name': AXE, 'damage': 30, 'uses': 6, 'accuracy': 0.76, 'spread': 6, 'crit': 0.15,
     'cost': 65, 'sell_value': 32, 'type': MELEE, 'sound': audio.AXE},

    {'name': FIRE_AXE, 'damage': 32, 'uses': 6, 'accuracy': 0.75, 'spread': 6, 'crit': 0.15,
     'cost': 70, 'sell_value': 35, 'type': MELEE, 'sound': audio.AXE},

    {'name': CROSSBOW, 'damage': 34, 'uses': 5, 'accuracy': 0.90, 'spread': 3, 'crit': 0.30,
     'cost': 80, 'sell_value': 40, 'type': PROJECTILE, 'sound': audio.ARROW},

    {'name': HARPOON, 'damage': 34, 'uses': 6, 'accuracy': 0.78, 'spread': 5, 'crit': 0.22,
     'cost': 85, 'sell_value': 42, 'type': PROJECTILE, 'sound': audio.ARROW},

    # --- Tier 4 Guns ---
    {'name': PISTOL, 'damage': 30, 'uses': 6, 'accuracy': 0.82, 'spread': 4, 'crit': 0.18,
     'cost': 70, 'sell_value': 34, 'type': PROJECTILE, 'sound': audio.PISTOL},

    {'name': REVOLVER, 'damage': 36, 'uses': 5, 'accuracy': 0.68, 'spread': 5, 'crit': 0.25,
     'cost': 78, 'sell_value': 39, 'type': PROJECTILE, 'sound': audio.PISTOL},

    {'name': RIFLE, 'damage': 38, 'uses': 6, 'accuracy': 0.90, 'spread': 4, 'crit': 0.20,
     'cost': 82, 'sell_value': 41, 'type': PROJECTILE, 'sound': audio.RIFLE},

    {'name': SHOTGUN, 'damage': 40, 'uses': 4, 'accuracy': 0.74, 'spread': 6, 'crit': 0.15,
     'cost': 90, 'sell_value': 45, 'type': PROJECTILE, 'sound': audio.SHOTGUN},

    # --- Tier 5 Heavy ---
    {'name': CHAINSAW, 'damage': 38, 'uses': 6, 'accuracy': 0.70, 'spread': 6, 'crit': 0.20,
     'cost': 95, 'sell_value': 47, 'type': MELEE, 'sound': audio.CHAINSAW},

    {'name': SLEDGEHAMMER, 'damage': 40, 'uses': 10, 'accuracy': 0.68, 'spread': 6, 'crit': 0.22,
     'cost': 100, 'sell_value': 50, 'type': MELEE, 'sound': audio.BLUNT},

    # --- Special ---
    {'name': TENCH_CANNON, 'damage': 100, 'uses': 1, 'accuracy': 0.2, 'spread': 6, 'crit': 0.1,
     'cost': 100, 'sell_value': 30, 'type': PROJECTILE, 'sound': audio.SHOTGUN},

    # --- Enemy / Monster ---
    {'name': CLAWS, 'damage': 22, 'uses': -1, 'accuracy': 0.86, 'spread': 5, 'crit': 0.18,
     'cost': 0, 'sell_value': 0, 'type': SPECIAL, 'sound': audio.PUNCH},

    {'name': VOODOO_STAFF, 'damage': 28, 'uses': -1, 'accuracy': 0.76, 'spread': 5, 'crit': 0.22,
     'cost': 0, 'sell_value': 0, 'type': SPECIAL, 'sound': audio.MAGIC},
]

