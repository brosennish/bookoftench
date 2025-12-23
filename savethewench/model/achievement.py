import random
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Dict

from savethewench import event_logger
from savethewench.data import Achievements
from savethewench.data.achievements import RewardType
from savethewench.data.perks import WENCH_LOCATION
from savethewench.event_base import EventType, Event
from savethewench.event_logger import subscribe_function
from savethewench.model.perk import Perk, load_perks
from savethewench.model.player import Player
from savethewench.model.events import KillEvent
from savethewench.ui import orange
from savethewench.util import print_and_sleep



@dataclass
class Achievement:
    id: str
    name: str
    description: str
    reward_type: RewardType

    event_type: EventType
    event_threshold: int

    reward_value: Optional[int] = None
    active: bool = False

    def activation_action(self, player: Player):
        match self.reward_type:
            case RewardType.XP:
                player.gain_xp_other(self.reward_value)
            case RewardType.COIN:
                player.gain_coins(self.reward_value)
            case RewardType.PERK:
                # TODO - this is duplicated
                filtered: List[Perk] = load_perks(lambda p: not (p.active or p.name == WENCH_LOCATION))
                if len(filtered) > 0:
                    reward: Perk = random.choice(filtered)
                    reward.activate()
            case _:
                raise NotImplementedError(f"No reward type: {self.reward_type}")


class AchievementEvent(Event):
    def __init__(self, achievement: Achievement):
        super().__init__(EventType.ACHIEVEMENT_UNLOCKED)
        self.achievement = achievement

    def activate(self, player: Player):
        self.achievement.active = True
        print_and_sleep(orange(f"ACHIEVEMENT UNLOCKED: {self.achievement.name}\n"
                               f"Reward: {self.achievement.description}"), 3)
        self.achievement.activation_action(player)

@dataclass
class KillAchievement(Achievement):

    def __post_init__(self):
        @subscribe_function(KillEvent, name_override=self.id)
        def handle_event(_: Event):
            if event_logger.get_count(self.event_type) == self.event_threshold:
                event_logger.log_event(AchievementEvent(self))


_ACHIEVEMENTS: Dict[str, Achievement] = {}

def set_achievement_cache(achievement_cache: Dict[str, Achievement]):
    global _ACHIEVEMENTS
    _ACHIEVEMENTS = achievement_cache

def load_achievements() -> List[Achievement]:
    global _ACHIEVEMENTS
    res = []
    for d in Achievements:
        match d['event_type']:
            case EventType.KILL:
                achievement = KillAchievement(**d)
                if achievement.id not in _ACHIEVEMENTS:
                    _ACHIEVEMENTS[achievement.id] = achievement
                res.append(_ACHIEVEMENTS[achievement.id])
            case _:
                raise NotImplementedError(f"No achievement for this type: {d['event_type']}")
    return res
