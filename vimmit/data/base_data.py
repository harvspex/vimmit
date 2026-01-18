from abc import ABC
from pathlib import Path

import pickle
    

class _BaseData(ABC):
    def __init__(self, filepath: Path):
        self.filepath = filepath
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