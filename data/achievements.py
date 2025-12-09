from events import EventType

KRILL_OR_BE_KRILLED = "Krill Or Be Krilled"
TENCH_KILLS = "Tench Kills"

Achievements = [
    {
        'id': KRILL_OR_BE_KRILLED,
        'name': "Krill or be Krilled",
        'description': "Defeat your first enemy",
        'reward_type': 'xp',
        'reward_value': 10,
        'listen_event': EventType.KILL,
        'trigger': lambda gs: gs.event_logger
    },
    {
        'id': TENCH_KILLS,
        'name': "Tench Kills",
        'description': "Defeat 10 enemies",
        'reward_type': 'perk',
        'reward_value': None,
        'listen_event': EventType.KILL,
    },
]
