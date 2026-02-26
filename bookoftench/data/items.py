from .areas import CITY, CAVE, FOREST, SWAMP

ABANDONED_EYEBALLS = "Abandoned Eyeballs"
ALIEN_REMAINS = "Alien Remains"
ANTS_ON_A_LOG = "Ants On A Log"
BAT_MATTER ="BaT Matter"
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
SOMEWHAT_SPICY_NOODLES = "Somewhat Spicy Noodles"
SOUR_MILK = "Sour Milk"
STALE_GREENS = "Stale Greens"
SUSPICIOUS_GUMBO = "Suspicious Gumbo"
TENCH_FILET = "Tench Filet"
TOAD_STOOL = "Toad Stool"
UNIDENTIFIED_MUSHROOMS = "Unidentified Mushrooms"
UNWANTED_PROTEIN = "Unwanted Protein"
VERY_SPICY_NOODLES = "Very Spicy Noodles"

Items = [
    # --- Tier 1 (10 HP) ---
    {'name': ANTS_ON_A_LOG, 'hp': 10, 'cost': 11, 'sell_value': 4, 'areas': [FOREST, SWAMP]},
    {'name': BERRIES, 'hp': 10, 'cost': 11, 'sell_value': 4, 'areas': [FOREST]},
    {'name': BONE_MEAL, 'hp': 10, 'cost': 12, 'sell_value': 5, 'areas': [CAVE, CITY]},
    {'name': FROZEN_WAFFLE, 'hp': 10, 'cost': 10, 'sell_value': 4, 'areas': [CITY]},
    {'name': GOBY, 'hp': 10, 'cost': 11, 'sell_value': 4, 'areas': [CAVE, SWAMP]},
    {'name': KRILL, 'hp': 10, 'cost': 11, 'sell_value': 4, 'areas': [CITY]},
    {'name': SOUR_MILK, 'hp': 10, 'cost': 10, 'sell_value': 4, 'areas': [CITY, FOREST, SWAMP]},
    {'name': STALE_GREENS, 'hp': 10, 'cost': 12, 'sell_value': 5, 'areas': [CAVE, CITY]},
    {'name': TOAD_STOOL, 'hp': 10, 'cost': 11, 'sell_value': 4, 'areas': [FOREST, SWAMP]},

    # --- Tier 2 (16–20 HP) ---
    {'name': BAT_MATTER, 'hp': 15, 'cost': 16, 'sell_value': 6, 'areas': [CAVE]},
    {'name': CAMPBELLS_GOOP, 'hp': 20, 'cost': 22, 'sell_value': 9, 'areas': [CITY, CAVE, FOREST]},
    {'name': CRAY, 'hp': 20, 'cost': 21, 'sell_value': 8, 'areas': [CAVE, SWAMP]},
    {'name': EGG_ON_EGGS, 'hp': 18, 'cost': 19, 'sell_value': 8, 'areas': [CAVE, CITY, FOREST, SWAMP]},
    {'name': EGGS_ON_EGG, 'hp': 18, 'cost': 20, 'sell_value': 8, 'areas': [CAVE, CITY, FOREST, SWAMP]},
    {'name': MYSTERY_MEAT, 'hp': 20, 'cost': 21, 'sell_value': 8, 'areas': [CAVE, SWAMP]},
    {'name': MUSKRAT_SKEWER, 'hp': 16, 'cost': 17, 'sell_value': 7, 'areas': [SWAMP]},
    {'name': ORGANIC_SLUDGE, 'hp': 16, 'cost': 17, 'sell_value': 7, 'areas': [CITY]},
    {'name': SOMEWHAT_SPICY_NOODLES, 'hp': 18, 'cost': 19, 'sell_value': 8, 'areas': [CITY]},

    # --- Tier 3 (24–28 HP) ---
    {'name': ABANDONED_EYEBALLS, 'hp': 28, 'cost': 29, 'sell_value': 13, 'areas': [CAVE, CITY, FOREST, SWAMP]},
    {'name': CATFISH_FILET, 'hp': 26, 'cost': 27, 'sell_value': 11, 'areas': [SWAMP]},
    {'name': CRABS_ON_RYE, 'hp': 28, 'cost': 30, 'sell_value': 12, 'areas': [CAVE, CITY]},  # +1 noise
    {'name': GIZZARDS_AND_LIVERS, 'hp': 26, 'cost': 27, 'sell_value': 11, 'areas': [CITY, FOREST, SWAMP]},
    {'name': LOST_SAUCE, 'hp': 25, 'cost': 26, 'sell_value': 10, 'areas': [CAVE]},
    {'name': MOREL, 'hp': 24, 'cost': 25, 'sell_value': 10, 'areas': [FOREST]},
    {'name': OWL_EGG, 'hp': 25, 'cost': 26, 'sell_value': 10, 'areas': [FOREST]},
    {'name': UNWANTED_PROTEIN, 'hp': 24, 'cost': 25, 'sell_value': 10, 'areas': [CAVE, FOREST]},
    {'name': VERY_SPICY_NOODLES, 'hp': 24, 'cost': 24, 'sell_value': 10, 'areas': [CITY, FOREST, SWAMP]},

    # --- Tier 4 (30–35 HP) ---
    {'name': CANNED_HORSE, 'hp': 35, 'cost': 36, 'sell_value': 15, 'areas': [CITY, CAVE]},
    {'name': CARP_FILET, 'hp': 35, 'cost': 37, 'sell_value': 15, 'areas': [CITY]},
    {'name': EAGLE_EGG, 'hp': 34, 'cost': 35, 'sell_value': 14, 'areas': [FOREST]},
    {'name': GATOR_TESTICLES, 'hp': 32, 'cost': 34, 'sell_value': 14, 'areas': [SWAMP]},
    {'name': HOG_LOINS, 'hp': 35, 'cost': 36, 'sell_value': 15, 'areas': [FOREST, SWAMP]},
    {'name': LACED_HONEY, 'hp': 33, 'cost': 35, 'sell_value': 14, 'areas': [CAVE, FOREST]},
    {'name': MOONSHINE, 'hp': 34, 'cost': 36, 'sell_value': 14, 'areas': [CAVE, SWAMP]},
    {'name': OCEAN_MAN_LUNCH_BOX, 'hp': 30, 'cost': 31, 'sell_value': 13, 'areas': [CITY, FOREST]},
    {'name': UNIDENTIFIED_MUSHROOMS, 'hp': 35, 'cost': 37, 'sell_value': 16, 'areas': [CAVE, FOREST, SWAMP]},

    # --- Tier 5 (38–40 HP) ---
    {'name': ALIEN_REMAINS, 'hp': 39, 'cost': 40, 'sell_value': 20, 'areas': [FOREST]},
    {'name': GIANT_TENTACLE, 'hp': 38, 'cost': 39, 'sell_value': 16, 'areas': [CITY]},
    {'name': MYSTICAL_MUSHROOMS, 'hp': 39, 'cost': 41, 'sell_value': 16, 'areas': [CAVE, FOREST, SWAMP]},
    {'name': PANTHER_LOINS, 'hp': 37, 'cost': 38, 'sell_value': 16, 'areas': [FOREST, SWAMP]},
    {'name': SUSPICIOUS_GUMBO, 'hp': 39, 'cost': 41, 'sell_value': 16, 'areas': [FOREST, SWAMP]},
    {'name': TENCH_FILET, 'hp': 40, 'cost': 41, 'sell_value': 17, 'areas': [CITY]},
]
