import time as t

from savethewench.event_base import Listener
from savethewench.model.events import ItemUsedEvent, TravelEvent
from savethewench.ui import yellow, cyan
from .audio import play_music
from .data.audio import TRAVEL_THEME
from .event_logger import subscribe_listener
from .util import print_and_sleep


@subscribe_listener(ItemUsedEvent)
class ItemUsedListener(Listener):
    @staticmethod
    def handle_event(event: ItemUsedEvent):
        print(f"\nYou used {event.item_name}: Your current HP is {event.player_hp}/{event.player_max_hp}\n")
        t.sleep(1)
        if event.items_remaining == 0:
            print(yellow(f"Your inventory is dry.\n"))
        t.sleep(1)

@subscribe_listener(TravelEvent)
class TravelListener(Listener):
    @staticmethod
    def handle_event(event: TravelEvent):
        play_music(TRAVEL_THEME)
        print_and_sleep(cyan(f'Traveling by six by eight to the {event.area_name}...'), 5)
