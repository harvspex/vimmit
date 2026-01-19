from typing import override

from data.base_data import BaseData, CWD
from data.config import Config


# TODO (maybe): reimplement blacklist hash, with re-check only on changed hash

class Blacklist(BaseData):
    ALL_SYSTEMS = 'All Systems'

    def __init__(self, config: Config):
        self.systems = config.data.get('systems', {}) # TODO: test
        super().__init__(CWD, 'blacklist.txt')
        self.save()

    @override
    def load(self) -> dict:
        # Init
        blacklist = {self.ALL_SYSTEMS: []}
        for val in self.systems.values():
            blacklist[val['bl_id']] = []

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
                blacklist[key] = sorted({_.lower() for _ in bl_file[key]})
            except KeyError:
                continue

        return blacklist

    @override
    def save(self):
        with open(self.filepath, 'w') as f:
            for bl_id, values in self.data.items():
                f.write(f'# {bl_id}\n')
                f.writelines([f'{v}\n' for v in values])
                f.write('\n')