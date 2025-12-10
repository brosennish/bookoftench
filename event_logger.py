from collections import Counter, defaultdict
from typing import Dict, Set

from events import Listener, EventType, Event

_COUNTER = Counter()
_LISTENERS: Dict[type[Event], Set[type[Listener]]] = defaultdict(set)


def log_event(event: Event):
    _COUNTER[event.type] += 1
    _notify(event)


def add_subscriber(listener: Listener, *event_types: type[Event]):
    global _LISTENERS
    for event_type in event_types:
        _LISTENERS[event_type].add(type[listener])


def remove_subscriber(listener: Listener):
    global _LISTENERS
    for event_type, listener_classes in _LISTENERS.items():
        if type(listener) in listener_classes:
            listener_classes.remove(type(listener))


def get_count(event_type: EventType) -> int:
    return _COUNTER[event_type]


def _notify(event: Event):
    for listener_class in _LISTENERS[type(event)]:
        listener_class.handle_event(event=event)


def reset():
    global _COUNTER, _LISTENERS
    _COUNTER.clear()
    _LISTENERS.clear()


# class-annotating decorator that will subscribe a class to the listed event types
def subscribe_listener(*event_types: type[Event]):
    def decorator(cls: type[Listener]):
        global _LISTENERS
        for event_type in event_types:
            _LISTENERS[event_type].add(cls)

    return decorator
