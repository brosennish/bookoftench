from dataclasses import dataclass

from bookoftench.data.enemies import Traits

# ================================================================================================

@dataclass
class Trait:
    name: str
    desc: str

# ================================================================================================

def load_traits(restriction: list[str] | None = None) -> list[Trait]:
    return [
        Trait(**trait_data)
        for trait_data in Traits
        if restriction is None or trait_data["name"] in restriction
    ]


def load_trait(entry: dict | None) -> Trait | None:
    if entry:
        return Trait(**entry)
    return None