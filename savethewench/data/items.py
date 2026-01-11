from .areas import CITY, CAVE, FOREST, SWAMP

ABANDONED_EYEBALLS = "Abandoned Eyeballs"
ALIEN_REMAINS = "Alien Remains"
ANTS_ON_A_LOG = "Ants On A Log"
BONE_MEAL = "Bone Meal"
CAMPBELLS_GOOP = "Campbell's Goop"
CANNED_HORSE = "Canned Horse"
CARP_FILET = "Carp Filet"
CRABS_ON_RYE = "Crabs on Rye"
CRAY = "Cray"
EGG_ON_EGGS = "Egg on Eggs"
FROZEN_WAFFLE = "Frozen Waffle"
GATOR_TESTICLES = "Gator Testicles"
GIZZARDS_AND_LIVERS = "Gizzards and Livers"
HOG_LOINS = "Hog Loins"
KRILL = "Krill"
MOONSHINE = "Moonshine"
MOREL = "Morel"
MUSKRAT_SKEWER = "Muskrat Skewer"
MYSTERY_MEAT = "Mystery Meat"
MYSTICAL_MUSHROOMS = "Mystical Mushrooms"
OCEAN_MAN_LUNCH_BOX = "Ocean Man Lunch Box"
ORGANIC_SLUDGE = "Organic Sludge"
STALE_GREENS = "Stale Greens"
SUSPICIOUS_GUMBO = "Suspicious Gumbo"
TENCH_FILET = "Tench Filet"
TOAD_STOOL = "Toad Stool"
UNIDENTIFIED_MUSHROOMS = "Unidentified Mushrooms"
UNWANTED_PROTEIN = "Unwanted Protein"
VERY_SPICY_NOODLES = "Very Spicy Noodles"


Items = [
    # --- Tier 1 (10 HP) ---
    {'name': ANTS_ON_A_LOG, 'hp': 10, 'cost': 9, 'sell_value': 3, 'areas': [FOREST, SWAMP]},
    {'name': TOAD_STOOL, 'hp': 10, 'cost': 9, 'sell_value': 3, 'areas': [FOREST, SWAMP]},
    {'name': FROZEN_WAFFLE, 'hp': 10, 'cost': 8, 'sell_value': 4, 'areas': [CITY]},
    {'name': KRILL, 'hp': 10, 'cost': 10, 'sell_value': 4, 'areas': [CITY]},
    {'name': STALE_GREENS, 'hp': 10, 'cost': 12, 'sell_value': 5, 'areas': [CAVE, CITY]},
    {'name': BONE_MEAL, 'hp': 10, 'cost': 10, 'sell_value': 5, 'areas': [CAVE, CITY]},

    # --- Tier 2 (16–20 HP) ---
    {'name': MUSKRAT_SKEWER, 'hp': 16, 'cost': 14, 'sell_value': 5, 'areas': [SWAMP]},
    {'name': ORGANIC_SLUDGE, 'hp': 16, 'cost': 14, 'sell_value': 5, 'areas': [CITY]},
    {'name': EGG_ON_EGGS, 'hp': 18, 'cost': 14, 'sell_value': 5, 'areas': [CAVE, CITY, FOREST, SWAMP]},
    {'name': MYSTERY_MEAT, 'hp': 20, 'cost': 18, 'sell_value': 7, 'areas': [CAVE, SWAMP]},
    {'name': CRAY, 'hp': 20, 'cost': 18, 'sell_value': 7, 'areas': [CAVE, SWAMP]},
    {'name': CAMPBELLS_GOOP, 'hp': 20, 'cost': 20, 'sell_value': 8, 'areas': [CITY, CAVE, FOREST]},

    # --- Tier 3 (24–28 HP) ---
    {'name': MOREL, 'hp': 24, 'cost': 22, 'sell_value': 9, 'areas': [FOREST]},
    {'name': GIZZARDS_AND_LIVERS, 'hp': 26, 'cost': 24, 'sell_value': 9, 'areas': [CITY, FOREST, SWAMP]},
    {'name': UNWANTED_PROTEIN, 'hp': 24, 'cost': 24, 'sell_value': 10, 'areas': [CAVE, FOREST]},
    {'name': CRABS_ON_RYE, 'hp': 28, 'cost': 28, 'sell_value': 11, 'areas': [CAVE, CITY]},
    {'name': VERY_SPICY_NOODLES, 'hp': 24, 'cost': 20, 'sell_value': 10, 'areas': [CITY, FOREST, SWAMP]},
    {'name': ABANDONED_EYEBALLS, 'hp': 28, 'cost': 28, 'sell_value': 14, 'areas': [CAVE, CITY, FOREST, SWAMP]},

    # --- Tier 4 (30–35 HP) ---
    {'name': OCEAN_MAN_LUNCH_BOX, 'hp': 30, 'cost': 30, 'sell_value': 12, 'areas': [CITY, FOREST]},
    {'name': GATOR_TESTICLES, 'hp': 32, 'cost': 34, 'sell_value': 14, 'areas': [SWAMP]},
    {'name': MOONSHINE, 'hp': 34, 'cost': 36, 'sell_value': 15, 'areas': [CAVE, SWAMP]},
    {'name': CARP_FILET, 'hp': 35, 'cost': 38, 'sell_value': 16, 'areas': [CITY]},
    {'name': HOG_LOINS, 'hp': 35, 'cost': 35, 'sell_value': 16, 'areas': [FOREST, SWAMP]},
    {'name': UNIDENTIFIED_MUSHROOMS, 'hp': 35, 'cost': 35, 'sell_value': 18, 'areas': [CAVE, FOREST, SWAMP]},

    # --- Tier 5 (38–40 HP) ---
    {'name': MYSTICAL_MUSHROOMS, 'hp': 40, 'cost': 42, 'sell_value': 17, 'areas': [CAVE, FOREST, SWAMP]},
    {'name': CANNED_HORSE, 'hp': 40, 'cost': 42, 'sell_value': 17, 'areas': [CITY, CAVE]},
    {'name': SUSPICIOUS_GUMBO, 'hp': 39, 'cost': 42, 'sell_value': 18, 'areas': [FOREST, SWAMP]},
    {'name': ALIEN_REMAINS, 'hp': 40, 'cost': 45, 'sell_value': 20, 'areas': [FOREST]},
    {'name': TENCH_FILET, 'hp': 40, 'cost': 43, 'sell_value': 16, 'areas': [CITY]},

]
