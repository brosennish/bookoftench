from bookoftench.data import bait as b

# ================================================================================================

# Species
TENCH = "Tench"

# ================================================================================================

# Rarities
COMMON = "Common"
UNCOMMON = "Uncommon"
RARE = "Rare"
LEGENDARY = "Legendary"
MYTHIC = "Mythic"

# Areas
SHALLOWS = "Shallows"
BAY = "Bay"
OCEAN = "Ocean"

# Time
DAY = "Day"
NIGHT = "Night"

# ================================================================================================

Fish_Species = [

    # --- if moon is empty, fish can spawn during any phase ---
    # --- length is in inches ---
    # --- weight is weight per inch ---
    # --- calculate weight, value, and hp in post_init ---
    # --- rage is a multiplier affecting fish breaking the line ---
    # --- speed is a multiplier affecting how far fish travels with slack ---
    # --- strength is a multiplier affecting how a fish loses stamina ---

    # =====================================================
    #                       SHALLOWS
    # =====================================================
    {'name': TENCH, 'rarity': RARE, 'areas': [SHALLOWS], 'time': [DAY], 'moon': '',
     'min_length': 8, 'max_length': 28, 'min_weight_per_inch': 0.28, 'max_weight_per_inch': 0.42,
     'value_for_size': 0.5, 'hp_for_size': 0.5, 'rage': 1, 'speed': 1, 'strength': 1,
     'preferred_bait': [b.WORM, b.DOUGH_BALL]
     },

    ]