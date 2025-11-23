# DATA TABLES - Areas, Enemies, Items, Weapons 
from collections import Counter


Perks = [
    {
        'name': 'Karate Lessons',
        'cost': 50,
        'description': "Bare Hands +2 damage",
        'type': 'perk',
    },
    {
        'name': 'Brown Friday',
        'cost': 120,
        'description': "Shop inventories contain +1 listing",
        'type': 'perk',
    },
    {
        'name': "Sledge Fund",
        'cost': 160,
        'description': "Bank interest rate +5%",
        'type': 'perk',
    },
    {
        'name': "Lucky Tench's Fin",
        'cost': 80,
        'description': "Crit chance +5%",
        'type': 'perk',
    },
    {
        'name': "Doctor Fish",
        'cost': 110,
        'description': "Healing items restore +2 additional HP",
        'type': 'perk',
    },
    {
        'name': 'Vagabondage',
        'cost': 100,
        'description': "Carry +1 weapon and item",
        'type': 'perk',
    },
    {
        'name': "Nomad's Land",
        'cost': 100,
        'description': "Carry +1 weapon and item",
        'type': 'perk',
    },
    {
        'name': 'Rickety Pickpocket',
        'cost': 130,
        'description': "Steal an extra 20–30 coins from every enemy you defeat",
        'type': 'perk',
    },
    {
        'name': 'Martial Arts Training',
        'cost': 100,
        'description': "Bare Hands +3 damage",
        'type': 'perk',
    },
    {
        'name': 'Used Sneakers',
        'cost': 40,
        'description': "Flee chance +5%",
        'type': 'perk',
    },
    {
        'name': 'Leather Skin',
        'cost': 160,
        'description': "Take 10% less damage from attacks",
        'type': 'perk',
    },
    {
        'name': 'Health Nut',
        'cost': 150,
        'description': "Gain +25% health from items",
        'type': 'perk',
    },
    {
        'name': 'Rosetti the Gym Rat',
        'cost': 140,
        'description': "Melee weapons do +10% damage",
        'type': 'perk',
    },
    {
        'name': 'Ambrose Blade',
        'cost': 130,
        'description': "Melee weapons do +3 damage",
        'type': 'perk',
    },
    {
        'name': 'New Sneakers',
        'cost': 90,
        'description': "Flee chance +10%",
        'type': 'perk',
    },
    {
        'name': 'Bulletproof',
        'cost': 130,
        'description': "Take 10% less damage from guns",
        'type': 'perk',
    },
    {
        'name': 'Wallet Chain',
        'cost': 90,
        'description': 'Save 25% of your coins upon death',
        'type': 'perk',
    },
    {
        'name': "Gramblin' Man",
        'cost': 100,
        'description': 'Enjoy +5 plays at the casino',
        'type': 'perk',
    },
    {
        'name': "Grambling Addict",
        'cost': 160,
        'description': 'Enjoy +5 plays and +5% payout at the casino',
        'type': 'perk',
    },
    {
        'name': 'Vampiric Sperm',
        'cost': 200,
        'description': 'Heal 3 HP each time you land a melee attack',
        'type': 'perk',
    },
    {
        'name': 'Metal Detective',
        'cost': 110,
        'description': "Find up to 20 extra coins when exploring",
        'type': 'perk',
    },
    {
        'name': 'Tench the Bounty Hunter',
        'cost': 120,
        'description': "Earn +25 coins from each bounty enemy",
        'type': 'perk',
    },
    {
        'name': 'Tench Eyes',
        'cost': 130,
        'description': "Projectile weapon accuracy +5%",
        'type': 'perk',
    },
    {
        'name': 'Death Can Wait',
        'cost': 150,
        'description': "Once per battle, a fatal blow leaves you at 1 HP",
        'type': 'perk',
    },
    {
        'name': 'Barter Sauce',
        'cost': 140,
        'description': "Shop prices are 10% lower",
        'type': 'perk',
    },
    {
        'name': 'Trade Ship',
        'cost': 300,
        'description': "Shop prices are 20% lower",
        'type': 'perk',
    },

    {
        'name': "Crow's Nest",
        'cost': 200,
        'description': "View enemies remaining in each area",
        'type': 'perk',
    },
    {
        'name': 'Solomon Train',
        'cost': 300,
        'description': "10% chance to negate a fatal blow and instantly kill the enemy instead",
        'type': 'perk',
    },
    {
        'name': 'Wench Location',
        'cost': 400,
        'description': "Reveal the wench's location",
        'type': 'perk',
    },
]


