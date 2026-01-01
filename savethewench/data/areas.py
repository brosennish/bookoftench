from . import audio, enemies

# Constants
CAVE = "Cave"
CITY = "City"
FOREST = "Forest"
SWAMP = "Swamp"

# TODO tweak 'explore_probabilities' for each area as desired
# e.g. 'explore_probabilities': {'coin_chance': 20, 'enemy_chance': 30, 'item_chance': 30,
#                                'weapon_chance': 10, 'perk_chance': 5}
Areas = [
    {'name': CITY,
     'enemies': [enemies.BANDIT, enemies.GOON, enemies.PIMP, enemies.HOBO,
                 enemies.SERIAL_KILLER],
     'boss_name': enemies.THE_MAYOR, 'theme': audio.CITY_THEME},
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
