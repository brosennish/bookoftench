from savethewench.data.areas import CAVE, CITY, FOREST, SWAMP

COMMON = "Common"
UNCOMMON = "Uncommon"
RARE = "Rare"
LEGENDARY = "Legendary"
MYTHIC = "Mythic"

Search_Discoverables = [
    # --- common ---
    {"pre": "a", "name": "Pair of Sunglasses", "value": 3, "hp": 0, "rarity": COMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP]},

    # --- uncommon ---
    {"pre": "a", "name": "Pocket Watch", "value": 10, "hp": 0, "rarity": UNCOMMON,
     "areas": [CAVE, CITY, FOREST, SWAMP]},

    # --- rare ---
    {"pre": "a", "name": "Digital Camera", "value": 20, "hp": 0, "rarity": RARE,
     "areas": [CAVE, CITY, FOREST, SWAMP]},

    # --- legendary ---
    {"pre": "a", "name": "Gold Chain", "value": 100, "hp": 0, "rarity": LEGENDARY,
     "areas": [CAVE, CITY, FOREST, SWAMP]},

    # --- mythic ---
    {"pre": None, "name": "Denny Biltmore's Lost Pinky Ring", "value": 1000, "hp": 0, "rarity": MYTHIC,
     "areas": [CAVE, CITY, FOREST, SWAMP]},
]