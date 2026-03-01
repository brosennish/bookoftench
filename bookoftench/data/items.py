from .areas import CITY, CAVE, FOREST, SWAMP

# --- items ---
ABANDONED_EYEBALLS = "Abandoned Eyeballs"
ALIEN_REMAINS = "Alien Remains"
ANTS_ON_A_LOG = "Ants On A Log"
BAT_MATTER ="Bat Matter"
BERRIES = "Berries"
BONE_MEAL = "Bone Meal"
CAMPBELLS_GOOP = "Campbell's Goop"
CANNED_HORSE = "Canned Horse"
CARP_FILET = "Carp Filet"
CATFISH_FILET = "Catfish Filet"
CRABS_ON_RYE = "Crabs on Rye"
CRAY = "Cray"
EAGLE_EGG = "Eagle Egg"
EGG_ON_EGGS = "Egg on Eggs"
EGGS_ON_EGG = "Eggs on Egg"
FROZEN_WAFFLE = "Frozen Waffle"
GATOR_TESTICLES = "Gator Testicles"
GIANT_TENTACLE = "Giant Tentacle"
GIZZARDS_AND_LIVERS = "Gizzards and Livers"
GOBY = "Goby"
HOG_LOINS = "Hog Loins"
IOU = "IOU"
KRILL = "Krill"
LACED_HONEY = "Laced Honey"
LOST_SAUCE = "Lost Sauce"
MOONSHINE = "Moonshine"
MOREL = "Morel"
MUSKRAT_SKEWER = "Muskrat Skewer"
MYSTERY_MEAT = "Mystery Meat"
MYSTICAL_MUSHROOMS = "Mystical Mushrooms"
OCEAN_MAN_LUNCH_BOX = "Ocean Man Lunch Box"
ORGANIC_SLUDGE = "Organic Sludge"
OWL_EGG = "Owl Egg"
PANTHER_LOINS = "Panther Loins"
SMOKE_BOMB = "Smoke Bomb"
SOMEWHAT_SPICY_NOODLES = "Somewhat Spicy Noodles"
SOUR_MILK = "Sour Milk"
STALE_GREENS = "Stale Greens"
SUSPICIOUS_GUMBO = "Suspicious Gumbo"
TENCH_FILET = "Tench Filet"
TOAD_STOOL = "Toad Stool"
UNIDENTIFIED_MUSHROOMS = "Unidentified Mushrooms"
UNWANTED_PROTEIN = "Unwanted Protein"
VERY_SPICY_NOODLES = "Very Spicy Noodles"
WORMHOLE = "Wormhole"

# --- types ---
FLEE = "Flee"
NORMAL = "Normal"

