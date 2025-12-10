import time as t

from data.colors import yellow as y, reset as rst
from events import Listener, ItemUsedEvent
from model.game_state import GameState
from event_logger import add_subscriber


class ItemUsedListener(Listener):
    def get_listen_type(self) -> type[ItemUsedEvent]:
        return ItemUsedEvent

    def handle_event(self, event: ItemUsedEvent):
        print(f"\nYou used {event.item.name}: Your current HP is {event.player_hp}/{event.player_max_hp}\n")
        t.sleep(1)
        if event.items_remaining == 0:
            print(f"{y}Your inventory is dry.{rst}\n")
        t.sleep(1)


def subscribe_listeners():
    add_subscriber(ItemUsedListener())
