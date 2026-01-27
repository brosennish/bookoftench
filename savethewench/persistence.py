from __future__ import annotations

import json
import pickle
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from savethewench.model import GameState
from savethewench.ui import cyan, red
from savethewench.util import print_and_sleep

_SAVE_DIR = ".saves"  # TODO don't just save straight to a directory in the repo
_SAVE_SLOTS = 5
_delimiter = '__'
_metadata_filename = "meta.json"
_save_filename = "game_state.tench"


class MetadataDeserializationError(Exception):
    def __init__(self, *args, **kwargs):  # real signature unknown
        pass


@dataclass
class Metadata:
    player_name: str
    player_level: int
    player_area: str
    player_lives: int
    save_time: float

    @classmethod
    def load(cls, file: Path) -> Optional[Metadata]:
        if not file.exists():
            return None
        try:
            with open(file, "r") as f:
                return Metadata(**json.load(f))
        except TypeError:
            raise MetadataDeserializationError()

    def save(self, file: Path) -> None:
        with open(file, "w") as f:
            json.dump(asdict(self), f)

    def format(self) -> str:
        return (f"{self.player_name} | "
                f"Level {self.player_level} | "
                f"Area: {self.player_area} | "
                f"Lives: {self.player_lives} | "
                f"Last Save: {datetime.fromtimestamp(self.save_time).strftime("%Y-%m-%d %H:%M:%S")}")


def slot_directory(slot_id: int) -> Path:
    return Path(f"{_SAVE_DIR}/slot_{slot_id}")


@dataclass
class SaveSlot:
    slot_id: int
    metadata: Optional[Metadata] = None

    def __post_init__(self):
        self._slot_directory.mkdir(parents=True, exist_ok=True)
        try:
            self.metadata = Metadata.load(self._metadata_path)
        except MetadataDeserializationError:
            print_and_sleep(red(f"Failed to deserialize metadata for slot {self.slot_id}."))

    @property
    def is_empty(self) -> bool:
        return self.metadata is None

    @property
    def _slot_directory(self) -> Path:
        return Path(f"{_SAVE_DIR}/slot_{self.slot_id}")

    @property
    def _metadata_path(self) -> Path:
        return self._slot_directory.joinpath(_metadata_filename)

    @property
    def _game_state_path(self) -> Path:
        return self._slot_directory.joinpath(_save_filename)

    def get_displayable_format(self) -> str:
        return self.metadata.format() if self.metadata is not None else "<empty>"

    def save_game(self, game_state: GameState):
        self.metadata = Metadata(player_name=game_state.player.name,
                                 player_level=game_state.player.lvl,
                                 player_area=game_state.current_area.name,
                                 player_lives=game_state.player.lives,
                                 save_time=time.time())
        self.metadata.save(self._metadata_path)
        with open(self._game_state_path, "wb") as f:  # noinspection PyTypeChecker
            pickle.dump(game_state, f)
        print_and_sleep(cyan("Game saved."), 1)

    def load_game(self) -> GameState:
        if self.is_empty:
            raise ValueError(f"No saved game exists in slot {self.slot_id}")

        with open(self._game_state_path, "rb") as f:
            return pickle.load(f)


def load_save_slots() -> List[SaveSlot]:
    return [SaveSlot(i) for i in range(1, _SAVE_SLOTS + 1)]
