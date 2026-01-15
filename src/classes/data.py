from utils.setup import handle_setup
from abc import ABC
from pathlib import Path
from typing import Any, override
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
        self.config = config
        filepath = Path.cwd() / 'blacklist.txt'
        super().__init__(filepath)
        self.validate()
        self.save()

    @override
    def load(self):
        try:
            with open(self.filepath, 'r') as f:
                blacklist = f.read()

            blacklist = blacklist.split('#')
            blacklist = blacklist[1:] if blacklist[0] != '' else blacklist
            blacklist = [_.splitlines() for _ in blacklist if _]
            blacklist = [[_.strip() for _ in sys if _] for sys in blacklist]
            blacklist = {_[0]:_[1:] for _ in blacklist}
            return blacklist

        except FileNotFoundError:
            # TODO
            return ...

    @override
    def save(self):
        # TODO: WIP
        with open(self.filepath, 'w') as f:
            for system, values in self.data.items():
                f.write(f'# {system}\n')
                f.writelines(values)
                f.write('\n\n')

    def validate(self):
        if self.ALL_SYSTEMS not in self.data:
            self.data[self.ALL_SYSTEMS] = []

        # TODO: Validate backwards (remove bad systems)

        for system in self.config.data['systems'].values():
            system_name = f'{system['name']} ({system['id']})'
            if system_name not in self.data.keys():
                self.data[system_name] = []

    def get_hash(self):
        import hashlib
        with open(self.filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
