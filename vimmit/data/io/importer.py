from typing import Any, override

from common.console import console
from data.base_data import BaseData
from data.blacklist import Blacklist
from data.config import Config
from data.games import Games
from data.io.io_utils import DataKeys, validate_import_path

# TODO: Colour printing
# TODO: Test that it's working as intended
# TODO (maybe): It's possible to import bad base_url data if exporting user:
# - Inits with good base_url
# - Manually changes url
# - Exports data


class Importer(BaseData):
    def __init__(self, filepath: str):
        self.filepath = validate_import_path(filepath)
        self.data = self.load()

    @staticmethod
    def _both_instance_of(a: Any, b: Any, type: type):
        return isinstance(a, type) and isinstance(b, type)

    @staticmethod
    @override
    def update(old_data: dict, new_data: dict) -> dict:
        for k, v in new_data.items():
            if k not in old_data:
                old_data[k] = v
            elif Importer._both_instance_of(old_data[k], v, dict):
                Importer.update(old_data[k], v)
            elif Importer._both_instance_of(old_data[k], v, list):
                data = set(old_data[k])
                data.update(set(v))
                old_data[k] = sorted(list(data))
        return old_data

    def import_games(
        self,
        config: Config,
        games: Games,
        will_import_seen: bool=False,
        will_print: bool=True
    ):
        self.update(config.data, self.data[DataKeys.CONFIG.value])
        new_games = self.data[DataKeys.GAMES.value]
        if not will_import_seen:
            games.clear_seen(new_games, new_games.keys())
        self.update(games.data, new_games)
        games.sort_all_games()
        games.save()
        if will_print:
           console.print(
               f'Imported games {'and seen data ' if will_import_seen else ''}'
               f'from: {self.filepath}'
            )

    def import_blacklist(self, blacklist: Blacklist, will_print: bool=True):
        self.update(blacklist.data, self.data[DataKeys.BLACKLIST.value])
        blacklist.save()
        if will_print:
            console.print(f'Imported blacklist from: {self.filepath}')

    def import_all(self, config: Config, games: Games, blacklist: Blacklist):
        self.import_games(config, games, will_import_seen=True, will_print=False)
        self.import_blacklist(blacklist, will_print=False)
        console.print(f'Imported all from: {self.filepath}')