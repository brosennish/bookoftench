from dataclasses import dataclass
from typing import Callable, List

from bookoftench.data.special_events import Special_Events


# ================================================================================================

@dataclass
class SpecialEvent:
    name: str
    color: Callable[[str], str]
    theme: str
    areas: list[str]
    time: str | None
    moon: str | None
    season: str | None
    text: str
    choices: list[str]
    method: str

# ================================================================================================

def load_special_event(name: str) -> SpecialEvent:
    matches = load_special_events([name])
    if len(matches) == 0:
        raise ValueError(f"Could not find special event data for {name}")
    return matches[0]

def load_special_events(restriction: List[str] = None) -> List[SpecialEvent]:
    return [SpecialEvent(**d) for d in Special_Events if restriction is None or d['name'] in restriction]