from . import audio, enemies

# Constants
CAVE = "Cave"
CITY = "City"
FOREST = "Forest"
SWAMP = "Swamp"

Areas = [
    {'name': CITY,
     'enemies': [enemies.BANDIT, enemies.GOON, enemies.PIMP, enemies.HOBO,
                 enemies.SERIAL_KILLER],
     'boss': enemies.THE_MAYOR, 'theme': audio.CITY_THEME},
    {'name': FOREST,
     'enemies': [enemies.HIKER, enemies.HUNTER, enemies.POACHER,
                 enemies.DISGRACED_EXILE, enemies.SERIAL_KILLER],
     'boss': enemies.SLEDGE_HAMMOND, 'theme': audio.FOREST_THEME},
    {'name': CAVE,
     'enemies': [enemies.MINER, enemies.SPELUNKER, enemies.MOLE_PERSON,
                 enemies.HUMANOID_CAVE_CREATURE],
     'boss': enemies.CAPTAIN_HOLE, 'theme': audio.CAVE_THEME},
    {'name': SWAMP,
     'enemies': [enemies.HAND_FISHERMAN, enemies.BAYOU_MAN, enemies.VOODOO_PRIESTESS,
                 enemies.SKIN_COLLECTOR],
     'boss': enemies.BAYOU_BILL, 'theme': audio.SWAMP_THEME},
]
