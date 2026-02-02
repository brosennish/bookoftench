# --- rarities ---
from savethewench.data.areas import CAVE, CITY, FOREST, SWAMP

COMMON = "Common"
UNCOMMON = "Uncommon"
RARE = "Rare"
LEGENDARY = "Legendary"
MYTHIC = "Mythic"

Search_Discoverables = [
    # --- common ---
    {"name": "Sunglasses", "value": 5, "hp": 0, "rarity": COMMON, "areas": [CAVE, CITY, FOREST, SWAMP]},

    # --- uncommon ---
    {"name": "Pocket Watch", "value": 10, "hp": 0, "rarity": UNCOMMON, "areas": [CAVE, CITY, FOREST, SWAMP]},

    # --- rare ---
    {"name": "Digital Camera", "value": 25, "hp": 0, "rarity": RARE, "areas": [CAVE, CITY, FOREST, SWAMP]},

    # --- legendary ---
    {"name": "Gold Chain", "value": 100, "hp": 0, "rarity": LEGENDARY, "areas": [CAVE, CITY, FOREST, SWAMP]},

    # --- mythic ---
    {"name": "Golden Tench", "value": 1000, "hp": 0, "rarity": MYTHIC, "areas": [CAVE, CITY, FOREST, SWAMP]},
]