from pathlib import Path

from data.base_data import BaseData


class Config(BaseData):
    def __init__(self):
        filepath = Path.cwd() / '.data' / 'config.dat'
        super().__init__(filepath)
        self.save()