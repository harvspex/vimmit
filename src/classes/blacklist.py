from classes.data import _BaseData, Config, Games
import hashlib
from pathlib import Path
from typing import override

class Blacklist(_BaseData):
    ALL_SYSTEMS = 'All Systems'

    def __init__(self, config: Config):
        self.config = config
        filepath = Path.cwd() / 'blacklist.txt'
        super().__init__(filepath)
        self.save()

    def apply(self, games: Games, will_check_hash: bool=True):
        bl_hash = self.get_hash()

        if will_check_hash and bl_hash == self.config.data['bl_hash']:
            return

        for system in games.data:
            bl_id = self.config.data['systems'][system]['id']
            for game in system:
                for phrase in self.data[self.ALL_SYSTEMS]:
                    if phrase in game['name']:
                        game['bl'] = True
                for phrase in self.data['bl_id']:
                    if phrase in game['name']:
                        game['bl'] = True
            # TODO This sucks

    def get_hash(self):
        with open(self.filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()

    @override
    def load(self) -> dict:
        # Init
        blacklist = {self.ALL_SYSTEMS: {'id': self.ALL_SYSTEMS}}
        for id, sys in self.config.data['systems'].items():
            blacklist[sys['bl']] = {'id': id}

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

        # Combine
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
