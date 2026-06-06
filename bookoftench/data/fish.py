from bookoftench.data import bait as b

# ================================================================================================

# Species
BARRACUDA = "Barracuda"
BULL_SHARK = "Bull Shark"
CHANNEL_CATFISH = "Channel Catfish"
GIANT_OARFISH = "Giant Oarfish"
GREAT_WHITE_SHARK = "Great White Shark"
MOLA_MOLA = "Mola Mola"
ROUND_GOBY = "Round Goby"
TARPON = "Tarpon"
TENCH = "Tench"

# ================================================================================================

# Rarities
COMMON = "Common"
UNCOMMON = "Uncommon"
RARE = "Rare"
LEGENDARY = "Legendary"

# Areas
SHALLOWS = "Shallows"
BAY = "Bay"
OCEAN = "Ocean"

# Time
DAY = "Day"
NIGHT = "Night"

# Sex
MALE = "Male"
FEMALE = "Female"
HERMAPHRODITE = "Hermaphrodite"

# States
CALM = "Calm"
SPOOKED = "Spooked"
AGITATED = "Agitated"
ENRAGED = "Enraged"

# ================================================================================================

# Variants
ALBINO = "Albino"
GLOWING = "Glowing"
IRIDESCENT = "Iridescent"
ONE_EYED = "One-eyed"
RADIOACTIVE = "Radioactive"
SAPIENT = "Sapient"
SCARRED = "Scarred"
TELEPATHIC = "Telepathic"
THREE_EYED = "Three-eyed"
TRANSLUCENT = "Translucent"
TWO_HEADED = "Two-headed"

VARIANTS = [
    {'name': ALBINO,      'chance': 0.03},
    {'name': GLOWING,     'chance': 0.01},
    {'name': IRIDESCENT,  'chance': 0.01},
    {'name': ONE_EYED,    'chance': 0.02},
    {'name': RADIOACTIVE, 'chance': 0.005},
    {'name': SAPIENT,     'chance': 0.001},
    {'name': SCARRED,     'chance': 0.03},
    {'name': TELEPATHIC,  'chance': 0.002},
    {'name': THREE_EYED,  'chance': 0.01},
    {'name': TRANSLUCENT, 'chance': 0.02},
    {'name': TWO_HEADED,  'chance': 0.005},
]

# ================================================================================================

VALUE_MULTIPLIER = 1

# ================================================================================================

