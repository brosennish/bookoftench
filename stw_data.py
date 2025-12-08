# DATA TABLES - Areas, Enemies, Items, Weapons 
from collections import Counter
import stw_constants as const


Perks = [
    {
        'name': const.Perks.KARATE_LESSONS,
        'cost': 50,
        'description': "Bare Hands +2 damage",
        'type': 'perk',
    },
    {
        'name': const.Perks.BEER_GOGGLES,
        'cost': 85,
        'description': "Prevents blindness",
        'type': 'perk',
    },
    {
        'name': const.Perks.BROWN_FRIDAY,
        'cost': 150,  # 120 → 150
        'description': "Shop inventories contain +1 additional item",
        'type': 'perk',
    },
    {
        'name': const.Perks.SLEDGE_FUND,
        'cost': 180,  # 160 → 180
        'description': "Bank interest rate +5%",
        'type': 'perk',
    },
    {
        'name': const.Perks.LUCKY_TENCHS_FIN,
        'cost': 80,
        'description': "Crit chance +5%",
        'type': 'perk',
    },
    {
        'name': const.Perks.DOCTOR_FISH,
        'cost': 120,  # 110 → 120
        'description': "Healing items restore +2 additional HP",
        'type': 'perk',
    },
    {
        'name': const.Perks.VAGABONDAGE,
        'cost': 100,
        'description': "Carry +1 additional weapon and +1 additional item (stacks with Nomad's Land)",
        'type': 'perk',
    },
    {
        'name': const.Perks.NOMADS_LAND,
        'cost': 100,
        'description': "Carry +1 additional weapon and +1 additional item (stacks with Vagabondage)",
        'type': 'perk',
    },
    {
        'name': const.Perks.RICKETY_PICKPOCKET,
        'cost': 160,  # 130 → 160
        'description': "Steal an extra 20–30 coins from every enemy you defeat",
        'type': 'perk',
    },
    {
        'name': const.Perks.MARTIAL_ARTS_TRAINING,
        'cost': 120,  # 100 → 120
        'description': "Bare Hands +3 damage",
        'type': 'perk',
    },
    {
        'name': const.Perks.USED_SNEAKERS,
        'cost': 40,
        'description': "Flee chance +5%",
        'type': 'perk',
    },
    {
        'name': const.Perks.LEATHER_SKIN,
        'cost': 180,  # 160 → 180
        'description': "Take 10% less damage from all attacks",
        'type': 'perk',
    },
    {
        'name': const.Perks.HEALTH_NUT,
        'cost': 170,  # 150 → 170
        'description': "Gain +25% health from items",
        'type': 'perk',
    },
    {
        'name': const.Perks.ROSETTI_THE_GYM_RAT,
        'cost': 160,  # 140 → 160
        'description': "Melee weapons do +10% damage",
        'type': 'perk',
    },
    {
        'name': const.Perks.AMBROSE_BLADE,
        'cost': 140,  # 130 → 140
        'description': "Melee weapons do +3 damage",
        'type': 'perk',
    },
    {
        'name': const.Perks.NEW_SNEAKERS,
        'cost': 90,
        'description': "Flee chance +10%",
        'type': 'perk',
    },
    {
        'name': const.Perks.BULLETPROOF,
        'cost': 140,  # 130 → 140
        'description': "Take 10% less damage from guns",
        'type': 'perk',
    },
    {
        'name': const.Perks.WALLET_CHAIN,
        'cost': 90,
        'description': 'Save 25% of your coins upon death',
        'type': 'perk',
    },
    {
        'name': const.Perks.GRAMBLIN_MAN,
        'cost': 100,
        'description': 'Gain +5 plays at the casino',
        'type': 'perk',
    },
    {
        'name': const.Perks.GRAMBLING_ADDICT,
        'cost': 160,
        'description': 'Gain +5 plays and +5% payout at the casino',
        'type': 'perk',
    },
    {
        'name': const.Perks.VAMPIRIC_SPERM,
        'cost': 250,  # 200 → 250
        'description': 'Heal 3 HP every time you land a melee attack',
        'type': 'perk',
    },
    {
        'name': const.Perks.METAL_DETECTIVE,
        'cost': 120,  # 110 → 120
        'description': "Find up to 25 more coins when exploring",
        'type': 'perk',
    },
    {
        'name': const.Perks.TENCH_THE_BOUNTY_HUNTER,
        'cost': 110,  # 120 → 110 (bounties are rare)
        'description': "Earn +25 coins from each bounty enemy you defeat",
        'type': 'perk',
    },
    {
        'name': const.Perks.TENCH_EYES,
        'cost': 120,  # 130 → 120
        'description': "Projectile weapon accuracy +5%",
        'type': 'perk',
    },
    {
        'name': const.Perks.DEATH_CAN_WAIT,
        'cost': 200,  # 150 → 200
        'description': "Once per battle, a fatal blow leaves you at 1 HP",
        'type': 'perk',
    },
    {
        'name': const.Perks.BARTER_SAUCE,
        'cost': 180,  # 140 → 180
        'description': "Shop prices are 10% lower",
        'type': 'perk',
    },
    {
        'name': const.Perks.TRADE_SHIP,
        'cost': 300,
        'description': "Shop prices are 20% lower",
        'type': 'perk',
    },
    {
        'name': const.Perks.INTRO_TO_TENCH,
        'cost': 140,
        'description': "+15% XP gained from winning battles",
        'type': 'perk',
    },

    {
        'name': const.Perks.AP_TENCH_STUDIES,
        'cost': 260,
        'description': "+30% XP from battles and +1 XP from all other sources",
        'type': 'perk',
    },
    {
        'name': const.Perks.CROWS_NEST,
        'cost': 180,  # 200 → 180
        'description': "View enemies remaining in each area",
        'type': 'perk',
    },
    {
        'name': const.Perks.SOLOMON_TRAIN,
        'cost': 350,  # 300 → 350
        'description': "10% chance to negate a fatal blow and instantly kill the enemy instead",
        'type': 'perk',
    },
    {
        'name': const.Perks.WENCH_LOCATION,
        'cost': 400,
        'description': "Reveal the wench's location",
        'type': 'perk',
    },
]

