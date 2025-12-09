from api import LabeledSelectionComponent, SelectionBinding, NoOpComponent
from model.game_state import GameState


class Casino(LabeledSelectionComponent):
    def __init__(self, game_state: GameState):
        super().__init__(game_state, bindings=[
            SelectionBinding('1', "Krill or Cray", KrillOrKray),
            SelectionBinding('2', "Above or Below", AboveOrBelow),
            SelectionBinding('3', "Wet or Dry (WIP)", WetOrDry),
            SelectionBinding('4', "Fish Bones (WIP)", FishBones),
            SelectionBinding('5', "Mystery Box (WIP)", MysteryBox),
            SelectionBinding('r', "Return", NoOpComponent)
        ])


class KrillOrKray(NoOpComponent): pass


class AboveOrBelow(NoOpComponent): pass


class WetOrDry(NoOpComponent): pass


class FishBones(NoOpComponent): pass


class MysteryBox(NoOpComponent): pass
