
# ================================================================================================

# Fishing Areas
SHALLOWS = "Shallows"
BAY = "Bay"
OCEAN = "Ocean"

# Seasons
DRY_SEASON = "Dry Season"
WET_SEASON = "Wet Season"

# Season Effects
DRY_SEASON_BITE_CHANCE_EFFECT = -0.05
WET_SEASON_BITE_CHANCE_EFFECT = 0.05

# Bite Chance Multiplier
BITE_CHANCE_MULTIPLIER = 1

# ================================================================================================

Fishing_Areas = [

    {'name': SHALLOWS, 'bite_chance': 0.35, 'hook_chance': 0.75,
     'travel_cost': 15, 'casts': 12, 'lvl': 1,
     'min_hook_distance': 10, 'max_hook_distance': 50,
     'escape_distance': 100},

    {'name': BAY, 'bite_chance': 0.30, 'hook_chance': 0.65,
     'travel_cost': 25, 'casts': 10, 'lvl': 1,
     'min_hook_distance': 50, 'max_hook_distance': 100,
     'escape_distance': 200},

    {'name': OCEAN, 'bite_chance': 0.25, 'hook_chance': 0.55,
     'travel_cost': 35, 'casts': 8, 'lvl': 1,
     'min_hook_distance': 100, 'max_hook_distance': 300,
     'escape_distance': 500},

]