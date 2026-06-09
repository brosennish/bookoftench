from bookoftench.data import bait as b

# ================================================================================================

# Species
BARRACUDA = "Barracuda"
BLUEGILL = "Bluegill"
BOTTLENOSE_DOLPHIN = "Bottlenose Dolphin"
BULL_SHARK = "Bull Shark"
CHANNEL_CATFISH = "Channel Catfish"
COMMON_CARP = "Common Carp"
GIANT_OARFISH = "Giant Oarfish"
GIANT_SQUID = "Giant Squid"
GREAT_WHITE_SHARK = "Great White Shark"
LARGEMOUTH_BASS = "Largemouth Bass"
MOLA_MOLA = "Mola Mola"
ROUND_GOBY = "Round Goby"
SHEEPSHEAD = "Sheepshead"
STURGEON = "Sturgeon"
TARPON = "Tarpon"
TENCH = "Tench"
WHALE_SHARK = "Whale Shark"

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

# Observable Characteristics
SPECIES = "Species"
VARIANT = "Variant"
STRENGTH = "Strength"
SPEED = "Speed"
STAMINA = "Stamina"
RAGE_FACTOR = "Rage Factor"

possible_observations = [
    SPECIES,
    VARIANT,
    STRENGTH,
    SPEED,
    RAGE_FACTOR,
]

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
    # ===========================
    #          SHALLOWS
    # ===========================

    {'name': BLUEGILL, 'rarity': COMMON, 'areas': [SHALLOWS], 'time': [DAY], 'moon': None,
     'min_length': 4, 'max_length': 14, 'min_weight_factor': 0.10, 'max_weight_factor': 0.22,
     'value_for_size': 0.90, 'rage_factor': 0.9, 'speed': 1.1, 'strength': 0.45, 'max_stamina': 25,
     'preferred_bait': [b.WORM, b.CRICKET, b.FLY, b.DOUGH_BALL],
     'spit_hook_chance': 0.010, 'max_age': 11,
     'description': 'A small sunfish known for its willingness to bite and energetic fight.',
     },

    {'name': CHANNEL_CATFISH, 'rarity': UNCOMMON, 'areas': [SHALLOWS, BAY], 'time': [DAY, NIGHT], 'moon': None,
     'min_length': 12, 'max_length': 42, 'min_weight_factor': 0.22, 'max_weight_factor': 0.50,
     'value_for_size': 0.10, 'rage_factor': 1.05, 'speed': 0.75, 'strength': 1.55, 'max_stamina': 80,
     'preferred_bait': [b.WORM, b.MEAT, b.DOUGH_BALL, b.CRAY],
     'spit_hook_chance': 0.005, 'max_age': 25,
     'description': 'They have taste buds spread all over their entire body.'
     },

    {'name': COMMON_CARP, 'rarity': UNCOMMON, 'areas': [SHALLOWS, BAY], 'time': [DAY, NIGHT], 'moon': None,
     'min_length': 12, 'max_length': 48, 'min_weight_factor': 0.45, 'max_weight_factor': 1.10,
     'value_for_size': 0.08, 'rage_factor': 0.85, 'speed': 0.75, 'strength': 1.35, 'max_stamina': 95,
     'preferred_bait': [b.DOUGH_BALL, b.WORM, b.CRICKET, b.KRILL, b.SHRIMP],
     'spit_hook_chance': 0.003, 'max_age': 60,
     'description': 'A heavy-bodied fish famous for its endurance and stubborn fights.',
     },

    {'name': LARGEMOUTH_BASS, 'rarity': COMMON, 'areas': [SHALLOWS, BAY], 'time': [DAY, NIGHT], 'moon': None,
     'min_length': 10, 'max_length': 30, 'min_weight_factor': 0.22, 'max_weight_factor': 0.45,
     'value_for_size': 0.28, 'rage_factor': 1.15, 'speed': 1.35, 'strength': 1.15, 'max_stamina': 55,
     'preferred_bait': [b.MINNOW, b.CRICKET, b.FROG, b.FLY, b.CRAY, b.SPOON],
     'spit_hook_chance': 0.006, 'max_age': 16,
     'description': 'An aggressive freshwater predator known for explosive strikes and fierce fights.',
     },

    {'name': ROUND_GOBY, 'rarity': COMMON, 'areas': [SHALLOWS, BAY], 'time': [DAY, NIGHT], 'moon': None,
     'min_length': 3, 'max_length': 10, 'min_weight_factor': 0.08, 'max_weight_factor': 0.18,
     'value_for_size': 2.2, 'rage_factor': 0.9, 'speed': 1.25, 'strength': 0.55, 'max_stamina': 30,
     'preferred_bait': [b.WORM, b.CRAY, b.SHRIMP],
     'spit_hook_chance': 0.008, 'max_age': 5,
     'description': 'A small invasive fish that thrives on rocky bottoms.',
     },

    {'name': SHEEPSHEAD, 'rarity': UNCOMMON, 'areas': [SHALLOWS, BAY], 'time': [DAY, NIGHT], 'moon': None,
     'min_length': 10, 'max_length': 32, 'min_weight_factor': 0.35, 'max_weight_factor': 0.90,
     'value_for_size': 0.12, 'rage_factor': 0.8, 'speed': 0.7, 'strength': 1.9, 'max_stamina': 70,
     'preferred_bait': [b.WORM, b.CRAY, b.SHRIMP, b.CRAB],
     'spit_hook_chance': 0.004, 'max_age': 20,
     'description': 'A powerful fish with human-like teeth built for crushing shells and mussels.',
     },

    {'name': STURGEON, 'rarity': RARE, 'areas': [SHALLOWS, BAY], 'time': [DAY, NIGHT], 'moon': None,
     'min_length': 24, 'max_length': 120, 'min_weight_factor': 0.80, 'max_weight_factor': 2.40,
     'value_for_size': 0.025, 'rage_factor': 0.75, 'speed': 0.65, 'strength': 2.10, 'max_stamina': 140,
     'preferred_bait': [b.WORM, b.CRAY, b.MEAT, b.SHRIMP, b.DOUGH_BALL],
     'spit_hook_chance': 0.002, 'max_age': 100,
     'description': 'An ancient armored fish that can live for more than a century.',
     },

    {'name': TENCH, 'rarity': RARE, 'areas': [SHALLOWS], 'time': [DAY], 'moon': None,
     'min_length': 8, 'max_length': 28, 'min_weight_factor': 0.18, 'max_weight_factor': 0.30,
     'value_for_size': 0.34, 'rage_factor': 0.95, 'speed': 1.0, 'strength': 1.0, 'max_stamina': 60,
     'preferred_bait': [b.WORM, b.DOUGH_BALL, b.CRICKET],
     'spit_hook_chance': 0.003, 'max_age': 20,
     'description': 'The holy fish.',
     },

    # ===========================
    #            BAY
    # ===========================

    {'name': BARRACUDA, 'rarity': COMMON, 'areas': [BAY, OCEAN], 'time': [DAY], 'moon': None,
     'min_length': 18, 'max_length': 60, 'min_weight_factor': 0.55, 'max_weight_factor': 1.10,
     'value_for_size': 0.075, 'rage_factor': 1.45, 'speed': 1.85, 'strength': 1.15, 'max_stamina': 55,
     'preferred_bait': [b.MINNOW, b.SPOON],
     'spit_hook_chance': 0.006, 'max_age': 15,
     'description': 'A fearsome, torpedo-shaped predator with hundreds of razor-sharp teeth.',
     },

    {'name': BULL_SHARK, 'rarity': RARE, 'areas': [SHALLOWS, BAY, OCEAN], 'time': [DAY, NIGHT], 'moon': None,
     'min_length': 36, 'max_length': 120, 'min_weight_factor': 1.20, 'max_weight_factor': 2.80,
     'value_for_size': 0.013, 'rage_factor': 1.25, 'speed': 1.2, 'strength': 2.45, 'max_stamina': 115,
     'preferred_bait': [b.MEAT, b.SQUID],
     'spit_hook_chance': 0.002, 'max_age': 30,
     'description': 'A large, aggressive shark that can enter freshwater.',
     },

    {'name': TARPON, 'rarity': UNCOMMON, 'areas': [BAY, OCEAN], 'time': [DAY, NIGHT], 'moon': None,
     'min_length': 24, 'max_length': 84, 'min_weight_factor': 0.85, 'max_weight_factor': 1.90,
     'value_for_size': 0.035, 'rage_factor': 1.35, 'speed': 1.65, 'strength': 1.75, 'max_stamina': 95,
     'preferred_bait': [b.SHRIMP, b.MINNOW],
     'spit_hook_chance': 0.010, 'max_age': 50,
     'description': 'Have roamed the oceans for over 100 million years.',
     },

    # ===========================
    #           OCEAN
    # ===========================

    {'name': BOTTLENOSE_DOLPHIN, 'rarity': RARE, 'areas': [BAY, OCEAN], 'time': [DAY], 'moon': None,
     'min_length': 72, 'max_length': 156, 'min_weight_factor': 1.6, 'max_weight_factor': 3.2,
     'value_for_size': 0.0068, 'rage_factor': 0.9, 'speed': 1.55, 'strength': 2.0, 'max_stamina': 120,
     'preferred_bait': [b.SQUID, b.MINNOW, b.SHRIMP],
     'spit_hook_chance': 0.003, 'max_age': 60,
     'description': 'A clever ocean mammal with surprising power and endurance.',
    },

    {'name': GIANT_OARFISH, 'rarity': LEGENDARY, 'areas': [OCEAN], 'time': [DAY, NIGHT], 'moon': None,
     'min_length': 72, 'max_length': 300, 'min_weight_factor': 0.22, 'max_weight_factor': 0.55,
     'value_for_size': 0.0065, 'rage_factor': 0.75, 'speed': 0.80, 'strength': 1.05, 'max_stamina': 125,
     'preferred_bait': [b.SQUID, b.GLOW_LURE],
     'spit_hook_chance': 0.004, 'max_age': 20,
     'description': 'The world\'s longest living bony fish.'
     },

    {'name': GIANT_SQUID, 'rarity': LEGENDARY, 'areas': [OCEAN], 'time': [NIGHT], 'moon': None,
     'min_length': 120, 'max_length': 480, 'min_weight_factor': 0.8, 'max_weight_factor': 2.5,
     'value_for_size': 0.0045, 'rage_factor': 0.6, 'speed': 0.7, 'strength': 3.5, 'max_stamina': 180,
     'preferred_bait': [b.SQUID, b.GLOW_LURE, b.RATTLER],
     'spit_hook_chance': 0.001, 'max_age': 15,
     'description': 'A colossal deep-sea predator rarely seen by human eyes.',
     },

    {'name': GREAT_WHITE_SHARK, 'rarity': RARE, 'areas': [BAY, OCEAN], 'time': [DAY, NIGHT], 'moon': None,
     'min_length': 60, 'max_length': 240, 'min_weight_factor': 1.60, 'max_weight_factor': 4.20,
     'value_for_size': 0.0042, 'rage_factor': 1.30, 'speed': 1.25, 'strength': 3.0, 'max_stamina': 150,
     'preferred_bait': [b.MEAT, b.SQUID],
     'spit_hook_chance': 0.001, 'max_age': 70,
     'description': 'The ocean\'s largest predatory fish.',
     },

    {'name': MOLA_MOLA, 'rarity': LEGENDARY, 'areas': [OCEAN], 'time': [DAY], 'moon': None,
     'min_length': 36, 'max_length': 120, 'min_weight_factor': 2.20, 'max_weight_factor': 5.20,
     'value_for_size': 0.008, 'rage_factor': 0.55, 'speed': 0.45, 'strength': 1.25, 'max_stamina': 135,
     'preferred_bait': [b.KRILL, b.SHRIMP],
     'spit_hook_chance': 0.002, 'max_age': 25,
     'description': 'The ocean sunfish, one of the ocean\'s most bizarre creatures.',
     },

    {'name': WHALE_SHARK, 'rarity': LEGENDARY, 'areas': [OCEAN], 'time': [DAY], 'moon': None,
     'min_length': 180, 'max_length': 720, 'min_weight_factor': 4.0, 'max_weight_factor': 12.0,
     'value_for_size': 0.0018, 'rage_factor': 0.4, 'speed': 0.4, 'strength': 1.6, 'max_stamina': 250,
     'preferred_bait': [b.KRILL, b.SHRIMP, b.CRAB],
     'spit_hook_chance': 0.0005, 'max_age': 100,
     'description': 'The largest fish in the ocean, a gentle giant that filters tiny prey from the water.',
     },

]