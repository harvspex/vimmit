from utils.setup import handle_setup
from abc import ABC
from pathlib import Path
from typing import override
import pickle

class _BaseData(ABC):
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.data = self.load()

    def save(self):
        with open(self.filepath, 'wb') as f:
            pickle.dump(self.data, f)

    def load(self) -> dict:
        with open(self.filepath, 'rb') as f:
            return pickle.load(f)


class Games(_BaseData):
    def __init__(self):
        filepath = Path.cwd() / '.data' / 'games.dat'
        super().__init__(filepath)

    @override
    def load(self):
        try:
            return super().load()
        except FileNotFoundError:
            return {}


class Config(_BaseData):
    def __init__(self):
        filepath = Path.cwd() / '.data' / 'config.dat'
        super().__init__(filepath)
        self.save()

    @override
    def load(self):
        try:
            return handle_setup(super().load())
        except FileNotFoundError:
            return handle_setup({})
