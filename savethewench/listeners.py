import time as t

from savethewench.data.colors import yellow as y, reset as rst
from savethewench.event_base import Listener
from event_logger import subscribe_listener
from savethewench.model.events import ItemUsedEvent


@subscribe_listener(ItemUsedEvent)
class ItemUsedListener(Listener):

    @staticmethod
    def handle_event(event: ItemUsedEvent):
        print(f"\nYou used {event.item.name}: Your current HP is {event.player_hp}/{event.player_max_hp}\n")
        t.sleep(1)
        if event.items_remaining == 0:
            print(f"{y}Your inventory is dry.{rst}\n")
        t.sleep(1)

