from __future__ import annotations

import os
import pickle
import time
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional

from savethewench.model import GameState
from savethewench.ui import cyan
from savethewench.util import print_and_sleep

_SAVE_DIR = ".saves"  # TODO don't just save straight to a directory in the repo
_SAVE_SLOTS = 5
_delimiter = '__'


@dataclass
class SaveSlot:
    slot_id: int
    player_name: Optional[str] = None
    player_level: Optional[int] = None
    player_area: Optional[str] = None
    save_time: Optional[float] = None

    @classmethod
    def from_filename(cls, filename: str) -> SaveSlot:
        parts = filename.split(_delimiter)
        if len(parts) != 5:
            raise ValueError(f"Invalid save filename: {filename}")
        return SaveSlot(int(parts[0]), parts[1], int(parts[2]), parts[3], float(parts[4]))

    @property
    def is_empty(self) -> bool:
        return not any([self.player_name, self.player_level, self.player_area, self.save_time])

    def format_filename(self) -> str:
        return _delimiter.join(str(val) for val in
                               [self.slot_id, self.player_name, self.player_level, self.player_area, self.save_time])

    def get_displayable_format(self) -> str:
        if self.is_empty:
            return "<empty>"
        return (f"{self.player_name} | "
                f"Level {self.player_level} | "
                f"Area: {self.player_area} | "
                f"Last Save: {datetime.fromtimestamp(self.save_time).strftime("%Y-%m-%d %H:%M:%S")}")

    def save_game(self, game_state: GameState):
        self.player_name = game_state.player.name
        self.player_level = game_state.player.lvl
        self.player_area = game_state.current_area.name
        self.save_time = time.time()
        with open(f"{_SAVE_DIR}/{self.format_filename()}", "wb") as f:  # noinspection PyTypeChecker
            pickle.dump(game_state, f)
        print_and_sleep(cyan("Game saved."), 1)

    def load_game(self) -> GameState:
        if self.is_empty:
            raise ValueError(f"No saved game exists in slot {self.slot_id}")
        with open(f"{_SAVE_DIR}/{self.format_filename()}", "rb") as f:
            return pickle.load(f)


def load_save_slots() -> List[SaveSlot]:
    if not os.path.isdir(_SAVE_DIR):
        os.mkdir(_SAVE_DIR)
    existing_saves: Dict[int, str] = dict((int(fn.split(_delimiter)[0]), fn) for fn in  os.listdir(_SAVE_DIR))
    result: List[SaveSlot] = []
    for i in range(1, _SAVE_SLOTS+1):
        if i in existing_saves:
            result.append(SaveSlot.from_filename(existing_saves[i]))
        else:
            result.append(SaveSlot(i))
    return result
