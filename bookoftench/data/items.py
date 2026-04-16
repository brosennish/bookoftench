from .areas import CITY, CAVE, FOREST, SWAMP
from .audio import DRINK, WHIFF, POSITIVE, MAGIC, SPRAY, EAT

# --- items ---
ABANDONED_EYEBALLS = "Abandoned Eyeballs"
ACCURACY_SEARUM = "Accuracy Searum"
ALIEN_REMAINS = "Alien Remains"
ANTS_ON_A_LOG = "Ants On A Log"
ASHWAGANDHA_GUMMIES = "Ashwagandha Gummies"
BAT_MATTER ="Bat Matter"
BERRIES = "Berries"
BONE_MEAL = "Bone Meal"
BOOMERANG = "Boomerang"
CAMPBELLS_GOOP = "Campbell's Goop"
CANNED_HORSE = "Canned Horse"
CARP_FILET = "Carp Filet"
CATFISH_FILET = "Catfish Filet"
CRABS_ON_RYE = "Crabs on Rye"
CRAY = "Cray"
CRITICAL_BASS = "Critical Bass"
EAGLE_EGG = "Eagle Egg"
EGG_ON_EGGS = "Egg on Eggs"
EGGS_ON_EGG = "Eggs on Egg"
ENERGY_CRYSTAL = "Energy Crystal"
FERMENTED_CELERY_MILK = "Fermented Celery Milk"
FLACCID_ACID = "Flaccid Acid"
FROZEN_WAFFLE = "Frozen Waffle"
GATOR_TESTICLES = "Gator Testicles"
GIANT_TENTACLE = "Giant Tentacle"
GIZZARDS_AND_LIVERS = "Gizzards and Livers"
GOBY = "Goby"
HOG_LOINS = "Hog Loins"
HTH = "HTH"
IOU = "IOU"
KRILL = "Krill"
LACED_HONEY = "Laced Honey"
LOST_SAUCE = "Lost Sauce"
MOON_RUNE = "Moon Rune"
MOONSHINE = "Moonshine"
MOREL = "Morel"
MUSKRAT_SKEWER = "Muskrat Skewer"
MYSTERY_MEAT = "Mystery Meat"
MYSTICAL_MUSHROOMS = "Mystical Mushrooms"
nPnG = "nPnG"
OCEAN_MAN_LUNCH_BOX = "Ocean Man Lunch Box"
ORGANIC_SLUDGE = "Organic Sludge"
OWL_EGG = "Owl Egg"
OXYGENATED_BIOFILM = "Oxygenated Biofilm"
PANTHER_LOINS = "Panther Loins"
PHOTOSYNTHOPHYL = "Photosynthophyl"
SMOKE_BOMB = "Smoke Bomb"
SOMEWHAT_SPICY_NOODLES = "Somewhat Spicy Noodles"
SOUR_MILK = "Sour Milk"
STALE_GREENS = "Stale Greens"
SUSPICIOUS_GUMBO = "Suspicious Gumbo"
TENCH_FILET = "Tench Filet"
TENCHTOSTERONE = "Tenchtosterone"
TOAD_STOOL = "Toad Stool"
UNIDENTIFIED_MUSHROOMS = "Unidentified Mushrooms"
UNWANTED_PROTEIN = "Unwanted Protein"
VERY_SPICY_NOODLES = "Very Spicy Noodles"
WORMHOLE = "Wormhole"

# --- types ---
CRIT = "crit"      # affects player attack critical hit odds
DMG = "dmg"        # affects player attack damage
ENEMY = "enemy"    # used against enemy
FLEE = "flee"      # used to escape from battle
HEALTH = "health"  # non-normal item used to restore HP
NORMAL = "normal"  # normal item used to restore HP
STAT = "stat"      # used to mutate one or more player stats

