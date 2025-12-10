from collections import Counter, defaultdict
from typing import Dict, Set, Callable, Any, List

from events import Listener, EventType, Event

_COUNTER = Counter()
_LISTENERS: Dict[EventType, Set[Listener]] = defaultdict(set)


def log_event(event: Event):
    _COUNTER[event.type] += 1
    _notify(event)


def add_subscriber(listener: Listener, event_types: List[EventType]):
    global _LISTENERS
    for eventType in event_types:
        _LISTENERS[eventType].add(listener)

def remove_subscriber(listener: Listener):
    global _LISTENERS
    for listeners in _LISTENERS.values():
        if listener in listeners:
            listeners.remove(listener)


def get_count(event_type: EventType) -> int:
    return _COUNTER[event_type]


def _notify(event: Event):
    for listener in _LISTENERS[event.type]:
        listener.handle_event(event)


def reset():
    global _COUNTER, _LISTENERS
    _COUNTER.clear()
    _LISTENERS.clear()


def subscribe_listener(func: Callable[[Any, Any], Listener], event_types: List[EventType]):
    def wrapper(*args, **kwargs):
        if func:
            result = func(*args, **kwargs)
            add_subscriber(result, event_types)
            return result
        return func
    return wrapper