Enemies = [
    # ========================
#        CITY ENEMIES
# ========================
{'name': const.Enemies.BANDIT,        'hp': 80,  'weapon': [const.Weapons.KNIFE, const.Weapons.BAT],                              'bounty': 60,  'type': 'normal'},
{'name': const.Enemies.GOON,          'hp': 100, 'weapon': [const.Weapons.CHILI_POWDER, const.Weapons.BAT, const.Weapons.PISTOL],'bounty': 75,  'type': 'normal'},
{'name': const.Enemies.PIMP,          'hp': 120, 'weapon': [const.Weapons.PEPPER_SPRAY, const.Weapons.BRASS_KNUCKLES, const.Weapons.REVOLVER],'bounty': 85,  'type': 'normal'},
{'name': const.Enemies.HOBO,          'hp': 80,  'weapon': [const.Weapons.BROKEN_BOTTLE, const.Weapons.KNIFE, const.Weapons.POCKET_SAND],     'bounty': 50,  'type': 'normal'},
{'name': const.Enemies.SERIAL_KILLER, 'hp': 120, 'weapon': [const.Weapons.KNIFE, const.Weapons.MACHETE],                          'bounty': 100, 'type': 'normal'},

# ========================
#       FOREST ENEMIES
# ========================
{'name': const.Enemies.HIKER,            'hp': 80,  'weapon': [const.Weapons.HATCHET, const.Weapons.KNIFE, const.Weapons.BEAR_SPRAY],       'bounty': 60,  'type': 'normal'},
{'name': const.Enemies.HUNTER,           'hp': 100, 'weapon': [const.Weapons.KNIFE, const.Weapons.RIFLE, const.Weapons.BEAR_SPRAY],         'bounty': 75,  'type': 'normal'},
{'name': const.Enemies.POACHER,          'hp': 120, 'weapon': [const.Weapons.CROSSBOW, const.Weapons.MACHETE, const.Weapons.BEAR_SPRAY],    'bounty': 85,  'type': 'normal'},
{'name': const.Enemies.DISGRACED_EXILE,  'hp': 100, 'weapon': [const.Weapons.HATCHET, const.Weapons.SHOVEL],                    'bounty': 70,  'type': 'normal'},

# ========================
#        CAVE ENEMIES
# ========================
{'name': const.Enemies.MINER,                 'hp': 80,  'weapon': [const.Weapons.PICKAXE, const.Weapons.KNIFE],                'bounty': 65,  'type': 'normal'},
{'name': const.Enemies.SPELUNKER,             'hp': 100, 'weapon': [const.Weapons.PICKAXE, const.Weapons.KNIFE],                'bounty': 70,  'type': 'normal'},
{'name': const.Enemies.MOLE_PERSON,           'hp': 120, 'weapon': [const.Weapons.CLAWS, const.Weapons.PICKAXE],                'bounty': 80,  'type': 'normal'},
{'name': const.Enemies.HUMANOID_CAVE_CREATURE,'hp': 120, 'weapon': [const.Weapons.CLAWS, const.Weapons.SLEDGEHAMMER],           'bounty': 95,  'type': 'normal'},

# ========================
#        SWAMP ENEMIES
# ========================
{'name': const.Enemies.HAND_FISHERMAN,  'hp': 80,  'weapon': [const.Weapons.HATCHET, const.Weapons.KNIFE],                      'bounty': 65,  'type': 'normal'},
{'name': const.Enemies.BAYOU_MAN,       'hp': 100, 'weapon': [const.Weapons.MACHETE, const.Weapons.SHOTGUN],                    'bounty': 75,  'type': 'normal'},
{'name': const.Enemies.VOODOO_PRIESTESS,'hp': 120, 'weapon': [const.Weapons.VOODOO_STAFF, const.Weapons.KNIFE, const.Weapons.CHILI_POWDER], 'bounty': 90,  'type': 'normal'},
{'name': const.Enemies.SKIN_COLLECTOR,  'hp': 110, 'weapon': [const.Weapons.MACHETE, const.Weapons.CHAINSAW],                   'bounty': 100, 'type': 'normal'},

# ========================
#        AREA BOSSES
# ========================
{'name': const.Enemies.SLEDGE_HAMMOND, 'hp': 220, 'weapon': [const.Weapons.SLEDGEHAMMER, const.Weapons.AXE, const.Weapons.CHAINSAW, const.Weapons.BRASS_KNUCKLES],
 'bounty': 0, 'type': 'boss', 'area': const.Areas.FOREST},

{'name': const.Enemies.THE_MAYOR,      'hp': 200, 'weapon': [const.Weapons.PISTOL, const.Weapons.SHOTGUN, const.Weapons.REVOLVER, const.Weapons.BRASS_KNUCKLES],
 'bounty': 0, 'type': 'boss', 'area': const.Areas.CITY},

{'name': const.Enemies.BAYOU_BILL,     'hp': 200, 'weapon': [const.Weapons.MACHETE, const.Weapons.SLEDGEHAMMER, const.Weapons.SHOTGUN, const.Weapons.CHAINSAW],
 'bounty': 0, 'type': 'boss', 'area': const.Areas.SWAMP},

{'name': const.Enemies.CAPTAIN_HOLE,   'hp': 200, 'weapon': [const.Weapons.RIFLE, const.Weapons.HARPOON, const.Weapons.KNIFE, const.Weapons.PISTOL],
 'bounty': 0, 'type': 'boss', 'area': const.Areas.CAVE},

# ========================
#        FINAL BOSS
# ========================
{'name': const.Enemies.DENNY_BILTMORE,'hp': 275, 'weapon': [const.Weapons.BRASS_KNUCKLES, const.Weapons.PISTOL, const.Weapons.REVOLVER, const.Weapons.SHOTGUN],
 'bounty': 0, 'type': 'boss_final', 'area': None},
]