Enemies = [
    # --- CITY ---
    {'name': 'Bandit',         'hp': 80,  'weapon': ['Knife', 'Bat'],                     'bounty': 30, 'type': 'normal'},
    {'name': 'Goon',           'hp': 100, 'weapon': ['Bat', 'Brass Knuckles', 'Pistol'],  'bounty': 40, 'type': 'normal'},
    {'name': 'Pimp',           'hp': 120, 'weapon': ['Bat', 'Brass Knuckles', 'Revolver'],'bounty': 60, 'type': 'normal'},
    {'name': 'Hobo',           'hp': 80,  'weapon': ['Broken Bottle', 'Knife'],           'bounty': 25, 'type': 'normal'},
    {'name': 'Serial Killer',  'hp': 120, 'weapon': ['Knife', 'Hatchet', 'Machete'],      'bounty': 65, 'type': 'normal'},

    # --- FOREST ---
    {'name': 'Hiker',            'hp': 80,  'weapon': ['Hatchet', 'Knife'],               'bounty': 30, 'type': 'normal'},
    {'name': 'Hunter',           'hp': 100, 'weapon': ['Machete', 'Shotgun', 'Rifle'],    'bounty': 50, 'type': 'normal'},
    {'name': 'Poacher',          'hp': 120, 'weapon': ['Crossbow', 'Machete'],            'bounty': 60, 'type': 'normal'},
    {'name': 'Disgraced Exile',  'hp': 100, 'weapon': ['Hatchet', 'Shovel'],              'bounty': 45, 'type': 'normal'},

    # --- CAVE ---
    {'name': 'Miner',                 'hp': 80,  'weapon': ['Pickaxe', 'Knife'],          'bounty': 35, 'type': 'normal'},
    {'name': 'Spelunker',             'hp': 100, 'weapon': ['Pickaxe', 'Knife'],          'bounty': 40, 'type': 'normal'},
    {'name': 'Mole Person',           'hp': 120, 'weapon': ['Claws', 'Pickaxe'],          'bounty': 55, 'type': 'normal'},
    {'name': 'Humanoid Cave Creature','hp': 120, 'weapon': ['Claws', 'Sledgehammer'],     'bounty': 65, 'type': 'normal'},

    # --- SWAMP ---
    {'name': 'Hand Fisherman',   'hp': 80,  'weapon': ['Hatchet', 'Knife'],                 'bounty': 30, 'type': 'normal'},
    {'name': 'Bayou Man',        'hp': 100, 'weapon': ['Machete', 'Shotgun'],               'bounty': 45, 'type': 'normal'},
    {'name': 'Voodoo Priestess', 'hp': 120, 'weapon': ['Voodoo Staff'],                     'bounty': 70, 'type': 'normal'},
    {'name': 'Skin Collector',   'hp': 110, 'weapon': ['Machete', 'Chainsaw', 'Harpoon'],   'bounty': 75, 'type': 'normal'},

    # --- AREA BOSSES ---
    {'name': 'Sledge Hammond',  'hp': 220, 'weapon': ['Sledgehammer', 'Axe', 'Chainsaw', 'Brass Knuckles'], 'bounty': 0,
     'type': 'boss', 'area': 'Forest'},

    {'name': 'The Mayor',      'hp': 200, 'weapon': ['Pistol', 'Shotgun', 'Revolver'], 'bounty': 0,
     'type': 'boss', 'area': 'City'},

    {'name': 'Bayou Bill',     'hp': 200, 'weapon': ['Machete', 'Sledgehammer', 'Shotgun', 'Chainsaw'], 'bounty': 0,
     'type': 'boss', 'area': 'Swamp'},

    {'name': 'Captain Hole',   'hp': 200, 'weapon': ['Revolver', 'Harpoon', 'Pickaxe'], 'bounty': 0,
     'type': 'boss', 'area': 'Cave'},

    # --- FINAL BOSS ---
    {'name': 'Denny Biltmore', 'hp': 275, 'weapon': ['Brass Knuckles', 'Pistol', 'Revolver', 'Shotgun'], 'bounty': 0,
     'type': 'boss_final', 'area': None},
]


