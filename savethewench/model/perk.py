from dataclasses import dataclass, field
from functools import cache
from typing import List, Callable, Dict
from typing import TypeVar

from savethewench.data import Perks
from savethewench.ui import purple

T = TypeVar('T')


@dataclass
class Perk[T]:
    name: str
    cost: int
    description: str
    _active: bool = field(init=False, repr=False)  # value should not be changed from outside of class methods
    wrapper: Callable[[T, str, bool], T] = field(default=lambda x, s, b: x)

    def __post_init__(self):
        self._active = False

    @property
    def active(self):
        return self._active

    def is_active(self) -> bool:
        return self.active

    def activate(self):
        print(purple(f"{self.name} added to perks."))
        self._active = True


_PERKS: Dict[str, Perk] = {}


def set_perk_cache(perk_cache: Dict[str, Perk]):
    global _PERKS
    _PERKS = perk_cache


def load_perks(perk_filter: Callable[[Perk], bool] = lambda _: True) -> List[Perk]:
    res = []
    for d in Perks:
        name = d['name']
        if name not in _PERKS:
            _PERKS[name] = Perk(**d)
        perk = _PERKS[name]
        if perk_filter(perk):
            res.append(_PERKS[name])
    return res


@cache
def load_perk(perk_name: str) -> Perk:
    if perk_name in _PERKS:
        return _PERKS[perk_name]
    return load_perks(lambda p: p.name == perk_name)[0]


def activate_perk(perk_name: str):
    load_perk(perk_name).activate()


def perk_is_active(perk_name: str) -> bool:
    return load_perk(perk_name).is_active()


def attach_perk(*perks: str, value_description: str = "", silent: bool = False):
    perk_impls = load_perks(lambda p: p.name in set(perks))

    def decorator(func):
        def wrapper(*args, **kwargs):
            value = func(*args, **kwargs)
            for perk in perk_impls:
                if perk.is_active():
                    value = perk.wrapper(value, value_description, silent)
            return value

        return wrapper

    return decorator
