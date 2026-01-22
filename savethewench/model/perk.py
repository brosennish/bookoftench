import copy
import random
from dataclasses import dataclass, field
from functools import partial, wraps
from typing import List, Callable, Dict, ParamSpec
from typing import TypeVar

from savethewench.data import Perks
from savethewench.data.perks import WrapperType
from savethewench.model.base import Buyable
from savethewench.ui import purple, dim, cyan, orange
from savethewench.util import print_and_sleep

T = TypeVar('T')
P = ParamSpec("P")


@dataclass
class WrapperConfig[T]:
    def to_wrapper(self, name: str, wrapper_type: WrapperType) -> Callable[[T, str, bool], T]:
        return lambda original, value_description, silent: original


@dataclass
class BooleanOverrideConfig(WrapperConfig):
    override: bool

    def to_wrapper(self, name: str, _: WrapperType) -> Callable[[bool, str, bool], bool]:
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


_int_change: Callable[[int, int], int] = lambda orig, i: orig + i
_percent_change: Callable[[float, int], float] = lambda orig, pct: orig + (float(pct) / 100.0)
_int_change_by_percent: Callable[[int, int], int] = lambda orig, pct: int(orig * (1 + (float(pct) / 100.0)))
_float_change_by_percent: Callable[[float, int], float] = lambda orig, pct: orig * (1 + (float(pct) / 100.0))


@dataclass
class NumericChangeConfig(WrapperConfig):
    change: int

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
                return partial(self._numeric_change, name=name, change_func=_int_change, is_percent=False)
            case WrapperType.PERCENT_CHANGE:
                return partial(self._numeric_change, name=name, change_func=_percent_change, is_percent=True)
            case WrapperType.INT_CHANGE_BY_PERCENT:
                return partial(self._numeric_change, name=name, change_func=_int_change_by_percent, is_percent=True)
            case WrapperType.FLOAT_CHANGE_BY_PERCENT:
                return partial(self._numeric_change, name=name, change_func=_float_change_by_percent, is_percent=True)
            case _:
                raise NotImplementedError(f"{wrapper_type} not implemented")


@dataclass
class FunctionWrapper:
    wrapper_type: WrapperType = WrapperType.NONE
    wrapper_config: WrapperConfig = field(default_factory=WrapperConfig)


@dataclass
class Perk[T](Buyable):
    name: str
    cost: int
    description: str
    _active: bool = False  # value should not be changed from outside of class methods
    wrappers: List[FunctionWrapper] = field(default_factory=list)

    @property
    def active(self) -> bool:
        return self._active

    def activate(self) -> None:
        print_and_sleep(purple(f"{self.name} added to perks."), 1)
        self._active = True

    def get_wrapper(self, index: int) -> Callable[[T, str, bool], T]:
        if index >= len(self.wrappers):
            raise IndexError(f"{self.name} has no wrapper with index {index}.")
        wrapper = self.wrappers[index]
        return wrapper.wrapper_config.to_wrapper(self.name, wrapper.wrapper_type)

    def __repr__(self) -> str:
        return dim(' | ').join([
            cyan(f"{self.name:<24}"),
            f"Cost: {orange(self.cost):<18}",
            f"{self.description}"
        ])


_PERKS: Dict[str, Perk] = {}


def set_perk_cache(perk_cache: Dict[str, Perk]) -> None:
    global _PERKS
    _PERKS = perk_cache


def map_wrapper_config(data: dict) -> WrapperConfig:
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
            if 'wrapper_type' in data and 'wrapper_config' in data:
                data['wrappers'] = [{'wrapper_type': data['wrapper_type'], 'wrapper_config': data['wrapper_config']}]
                del data['wrapper_type']
                del data['wrapper_config']
            if 'wrappers' in data:
                wrappers = []
                for wrapper_data in data['wrappers']:
                    wrapper_data['wrapper_config'] = map_wrapper_config(wrapper_data)
                    wrappers.append(FunctionWrapper(**wrapper_data))
                data['wrappers'] = wrappers
            _PERKS[name] = Perk(**data)
        perk = _PERKS[name]
        if perk_filter(perk):
            res.append(_PERKS[name])
    return res


def load_perk(perk_name: str) -> Perk:
    if perk_name in _PERKS:
        return _PERKS[perk_name]
    return load_perks(lambda p: p.name == perk_name)[0]


def activate_perk(perk_name: str) -> None:
    load_perk(perk_name).activate()


def perk_is_active(perk_name: str) -> bool:
    return load_perk(perk_name).active


def attach_perk(perk: str, wrapper_idx: int = 0, value_description: str = "", silent: bool = False,
                condition: Callable[[], bool] = lambda: True) -> Callable[[Callable[[P], T]], Callable[[P], T]]:
    perk_impl = load_perk(perk)

    def decorator(func: Callable[[P], T]) -> Callable[[P], T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            value: T = func(*args, **kwargs)
            if perk_is_active(perk_impl.name) and condition():
                value = perk_impl.get_wrapper(wrapper_idx)(value, value_description, silent)
            return value

        return wrapper

    return decorator


def attach_perks(*perks: str, value_description: str = "", silent: bool = False,
                 condition: Callable[[], bool] = lambda: True) -> Callable[[Callable[[P], T]], Callable[[P], T]]:
    if len(perks) == 0:
        raise ValueError('No perk names provided to attach.')

    # decompose "attach_perks" into "attach_perk" invocations
    def decorator(func: Callable[[P], T]) -> Callable[[P], T]:
        for perk in perks:
            func = attach_perk(perk, value_description=value_description, silent=silent, condition=condition)(func)
        return func

    return decorator
