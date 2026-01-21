from enum import Enum
from typing import Any

from common.console import console
from data.base_data import BaseData
from data.blacklist import Blacklist
from data.config import Config
from data.games import Games
from data.io._validate_path import validate_import_path

# TODO: colour printing


class ImportModes(Enum):
    GAMES = 'games'
    SEEN = 'seen'
    BLACKLIST = 'blacklist'
    ALL = 'all'


class Importer(BaseData):
    def __init__(self, filepath: str):
        self.filepath = validate_import_path(filepath)

    @staticmethod
    def _both_instance_of(a: Any, b: Any, type: type):
        return isinstance(a, type) and isinstance(b, type)

    @staticmethod
    def _update(old_data: dict, new_data: dict) -> dict:
        for k, v in new_data.items():
            if k not in old_data:
                old_data[k] = v
            elif Importer._both_instance_of(old_data[k], v, dict):
                Importer._update(old_data[k], v)
            elif Importer._both_instance_of(old_data[k], v, list):
                data = set(old_data[k])
                data.update(set(v))
                old_data[k] = sorted(list(data))
        return old_data

    def import_file(
        self,
        old_config: Config,
        old_games: Games,
        old_blacklist: Blacklist
    ):
        old_data = {
            'config': old_config, 
            'games': old_games, 
            'blacklist': old_blacklist,
        }
        new_data = self.load()
        for key, obj in old_data.items():
            self._update(obj.data, new_data[key])
            obj.save()
        # TODO (maybe): sort system lists?
        old_games.sort_all_games()
        old_games.save()
        console.print(f'Imported file: {self.filepath}')