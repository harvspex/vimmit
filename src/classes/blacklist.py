from classes.data import _BaseData, Config
import hashlib
from pathlib import Path
from typing import override

ALL_SYSTEMS = 'All Systems'

class Blacklist(_BaseData):
    def __init__(self, config: Config):
        self.config = config
        filepath = Path.cwd() / 'blacklist.txt'
        super().__init__(filepath)
        self.save()

    def get_hash(self):
        with open(self.filepath, 'rb') as f:
            hash = hashlib.md5(f.read()).hexdigest()
            self.config.data['bl_hash'] = hash
            return hash

    @override
    def load(self) -> dict:
        blacklist = {ALL_SYSTEMS: {'id': ALL_SYSTEMS}}
        for id, sys in self.config.data['systems'].items():
            blacklist[sys['bl']] = {'id': id}
        try:
            with open(self.filepath, 'r') as f:
                bl_file = f.read()
        except FileNotFoundError:
            return blacklist

        bl_file = bl_file.split('#')
        bl_file = bl_file[1:] if bl_file[0] != '' else bl_file
        bl_file = [_.splitlines() for _ in bl_file if _]
        bl_file = [[_.strip() for _ in sys if _] for sys in bl_file]
        bl_file = {_[0]:_[1:] for _ in bl_file}
        for key in blacklist:
            try:
                blacklist[key]['list'] = bl_file[key]
            except KeyError:
                blacklist[key]['list'] = []
        return blacklist

    @override
    def save(self):
        with open(self.filepath, 'w') as f:
            for bl_id, values in self.data.items():
                f.write(f'# {bl_id}\n')
                f.writelines([f'{v}\n' for v in values['list']])
                f.write('\n')
