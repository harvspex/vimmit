from abc import ABC
from pathlib import Path
from typing import Callable

import pickle


CWD = Path.cwd()
DATA_DIR = CWD / '.data'


class BaseData(ABC):
    def __init__(self, path: Path, filename: str):
        if not path.exists():
            path.mkdir(parents=True)
        self.filepath = path / filename
        self.data = self.load()

    def save(self):
        with open(self.filepath, 'wb') as f:
            pickle.dump(self.data, f)

    def load(self) -> dict:
        try:
            with open(self.filepath, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {}

    def update(self, key: str, overwrite: bool, func: Callable, *args, **kwargs) -> bool:
        if not self.data.get(key, False) or overwrite:
            self.data[key] = func(*args, **kwargs)
            return True
        return False

    def clear(self, keys: list, clear_all: bool=False):
        if clear_all:
            self.data.clear()
            return
        for key in keys:
            del self.data[key]