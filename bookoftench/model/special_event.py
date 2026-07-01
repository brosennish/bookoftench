from collections.abc import Callable
from dataclasses import dataclass, field

from bookoftench.data.special_events import Special_Events

# ================================================================================================

@dataclass
class SpecialEvent:
    name: str
    color: Callable[[str], str]
    sleep: int
    theme: str
    type: str
    areas: list[str]
    time: list[str]
    moon: list[str] | None
    season: list[str] | None
    text: str
    choices: list[str]
    optional: bool
    method: str | None
    replayable: bool
    related: list[str] = field(default_factory=list)
    stage: int | None = 1
    investment: str | None = None

# ================================================================================================

def load_special_event(name: str) -> SpecialEvent:
    matches = load_special_events([name])
    if not matches:
        raise ValueError(f"Could not find special event data for {name}")
    return matches[0]


def load_special_events(restriction: list[str] | None = None) -> list[SpecialEvent]:
    return [
        SpecialEvent(**event_data)
        for event_data in Special_Events
        if restriction is None or event_data["name"] in restriction
    ]