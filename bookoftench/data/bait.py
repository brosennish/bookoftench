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
    {'name': WORM, 'areas': [SHALLOWS], 'casts': 2, 'cost': 3,
     'description': 'Cheap bait for common freshwater fish.'},

    {'name': DOUGH_BALL, 'areas': [SHALLOWS], 'casts': 1, 'cost': 1,
     'description': 'Simple bait favored by peaceful fish.'},

    {'name': CRICKET, 'areas': [SHALLOWS], 'casts': 2, 'cost': 4,
     'description': 'Attracts surface-feeding fish in shallows.'},

    {'name': MINNOW, 'areas': [SHALLOWS], 'casts': 2, 'cost': 6,
     'description': 'Live bait for larger predatory fish.'},

    {'name': CRAY, 'areas': [SHALLOWS], 'casts': 3, 'cost': 8,
     'description': 'Excellent for bottom-feeding predators.'},

    {'name': FROG, 'areas': [SHALLOWS], 'casts': 12, 'cost': 20,
     'description': 'Durable lure for aggressive freshwater hunters.'},

    {'name': FLY, 'areas': [SHALLOWS], 'casts': 15, 'cost': 28,
     'description': 'Targets surface fish with repeated casts.'},

    # --- BAY ---
    {'name': SHRIMP, 'areas': [BAY], 'casts': 2, 'cost': 3,
     'description': 'Reliable bay bait for many species.'},

    {'name': CRAB, 'areas': [BAY], 'casts': 4, 'cost': 10,
     'description': 'Attracts stronger fish near structure.'},

    {'name': SPOON, 'areas': [BAY], 'casts': 20, 'cost': 45,
     'description': 'Reusable lure for fast predatory fish.'},

    # --- OCEAN ---
    {'name': KRILL, 'areas': [OCEAN], 'casts': 1, 'cost': 2,
     'description': 'Tiny ocean bait for unusual species.'},

    # --- MULTI-ZONE SALTWATER ---
    {'name': MEAT, 'areas': [BAY, OCEAN], 'casts': 2, 'cost': 8,
     'description': 'Bloody bait attracting powerful predators.'},

    {'name': SQUID, 'areas': [BAY, OCEAN], 'casts': 4, 'cost': 12,
     'description': 'Versatile bait favored by large fish.'},

    # --- NOCTURNAL / ALL-ZONE ---
    {'name': RATTLER, 'areas': [SHALLOWS, BAY, OCEAN], 'casts': 15, 'cost': 35,
     'description': 'Noisy lure effective in low visibility.'},

    {'name': GLOW_LURE, 'areas': [SHALLOWS, BAY, OCEAN], 'casts': 20, 'cost': 50,
     'description': 'Glowing lure for night and depths.'},

]