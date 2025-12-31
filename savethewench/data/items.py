from .areas import CITY, CAVE, FOREST, SWAMP

BAG_OF_SLUDGE = "Bag of Sludge"
CAMPBELLS_GOOP = "Campbell's Goop"
CANNED_HORSE = "Canned Horse"
CHICKEN_OF_THE_CAVE = "Chicken of the Cave"
COUGHYS_CAPUCCINO = "Coughy's Capuccino"
COUGHYS_COFFEE = "Coughy's Coffee"
COUGHYS_COLD_BREW = "Coughy's Cold Brew"
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
MYSTICAL_MUSHROOMS = "Mystical Mushrooms"
OCEAN_MAN_LUNCH_BOX = "Ocean Man Lunch Box"
PROTEIN_GLOB = "Protein Glob"
STALE_GREENS = "Stale Greens"
SUSPICIOUS_GUMBO = "Suspicious Gumbo"
TENCH_FILET = "Tench Filet"
UNIDENTIFIED_MUSHROOMS = "Unidentified Mushrooms"

# TODO - Add more items and organize by area to support distinct shops and discoveries
Coughy_Items = [
    {'name': COUGHYS_COFFEE, 'hp': 10, 'cost': 4, 'risk': 0.07},
    {'name': COUGHYS_COLD_BREW, 'hp': 15, 'cost': 5, 'risk': 0.085},
    {'name': COUGHYS_CAPUCCINO, 'hp': 20, 'cost': 6, 'risk': 0.10},
]

Items = [
    # --- Tier 1 (10 HP) ---
    {'name': FROZEN_WAFFLE, 'hp': 10, 'cost': 8, 'sell_value': 3, 'areas': [CITY]},
    {'name': KRILL, 'hp': 10, 'cost': 10, 'sell_value': 4, 'areas': [CITY]},
    {'name': STALE_GREENS, 'hp': 10, 'cost': 12, 'sell_value': 5, 'areas': [CITY, CAVE]},

    # --- Tier 2 (16–20 HP) ---
    {'name': MUSKRAT_SKEWER, 'hp': 16, 'cost': 14, 'sell_value': 5, 'areas': [SWAMP]},
    {'name': BAG_OF_SLUDGE, 'hp': 16, 'cost': 14, 'sell_value': 5, 'areas': [CITY]},
    {'name': MYSTERY_MEAT, 'hp': 20, 'cost': 18, 'sell_value': 7, 'areas': [CAVE, SWAMP]},
    {'name': CRAY, 'hp': 20, 'cost': 18, 'sell_value': 7, 'areas': [CAVE, SWAMP]},
    {'name': CAMPBELLS_GOOP, 'hp': 20, 'cost': 20, 'sell_value': 8, 'areas': [CITY, CAVE, FOREST]},

    # --- Tier 3 (24–28 HP) ---
    {'name': MOREL, 'hp': 24, 'cost': 22, 'sell_value': 9, 'areas': [FOREST]},
    {'name': PROTEIN_GLOB, 'hp': 24, 'cost': 24, 'sell_value': 10, 'areas': [FOREST]},
    {'name': CRABS_ON_RYE, 'hp': 28, 'cost': 28, 'sell_value': 11, 'areas': [CITY]},

    # --- Tier 4 (30–35 HP) ---
    {'name': OCEAN_MAN_LUNCH_BOX, 'hp': 30, 'cost': 30, 'sell_value': 12, 'areas': [CITY, FOREST]},
    {'name': GATOR_TESTICLES, 'hp': 32, 'cost': 34, 'sell_value': 14, 'areas': [SWAMP]},
    {'name': UNIDENTIFIED_MUSHROOMS, 'hp': 33, 'cost': 35, 'sell_value': 15, 'areas': [CAVE, FOREST, SWAMP]},
    {'name': MOONSHINE, 'hp': 35, 'cost': 36, 'sell_value': 15, 'areas': [CAVE, SWAMP]},
    {'name': CHICKEN_OF_THE_CAVE, 'hp': 35, 'cost': 38, 'sell_value': 16, 'areas': [CAVE]},

    # --- Tier 5 (38–40 HP) ---
    {'name': TENCH_FILET, 'hp': 38, 'cost': 40, 'sell_value': 16, 'areas': [CITY]},
    {'name': MYSTICAL_MUSHROOMS, 'hp': 40, 'cost': 42, 'sell_value': 17, 'areas': [CAVE, FOREST]},
    {'name': CANNED_HORSE, 'hp': 40, 'cost': 42, 'sell_value': 17, 'areas': [CITY, CAVE]},
    {'name': SUSPICIOUS_GUMBO, 'hp': 40, 'cost': 45, 'sell_value': 18, 'areas': [SWAMP]},
    {'name': HOG_LOINS, 'hp': 40, 'cost': 45, 'sell_value': 18, 'areas': [FOREST, SWAMP]},
]

# FLOW:
# Menu option > Run component > Coughy intro static method >
# Display Coughy_Items > Labeled Selection > log_event >
# handle_event > coffee_effect

# TODO - Component, intro, display, selection, complete effect

# ADDED -> Coughy_Items; CoffeeEvent; handle_coffee_event(); coffee_effect(), Menu option,

