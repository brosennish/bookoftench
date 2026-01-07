from typing import List

from savethewench.ui import purple

ACHIEVEMENTS = "Achievements"
AREA_BOSS_FIGHT = "Fight Boss"
BANK = "Bank"
CASINO = "Casino"
COFFEE_SHOP = "Coffee Shop"
CRYPTO_EXCHANGE = "Crypto Exchange"
DISCOVER_COIN = "Discover Coin"
DISCOVER_ITEM = "Discover Item"
DISCOVER_PERK = "Discover Perk"
DISCOVER_WEAPON = "Discover Weapon"
EQUIP_WEAPON = "Equip Weapon"
EXPLORE = "Explore"
FINAL_BOSS_FIGHT = purple("BATTLE DENNY BILTMORE")
LOAD_GAME = "Load Game"
NEW_GAME = "New Game"
OVERVIEW = "Overview"
PERKS = "Perks"
QUIT_GAME = "Quit"
SAVE_GAME = "Save Game"
SETTINGS = "Settings"
SHOP = "Shop"
SPAWN_ENEMY = "Spawn Enemy"
TRAVEL = "Travel"
USE_ITEM = "Use Item"

class ActionMenuDefaults:
    page_one: List[str] = [EXPLORE, USE_ITEM, EQUIP_WEAPON, SHOP, TRAVEL]
    page_two: List[str] = [ACHIEVEMENTS, BANK, CASINO, PERKS, OVERVIEW]

class InGameMenuDefaults:
    page_one: List[str] = [NEW_GAME, SAVE_GAME, LOAD_GAME, SETTINGS, QUIT_GAME]