Items = [
    # --- SPECIAL ---
    {'name': IOU, 'type': FLEE, 'hp': 0, 'cost': 10, 'sell_value': 3, 'areas': [CAVE, CITY, FOREST, SWAMP], 'desc': 'Use to escape from battle'},
    {'name': SMOKE_BOMB, 'type': FLEE, 'hp': 0, 'cost': 20, 'sell_value': 7, 'areas': [CAVE, CITY, FOREST, SWAMP], 'desc': 'Use to escape from battle'},
    {'name': WORMHOLE, 'type': FLEE, 'hp': 0, 'cost': 30, 'sell_value': 11, 'areas': [CAVE, CITY, FOREST, SWAMP],
     'desc': 'Use to escape from battle'},

    # --- Tier 1 (10 HP) ---
    {'name': ANTS_ON_A_LOG, 'type': NORMAL, 'hp': 10, 'cost': 11, 'sell_value': 4, 'areas': [FOREST, SWAMP], 'desc': None},
    {'name': BERRIES, 'type': NORMAL, 'hp': 10, 'cost': 11, 'sell_value': 4, 'areas': [FOREST], 'desc': None},
    {'name': BONE_MEAL, 'type': NORMAL, 'hp': 10, 'cost': 12, 'sell_value': 5, 'areas': [CAVE, CITY], 'desc': None},
    {'name': FROZEN_WAFFLE, 'type': NORMAL, 'hp': 10, 'cost': 10, 'sell_value': 4, 'areas': [CITY], 'desc': None},
    {'name': GOBY, 'type': NORMAL, 'hp': 10, 'cost': 11, 'sell_value': 4, 'areas': [CAVE, SWAMP], 'desc': None},
    {'name': KRILL, 'type': NORMAL, 'hp': 10, 'cost': 11, 'sell_value': 4, 'areas': [CITY], 'desc': None},
    {'name': SOUR_MILK, 'type': NORMAL, 'hp': 10, 'cost': 10, 'sell_value': 4, 'areas': [CITY, FOREST, SWAMP], 'desc': None},
    {'name': STALE_GREENS, 'type': NORMAL, 'hp': 10, 'cost': 12, 'sell_value': 5, 'areas': [CAVE, CITY], 'desc': None},
    {'name': TOAD_STOOL, 'type': NORMAL, 'hp': 10, 'cost': 11, 'sell_value': 4, 'areas': [FOREST, SWAMP], 'desc': None},

    # --- Tier 2 (16–20 HP) ---
    {'name': BAT_MATTER, 'type': NORMAL, 'hp': 15, 'cost': 16, 'sell_value': 6, 'areas': [CAVE], 'desc': None},
    {'name': CAMPBELLS_GOOP, 'type': NORMAL, 'hp': 20, 'cost': 22, 'sell_value': 9, 'areas': [CITY, CAVE, FOREST], 'desc': None},
    {'name': CRAY, 'type': NORMAL, 'hp': 20, 'cost': 21, 'sell_value': 8, 'areas': [CAVE, SWAMP], 'desc': None},
    {'name': EGG_ON_EGGS, 'type': NORMAL, 'hp': 18, 'cost': 19, 'sell_value': 8, 'areas': [CAVE, CITY, FOREST, SWAMP], 'desc': None},
    {'name': EGGS_ON_EGG, 'type': NORMAL, 'hp': 18, 'cost': 20, 'sell_value': 8, 'areas': [CAVE, CITY, FOREST, SWAMP], 'desc': None},
    {'name': MYSTERY_MEAT, 'type': NORMAL, 'hp': 20, 'cost': 21, 'sell_value': 8, 'areas': [CAVE, SWAMP], 'desc': None},
    {'name': MUSKRAT_SKEWER, 'type': NORMAL, 'hp': 16, 'cost': 17, 'sell_value': 7, 'areas': [SWAMP], 'desc': None},
    {'name': ORGANIC_SLUDGE, 'type': NORMAL, 'hp': 16, 'cost': 17, 'sell_value': 7, 'areas': [CITY], 'desc': None},
    {'name': SOMEWHAT_SPICY_NOODLES, 'type': NORMAL, 'hp': 18, 'cost': 19, 'sell_value': 8, 'areas': [CITY], 'desc': None},

    # --- Tier 3 (24–28 HP) ---
    {'name': ABANDONED_EYEBALLS, 'type': NORMAL, 'hp': 28, 'cost': 29, 'sell_value': 13, 'areas': [CAVE, CITY, FOREST, SWAMP], 'desc': None},
    {'name': CATFISH_FILET, 'type': NORMAL, 'hp': 26, 'cost': 27, 'sell_value': 11, 'areas': [SWAMP], 'desc': None},
    {'name': CRABS_ON_RYE, 'type': NORMAL, 'hp': 28, 'cost': 30, 'sell_value': 12, 'areas': [CAVE, CITY], 'desc': None},  # +1 noise
    {'name': GIZZARDS_AND_LIVERS, 'type': NORMAL, 'hp': 26, 'cost': 27, 'sell_value': 11, 'areas': [CITY, FOREST, SWAMP], 'desc': None},
    {'name': LOST_SAUCE, 'type': NORMAL, 'hp': 25, 'cost': 26, 'sell_value': 10, 'areas': [CAVE], 'desc': None},
    {'name': MOREL, 'type': NORMAL, 'hp': 24, 'cost': 25, 'sell_value': 10, 'areas': [FOREST], 'desc': None},
    {'name': OWL_EGG, 'type': NORMAL, 'hp': 25, 'cost': 26, 'sell_value': 10, 'areas': [FOREST], 'desc': None},
    {'name': UNWANTED_PROTEIN, 'type': NORMAL, 'hp': 24, 'cost': 25, 'sell_value': 10, 'areas': [CAVE, FOREST], 'desc': None},
    {'name': VERY_SPICY_NOODLES, 'type': NORMAL, 'hp': 24, 'cost': 24, 'sell_value': 10, 'areas': [CITY, FOREST, SWAMP], 'desc': None},

    # --- Tier 4 (30–35 HP) ---
    {'name': CANNED_HORSE, 'type': NORMAL, 'hp': 35, 'cost': 36, 'sell_value': 15, 'areas': [CITY, CAVE], 'desc': None},
    {'name': CARP_FILET, 'type': NORMAL, 'hp': 35, 'cost': 37, 'sell_value': 15, 'areas': [CITY], 'desc': None},
    {'name': EAGLE_EGG, 'type': NORMAL, 'hp': 34, 'cost': 35, 'sell_value': 14, 'areas': [FOREST], 'desc': None},
    {'name': GATOR_TESTICLES, 'type': NORMAL, 'hp': 32, 'cost': 34, 'sell_value': 14, 'areas': [SWAMP], 'desc': None},
    {'name': HOG_LOINS, 'type': NORMAL, 'hp': 35, 'cost': 36, 'sell_value': 15, 'areas': [FOREST, SWAMP], 'desc': None},
    {'name': LACED_HONEY, 'type': NORMAL, 'hp': 33, 'cost': 35, 'sell_value': 14, 'areas': [CAVE, FOREST], 'desc': None},
    {'name': MOONSHINE, 'type': NORMAL, 'hp': 34, 'cost': 36, 'sell_value': 14, 'areas': [CAVE, SWAMP], 'desc': None},
    {'name': OCEAN_MAN_LUNCH_BOX, 'type': NORMAL, 'hp': 30, 'cost': 31, 'sell_value': 13, 'areas': [CITY, FOREST], 'desc': None},
    {'name': UNIDENTIFIED_MUSHROOMS, 'type': NORMAL, 'hp': 35, 'cost': 37, 'sell_value': 16, 'areas': [CAVE, FOREST, SWAMP], 'desc': None},

    # --- Tier 5 (38–40 HP) ---
    {'name': ALIEN_REMAINS, 'type': NORMAL, 'hp': 39, 'cost': 40, 'sell_value': 20, 'areas': [FOREST], 'desc': None},
    {'name': GIANT_TENTACLE, 'type': NORMAL, 'hp': 38, 'cost': 39, 'sell_value': 16, 'areas': [CITY], 'desc': None},
    {'name': MYSTICAL_MUSHROOMS, 'type': NORMAL, 'hp': 39, 'cost': 41, 'sell_value': 16, 'areas': [CAVE, FOREST, SWAMP], 'desc': None},
    {'name': PANTHER_LOINS, 'type': NORMAL, 'hp': 37, 'cost': 38, 'sell_value': 16, 'areas': [FOREST, SWAMP], 'desc': None},
    {'name': SUSPICIOUS_GUMBO, 'type': NORMAL, 'hp': 39, 'cost': 41, 'sell_value': 16, 'areas': [FOREST, SWAMP], 'desc': None},
    {'name': TENCH_FILET, 'type': NORMAL, 'hp': 40, 'cost': 41, 'sell_value': 17, 'areas': [CITY], 'desc': None},
]
