from abc import ABCMeta
from collections import Counter, defaultdict
from typing import Dict, Set, Callable

from savethewench.event_base import Listener, EventType, Event

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


# annotate a class to subscribe to provided event types
# class must implement event_base.Listener
def subscribe_listener(*event_types: type[Event]):
    def decorator(cls: type[Listener]):
        global _LISTENERS
        for event_type in event_types:
            _LISTENERS[event_type].add(cls)

    return decorator


# annotate a function to subscribe to provided event types
# function must have signature (Event) -> None
def subscribe_function(*event_types: type[Event]):
    def decorator(func: Callable[[Event], None]):
        class FunctionNamingMC(ABCMeta, type):
            def __new__(cls, name, bases, attrs):
                func_name, func_module = func.__name__, func.__module__
                attrs['__qualname__'] = func_name
                attrs['__module__'] = func_module
                return super().__new__(cls, func_name, bases, attrs)

        class AnonymousListener(Listener, metaclass=FunctionNamingMC):
            @staticmethod
            def handle_event(event: Event):
                func(event)

        global _LISTENERS
        for event_type in event_types:
            _LISTENERS[event_type].add(AnonymousListener)

    return decorator
