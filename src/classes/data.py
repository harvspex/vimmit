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


class Blacklist(_BaseData):
    ALL_SYSTEMS = 'All Systems'

    def __init__(self, config: Config):
        self.systems = config.data['systems']
        filepath = Path.cwd() / 'blacklist.txt'
        super().__init__(filepath)
        self.save()

    @override
    def load(self) -> dict:
        # Init
        blacklist = {self.ALL_SYSTEMS: []}
        for val in self.systems.values():
            blacklist[val['bl']] = []

        # Read
        try:
            with open(self.filepath, 'r') as f:
                bl_file = f.read()
        except FileNotFoundError:
            return blacklist

        # Parse
        bl_file = bl_file.split('#')
        bl_file = bl_file[1:] if bl_file[0] != '' else bl_file
        bl_file = [_.splitlines() for _ in bl_file if _]
        bl_file = [[_.strip() for _ in sys if _] for sys in bl_file]
        bl_file = {_[0]:_[1:] for _ in bl_file}

        # Validate
        for key in blacklist.keys():
            try:
                blacklist[key] = bl_file[key]
            except KeyError:
                continue

        return blacklist

    @override
    def save(self):
        with open(self.filepath, 'w') as f:
            for bl_id, values in self.data.items():
                f.write(f'# {bl_id}\n')
                f.writelines([f'{v}\n' for v in values['list']])
                f.write('\n')
