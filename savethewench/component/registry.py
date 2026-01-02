from typing import Callable

from savethewench.component.base import Component

_REGISTRY = {}


# decorator that registers a component under the provided name
def register_component(name: str) -> Callable[[type[Component]], type[Component]]:
    def decorator(cls: type[Component]) -> type[Component]:
        if name in _REGISTRY and cls != _REGISTRY[name]:
            raise RuntimeError(f'Two components registered under the same name: {cls.__name__} and {_REGISTRY[name]}')
        _REGISTRY[name] = cls
        return cls
    return decorator


def get_registered_component(name: str) -> type[Component]:
    if name in _REGISTRY:
        return _REGISTRY[name]
    raise RuntimeError(f'No component registered under "{name}"')