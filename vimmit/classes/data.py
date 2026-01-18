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
        try:
            with open(self.filepath, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {}


class Games(_BaseData):
    # TODO: Fix duplicate object key bug (some games with str keys of same int value)
    # May not need fixing - bad data is holdover from older version of vimmit

    def __init__(self):
        filepath = Path.cwd() / '.data' / 'games.dat'
        super().__init__(filepath)

    def dump_json(self, filepath: Path | None=None):
        # TODO: Fix
        import json
        filename = 'games.json'
        # filepath = filepath / filename if filepath else Path.cwd() / filename
        filepath = Path.cwd() / filename

        with open(filepath, 'w') as f:
            json.dump(self.data, f, indent=2)

    def dump_history(self, config: Config, filepath: Path):
        extract_names = lambda data: [f'{game['name']}\n' for game in data.values() if game.get('seen', False)]
        history = {system: extract_names(games) for system, games in self.data.items()}
        with open(filepath, 'w') as f:
            for sys_id, games in history.items():
                bl_id = config.data['systems'][sys_id]['bl_id']
                f.write(f'# {bl_id}\n')
                f.writelines(games)
                f.write('\n')


class Config(_BaseData):
    def __init__(self):
        filepath = Path.cwd() / '.data' / 'config.dat'
        super().__init__(filepath)
        self.save()


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


class ImportExport(_BaseData):
    # TODO: Read Exceptions?
    # TODO: Import blacklist?

    def __init__(self, filepath):
        self.filepath = self._validate_filepath(filepath)

    @staticmethod
    def _validate_filepath(filepath: str):
        # TODO
        ...
        return filepath

    @staticmethod
    def _update(old_data: dict, new_data: dict) -> dict:
        # NOTE: Updated gamelist may lose alphabetic ordering
        for k, v in new_data.items():
            if k not in old_data:
                old_data[k] = v
            elif isinstance(old_data[k], dict) and isinstance(v, dict):
                ImportExport._update(old_data[k], v)
        return old_data

    def import_file(self, old_config: Config, old_games: Games) -> tuple[Config, Games]:
        # Updates without overwriting
        data = self.load()
        return self._update(old_config, data['config']), self._update(old_games, data['games'])

    def export_file(self, config: Config, games: Games):
        self.data = {
            'config': config,
            'games': games
        }
        self.save()
