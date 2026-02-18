from enum import Enum

from . import audio, enemies
from bookoftench.data.enemies import Enemies
from .components import ActionMenuDefaults, COFFEE_SHOP, HOSPITAL, OFFICER, OCCULTIST, SHAMAN, WIZARD

# Constants
CAVE = "Cave"
CITY = "City"
FOREST = "Forest"
SWAMP = "Swamp"


class EncounterType(Enum):
    POST_KILL = 0


# TODO tweak 'search_probabilities' for each area as desired
# map names of registered components to (int percent) probabilities
# can include *any* registered component - useful for future npc encounters, etc...
# e.g. 'search_probabilities': {DISCOVER_COIN: 20, SPAWN_ENEMY: 30, DISCOVER_ITEM: 30,
#                                DISCOVER_WEAPON: 10, DISCOVER_PERK: 5}
Areas = [
    {'name': CITY,
     'enemies': [i['name'] for i in Enemies if CITY in i['areas']],
     'boss_name': enemies.THE_MAYOR, 'theme': audio.CITY_THEME,
     'actions_menu': {'pages': [ActionMenuDefaults.page_one, [*ActionMenuDefaults.page_two, COFFEE_SHOP, HOSPITAL]]},
     'encounters': [{'type': EncounterType.POST_KILL, 'component': OFFICER}]},
    {'name': FOREST,
     'enemies': [i['name'] for i in Enemies if FOREST in i['areas']],
     'boss_name': enemies.SLEDGE_HAMMOND, 'theme': audio.FOREST_THEME,
     'actions_menu': {'pages': [ActionMenuDefaults.page_one, [*ActionMenuDefaults.page_two, WIZARD]]}},
    {'name': CAVE,
     'enemies': [i['name'] for i in Enemies if CAVE in i['areas']],
     'boss_name': enemies.CAPTAIN_HOLE, 'theme': audio.CAVE_THEME,
     'actions_menu': {'pages': [ActionMenuDefaults.page_one, [*ActionMenuDefaults.page_two, OCCULTIST]]}},
    {'name': SWAMP,
     'enemies': [i['name'] for i in Enemies if SWAMP in i['areas']],
     'boss_name': enemies.BAYOU_BILL, 'theme': audio.SWAMP_THEME,
     'actions_menu': {'pages': [ActionMenuDefaults.page_one, [*ActionMenuDefaults.page_two, SHAMAN]]}},
]
