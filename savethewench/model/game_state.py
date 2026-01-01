import random
from collections import Counter
from dataclasses import dataclass, field
from typing import List, Dict

from savethewench import event_logger
from savethewench.audio import play_music
from savethewench.data.perks import TENCH_THE_BOUNTY_HUNTER
from savethewench.event_logger import subscribe_function, log_event
from savethewench.ui import green, red
from savethewench.util import print_and_sleep
from .achievement import AchievementEvent, set_achievement_cache, load_achievements, Achievement
from .area import Area, load_areas
from .bank import Bank
from .enemy import Enemy, load_enemy
from .events import TravelEvent, BountyCollectedEvent, PlayerDeathEvent, CoffeeEvent
from .item import Item
from .perk import attach_perk, Perk, set_perk_cache
from .player import Player
from .shop import Shop
from .weapon import Weapon
from ..data.illnesses import LATE_ONSET_SIDS, Illnesses


@dataclass
class GameState:
    player: Player = field(default_factory=Player)

    bank: Bank = field(default_factory=Bank)
    areas: List[Area] = field(default_factory=load_areas)
    current_area: Area = None

    wench_area: Area = field(default_factory=lambda: random.choice(load_areas()))  # TODO

    found_item: Item = None
    found_weapon: Weapon = None

    wanted: str = ''
    _bounty: int = 0

    victory = False

    event_counter: Counter = field(default_factory=Counter)
    perk_cache: Dict[str, Perk] = field(default_factory=dict)
    achievement_cache: Dict[str, Achievement] = field(default_factory=dict)

    @property
    def shop(self) -> Shop:
        return self.current_area.shop

    @property
    @attach_perk(TENCH_THE_BOUNTY_HUNTER, silent=True)
    def bounty(self):
        return self._bounty

    @bounty.setter
    def bounty(self, value):
        self._bounty = value

    def __post_init__(self):
        if self.current_area is None:
            self.current_area = self.areas[0]
        if len(self.wanted) == 0:
            self.refresh_bounty()
        event_logger.set_counter(self.event_counter)
        set_achievement_cache(self.achievement_cache)
        set_perk_cache(self.perk_cache)
        load_achievements()
        self._subscribe_listeners()

    def refresh_bounty(self):
        bounty_area = random.choice(self.areas)
        enemy_choice: Enemy = load_enemy(random.choice(bounty_area.enemies))  # = random.choice(load_enemies())
        self.wanted = enemy_choice.name
        self.bounty = enemy_choice.bounty

    def update_current_area(self, area_name: str):
        for area in self.areas:
            if area.name == area_name:
                self.current_area = area
                event_logger.log_event(TravelEvent(area_name))
                return
        raise KeyError(f"Area '{area_name}' not found")

    def play_current_area_theme(self):
        play_music(self.current_area.theme)

    def coffee_effect(self, item: Dict):
        if random.random() < item['risk']:
            player = self.player
            illness = random.choice(Illnesses)

            if illness['name'] != LATE_ONSET_SIDS:
                player.illness = illness['name']
                player.illness_death_lvl = player.lvl + illness['levels_until_death']

                print_and_sleep(red(f"Coughy coughed on your coffee and now you're sicker than Hell."), 4)
                print_and_sleep(red(f"Illness: {illness['name']}"), 3)
                print_and_sleep(red(f"Description: {illness['description']}"), 4)
                print_and_sleep(f"\nVisit the Free Range Children's Hospital for the cure "
                                f"or die when you reach level {player.illness_death_lvl}.", 4)
            else:
                print_and_sleep(red(f"Coughy coughed on your coffee and now you're just a worthless bag of bones."), 4)
                print_and_sleep(red(f"Cause of Death: {illness['name']}"), 3)
                print_and_sleep(red(f"Description: {illness['description']}"), 4)
                #TODO - Queue death

    def _subscribe_listeners(self):
        @subscribe_function(BountyCollectedEvent)
        def handle_bounty_collected_event(event: BountyCollectedEvent):
            print_and_sleep(green(f"You killed {event.enemy_name} and collected a bounty of {self.bounty} coins!"), 1)
            self.player.coins += self.bounty
            self.refresh_bounty()

        @subscribe_function(AchievementEvent)
        def handle_achievement_event(event: AchievementEvent):
            event.activate(self.player)

        @subscribe_function(CoffeeEvent)
        def handle_coffee_event(event: CoffeeEvent):
            self.coffee_effect()

    def is_final_boss_available(self) -> bool:
        return self.current_area.boss_defeated and (self.wench_area == self.current_area) and not self.victory

    def is_wanted(self, combatant):
        return self.wanted in combatant.name

    # for loading from save file
    def __setstate__(self, state):
        self.__dict__.update(state)
        self.__post_init__()
