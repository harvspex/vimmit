from src.classes.data import _BaseData, Config
import hashlib
from pathlib import Path
from typing import override

ALL_SYSTEMS = 'All Systems'

class Blacklist(_BaseData):
    def __init__(self, config: Config):
        self.systems = config.data['systems']
        filepath = Path.cwd() / 'blacklist.txt'
        super().__init__(filepath)
        self.save()

    def get_hash(self):
        with open(self.filepath, 'rb') as f:
            hash = hashlib.md5(f.read()).hexdigest()
            self.config.data['bl_hash'] = hash
            return hash

    @staticmethod
    def _init_blacklist(systems: dict) -> dict:
        blacklist_keys = {ALL_SYSTEMS: ALL_SYSTEMS}
        for id, sys in systems:
            blacklist_keys[sys['bl']] = {'id': id}
        return blacklist_keys

    def _read_blacklist(self):
        try:
            with open(self.filepath, 'r') as f:
                blacklist = f.read()
            blacklist = blacklist.split('#')
            blacklist = blacklist[1:] if blacklist[0] != '' else blacklist
            blacklist = [_.splitlines() for _ in blacklist if _]
            blacklist = [[_.strip() for _ in sys if _] for sys in blacklist]
            blacklist = {_[0]:_[1:] for _ in blacklist}
            blacklist = self._validate(blacklist)
            return blacklist

        except FileNotFoundError:
            # TODO
            return ...

    def _validate_blacklist(self, blacklist: dict):
        blacklist_ids = self.data.keys()
        for sys_id in blacklist_ids:
            if sys_id not in self.data.keys():
                self.data[sys_id] = []

        difference = set(self.data.keys()).difference(blacklist_ids)
        for key in difference:
            del self.data[key]

    @override
    def load(self) -> dict:
        # TODO
        blacklist = self._init_blacklist()
        blacklist = self._read_blacklist()
        blacklist = self._validate_blacklist()
        return blacklist

    @override
    def save(self):
        with open(self.filepath, 'w') as f:
            for system, values in self.data.items():
                f.write(f'# {system}\n')
                f.writelines([f'{v}\n' for v in values])
                f.write('\n')