Areas = [
    {'name': 'City',        'enemies': ['Bandit', 'Goon', 'Pimp', 'Hobo', 'Serial Killer']},
    {'name': 'Forest',      'enemies': ['Hiker', 'Hunter', 'Poacher', 'Disgraced Exile', 'Serial Killer']},
    {'name': 'Cave',        'enemies': ['Miner', 'Spelunker', 'Mole Person', 'Humanoid Cave Creature']},
    {'name': 'Swamp',       'enemies': ['Hand Fisherman', 'Bayou Man', 'Voodoo Priestess', 'Skin Collector']},
]


Items = [
    # --- Tier 1 (10 HP) ---
    {'name': 'Frozen Waffle',        'hp': 10, 'cost':  8, 'sell_value': 3},
    {'name': 'Krill',                'hp': 10, 'cost': 10, 'sell_value': 4},
    {'name': 'Stale Greens',         'hp': 10, 'cost': 12, 'sell_value': 5},

    # --- Tier 2 (16–20 HP) ---
    {'name': 'Muskrat Skewer',       'hp': 16, 'cost': 14, 'sell_value': 5},
    {'name': 'Bag of Sludge',        'hp': 16, 'cost': 14, 'sell_value': 5},
    {'name': 'Mystery Meat',         'hp': 20, 'cost': 18, 'sell_value': 7},
    {'name': 'Cray',                 'hp': 20, 'cost': 18, 'sell_value': 7},
    {'name': "Campbell's Goop",      'hp': 20, 'cost': 20, 'sell_value': 8},

    # --- Tier 3 (24–28 HP) ---
    {'name': 'Morel',                'hp': 24, 'cost': 22, 'sell_value': 9},
    {'name': 'Protein Glob',         'hp': 24, 'cost': 24, 'sell_value': 10},
    {'name': 'Crabs on Rye',         'hp': 28, 'cost': 28, 'sell_value': 11},

    # --- Tier 4 (30–35 HP) ---
    {'name': 'Adolescent Lunch Box', 'hp': 30, 'cost': 30, 'sell_value': 12},
    {'name': 'Gator Testicles',      'hp': 32, 'cost': 34, 'sell_value': 14},
    {'name': 'Moonshine',            'hp': 35, 'cost': 36, 'sell_value': 15},
    {'name': 'Chicken of the Cave',  'hp': 35, 'cost': 38, 'sell_value': 16},

    # --- Tier 5 (38–40 HP) ---
    {'name': 'Tench Filet',          'hp': 38, 'cost': 40, 'sell_value': 16},
    {'name': 'Unidentified Mushrooms','hp':40, 'cost': 42, 'sell_value': 17},
    {'name': 'Canned Horse',         'hp': 40, 'cost': 42, 'sell_value': 17},
    {'name': 'Suspicious Gumbo',     'hp': 40, 'cost': 45, 'sell_value': 18},
    {'name': 'Hog Loins',            'hp': 40, 'cost': 45, 'sell_value': 18},
]


