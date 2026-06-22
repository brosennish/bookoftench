BABIES = "Babies"
FEVER_DREAMS = "Fever Dreams"
HEAVY_HEAD_SYNDROME = "Heavy Head Syndrome"
HERPES = "Herpes"
LATE_ONSET_SIDS = "Late Onset Sudden Infant Death Syndrome"
MAD_TENCH_DISEASE = "Mad Tench Disease"
MIND_EATING_BACTERIA_DISORDER = "Mind-Eating Bacteria Disorder"
PHANTOM_HIM_SYNDROME = "Phantom Him Syndrome"
POST_SHARTUM_DEPRESSION = "Post-Shartum Depression"
RESTLESS_BUTT_SYNDROME = "Restless Butt Syndrome"
INWARD_HAIR_GROWTH_DISORDER = "Inward Hair Growth Disorder"
TERMITE_INFESTATION = "Termite Infestation"

# ================================================================================================

Illnesses = [

    # ============================
    #        SUDDEN DEATH
    # ============================

    {'name': LATE_ONSET_SIDS,
     'description': "Sudden infant death syndrome that occurs after infancy.",
     'levels_until_death': 0,
     'cost': 0,
     'success_rate': 0},

    # ============================
    #         ONE LEVEL
    # ============================

    {'name': MAD_TENCH_DISEASE,
     'description': "A condition characterized by a loss of sanity over the immeasurable glory of tench.",
     'levels_until_death': 1,
     'cost': 60,
     'success_rate': 0.22},

    # ============================
    #         TWO LEVELS
    # ============================

    {'name': HEAVY_HEAD_SYNDROME,
     'description': "A condition in which your head grows heavier until it rips off of your neck.",
     'levels_until_death': 2,
     'cost': 105,
     'success_rate': 0.75},

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

    # ============================
    #        THREE LEVELS
    # ============================

    {'name': FEVER_DREAMS,
     'description': "A condition in which your temperature can rise to fatal levels while you dream.",
     'levels_until_death': 3,
     'cost': 130,
     'success_rate': 0.75},

    {'name': HERPES,
     'description': "It's not not herpes.",
     'levels_until_death': 3,
     'cost': 120,
     'success_rate': 0.80},

    {'name': MIND_EATING_BACTERIA_DISORDER,
     'description': "A fatal disorder in which one's mind consumes dangerous amounts of bacteria.",
     'levels_until_death': 3,
     'cost': 160,
     'success_rate': 0.65},

    {'name': INWARD_HAIR_GROWTH_DISORDER,
     'description': "A condition characterized by one's hair growing into their body and filling the spaces within.",
     'levels_until_death': 3,
     'cost': 135,
     'success_rate': 0.70},

    # ============================
    #        FOUR LEVELS
    # ============================

    {'name': POST_SHARTUM_DEPRESSION,
     'description': "An extensive, fatal depression brought on by a profoundly traumatic sharting event.",
     'levels_until_death': 4,
     'cost': 100,
     'success_rate': 0.50},

    {'name': TERMITE_INFESTATION,
     'description': "A condition in which a rapidly growing termite colony voraciously devours you from the inside.",
     'levels_until_death': 4,
     'cost': 100,
     'success_rate': 0.80},

]
