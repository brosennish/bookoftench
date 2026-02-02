from typing import List

from savethewench.globals import is_debug_mode
from savethewench.ui import purple

ACHIEVEMENTS = "Achievements"
AREA_BOSS_FIGHT = "Fight Boss"
BANK = "Bank"
CASINO = "Casino"
COFFEE_SHOP = "Coffee Shop"
CRYPTO_EXCHANGE = "Crypto Exchange (Experimental)"
DISCOVER_COIN = "Discover Coin"
DISCOVER_ITEM = "Discover Item"
DISCOVER_PERK = "Discover Perk"
DISCOVER_WEAPON = "Discover Weapon"
EQUIP_WEAPON = "Equip Weapon"
FINAL_BOSS_FIGHT = purple("BATTLE DENNY BILTMORE")
HOSPITAL = "Hospital"
LOAD_GAME = "Load Game"
NEW_GAME = "New Game"
OCCULTIST = "Occultist"
OFFICER = "Officer"
SEARCH = "Search"
STATS = "Stats"
PERKS = "Perks"
QUIT_GAME = "Quit"
SAVE_GAME = "Save Game"
SETTINGS = "Settings"
SHOP = "Shop"
SPAWN_ENEMY = "Spawn Enemy"
TRAVEL = "Travel"
USE_ITEM = "Use Item"


class StartGameMenuDefaults:
    page_one: List[str] = [NEW_GAME, LOAD_GAME, QUIT_GAME]


class ActionMenuDefaults:
    page_one: List[str] = [SEARCH, USE_ITEM, EQUIP_WEAPON, SHOP, TRAVEL]
    page_two: List[str] = [ACHIEVEMENTS, BANK, CASINO, PERKS, STATS]


class InGameMenuDefaults:
    page_one: List[str] = [NEW_GAME, SETTINGS, QUIT_GAME]