Weapons = [
    # --- Default ---
    {'name': 'Bare Hands',  'damage': 10, 'uses': -1, 'accuracy': 0.90, 'spread': 3, 'crit': 0.10,
     'cost': 0,  'sell_value': 0, 'type': 'melee'},

    # --- Tier 1 ---
    {'name': 'Knife',          'damage': 16, 'uses': 8, 'accuracy': 0.88, 'spread': 4, 'crit': 0.22,
     'cost': 25,  'sell_value': 12, 'type': 'melee'},

    {'name': 'Broken Bottle',  'damage': 14, 'uses': 6, 'accuracy': 0.82, 'spread': 5, 'crit': 0.20,
     'cost': 20,  'sell_value': 8, 'type': 'melee'},

    {'name': 'Hatchet',        'damage': 18, 'uses': 8, 'accuracy': 0.82, 'spread': 5, 'crit': 0.16,
     'cost': 30,  'sell_value': 15, 'type': 'melee'},

    # --- Tier 2 ---
    {'name': 'Bat',            'damage': 20, 'uses': 9, 'accuracy': 0.80, 'spread': 6, 'crit': 0.14,
     'cost': 40,  'sell_value': 20, 'type': 'melee'},

    {'name': 'Crowbar',        'damage': 22, 'uses': 8, 'accuracy': 0.80, 'spread': 5, 'crit': 0.12,
     'cost': 45,  'sell_value': 22, 'type': 'melee'},

    {'name': 'Brass Knuckles', 'damage': 22, 'uses': 9, 'accuracy': 0.90, 'spread': 4, 'crit': 0.25,
     'cost': 50,  'sell_value': 25, 'type': 'melee'},

    {'name': 'Shovel',         'damage': 20, 'uses': 7, 'accuracy': 0.78, 'spread': 6, 'crit': 0.14,
     'cost': 38,  'sell_value': 19, 'type': 'melee'},

    # --- Tier 3 ---
    {'name': 'Pickaxe',        'damage': 24, 'uses': 7, 'accuracy': 0.78, 'spread': 7, 'crit': 0.12,
     'cost': 55,  'sell_value': 28, 'type': 'melee'},

    {'name': 'Machete',        'damage': 26, 'uses': 7, 'accuracy': 0.80, 'spread': 6, 'crit': 0.18,
     'cost': 60,  'sell_value': 30, 'type': 'melee'},

    {'name': 'Axe',            'damage': 30, 'uses': 6, 'accuracy': 0.76, 'spread': 8, 'crit': 0.15,
     'cost': 65,  'sell_value': 32, 'type': 'melee'},

    {'name': 'Fire Axe',       'damage': 32, 'uses': 6, 'accuracy': 0.75, 'spread': 8, 'crit': 0.15,
     'cost': 70,  'sell_value': 35, 'type': 'melee'},

    {'name': 'Crossbow',       'damage': 34, 'uses': 5, 'accuracy': 0.90, 'spread': 3, 'crit': 0.30,
     'cost': 80,  'sell_value': 40, 'type': 'projectile'},

    {'name': 'Harpoon',        'damage': 34, 'uses': 6, 'accuracy': 0.78, 'spread': 6, 'crit': 0.22,
     'cost': 85,  'sell_value': 42, 'type': 'projectile'},

    # --- Tier 4 Guns ---
    {'name': 'Pistol',         'damage': 30, 'uses': 6, 'accuracy': 0.82, 'spread': 4, 'crit': 0.18,
     'cost': 70,  'sell_value': 34, 'type': 'projectile'},

    {'name': 'Revolver',       'damage': 36, 'uses': 5, 'accuracy': 0.68, 'spread': 6, 'crit': 0.25,
     'cost': 78,  'sell_value': 39, 'type': 'projectile'},

    {'name': 'Rifle',          'damage': 38, 'uses': 6, 'accuracy': 0.90, 'spread': 4, 'crit': 0.20,
     'cost': 82,  'sell_value': 41, 'type': 'projectile'},

    {'name': 'Shotgun',        'damage': 40, 'uses': 4, 'accuracy': 0.74, 'spread': 10, 'crit': 0.15,
     'cost': 90,  'sell_value': 45, 'type': 'projectile'},

    # --- Tier 5 Heavy ---
    {'name': 'Chainsaw',       'damage': 38, 'uses': 6, 'accuracy': 0.70, 'spread': 10, 'crit': 0.20,
     'cost': 95,  'sell_value': 47, 'type': 'melee'},

    {'name': 'Sledgehammer',   'damage': 40, 'uses': 10, 'accuracy': 0.68, 'spread': 8, 'crit': 0.22,
     'cost': 100,  'sell_value': 50, 'type': 'melee'},

    # --- Enemy / Monster ---
    {'name': 'Claws',          'damage': 22, 'uses': -1, 'accuracy': 0.86, 'spread': 4, 'crit': 0.18,
     'cost': 0,  'sell_value': 0, 'type': 'special'},

    {'name': 'Voodoo Staff',   'damage': 28, 'uses': -1, 'accuracy': 0.76, 'spread': 7, 'crit': 0.22,
     'cost': 0,  'sell_value': 0, 'type': 'special'},
]


# COUNTERS: Initialize at zero

Results = Counter({
    'hit': 0,
    'miss': 0,
    'crit': 0,
    'weapon_broke': 0,
    'flee': 0,
    'kill': 0,
    'buy_item': 0,
    'sell_item': 0,
    'buy_perk': 0,
    'use_item': 0,
    'buy_weapon': 0,
    'sell_weapon': 0,
    'swap_weapon': 0,
    'level_up': 0,
    'travel': 0,
    'deposit': 0,
    'withdraw': 0,
    'bounty_collected': 0,
})