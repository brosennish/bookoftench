from typing import List

from savethewench.ui import purple

ACHIEVEMENTS = "Achievements"
AREA_BOSS_FIGHT = "Fight Boss"
BANK = "Bank"
CASINO = "Casino"
COFFEE_SHOP = "Coffee Shop"
EQUIP_WEAPON = "Equip Weapon"
EXPLORE = "Explore"
FINAL_BOSS_FIGHT = purple("BATTLE DENNY BILTMORE")
OVERVIEW = "Overview"
PERKS = "Perks"
SHOP = "Shop"
TRAVEL = "Travel"
USE_ITEM = "Use Item"

class MenuDefaults:
    page_one: List[str] = [EXPLORE, USE_ITEM, EQUIP_WEAPON, SHOP, TRAVEL]
    page_two: List[str] = [ACHIEVEMENTS, BANK, CASINO, PERKS, OVERVIEW]