Items = [
    # --- Tier 1 (10 HP) ---
    {'name': ANTS_ON_A_LOG, 'type': NORMAL, 'hp': 10, 'cost': 10, 'sell_value': 4, 'areas': [FOREST, SWAMP], 'desc': None,
     'sound': EAT},
    {'name': BERRIES, 'type': NORMAL, 'hp': 10, 'cost': 9, 'sell_value': 4, 'areas': [FOREST], 'desc': None,
     'sound': EAT},
    {'name': BONE_MEAL, 'type': NORMAL, 'hp': 10, 'cost': 12, 'sell_value': 5, 'areas': [CAVE, CITY], 'desc': None,
     'sound': EAT},
    {'name': FROZEN_WAFFLE, 'type': NORMAL, 'hp': 10, 'cost': 12, 'sell_value': 4, 'areas': [CITY], 'desc': None,
     'sound': EAT},
    {'name': GOBY, 'type': NORMAL, 'hp': 10, 'cost': 10, 'sell_value': 4, 'areas': [CAVE, SWAMP], 'desc': None,
     'sound': EAT},
    {'name': KRILL, 'type': NORMAL, 'hp': 10, 'cost': 12, 'sell_value': 4, 'areas': [CITY], 'desc': None,
     'sound': EAT},
    {'name': SOUR_MILK, 'type': NORMAL, 'hp': 10, 'cost': 10, 'sell_value': 4, 'areas': [CITY, FOREST, SWAMP], 'desc': None,
     'sound': DRINK},
    {'name': STALE_GREENS, 'type': NORMAL, 'hp': 10, 'cost': 9, 'sell_value': 5, 'areas': [CAVE, CITY], 'desc': None,
     'sound': EAT},
    {'name': TOAD_STOOL, 'type': NORMAL, 'hp': 10, 'cost': 9, 'sell_value': 4, 'areas': [FOREST, SWAMP], 'desc': None,
     'sound': EAT},

    # --- Tier 2 (16–20 HP) ---
    {'name': BAT_MATTER, 'type': NORMAL, 'hp': 15, 'cost': 16, 'sell_value': 6, 'areas': [CAVE], 'desc': None,
     'sound': EAT},
    {'name': CAMPBELLS_GOOP, 'type': NORMAL, 'hp': 20, 'cost': 22, 'sell_value': 9, 'areas': [CITY, CAVE, FOREST], 'desc': None,
     'sound': DRINK},
    {'name': CRAY, 'type': NORMAL, 'hp': 20, 'cost': 22, 'sell_value': 8, 'areas': [CAVE, SWAMP], 'desc': None,
     'sound': EAT},
    {'name': EGG_ON_EGGS, 'type': NORMAL, 'hp': 18, 'cost': 20, 'sell_value': 8, 'areas': [CAVE, CITY, FOREST, SWAMP], 'desc': None,
     'sound': EAT},
    {'name': EGGS_ON_EGG, 'type': NORMAL, 'hp': 18, 'cost': 20, 'sell_value': 8, 'areas': [CAVE, CITY, FOREST, SWAMP], 'desc': None,
     'sound': EAT},
    {'name': MYSTERY_MEAT, 'type': NORMAL, 'hp': 20, 'cost': 22, 'sell_value': 8, 'areas': [CAVE, SWAMP], 'desc': None,
     'sound': EAT},
    {'name': MUSKRAT_SKEWER, 'type': NORMAL, 'hp': 16, 'cost': 17, 'sell_value': 7, 'areas': [SWAMP], 'desc': None,
     'sound': EAT},
    {'name': ORGANIC_SLUDGE, 'type': NORMAL, 'hp': 16, 'cost': 17, 'sell_value': 7, 'areas': [CITY], 'desc': None,
     'sound': DRINK},
    {'name': SOMEWHAT_SPICY_NOODLES, 'type': NORMAL, 'hp': 18, 'cost': 20, 'sell_value': 8, 'areas': [CITY], 'desc': None,
     'sound': EAT},

    # --- Tier 3 (24–28 HP) ---
    {'name': ABANDONED_EYEBALLS, 'type': NORMAL, 'hp': 28, 'cost': 32, 'sell_value': 13, 'areas': [CAVE, CITY, FOREST, SWAMP], 'desc': None,
     'sound': EAT},
    {'name': CATFISH_FILET, 'type': NORMAL, 'hp': 26, 'cost': 27, 'sell_value': 11, 'areas': [SWAMP], 'desc': None,
     'sound': EAT},
    {'name': CRABS_ON_RYE, 'type': NORMAL, 'hp': 28, 'cost': 30, 'sell_value': 12, 'areas': [CAVE, CITY], 'desc': None,
     'sound': EAT},
    {'name': GIZZARDS_AND_LIVERS, 'type': NORMAL, 'hp': 26, 'cost': 27, 'sell_value': 11, 'areas': [CITY, FOREST, SWAMP], 'desc': None,
     'sound': EAT},
    {'name': LOST_SAUCE, 'type': NORMAL, 'hp': 25, 'cost': 25, 'sell_value': 10, 'areas': [CAVE], 'desc': None,
     'sound': DRINK},
    {'name': MOREL, 'type': NORMAL, 'hp': 24, 'cost': 24, 'sell_value': 10, 'areas': [FOREST], 'desc': None,
     'sound': EAT},
    {'name': OWL_EGG, 'type': NORMAL, 'hp': 25, 'cost': 25, 'sell_value': 10, 'areas': [FOREST], 'desc': None,
     'sound': EAT},
    {'name': UNWANTED_PROTEIN, 'type': NORMAL, 'hp': 24, 'cost': 25, 'sell_value': 10, 'areas': [CAVE, FOREST], 'desc': None,
     'sound': EAT},
    {'name': VERY_SPICY_NOODLES, 'type': NORMAL, 'hp': 24, 'cost': 24, 'sell_value': 10, 'areas': [CITY, FOREST, SWAMP], 'desc': None,
     'sound': EAT},

    # --- Tier 4 (30–35 HP) ---
    {'name': CANNED_HORSE, 'type': NORMAL, 'hp': 35, 'cost': 37, 'sell_value': 15, 'areas': [CITY, CAVE], 'desc': None,
     'sound': EAT},
    {'name': CARP_FILET, 'type': NORMAL, 'hp': 35, 'cost': 35, 'sell_value': 15, 'areas': [CITY], 'desc': None,
     'sound': EAT},
    {'name': EAGLE_EGG, 'type': NORMAL, 'hp': 34, 'cost': 35, 'sell_value': 14, 'areas': [FOREST], 'desc': None,
     'sound': DRINK},
    {'name': GATOR_TESTICLES, 'type': NORMAL, 'hp': 35, 'cost': 34, 'sell_value': 14, 'areas': [SWAMP], 'desc': None,
     'sound': EAT},
    {'name': HOG_LOINS, 'type': NORMAL, 'hp': 35, 'cost': 37, 'sell_value': 15, 'areas': [FOREST, SWAMP], 'desc': None,
     'sound': EAT},
    {'name': LACED_HONEY, 'type': NORMAL, 'hp': 33, 'cost': 33, 'sell_value': 14, 'areas': [CAVE, FOREST], 'desc': None,
     'sound': DRINK},
    {'name': MOONSHINE, 'type': NORMAL, 'hp': 34, 'cost': 35, 'sell_value': 14, 'areas': [CAVE, SWAMP], 'desc': None,
     'sound': DRINK},
    {'name': OCEAN_MAN_LUNCH_BOX, 'type': NORMAL, 'hp': 34, 'cost': 35, 'sell_value': 13, 'areas': [CITY, FOREST], 'desc': None,
     'sound': EAT},
    {'name': UNIDENTIFIED_MUSHROOMS, 'type': NORMAL, 'hp': 35, 'cost': 35, 'sell_value': 16, 'areas': [CAVE, FOREST, SWAMP], 'desc': None,
     'sound': EAT},

    # --- Tier 5 (38–40 HP) ---
    {'name': ALIEN_REMAINS, 'type': NORMAL, 'hp': 39, 'cost': 40, 'sell_value': 20, 'areas': [FOREST], 'desc': None,
     'sound': EAT},
    {'name': GIANT_TENTACLE, 'type': NORMAL, 'hp': 38, 'cost': 42, 'sell_value': 16, 'areas': [CITY], 'desc': None,
     'sound': EAT},
    {'name': MYSTICAL_MUSHROOMS, 'type': NORMAL, 'hp': 39, 'cost': 38, 'sell_value': 16, 'areas': [CAVE, FOREST, SWAMP], 'desc': None,
     'sound': EAT},
    {'name': PANTHER_LOINS, 'type': NORMAL, 'hp': 37, 'cost': 42, 'sell_value': 16, 'areas': [FOREST, SWAMP], 'desc': None,
     'sound': EAT},
    {'name': SUSPICIOUS_GUMBO, 'type': NORMAL, 'hp': 39, 'cost': 40, 'sell_value': 16, 'areas': [FOREST, SWAMP], 'desc': None,
     'sound': EAT},
    {'name': TENCH_FILET, 'type': NORMAL, 'hp': 40, 'cost': 42, 'sell_value': 17, 'areas': [CITY], 'desc': None,
     'sound': EAT},

    # --- Tier 6 (50 HP) ---
    {'name': ASHWAGANDHA_GUMMIES, 'type': NORMAL, 'hp': 50, 'cost': 55, 'sell_value': 23, 'areas': [CITY, FOREST, SWAMP], 'desc': None,
     'sound': EAT},
    {'name': ENERGY_CRYSTAL, 'type': NORMAL, 'hp': 50, 'cost': 55, 'sell_value': 24, 'areas': [CAVE, CITY, SWAMP], 'desc': None,
     'sound': EAT},
    {'name': FERMENTED_CELERY_MILK, 'type': NORMAL, 'hp': 50, 'cost': 55, 'sell_value': 22, 'areas': [CITY, FOREST, SWAMP], 'desc': None,
     'sound': DRINK},
    {'name': OXYGENATED_BIOFILM, 'type': NORMAL, 'hp': 50, 'cost': 55, 'sell_value': 23, 'areas': [CAVE], 'desc': None,
     'sound': EAT},

    # --- SPECIAL ---
    {'name': ACCURACY_SEARUM, 'type': STAT, 'hp': 0, 'cost': 110, 'sell_value': 55, 'areas': [CAVE, FOREST],
     'desc': 'Increase accuracy by 0.03', 'sound': DRINK},
    {'name': BOOMERANG, 'type': ENEMY, 'hp': 0, 'cost': 45, 'sell_value': 0, 'areas': [CITY, FOREST, SWAMP],
     'desc': 'Do X damage to enemy and lose X HP', 'sound': BOOMERANG},
    {'name': CRITICAL_BASS, 'type': CRIT, 'hp': 0, 'cost': 55, 'sell_value': 18, 'areas': [CAVE, FOREST],
     'desc': 'Make your next attack a critical hit', 'sound': EAT},
    {'name': FLACCID_ACID, 'type': ENEMY, 'hp': 0, 'cost': 75, 'sell_value': 22, 'areas': [CAVE, CITY, SWAMP],
     'desc': 'Lower enemy strength by 25%', 'sound': SPRAY},
    {'name': HTH, 'type': STAT, 'hp': 0, 'cost': 110, 'sell_value': 55, 'areas': [CITY, SWAMP],
     'desc': 'Increase strength by 0.03', 'sound': POSITIVE},
    {'name': IOU, 'type': FLEE, 'hp': 0, 'cost': 10, 'sell_value': 3, 'areas': [CITY],
     'desc': 'Use to escape from battle', 'sound': WHIFF},
    {'name': MOON_RUNE, 'type': ENEMY, 'hp': 0, 'cost': 80, 'sell_value': 24, 'areas': [CAVE, FOREST],
     'desc': 'Do damage to enemy based on the Moon (requires moonlight)', 'sound': MAGIC},
    {'name': PHOTOSYNTHOPHYL, 'type': HEALTH, 'hp': 0, 'cost': 110, 'sell_value': 50, 'areas': [FOREST, SWAMP],
     'desc': 'Fully restore HP (requires sunlight)', 'sound': POSITIVE},
    {'name': SMOKE_BOMB, 'type': FLEE, 'hp': 0, 'cost': 20, 'sell_value': 7, 'areas': [CAVE, CITY, FOREST, SWAMP],
     'desc': 'Use to escape from battle', 'sound': WHIFF},
    {'name': TENCHTOSTERONE, 'type': DMG, 'hp': 0, 'cost': 95, 'sell_value': 45, 'areas': [CITY, SWAMP],
     'desc': 'Double the damage of your next melee attack', 'sound': DRINK},
    {'name': WORMHOLE, 'type': FLEE, 'hp': 0, 'cost': 30, 'sell_value': 11, 'areas': [CAVE, FOREST],
     'desc': 'Use to escape from battle', 'sound': MAGIC},
    {'name': nPnG, 'type': HEALTH, 'hp': 0, 'cost': 105, 'sell_value': 28, 'areas': [CAVE, CITY],
     'desc': 'Lose X HP and increase max HP by X', 'sound': DRINK},
]
