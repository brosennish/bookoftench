import random
from dataclasses import dataclass
from typing import Optional, List, Dict

from bookoftench import event_logger
from bookoftench.data import Achievements
from bookoftench.data.achievements import RewardType
from bookoftench.data.perks import WENCH_LOCATION
from bookoftench.event_base import EventType, Event
from bookoftench.event_logger import subscribe_function
from bookoftench.model.events import KillEvent, CoffeeEvent, LevelUpEvent, FleeEvent, BountyCollectedEvent, \
    TreatmentEvent, GenericStealEvent, DiscoveryEventLegendary, DiscoveryEventMythic
from bookoftench.model.perk import Perk, load_perks
from bookoftench.model.player import Player
from bookoftench.ui import orange
from bookoftench.util import print_and_sleep


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

    def do_activation_action(self, player: Player) -> None:
        reward_str: str = ''
        reward_callback = lambda: None  # so we can print the achievement unlock before any reward messaging
        match self.reward_type:
            case RewardType.XP:
                reward_callback = lambda: player.gain_xp_other(self.reward_value)
                reward_str = f"{self.reward_value} XP"
            case RewardType.COIN:
                reward_callback = lambda: player.gain_coins(self.reward_value)
                reward_str = f"{self.reward_value} of coin"
            case RewardType.PERK:
                # TODO - this is duplicated
                filtered: List[Perk] = load_perks(lambda p: not (p.active or p.name == WENCH_LOCATION))
                if len(filtered) > 0:
                    reward: Perk = random.choice(filtered)
                    reward_callback = lambda: reward.activate()
                    reward_str = f"{reward.name} | {reward.description}"
            case _:
                raise NotImplementedError(f"No reward type: {self.reward_type}")
        print_and_sleep(orange(f"ACHIEVEMENT UNLOCKED: {self.name} ({self.description})"
                               f"{f"\nReward: {reward_str}" if len(reward_str) > 0 else ''}"), 2)
        reward_callback()


class AchievementEvent(Event):
    def __init__(self, achievement: Achievement):
        super().__init__(EventType.ACHIEVEMENT_UNLOCKED)
        self.achievement = achievement

    def activate(self, player: Player) -> None:
        self.achievement.active = True
        self.achievement.do_activation_action(player)


@dataclass
class BountyCollectedAchievement(Achievement):

    def __post_init__(self):
        @subscribe_function(BountyCollectedEvent, name_override=self.id)
        def handle_event(_: Event):
            if event_logger.get_count(self.event_type) == self.event_threshold:
                event_logger.log_event(AchievementEvent(self))


@dataclass
class CoffeeAchievement(Achievement):

    def __post_init__(self):
        @subscribe_function(CoffeeEvent, name_override=self.id)
        def handle_event(_: Event):
            if event_logger.get_count(self.event_type) == self.event_threshold:
                event_logger.log_event(AchievementEvent(self))


@dataclass
class DiscoveryEventAchievement(Achievement):

    def __post_init__(self):
        @subscribe_function(DiscoveryEventLegendary, DiscoveryEventMythic, name_override=self.id)
        def handle_event(_: Event):
            if event_logger.get_count(self.event_type) == self.event_threshold:
                event_logger.log_event(AchievementEvent(self))


@dataclass
class FleeAchievement(Achievement):

    def __post_init__(self):
        @subscribe_function(FleeEvent, name_override=self.id)
        def handle_event(_: Event):
            if event_logger.get_count(self.event_type) == self.event_threshold:
                event_logger.log_event(AchievementEvent(self))


@dataclass
class KillAchievement(Achievement):

    def __post_init__(self):
        @subscribe_function(KillEvent, name_override=self.id)
        def handle_event(_: Event):
            if event_logger.get_count(self.event_type) == self.event_threshold:
                event_logger.log_event(AchievementEvent(self))


@dataclass
class LevelUpAchievement(Achievement):

    def __post_init__(self):
        @subscribe_function(LevelUpEvent, name_override=self.id)
        def handle_event(_: Event):
            if event_logger.get_count(self.event_type) == self.event_threshold:
                event_logger.log_event(AchievementEvent(self))


@dataclass
class TreatmentEventAchievement(Achievement):

    def __post_init__(self):
        @subscribe_function(TreatmentEvent, name_override=self.id)
        def handle_event(_: Event):
            if event_logger.get_count(self.event_type) == self.event_threshold:
                event_logger.log_event(AchievementEvent(self))


@dataclass
class StealingAchievement(Achievement):

    def __post_init__(self):
        @subscribe_function(GenericStealEvent, name_override=self.id)
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
            case EventType.BOUNTY_COLLECTED:
                achievement = BountyCollectedAchievement(**d)
                if achievement.id not in _ACHIEVEMENTS:
                    _ACHIEVEMENTS[achievement.id] = achievement
                res.append(_ACHIEVEMENTS[achievement.id])
            case EventType.COFFEE_EVENT:
                achievement = CoffeeAchievement(**d)
                if achievement.id not in _ACHIEVEMENTS:
                    _ACHIEVEMENTS[achievement.id] = achievement
                res.append(_ACHIEVEMENTS[achievement.id])
            case EventType.FLEE:
                achievement = FleeAchievement(**d)
                if achievement.id not in _ACHIEVEMENTS:
                    _ACHIEVEMENTS[achievement.id] = achievement
                res.append(_ACHIEVEMENTS[achievement.id])
            case EventType.KILL:
                achievement = KillAchievement(**d)
                if achievement.id not in _ACHIEVEMENTS:
                    _ACHIEVEMENTS[achievement.id] = achievement
                res.append(_ACHIEVEMENTS[achievement.id])
            case EventType.LEVEL_UP:
                achievement = LevelUpAchievement(**d)
                if achievement.id not in _ACHIEVEMENTS:
                    _ACHIEVEMENTS[achievement.id] = achievement
                res.append(_ACHIEVEMENTS[achievement.id])
            case EventType.STEAL:
                achievement = StealingAchievement(**d)
                if achievement.id not in _ACHIEVEMENTS:
                    _ACHIEVEMENTS[achievement.id] = achievement
                res.append(_ACHIEVEMENTS[achievement.id])
            case EventType.TREATMENT_EVENT:
                achievement = TreatmentEventAchievement(**d)
                if achievement.id not in _ACHIEVEMENTS:
                    _ACHIEVEMENTS[achievement.id] = achievement
                res.append(_ACHIEVEMENTS[achievement.id])
            case _:
                raise NotImplementedError(f"No achievement for this type: {d['event_type']}")
    return res
