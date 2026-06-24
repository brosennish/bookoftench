import random
from dataclasses import dataclass

from bookoftench.audio import play_sound
from bookoftench.data.audio import MAGIC
from bookoftench.data.spells import ITEM_MAGIC, Spells, WEAPON_MAGIC
from bookoftench.data.weapons import BLIND, SPECIAL
from bookoftench.model.base import Buyable
from bookoftench.model.item import load_items
from bookoftench.model.player import Player
from bookoftench.model.weapon import load_weapons, make_elite_weapon
from bookoftench.ui import cyan, dim, orange, purple
from bookoftench.util import print_and_sleep

# ================================================================================================

@dataclass
class Spell(Buyable):
    name: str
    description: str
    cost: int
    type: str

    def __repr__(self) -> str:
        return dim(" | ").join([
            cyan(f"{self.name:<12}"),
            f"Cost: {orange(self.cost)}",
            purple(self.description),
        ])

    def cast(self, player: Player) -> None:
        if self.name == ITEM_MAGIC:
            filtered = [
                item for item in load_items()
                if item.name not in player.items
            ]
            item = random.choice(filtered)
            player.add_item(item)
            play_sound(MAGIC)
            print_and_sleep(cyan(f"{item.name} magically added to sack."), 2)

        elif self.name == WEAPON_MAGIC:
            player_weapon_names = [
                weapon.name for weapon in player.get_weapons()
            ]
            filtered = [
                weapon for weapon in load_weapons()
                if weapon.name not in player_weapon_names
                and weapon.tier > 1
                and weapon.uses > 0
            ]
            weapon = random.choice(filtered)

            low = min(5, weapon.uses)
            high = min(8, weapon.uses)
            weapon.uses = random.randint(low, high)

            if weapon.type not in [BLIND, SPECIAL] and random.random() < 0.15:
                weapon = make_elite_weapon(weapon)

            player.add_weapon(weapon)
            play_sound(MAGIC)
            print_and_sleep(cyan(f"{weapon.name} magically added to sack."), 2)

# ================================================================================================

def load_spells() -> list[Spell]:
    return [
        Spell(**spell_dict)
        for spell_dict in Spells
    ]