Areas = [
    {'name': const.Areas.CITY,        'enemies': [const.Enemies.BANDIT, const.Enemies.GOON, const.Enemies.PIMP, const.Enemies.HOBO, const.Enemies.SERIAL_KILLER]},
    {'name': const.Areas.FOREST,      'enemies': [const.Enemies.HIKER, const.Enemies.HUNTER, const.Enemies.POACHER, const.Enemies.DISGRACED_EXILE, const.Enemies.SERIAL_KILLER]},
    {'name': const.Areas.CAVE,        'enemies': [const.Enemies.MINER, const.Enemies.SPELUNKER, const.Enemies.MOLE_PERSON, const.Enemies.HUMANOID_CAVE_CREATURE]},
    {'name': const.Areas.SWAMP,       'enemies': [const.Enemies.HAND_FISHERMAN, const.Enemies.BAYOU_MAN, const.Enemies.VOODOO_PRIESTESS, const.Enemies.SKIN_COLLECTOR]},
]


Items = [
    # --- Tier 1 (10 HP) ---
    {'name': const.Items.FROZEN_WAFFLE,         'hp': 10, 'cost':  9, 'sell_value': 3},
    {'name': const.Items.KRILL,                 'hp': 10, 'cost': 10, 'sell_value': 4},
    {'name': const.Items.STALE_GREENS,          'hp': 10, 'cost': 12, 'sell_value': 5},

    # --- Tier 2 (16–20 HP) ---
    {'name': const.Items.MUSKRAT_SKEWER,        'hp': 16, 'cost': 14, 'sell_value': 5},
    {'name': const.Items.BAG_OF_SLUDGE,         'hp': 16, 'cost': 14, 'sell_value': 5},
    {'name': const.Items.MYSTERY_MEAT,          'hp': 20, 'cost': 18, 'sell_value': 7},
    {'name': const.Items.CRAY,                  'hp': 20, 'cost': 18, 'sell_value': 7},
    {'name': const.Items.CAMPBELLS_GOOP,        'hp': 20, 'cost': 20, 'sell_value': 8},

    # --- Tier 3 (24–28 HP) ---
    {'name': const.Items.MOREL,                 'hp': 24, 'cost': 22, 'sell_value': 9},
    {'name': const.Items.PROTEIN_GLOB,          'hp': 24, 'cost': 24, 'sell_value': 10},
    {'name': const.Items.CRABS_ON_RYE,          'hp': 28, 'cost': 28, 'sell_value': 11},

    # --- Tier 4 (30–35 HP) ---
    {'name': const.Items.OCEAN_MAN_LUNCH_BOX,   'hp': 30, 'cost': 30, 'sell_value': 12},
    {'name': const.Items.GATOR_TESTICLES,       'hp': 32, 'cost': 33, 'sell_value': 13},
    {'name': const.Items.MOONSHINE,             'hp': 35, 'cost': 36, 'sell_value': 15},
    {'name': const.Items.CHICKEN_OF_THE_CAVE,   'hp': 35, 'cost': 38, 'sell_value': 16},

    # --- Tier 5 (38–40 HP) ---
    {'name': const.Items.TENCH_FILET,           'hp': 38, 'cost': 40, 'sell_value': 16},
    {'name': const.Items.UNIDENTIFIED_MUSHROOMS,'hp': 40, 'cost': 42, 'sell_value': 17},
    {'name': const.Items.CANNED_HORSE,          'hp': 40, 'cost': 42, 'sell_value': 17},
    {'name': const.Items.SUSPICIOUS_GUMBO,      'hp': 40, 'cost': 45, 'sell_value': 18},
    {'name': const.Items.HOG_LOINS,             'hp': 40, 'cost': 45, 'sell_value': 18},
]


