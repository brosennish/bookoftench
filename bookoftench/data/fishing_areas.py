
# ================================================================================================

# Fishing Areas
SHALLOWS = "Shallows"
BAY = "Bay"
OCEAN = "Ocean"

# Seasons
DRY_SEASON = "Dry Season"
WET_SEASON = "Wet Season"

# Season Effects
DRY_SEASON_BITE_CHANCE_EFFECT = -0.10
WET_SEASON_BITE_CHANCE_EFFECT = 0.05

# Bite Chance Multiplier
BITE_CHANCE_MULTIPLIER = 1

# ================================================================================================

Fishing_Areas = [

    {'name': SHALLOWS, 'bite_chance': 0.35, 'hook_chance': 0.75,
     'travel_cost': 15, 'casts': 6, 'lvl': 1,
     'pull_mult': 1.0, 'run_mult': 1.0,
     'min_hook_distance': 25, 'max_hook_distance': 75,
     'escape_distance': 100},

    {'name': BAY, 'bite_chance': 0.30, 'hook_chance': 0.65,
     'travel_cost': 35, 'casts': 6, 'lvl': 1,
     'pull_mult': 1.5, 'run_mult': 1.5,
     'min_hook_distance': 50, 'max_hook_distance': 150,
     'escape_distance': 200},

    {'name': OCEAN, 'bite_chance': 0.25, 'hook_chance': 0.55,
     'travel_cost': 60, 'casts': 6, 'lvl': 1,
     'pull_mult': 2.0, 'run_mult': 2.0,
     'min_hook_distance': 100, 'max_hook_distance': 200,
     'escape_distance': 300},

]