Fish_Species = [

    # --- if moon is None, fish can spawn during any phase ---
    # --- length is in inches ---
    # --- weight = (length² × weight_factor) / 144 ---
    # --- calculate weight, value, etc. in post_init ---
    # --- rage is a multiplier affecting fish breaking the line ---
    # --- speed is a multiplier affecting how far fish travels with slack ---
    # --- strength is a multiplier affecting how a fish loses stamina ---

    # =====================================================
    #                       SHALLOWS
    # =====================================================

    {'name': CHANNEL_CATFISH, 'rarity': UNCOMMON, 'areas': [SHALLOWS, BAY], 'time': [DAY, NIGHT], 'moon': None,
     'min_length': 12, 'max_length': 42, 'min_weight_factor': 0.25, 'max_weight_factor': 0.55,
     'value_for_size': 0.09, 'rage': 1.1, 'speed': 0.8, 'strength': 1.6,
     'preferred_bait': [b.WORM, b.MEAT], 'spit_hook_chance': 0.005, 'max_age': 25,
     'description': 'They have taste buds spread all over their entire body.'
     },

    {'name': ROUND_GOBY, 'rarity': COMMON, 'areas': [SHALLOWS, BAY], 'time': [DAY, NIGHT], 'moon': None,
     'min_length': 3, 'max_length': 10, 'min_weight_factor': 0.08, 'max_weight_factor': 0.18,
     'value_for_size': 2.5, 'rage': 0.8, 'speed': 1.2, 'strength': 0.6,
     'preferred_bait': [b.WORM, b.CRAY], 'spit_hook_chance': 0.008, 'max_age': 5,
     'description': 'A small invasive fish that thrives on rocky bottoms.',
     },

    {'name': TENCH, 'rarity': RARE, 'areas': [SHALLOWS], 'time': [DAY], 'moon': None,
     'min_length': 8, 'max_length': 28, 'min_weight_factor': 0.18, 'max_weight_factor': 0.30,
     'value_for_size': 0.32, 'rage': 1, 'speed': 1, 'strength': 1,
     'preferred_bait': [b.WORM, b.DOUGH_BALL], 'spit_hook_chance': 0.003, 'max_age': 20,
     'description': 'The holy fish.',
     },

    # =====================================================
    #                        BAY
    # =====================================================

    {'name': BARRACUDA, 'rarity': COMMON, 'areas': [BAY, OCEAN], 'time': [DAY], 'moon': None,
     'min_length': 18, 'max_length': 60, 'min_weight_factor': 0.8, 'max_weight_factor': 1.8,
     'value_for_size': 0.056, 'rage': 1.4, 'speed': 1.8, 'strength': 1.2,
     'preferred_bait': [b.MINNOW, b.SPOON], 'spit_hook_chance': 0.006, 'max_age': 15,
     'description': 'A fearsome, torpedo-shaped predator with hundreds of razor-sharp teeth.',
     },

    {'name': BULL_SHARK, 'rarity': RARE, 'areas': [SHALLOWS, BAY, OCEAN], 'time': [DAY, NIGHT], 'moon': None,
     'min_length': 36, 'max_length': 120, 'min_weight_factor': 2.0, 'max_weight_factor': 5.0,
     'value_for_size': 0.0052, 'rage': 1.2, 'speed': 1.1, 'strength': 2.5,
     'preferred_bait': [b.MEAT, b.SQUID], 'spit_hook_chance': 0.002, 'max_age': 30,
     'description': 'A large, aggressive shark that can enter freshwater.',
     },

    {'name': TARPON, 'rarity': UNCOMMON, 'areas': [BAY, OCEAN], 'time': [DAY, NIGHT], 'moon': None,
     'min_length': 24, 'max_length': 84, 'min_weight_factor': 1.4, 'max_weight_factor': 3.5,
     'value_for_size': 0.017, 'rage': 1.3, 'speed': 1.7, 'strength': 1.8,
     'preferred_bait': [b.SHRIMP, b.MINNOW], 'spit_hook_chance': 0.012, 'max_age': 50,
     'description': 'Have roamed the oceans for over 100 million years.',
     },

    # =====================================================
    #                        OCEAN
    # =====================================================

    {'name': GREAT_WHITE_SHARK, 'rarity': RARE, 'areas': [BAY, OCEAN], 'time': [DAY, NIGHT], 'moon': None,
     'min_length': 60, 'max_length': 240, 'min_weight_factor': 4.0, 'max_weight_factor': 16.0,
     'value_for_size': 0.00053, 'rage': 1.3, 'speed': 1.3, 'strength': 3.0,
     'preferred_bait': [b.MEAT, b.SQUID], 'spit_hook_chance': 0.001, 'max_age': 70,
     'description': 'The ocean\'s largest predatory fish.',
     },

    {'name': MOLA_MOLA, 'rarity': LEGENDARY, 'areas': [OCEAN], 'time': [DAY], 'moon': None,
     'min_length': 36, 'max_length': 120, 'min_weight_factor': 6.0, 'max_weight_factor': 16.0,
     'value_for_size': 0.0021, 'rage': 0.6, 'speed': 0.5, 'strength': 1.2,
     'preferred_bait': [b.KRILL, b.SHRIMP], 'spit_hook_chance': 0.002, 'max_age': 25,
     'description': 'The ocean sunfish, one of the ocean\'s most bizarre creatures.',
     },

    {'name': GIANT_OARFISH, 'rarity': LEGENDARY, 'areas': [OCEAN], 'time': [DAY, NIGHT], 'moon': None,
     'min_length': 72, 'max_length': 300, 'min_weight_factor': 0.3, 'max_weight_factor': 0.8,
     'value_for_size': 0.0037, 'rage': 0.7, 'speed': 0.8, 'strength': 1.0,
     'preferred_bait': [b.SQUID, b.GLOW_LURE], 'spit_hook_chance': 0.004, 'max_age': 20,
     'description': 'The world\'s longest living bony fish.'
     },

]