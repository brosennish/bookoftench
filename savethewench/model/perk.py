import copy
import random
from dataclasses import dataclass, field
from functools import cache, partial
from typing import List, Callable, Dict
from typing import TypeVar

from savethewench.data import Perks
from savethewench.data.perks import WrapperType
from savethewench.model.base import Buyable
from savethewench.ui import purple, dim, cyan, orange
from savethewench.util import print_and_sleep

T = TypeVar('T')


@dataclass
class WrapperConfig[T]:
    def to_wrapper(self, name: str, wrapper_type: WrapperType) -> Callable[[T, str, bool], T]:
        return lambda original, value_description, silent: original

@dataclass
class BooleanOverrideConfig(WrapperConfig):
    override: bool

    def to_wrapper(self,  name: str, _: WrapperType) -> Callable[[bool, str, bool], bool]:
        return lambda original, value_description, silent: self.override

@dataclass
class BoundedRandomConfig(WrapperConfig):
    lower_bound: int
    upper_bound: int

    def _wrapper(self, original: int, value_description: str, silent: bool, name: str) -> int:
        val = random.randint(self.lower_bound, self.upper_bound)
        if not silent:
            if len(value_description) == 0:
                print_and_sleep(f"Applied perk: {name}", 1)
            else:
                print_and_sleep(purple(f"{name} increased {original} {value_description} to {original + val}"), 1)
        return original + val

    def to_wrapper(self, name: str, _: WrapperType) -> Callable[[int, str, bool], int]:
        return partial(self._wrapper, name=name)

@dataclass
class NumericChangeConfig(WrapperConfig):
    change: int

    _int_change: Callable[[int, int], int] = lambda orig, i: orig + i
    _percent_change: Callable[[float, int], float] = lambda orig, pct: orig + (float(pct) / 100.0)
    _int_change_by_percent: Callable[[int, int], int] = lambda orig, pct: int(orig * (1 + (float(pct) / 100.0)))
    _float_change_by_percent: Callable[[float, int], float] = lambda orig, pct: orig * (1 + (float(pct) / 100.0))

    def _numeric_change(self, original: int | float, value_description: str, silent: bool, name: str,
                        change_func: Callable[[int | float, int | float], int | float], is_percent=True) -> int | float:
        if not silent:
            if len(value_description) == 0:
                print_and_sleep(purple(f"Applied perk: {name}"), 1)
            else:
                inc_or_dec = "increased" if self.change >= 0 else "decreased"
                print_and_sleep(purple(f"{name} {inc_or_dec} {value_description} by "
                                       f"{abs(self.change)}{'%' if is_percent else ''}"), 1)
        return change_func(original, self.change)

    def to_wrapper(self, name: str, wrapper_type: WrapperType) -> Callable[[T, str, bool], T]:
        match wrapper_type:
            case WrapperType.INT_CHANGE:
                return partial(self._numeric_change, name=name, change_func=self._int_change, is_percent=False)
            case WrapperType.PERCENT_CHANGE:
                return partial(self._numeric_change, name=name, change_func=self._percent_change, is_percent=True)
            case WrapperType.INT_CHANGE_BY_PERCENT:
                return partial(self._numeric_change, name=name, change_func=self._int_change_by_percent, is_percent=True)
            case WrapperType.FLOAT_CHANGE_BY_PERCENT:
                return partial(self._numeric_change, name=name, change_func=self._float_change_by_percent, is_percent=True)
            case _:
                raise NotImplementedError(f"{wrapper_type} not implemented")

@dataclass
class Perk[T](Buyable):
    name: str
    cost: int
    description: str
    _active: bool = False  # value should not be changed from outside of class methods
    wrapper_type: WrapperType = WrapperType.NONE
    wrapper_config: WrapperConfig = field(default_factory=WrapperConfig)
    wrapper: Callable[[T, str, bool], T] = field(init=False, repr=False)

    def __post_init__(self):
        self.wrapper = self.wrapper_config.to_wrapper(self.name, self.wrapper_type)

    @property
    def active(self):
        return self._active

    def activate(self):
        print_and_sleep(purple(f"{self.name} added to perks."), 1)
        self._active = True

    def __repr__(self):
        return dim(' | ').join([
            cyan(f"{self.name:<24}"),
            f"Cost: {orange(self.cost):<18}",
            f"{self.description}"
        ])


_PERKS: Dict[str, Perk] = {}


def set_perk_cache(perk_cache: Dict[str, Perk]):
    global _PERKS
    _PERKS = perk_cache


def map_wrapper_config(data: dict) -> WrapperConfig:
    print(data['name'])
    wrapper_type: WrapperType = data['wrapper_type'] if 'wrapper_type' in data else WrapperType.NONE
    match wrapper_type:
        case WrapperType.NONE:
            return WrapperConfig()
        case WrapperType.BOOLEAN_OVERRIDE:
            return BooleanOverrideConfig(**data['wrapper_config'])
        case WrapperType.BOUNDED_RANDOM:
            return BoundedRandomConfig(**data['wrapper_config'])
        case _:
            return NumericChangeConfig(**data['wrapper_config'])

def load_perks(perk_filter: Callable[[Perk], bool] = lambda _: True) -> List[Perk]:
    res = []
    for d in Perks:
        data = copy.deepcopy(d)
        name = data['name']
        if name not in _PERKS:
            data['wrapper_config'] = map_wrapper_config(data)
            _PERKS[name] = Perk(**data)
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
    return load_perk(perk_name).active


def attach_perk_conditional(*perks: str, value_description: str = "",
                            silent: bool = False, condition: Callable[[], bool]):
    perk_impls = load_perks(lambda p: p.name in set(perks))

    def decorator(func):
        def wrapper(*args, **kwargs):
            value = func(*args, **kwargs)
            for perk in perk_impls:
                if perk.active and condition():
                    value = perk.wrapper(value, value_description, silent)
            return value

        return wrapper

    return decorator


def attach_perk(*perks: str, value_description: str = "", silent: bool = False):
    return attach_perk_conditional(*perks, value_description=value_description,
                                   silent=silent, condition=lambda: True)


