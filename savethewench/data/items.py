from .areas import CITY, CAVE, FOREST, SWAMP

BAG_OF_SLUDGE = "Bag of Sludge"
CAMPBELLS_GOOP = "Campbell's Goop"
CANNED_HORSE = "Canned Horse"
CHICKEN_OF_THE_CAVE = "Chicken of the Cave"
COUGHYS_COFFEE = "Coughy's Coffee"
CRABS_ON_RYE = "Crabs on Rye"
CRAY = "Cray"
FROZEN_WAFFLE = "Frozen Waffle"
GATOR_TESTICLES = "Gator Testicles"
HOG_LOINS = "Hog Loins"
KRILL = "Krill"
MOONSHINE = "Moonshine"
MOREL = "Morel"
MUSKRAT_SKEWER = "Muskrat Skewer"
MYSTERY_MEAT = "Mystery Meat"
OCEAN_MAN_LUNCH_BOX = "Ocean Man Lunch Box"
PROTEIN_GLOB = "Protein Glob"
STALE_GREENS = "Stale Greens"
SUSPICIOUS_GUMBO = "Suspicious Gumbo"
TENCH_FILET = "Tench Filet"
UNIDENTIFIED_MUSHROOMS = "Unidentified Mushrooms"

# TODO - Add more items and organize by area to support distinct shops and discoveries
Items = [
    # --- Special ---
    {'name': COUGHYS_COFFEE, 'hp': 20, 'cost': 5, 'sell_value': 0, 'area': CITY},

    # --- Tier 1 (10 HP) ---
    {'name': FROZEN_WAFFLE, 'hp': 10, 'cost': 8, 'sell_value': 3, 'area': CITY},
    {'name': KRILL, 'hp': 10, 'cost': 10, 'sell_value': 4, 'area': CITY},
    {'name': STALE_GREENS, 'hp': 10, 'cost': 12, 'sell_value': 5, 'area': [CITY, CAVE]},

    # --- Tier 2 (16–20 HP) ---
    {'name': MUSKRAT_SKEWER, 'hp': 16, 'cost': 14, 'sell_value': 5, 'area': SWAMP},
    {'name': BAG_OF_SLUDGE, 'hp': 16, 'cost': 14, 'sell_value': 5, 'area': CITY},
    {'name': MYSTERY_MEAT, 'hp': 20, 'cost': 18, 'sell_value': 7, 'area': [CAVE, SWAMP]},
    {'name': CRAY, 'hp': 20, 'cost': 18, 'sell_value': 7, 'area': [CAVE, SWAMP]},
    {'name': CAMPBELLS_GOOP, 'hp': 20, 'cost': 20, 'sell_value': 8, 'area': [CITY, CAVE, FOREST]},

    # --- Tier 3 (24–28 HP) ---
    {'name': MOREL, 'hp': 24, 'cost': 22, 'sell_value': 9, 'area': FOREST},
    {'name': PROTEIN_GLOB, 'hp': 24, 'cost': 24, 'sell_value': 10, 'area': FOREST},
    {'name': CRABS_ON_RYE, 'hp': 28, 'cost': 28, 'sell_value': 11, 'area': CITY},

    # --- Tier 4 (30–35 HP) ---
    {'name': OCEAN_MAN_LUNCH_BOX, 'hp': 30, 'cost': 30, 'sell_value': 12, 'area': [CITY, FOREST]},
    {'name': GATOR_TESTICLES, 'hp': 32, 'cost': 34, 'sell_value': 14, 'area': SWAMP},
    {'name': MOONSHINE, 'hp': 35, 'cost': 36, 'sell_value': 15, 'area': [CAVE, SWAMP]},
    {'name': CHICKEN_OF_THE_CAVE, 'hp': 35, 'cost': 38, 'sell_value': 16, 'area': CAVE},

    # --- Tier 5 (38–40 HP) ---
    {'name': TENCH_FILET, 'hp': 38, 'cost': 40, 'sell_value': 16, 'area': CITY},
    {'name': UNIDENTIFIED_MUSHROOMS, 'hp': 40, 'cost': 42, 'sell_value': 17, 'area': [CAVE, FOREST]},
    {'name': CANNED_HORSE, 'hp': 40, 'cost': 42, 'sell_value': 17, 'area': [CITY, CAVE]},
    {'name': SUSPICIOUS_GUMBO, 'hp': 40, 'cost': 45, 'sell_value': 18, 'area': SWAMP},
    {'name': HOG_LOINS, 'hp': 40, 'cost': 45, 'sell_value': 18, 'area': [FOREST, SWAMP]},
]

