from abc import ABCMeta
from collections import Counter, defaultdict
from typing import Dict, Set, Callable

from bookoftench.event_base import Listener, EventType, Event

_COUNTER = Counter()
_LISTENERS: Dict[type[Event], Set[type[Listener]]] = defaultdict(set)


# log events to a counter from a different class -
# to GameState in particular, so that counts can be
# serialized more easily when game is saved and
# set when game is loaded
def set_counter(counter: Counter) -> None:
    global _COUNTER
    _COUNTER = counter


def log_event(event: Event) -> None:
    _COUNTER[event.type] += 1
    event.callback()
    _notify(event)


def add_subscriber(listener: Listener, *event_types: type[Event]) -> None:
    global _LISTENERS
    for event_type in event_types:
        _LISTENERS[event_type].add(type[listener])


def remove_subscriber(listener: Listener) -> None:
    global _LISTENERS
    for event_type, listener_classes in _LISTENERS.items():
        if type(listener) in listener_classes:
            listener_classes.remove(type(listener))


def get_count(event_type: EventType) -> int:
    return _COUNTER[event_type]


def _notify(event: Event) -> None:
    for listener_class in _LISTENERS[type(event)]:
        listener_class.handle_event(event=event)


def reset() -> None:
    global _COUNTER, _LISTENERS
    _COUNTER.clear()
    _LISTENERS.clear()


# annotate a class to subscribe to provided event types
# class must implement event_base.Listener
def subscribe_listener(*event_types: type[Event]) -> Callable[[type[Listener]], None]:
    def decorator(cls: type[Listener]) -> None:
        global _LISTENERS
        for event_type in event_types:
            _LISTENERS[event_type].add(cls)

    return decorator


# annotate a function to subscribe to provided event types
# function must have signature (Event) -> None
def subscribe_function(*event_types: type[Event], name_override: str = None):
    def decorator(func: Callable[[Event], None]):
        class FunctionNamingMC(ABCMeta, type):
            def __new__(cls, name, bases, attrs):
                func_name, func_module = func.__name__, func.__module__
                attrs['__qualname__'] = name_override if name_override else func_name
                attrs['__module__'] = func_module
                return super().__new__(cls, func_name, bases, attrs)

            def __eq__(self, other):
                return self.__module__ == other.__module__ and self.__qualname__ == other.__qualname__

            def __hash__(self):
                return hash((self.__module__, self.__qualname__))

        class AnonymousListener(Listener, metaclass=FunctionNamingMC):
            @staticmethod
            def handle_event(event: Event):
                func(event)

        global _LISTENERS
        for event_type in event_types:
            s = _LISTENERS[event_type]
            if AnonymousListener in s:
                # important so that the most recent instance is always present, when listener is stateful
                s.remove(AnonymousListener)
            s.add(AnonymousListener)

    return decorator
