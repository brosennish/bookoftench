
# ================================================================================================

# Fishing Items
BARB_HOOK = "Barb Hook"
LAMPREYS = "Lampreys"
LEECHES = "Leeches"
MOTION_POTION = "Motion Potion"
OCEAN_LOTION = "Ocean Lotion"
REEFER = "Reefer"
SEA_WEED = "Sea Weed"

# Types
RAGE = "Rage"
SPEED = "Speed"
SPIT_HOOK = "Spit Hook"
STAMINA = "Stamina"

# ================================================================================================

# Shop -> [B] Bait [I] Items
# Use tackle box for storage
# Use items during battle

Fishing_Items = [
    {'name': BARB_HOOK, 'description': 'Prevents spit hook for 6 turns.',
     'type': SPIT_HOOK, 'cost': 15, 'min_turns': 6, 'max_turns': 6,
     'speed_reduction': 0, 'stamina_reduction': 0, 'rage_reduction': 0,
     'strength_reduction': 0, 'spit_hook_prevention': True,
     },
    {'name': LAMPREYS, 'description': 'Increases stamina loss by 30% for 4-6 turns.',
     'type': STAMINA, 'cost': 40, 'min_turns': 4, 'max_turns': 6,
     'speed_reduction': 0, 'stamina_reduction': 0.30, 'rage_reduction': 0,
     'strength_reduction': 0, 'spit_hook_prevention': False,
     },
    {'name': LEECHES, 'description': 'Increases stamina loss by 15% for 4-8 turns.',
     'type': STAMINA, 'cost': 20, 'min_turns': 4, 'max_turns': 8,
     'speed_reduction': 0, 'stamina_reduction': 0.15, 'rage_reduction': 0,
     'strength_reduction': 0, 'spit_hook_prevention': False,
     },
    {'name': MOTION_POTION, 'description': 'Lowers speed by 35% for 4-6 turns.',
     'type': SPEED, 'cost': 30, 'min_turns': 4, 'max_turns': 6,
     'speed_reduction': 0.35, 'stamina_reduction': 0, 'rage_reduction': 0,
     'strength_reduction': 0, 'spit_hook_prevention': False,
     },
    {'name': OCEAN_LOTION, 'description': 'Lowers rage gain by 50% for 3-5 turns.',
     'type': RAGE, 'cost': 50, 'min_turns': 3, 'max_turns': 5,
     'speed_reduction': 0, 'stamina_reduction': 0, 'rage_reduction': 0.50,
     'strength_reduction': 0, 'spit_hook_prevention': False,
     },
    {'name': REEFER, 'description': 'Lowers rage gain by 25% for 3-5 turns.',
     'type': RAGE, 'cost': 20, 'min_turns': 3, 'max_turns': 5,
     'speed_reduction': 0, 'stamina_reduction': 0, 'rage_reduction': 0.25,
     'strength_reduction': 0, 'spit_hook_prevention': False,
     },
    {'name': SEA_WEED, 'description': 'Lowers rage gain by 35% for 3-5 turns.',
     'type': RAGE, 'cost': 35, 'min_turns': 3, 'max_turns': 5,
     'speed_reduction': 0, 'stamina_reduction': 0, 'rage_reduction': 0.35,
     'strength_reduction': 0, 'spit_hook_prevention': False,
     },
]