Weapons = [
    # --- Default ---
    {'name': const.Weapons.BARE_HANDS,    'damage': 10, 'uses': -1, 'accuracy': 0.90, 'spread': 3,
     const.Events.CRIT: 0.10, 'cost': 0,  'sell_value': 0, 'type': 'melee'},

    # --- Blinding / Debuff ---
    {'name': const.Weapons.PEPPER_SPRAY, 'damage': 6, 'uses': 3, 'accuracy': 0.85, 'spread': 2,
     const.Events.CRIT: 0.05, 'cost': 25, 'sell_value': 12, 'type': 'blind'},

    {'name': const.Weapons.BEAR_SPRAY, 'damage': 0, 'uses': 1, 'accuracy': 0.85, 'spread': 0,
     const.Events.CRIT: 0.00, 'cost': 60, 'sell_value': 30, 'type': 'blind'},

    {'name': const.Weapons.CHILI_POWDER, 'damage': 4, 'uses': 1, 'accuracy': 0.90, 'spread': 1,
     const.Events.CRIT: 0.05, 'cost': 30, 'sell_value': 15, 'type': 'blind'},

    {'name': const.Weapons.POCKET_SAND, 'damage': 0, 'uses': 1, 'accuracy': 0.90, 'spread': 0,
     const.Events.CRIT: 0.00, 'cost': 20, 'sell_value': 8, 'type': 'blind'},

    # --- Tier 1 ---
    {'name': const.Weapons.KNIFE,          'damage': 16, 'uses': 8, 'accuracy': 0.88, 'spread': 4,
     const.Events.CRIT: 0.13, 'cost': 25,  'sell_value': 12, 'type': 'melee'},

    {'name': const.Weapons.BROKEN_BOTTLE,  'damage': 14, 'uses': 6, 'accuracy': 0.82, 'spread': 5,
     const.Events.CRIT: 0.15, 'cost': 20,  'sell_value': 8, 'type': 'melee'},

    {'name': const.Weapons.HATCHET,        'damage': 18, 'uses': 8, 'accuracy': 0.82, 'spread': 5,
     const.Events.CRIT: 0.13, 'cost': 30,  'sell_value': 15, 'type': 'melee'},

    # --- Tier 2 ---
    {'name': const.Weapons.BAT,            'damage': 20, 'uses': 9, 'accuracy': 0.80, 'spread': 6,
     const.Events.CRIT: 0.13, 'cost': 40,  'sell_value': 20, 'type': 'melee'},

    {'name': const.Weapons.CROWBAR,        'damage': 22, 'uses': 8, 'accuracy': 0.80, 'spread': 5,
     const.Events.CRIT: 0.12, 'cost': 45,  'sell_value': 22, 'type': 'melee'},

    {'name': const.Weapons.BRASS_KNUCKLES, 'damage': 22, 'uses': 9, 'accuracy': 0.90, 'spread': 4,
     const.Events.CRIT: 0.12, 'cost': 50,  'sell_value': 25, 'type': 'melee'},

    {'name': const.Weapons.SHOVEL,         'damage': 20, 'uses': 7, 'accuracy': 0.78, 'spread': 6,
     const.Events.CRIT: 0.14, 'cost': 38,  'sell_value': 19, 'type': 'melee'},

    # --- Tier 3 ---
    {'name': const.Weapons.PICKAXE,        'damage': 24, 'uses': 7, 'accuracy': 0.78, 'spread': 7,
     const.Events.CRIT: 0.12, 'cost': 55,  'sell_value': 28, 'type': 'melee'},

    {'name': const.Weapons.MACHETE,        'damage': 26, 'uses': 7, 'accuracy': 0.80, 'spread': 6,
     const.Events.CRIT: 0.13, 'cost': 60,  'sell_value': 30, 'type': 'melee'},

    {'name': const.Weapons.AXE,            'damage': 30, 'uses': 6, 'accuracy': 0.76, 'spread': 8,
     const.Events.CRIT: 0.14, 'cost': 65,  'sell_value': 32, 'type': 'melee'},

    {'name': const.Weapons.FIRE_AXE,       'damage': 32, 'uses': 6, 'accuracy': 0.75, 'spread': 8,
     const.Events.CRIT: 0.14, 'cost': 70,  'sell_value': 35, 'type': 'melee'},

    {'name': const.Weapons.CROSSBOW,       'damage': 34, 'uses': 5, 'accuracy': 0.90, 'spread': 3,
     const.Events.CRIT: 0.14, 'cost': 85,  'sell_value': 42, 'type': 'projectile'},

    {'name': const.Weapons.HARPOON,        'damage': 34, 'uses': 6, 'accuracy': 0.78, 'spread': 6,
     const.Events.CRIT: 0.10, 'cost': 80,  'sell_value': 40, 'type': 'projectile'},

    # --- Tier 4 Guns ---
    {'name': const.Weapons.PISTOL,         'damage': 30, 'uses': 6, 'accuracy': 0.82, 'spread': 4,
     const.Events.CRIT: 0.11, 'cost': 70,  'sell_value': 34, 'type': 'projectile'},

    {'name': const.Weapons.REVOLVER,       'damage': 33, 'uses': 5, 'accuracy': 0.68, 'spread': 6,
     const.Events.CRIT: 0.11, 'cost': 78,  'sell_value': 39, 'type': 'projectile'},

    {'name': const.Weapons.RIFLE,          'damage': 35, 'uses': 6, 'accuracy': 0.90, 'spread': 4,
     const.Events.CRIT: 0.09, 'cost': 82,  'sell_value': 41, 'type': 'projectile'},

    {'name': const.Weapons.SHOTGUN,        'damage': 34, 'uses': 4, 'accuracy': 0.74, 'spread': 6,
     const.Events.CRIT: 0.08, 'cost': 90,  'sell_value': 45, 'type': 'projectile'},

    # --- Tier 5 Heavy ---
    {'name': const.Weapons.CHAINSAW,       'damage': 34, 'uses': 6, 'accuracy': 0.70, 'spread': 8,
     const.Events.CRIT: 0.12, 'cost': 95,  'sell_value': 47, 'type': 'melee'},

    {'name': const.Weapons.SLEDGEHAMMER,   'damage': 35, 'uses': 10, 'accuracy': 0.68, 'spread': 8,
     const.Events.CRIT: 0.13, 'cost': 100, 'sell_value': 50, 'type': 'melee'},

    # --- Enemy / Monster ---
    {'name': const.Weapons.CLAWS,          'damage': 22, 'uses': -1, 'accuracy': 0.86, 'spread': 4,
     const.Events.CRIT: 0.12, 'cost': 0,  'sell_value': 0, 'type': 'special'},

    {'name': const.Weapons.VOODOO_STAFF,   'damage': 28, 'uses': -1, 'accuracy': 0.76, 'spread': 7,
     const.Events.CRIT: 0.14, 'cost': 0,  'sell_value': 0, 'type': 'special'},
]

# COUNTERS: Initialize at zero

Results = Counter({
    const.Events.HIT: 0,
    const.Events.MISS: 0,
    const.Events.CRIT: 0,
    const.Events.WEAPON_BROKE: 0,
    const.Events.FLEE: 0,
    const.Events.KILL: 0,
    const.Events.BUY_ITEM: 0,
    const.Events.SELL_ITEM: 0,
    const.Events.BUY_PERK: 0,
    const.Events.USE_ITEM: 0,
    const.Events.BUY_WEAPON: 0,
    const.Events.SELL_WEAPON: 0,
    const.Events.SWAP_WEAPON: 0,
    const.Events.LEVEL_UP: 0,
    const.Events.TRAVEL: 0,
    const.Events.DEPOSIT: 0,
    const.Events.WITHDRAW: 0,
    const.Events.BOUNTY_COLLECTED: 0,
})