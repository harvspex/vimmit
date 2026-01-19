from pathlib import Path

from data.base_data import BaseData
from data.blacklist import Blacklist
from data.config import Config
from data.games import Games


class ImportExport(BaseData):
    # TODO: Handle Read Exceptions?
    # TODO (maybe): Import blacklist?

    def __init__(self, filepath: Path):
        self.filepath = self._validate_filepath(filepath)

    @staticmethod
    def _validate_filepath(filepath: str=None):
        if filepath is None:
            return Path.cwd() / 'vimmit.vmt'
        # TODO: Complete
        ...
        return filepath

    @staticmethod
    def _update(old_data: dict, new_data: dict) -> dict:
        # NOTE: Updates without overwriting
        for k, v in new_data.items():
            if k not in old_data:
                old_data[k] = v
            elif isinstance(old_data[k], dict) and isinstance(v, dict):
                ImportExport._update(old_data[k], v)
        return old_data

    def import_file(
        self,
        old_config: Config,
        old_games: Games,
        old_blacklist: Blacklist
    ):
        # TODO: Updated gamelist may lose alphabetic ordering
        # Sort gamelists and systems list?
        old_data = {
            'config': old_config, 
            'games': old_games, 
            'blacklist': old_blacklist,
        }
        new_data = self.load()
        for key, obj in old_data.items():
            self._update(obj.data, new_data[key])
            obj.save()

    def export_file(self, config: Config, games: Games, blacklist: Blacklist):
        self.data = {
            'config': config.data,
            'games': games.data,
            'blacklist': blacklist.data
        }
        # TODO: Problem importing blacklist
        # Seems to work normally if there is already a blacklist file
        # However if there is no blacklist file, does not load All Systems data
        # Could indicate problem with loading config or games too
        self.save()
        with open(Path.cwd() / 'test.json', 'w') as f:
            import json
            json.dump(self.data, f, indent=2)