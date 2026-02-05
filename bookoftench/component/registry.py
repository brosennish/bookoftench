from typing import Callable, TypeVar

from bookoftench.component.base import Component

_REGISTRY = {}

C = TypeVar('C', bound=Component)


# decorator that registers a component under the provided name
def register_component(name: str) -> Callable[[type[C]], type[C]]:
    def decorator(cls: type[C]) -> type[C]:
        if name in _REGISTRY and cls != _REGISTRY[name]:
            raise RuntimeError(f'Two components registered under the same name: {cls.__name__} and {_REGISTRY[name]}')
        _REGISTRY[name] = cls
        return cls

    return decorator


def get_registered_component(name: str) -> type[C]:
    if name in _REGISTRY:
        return _REGISTRY[name]
    raise RuntimeError(f'No component registered under "{name}"')
