from . import audio, enemies
from .components import ActionMenuDefaults, COFFEE_SHOP, HOSPITAL

# Constants
CAVE = "Cave"
CITY = "City"
FOREST = "Forest"
SWAMP = "Swamp"

# TODO tweak 'explore_probabilities' for each area as desired
# map names of registered components to (int percent) probabilities
# can include *any* registered component - useful for future npc encounters, etc...
# e.g. 'explore_probabilities': {DISCOVER_COIN: 20, SPAWN_ENEMY: 30, DISCOVER_ITEM: 30,
#                                DISCOVER_WEAPON: 10, DISCOVER_PERK: 5}
Areas = [
    {'name': CITY,
     'enemies': [enemies.BANDIT, enemies.GOON, enemies.PIMP, enemies.HOBO,
                 enemies.SERIAL_KILLER],
     'boss_name': enemies.THE_MAYOR, 'theme': audio.CITY_THEME,
     'actions_menu': {'pages': [ActionMenuDefaults.page_one, ActionMenuDefaults.page_two, [COFFEE_SHOP, HOSPITAL]]}},
    {'name': FOREST,
     'enemies': [enemies.HIKER, enemies.HUNTER, enemies.POACHER,
                 enemies.DISGRACED_EXILE, enemies.SERIAL_KILLER],
     'boss_name': enemies.SLEDGE_HAMMOND, 'theme': audio.FOREST_THEME},
    {'name': CAVE,
     'enemies': [enemies.MINER, enemies.SPELUNKER, enemies.MOLE_PERSON,
                 enemies.HUMANOID_CAVE_CREATURE],
     'boss_name': enemies.CAPTAIN_HOLE, 'theme': audio.CAVE_THEME},
    {'name': SWAMP,
     'enemies': [enemies.HAND_FISHERMAN, enemies.BAYOU_MAN, enemies.VOODOO_PRIESTESS,
                 enemies.SKIN_COLLECTOR],
     'boss_name': enemies.BAYOU_BILL, 'theme': audio.SWAMP_THEME},
]
