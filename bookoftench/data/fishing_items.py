
# ================================================================================================

# Fishing Items
BARB_HOOK = "Barb Hook"
LAMPREYS = "Lampreys"
LEECHES = "Leeches"
LIP_RING = "Lip Ring"
KELP_NET = "Kelp Net"
MOTION_POTION = "Motion Potion"
SALT_RUB = "Salt Rub"
REEFER = "Reefer"
SEA_WEED = "Sea Weed"
SNAIL_LUBE = "Snail Lube"

# Types
RAGE = "Rage"
SPEED = "Speed"
SPIT_HOOK = "Spit Hook"
STAMINA = "Stamina"

# ================================================================================================

Fishing_Items = [
    {'name': LIP_RING, 'description': 'Prevents spit hook for 6-8 turns.',
     'type': SPIT_HOOK, 'cost': 10, 'min_turns': 6, 'max_turns': 8,
     'speed_reduction': 0, 'stamina_reduction': 0, 'rage_reduction': 0,
     'strength_reduction': 0, 'spit_hook_prevention': True,
     },

    {'name': BARB_HOOK, 'description': 'Prevents spit hook for 10-12 turns.',
     'type': SPIT_HOOK, 'cost': 22, 'min_turns': 10, 'max_turns': 12,
     'speed_reduction': 0, 'stamina_reduction': 0, 'rage_reduction': 0,
     'strength_reduction': 0, 'spit_hook_prevention': True,
     },

    {'name': KELP_NET, 'description': 'Lowers speed by 50% for 3-5 turns.',
     'type': SPEED, 'cost': 30, 'min_turns': 3, 'max_turns': 5,
     'speed_reduction': 0.50, 'stamina_reduction': 0, 'rage_reduction': 0,
     'strength_reduction': 0, 'spit_hook_prevention': False,
     },

    {'name': LAMPREYS, 'description': 'Increases stamina loss by 35% for 4-6 turns.',
     'type': STAMINA, 'cost': 24, 'min_turns': 4, 'max_turns': 6,
     'speed_reduction': 0, 'stamina_reduction': 0.35, 'rage_reduction': 0,
     'strength_reduction': 0, 'spit_hook_prevention': False,
     },

    {'name': LEECHES, 'description': 'Increases stamina loss by 15% for 4-8 turns.',
     'type': STAMINA, 'cost': 12, 'min_turns': 4, 'max_turns': 8,
     'speed_reduction': 0, 'stamina_reduction': 0.15, 'rage_reduction': 0,
     'strength_reduction': 0, 'spit_hook_prevention': False,
     },

    {'name': MOTION_POTION, 'description': 'Lowers speed by 35% for 4-6 turns.',
     'type': SPEED, 'cost': 20, 'min_turns': 4, 'max_turns': 6,
     'speed_reduction': 0.35, 'stamina_reduction': 0, 'rage_reduction': 0,
     'strength_reduction': 0, 'spit_hook_prevention': False,
     },

    {'name': SNAIL_LUBE, 'description': 'Lowers speed by 15% for 4-8 turns.',
     'type': SPEED, 'cost': 12, 'min_turns': 4, 'max_turns': 8,
     'speed_reduction': 0.15, 'stamina_reduction': 0, 'rage_reduction': 0,
     'strength_reduction': 0, 'spit_hook_prevention': False,
     },

    {'name': SALT_RUB, 'description': 'Lowers rage gain by 50% for 3-5 turns.',
     'type': RAGE, 'cost': 35, 'min_turns': 3, 'max_turns': 5,
     'speed_reduction': 0, 'stamina_reduction': 0, 'rage_reduction': 0.50,
     'strength_reduction': 0, 'spit_hook_prevention': False,
     },

    {'name': REEFER, 'description': 'Lowers rage gain by 25% for 3-5 turns.',
     'type': RAGE, 'cost': 15, 'min_turns': 3, 'max_turns': 5,
     'speed_reduction': 0, 'stamina_reduction': 0, 'rage_reduction': 0.25,
     'strength_reduction': 0, 'spit_hook_prevention': False,
     },

    {'name': SEA_WEED, 'description': 'Lowers rage gain by 35% for 4-6 turns.',
     'type': RAGE, 'cost': 26, 'min_turns': 4, 'max_turns': 6,
     'speed_reduction': 0, 'stamina_reduction': 0, 'rage_reduction': 0.35,
     'strength_reduction': 0, 'spit_hook_prevention': False,
     },
]