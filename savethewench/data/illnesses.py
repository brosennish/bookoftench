LATE_ONSET_SIDS = "Late Onset Sudden Infant Death Syndrome"
PHANTOM_HIM_SYNDROME = "Phantom Him Syndrome"
RESTLESS_BUTT_SYNDROME = "Restless Butt Syndrome"
REVERSE_HAIR_GROWTH_SYNDROME = "Reverse Hair Growth Syndrome"


# TODO - Add more illnesses
Illnesses = [
    # --- Instant Death ---
    {'name': LATE_ONSET_SIDS,
     'description': "Sudden infant death syndrome that does not take effect until after one's infancy.",
     'levels_until_death': 0,
     'cost': 0,
     'success_rate': 0},

    # --- One Level ---


    # --- Two Levels ---
    {'name': PHANTOM_HIM_SYNDROME,
     'description': "A chilling condition in which one experiences a man who is not there."
                    "\nHowever, without medical intervention, this man will kill you after some time.",
    'levels_until_death': 2,
    'cost': 200},
    {'name': RESTLESS_BUTT_SYNDROME,
     'description': "Left untreated, you will, not unlike a whoopee cushion, deflate entirely.",
    'levels_until_death': 2,
     'cost': 150},

    # --- Three Levels ---
    {'name': REVERSE_HAIR_GROWTH_SYNDROME,
     'description': "A surprisingly common condition in which one's hair grows inward instead of outward."
                    "\nOver time, the disorderly will fill with hair until there's no room left in there.",
    'levels_until_death': 3,
     'cost': 175},
]

