# Bait and Lures
WORM = "Worm"             # Freshwater/shallow baseline
KRILL = "Krill"           # Saltwater/bay baseline
DOUGH_BALL = "Dough Ball" # Bottom-feeders
MINNOW = "Minnow"         # Medium predators
FROG = "Frog"             # Topwater/weedless bait for shallow heavy cover
CRICKET = "Cricket"       # Surface bugs
CRAY = "Cray"             # Rocky/bottom predators
FLY = "Fly"               # Ultra-lightweight surface bait for finicky river species
MEAT = "Meat"             # Scent-hunting scavengers/sharks
CRAB = "Crab"             # Structure-dwelling crushers
SHRIMP = "Shrimp"         # The ultimate live saltwater generalist
SPOON = "Spoon"           # Flashy, visual gamefish
SQUID = "Squid"           # Rubbery, highly durable bait for multi-hook rigs and hard-biting sea fish
GLOW_LURE = "Glow Lure"   # Light attractors
RATTLER = "Rattler"       # Sound/vibration hunters

# ================================================================================================

# Areas
SHALLOWS = "Shallows"
BAY = "Bay"
OCEAN = "Ocean"

# ================================================================================================

Bait_And_Lures = [

    # --- add tackle box dict of bait ---

    # --- SHALLOWS ---
    {'name': WORM, 'areas': [SHALLOWS], 'casts': 2, 'cost': 3},
    {'name': DOUGH_BALL, 'areas': [SHALLOWS], 'casts': 1, 'cost': 1},
    {'name': CRICKET, 'areas': [SHALLOWS], 'casts': 2, 'cost': 5},
    {'name': MINNOW, 'areas': [SHALLOWS], 'casts': 2, 'cost': 6},
    {'name': CRAY, 'areas': [SHALLOWS], 'casts': 3, 'cost': 9},
    {'name': FROG, 'areas': [SHALLOWS], 'casts': 10, 'cost': 18},
    {'name': FLY, 'areas': [SHALLOWS], 'casts': 15, 'cost': 30},

    # --- BAY ---
    {'name': SHRIMP, 'areas': [BAY], 'casts': 2, 'cost': 3},
    {'name': CRAB, 'areas': [BAY], 'casts': 4, 'cost': 12},
    {'name': SPOON, 'areas': [BAY], 'casts': 20, 'cost': 45},

    # --- OCEAN ---
    {'name': KRILL, 'areas': [OCEAN], 'casts': 2, 'cost': 3},

    # --- MULTI-ZONE SALTWATER ---
    {'name': MEAT, 'areas': [BAY, OCEAN], 'casts': 3, 'cost': 10},
    {'name': SQUID, 'areas': [BAY, OCEAN], 'casts': 4, 'cost': 15},

    # --- NOCTURNAL / ALL-ZONE ---
    {'name': RATTLER, 'areas': [SHALLOWS, BAY, OCEAN], 'casts': 15, 'cost': 35},
    {'name': GLOW_LURE, 'areas': [SHALLOWS, BAY, OCEAN], 'casts': 20, 'cost': 50}

]