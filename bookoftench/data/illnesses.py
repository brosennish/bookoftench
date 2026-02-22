BABIES = "Babies"
LATE_ONSET_SIDS = "Late Onset Sudden Infant Death Syndrome"
MAD_TENCH_DISEASE = "Mad Tench Disease"
MIND_EATING_BACTERIAL_DISEASE = "Mind Eating Bacterial Disease"
PHANTOM_HIM_SYNDROME = "Phantom Him Syndrome"
RESTLESS_BUTT_SYNDROME = "Restless Butt Syndrome"
INWARD_HAIR_GROWTH_DISORDER = "Inward Hair Growth Disorder"

Illnesses = [
    # --- Instant Death ---
    {'name': LATE_ONSET_SIDS,
     'description': "Sudden infant death syndrome that occurs after infancy.",
     'levels_until_death': 0,
     'cost': 0,
     'success_rate': 0},

    # --- Two Levels ---
    {'name': PHANTOM_HIM_SYNDROME,
     'description': "A condition in which one eventually dies at the hands of a man only they can perceive.",
     'levels_until_death': 2,
     'cost': 120,
     'success_rate': 0.70},

    {'name': RESTLESS_BUTT_SYNDROME,
     'description': "Left untreated, you will, not unlike a whoopee cushion, deflate entirely.",
     'levels_until_death': 2,
     'cost': 105,
     'success_rate': 0.75},

    {'name': BABIES,
     'description': "Like rabies, but instead of turning rabid, you turn infantile and die.",
     'levels_until_death': 2,
     'cost': 95,
     'success_rate': 0.80},

    # --- Three Levels ---
    {'name': MIND_EATING_BACTERIAL_DISEASE,
     'description': "An infection involving mind-eating bacteria.",
     'levels_until_death': 3,
     'cost': 160,
     'success_rate': 0.65},

    {'name': INWARD_HAIR_GROWTH_DISORDER,
     'description': "A condition characterized by one's hair growing into their body.",
     'levels_until_death': 3,
     'cost': 135,
     'success_rate': 0.70},

    {'name': MAD_TENCH_DISEASE,
     'description': "A condition characterized by a loss of sanity over the sanctity of tench.",
     'levels_until_death': 3,
     'cost': 60,
     'success_rate': 0.20},
]
