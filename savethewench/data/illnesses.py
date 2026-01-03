LATE_ONSET_SIDS = "Late Onset Sudden Infant Death Syndrome"
PHANTOM_HIM_SYNDROME = "Phantom Him Syndrome"
RESTLESS_BUTT_SYNDROME = "Restless Butt Syndrome"
REVERSE_HAIR_GROWTH_SYNDROME = "Reverse Hair Growth Syndrome"


# TODO - Add more illnesses
Illnesses = [
    # --- Instant Death ---
    {'name': LATE_ONSET_SIDS,
     'description': "Sudden infant death syndrome occurring after infancy.",
     'levels_until_death': 0,
     'cost': 0,
     'success_rate': 0},

    # --- One Level ---


    # --- Two Levels ---
    {'name': PHANTOM_HIM_SYNDROME,
     'description': "You experience a man who is not there, but he will still kill you eventually.",
    'levels_until_death': 2,
    'cost': 200,
     'success_rate': 0.80},
    {'name': RESTLESS_BUTT_SYNDROME,
     'description': "Left untreated, you will, not unlike a whoopee cushion, deflate entirely.",
    'levels_until_death': 3,
     'cost': 150,
     'success_rate': 0.95},

    # --- Three Levels ---
    {'name': REVERSE_HAIR_GROWTH_SYNDROME,
     'description': "You fill with hair as it grows into your body rather than out from it.",
    'levels_until_death': 4,
     'cost': 175,
     'success_rate': 0.85},
]

