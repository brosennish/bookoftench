import time as t

from savethewench.event_base import Listener
from savethewench.model.events import ItemUsedEvent
from savethewench.ui import yellow
from .event_logger import subscribe_listener


@subscribe_listener(ItemUsedEvent)
class ItemUsedListener(Listener):
    def handle_event(self, event: ItemUsedEvent):
        print(f"\nYou used {event.item_name}: Your current HP is {event.player_hp}/{event.player_max_hp}\n")
        t.sleep(1)
        if event.items_remaining == 0:
            print(yellow(f"Your inventory is dry.\n"))
        t.sleep(1)
