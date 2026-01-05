from typing import List

from savethewench.ui import purple

ACHIEVEMENTS = "Achievements"
AREA_BOSS_FIGHT = "Fight Boss"
BANK = "Bank"
CASINO = "Casino"
COFFEE_SHOP = "Coffee Shop"
DISCOVER_COIN = "Discover Coin"
DISCOVER_ITEM = "Discover Item"
DISCOVER_PERK = "Discover Perk"
DISCOVER_WEAPON = "Discover Weapon"
EQUIP_WEAPON = "Equip Weapon"
EXPLORE = "Explore"
FINAL_BOSS_FIGHT = purple("BATTLE DENNY BILTMORE")
HOSPITAL = "Hospital"
OVERVIEW = "Overview"
PERKS = "Perks"
SHOP = "Shop"
SPAWN_ENEMY = "Spawn Enemy"
TRAVEL = "Travel"
USE_ITEM = "Use Item"

class MenuDefaults:
    page_one: List[str] = [EXPLORE, USE_ITEM, EQUIP_WEAPON, SHOP, TRAVEL]
    page_two: List[str] = [ACHIEVEMENTS, BANK, CASINO, PERKS, OVERVIEW]