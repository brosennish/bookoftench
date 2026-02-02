from savethewench.data.areas import CAVE, CITY, FOREST, SWAMP

COMMON = "Common"
UNCOMMON = "Uncommon"
RARE = "Rare"
LEGENDARY = "Legendary"
MYTHIC = "Mythic"

Search_Discoverables = [
    # --- common (1-5 value | 0-5 hp) ---
    {"pre": "a", "name": "Broken Compass", "value": 3, "hp": 0, "rarity": COMMON,
     "areas": [FOREST, SWAMP]},
    {"pre": "a", "name": "Bunless Hot Dog", "value": 1, "hp": 5, "rarity": COMMON,
     "areas": [FOREST, SWAMP]},
    {"pre": "a", "name": "Chakra Specialist", "value": 0, "hp": 0, "rarity": COMMON,
     "areas": [FOREST, SWAMP]},
    {"pre": "a", "name": "Cigarette Butt", "value": 1, "hp": 1, "rarity": COMMON,
     "areas": [CITY, FOREST, SWAMP]},
    {"pre": "a", "name": "Disposable Camera", "value": 3, "hp": 0, "rarity": COMMON,
     "areas": [CITY, FOREST, SWAMP]},
    {"pre": "an", "name": "Empty Flask", "value": 5, "hp": 0, "rarity": COMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP]},
    {"pre": "an", "name": "Oily Doily's Coupon", "value": 2, "hp": 0, "rarity": UNCOMMON,
     "areas": [CITY]},
    {"pre": "a", "name": "Pair of Sunglasses", "value": 3, "hp": 0, "rarity": COMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP]},
    {"pre": "a", "name": "Turtle Shell", "value": 5, "hp": 0, "rarity": COMMON,
     "areas": [FOREST, SWAMP]},

    # --- uncommon (6-15 value | 0-10 hp) ---
    {"pre": "a", "name": "Blood Bucket", "value": 8, "hp": 8, "rarity": UNCOMMON,
     "areas": [CITY, FOREST, SWAMP]},
    {"pre": "a", "name": "Digital Camera", "value": 15, "hp": 0, "rarity": UNCOMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP]},
    {"pre": "a", "name": "Paper Mache Tench Balloon", "value": 15, "hp": 0, "rarity": UNCOMMON,
     "areas": [CITY]},
    {"pre": "a", "name": "Pocket Watch", "value": 12, "hp": 0, "rarity": UNCOMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP]},
    {"pre": "a", "name": "Tackle Box", "value": 10, "hp": 0, "rarity": UNCOMMON,
     "areas": [SWAMP]},

    # --- rare (25-100 value | 0 hp) ---
    {"pre": "a", "name": "Cigar Box Guitar", "value": 33, "hp": 0, "rarity": RARE,
     "areas": [CAVE, CITY, FOREST, SWAMP]},
    {"pre": "a", "name": "Fretless Bass Guitar", "value": 69, "hp": 0, "rarity": RARE,
     "areas": [CITY]},
    {"pre": "a", "name": "Glass Eye", "value": 30, "hp": 0, "rarity": RARE,
     "areas": [CAVE, CITY, FOREST, SWAMP]},
    {"pre": "a", "name": "Gold Chain", "value": 100, "hp": 0, "rarity": RARE,
     "areas": [CAVE, CITY, FOREST, SWAMP]},
    {"pre": "a", "name": "Flange Pedal", "value": 30, "hp": 0, "rarity": RARE,
     "areas": [CITY]},
    {"pre": "a", "name": "Fossilized Tench", "value": 50, "hp": 0, "rarity": RARE,
     "areas": [CAVE, FOREST, SWAMP]},
    {"pre": "a", "name": "Peg Leg", "value": 25, "hp": 0, "rarity": RARE,
     "areas": [CAVE]},
    {"pre": "a", "name": "Pirate Cutlass", "value": 35, "hp": 0, "rarity": RARE,
     "areas": [CAVE]},
    {"pre": "a", "name": "Shrunken Head", "value": 25, "hp": 0, "rarity": RARE,
     "areas": [SWAMP]},

    # --- legendary (250-500 value | 0 hp) ---
    {"pre": "a", "name": "Fossilized Hohkken", "value": 500, "hp": 0, "rarity": LEGENDARY,
     "areas": [CAVE]},

    # --- mythic (1000+ value | 0 hp) ---
    {"pre": None, "name": "Denny Biltmore's Lost Pinky Ring", "value": 1000, "hp": 0, "rarity": MYTHIC,
     "areas": [CITY]},
    {"pre": None, "name": "The Book of Tench", "value": 1000, "hp": 0, "rarity": MYTHIC,
     "areas": [CAVE]},
]