from bookoftench.event_base import Listener
from bookoftench.model.events import ItemUsedEvent, TravelEvent
from bookoftench.ui import yellow, cyan
from .audio import play_music
from .data.audio import TRAVEL_THEME
from .data.items import NORMAL, FLEE
from .event_logger import subscribe_listener
from .util import print_and_sleep


@subscribe_listener(ItemUsedEvent)
class ItemUsedListener(Listener):
    @staticmethod
    def handle_event(event: ItemUsedEvent):
        if event.item_type == NORMAL:
            print_and_sleep(
                f"You used {event.item_name}: Your current HP is {event.player_hp}/{event.player_max_hp}", 1)
        if event.item_type == FLEE:
            print_and_sleep(
                f"You used {event.item_name}.", 1)
        if event.items_remaining == 0:
            print_and_sleep(yellow(f"Your inventory is dry."), 1)


@subscribe_listener(TravelEvent)
class TravelListener(Listener):
    @staticmethod
    def handle_event(event: TravelEvent):
        play_music(TRAVEL_THEME)
        print_and_sleep(cyan(f'Traveling by six-by-eight to the {event.area_name}...'), 5)
