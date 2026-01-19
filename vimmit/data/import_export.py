from pathlib import Path
from typing import Any

from data.base_data import BaseData
from data.blacklist import Blacklist
from data.config import Config
from data.games import Games
from utils.exceptions import ImportExportException

# TODO: add validate_import_path
# Split ImportExport into Importer and Exporter
# Finalise

def validate_export_path(filepath: str) -> Path:
    VMT_SUFFIX = '.vmt'
    DEFAULT_FILENAME = 'data'
    path = Path(filepath).expanduser()

    if not path.parent.exists():
        raise ImportExportException('Parent directory does not exist.')

    if path.exists():
        if path.is_file() and path.suffix == VMT_SUFFIX:
            raise ImportExportException('File already exists.')
        if path.is_dir():
            path /= DEFAULT_FILENAME

    return path.with_suffix(VMT_SUFFIX)


class ImportExport(BaseData):
    # TODO: Handle Read Exceptions?

    def __init__(self, filepath: str):
        self.filepath = self._validate_filepath(filepath)

    # @staticmethod
    # def _validate_filepath(filepath: str) -> Path:
    #     VMT_SUFFIX = '.vmt'
    #     DEFAULT_FILENAME = 'vimmit'
    #     path = Path(filepath).expanduser()

    #     if not path.parent.exists():
    #         raise ImportExportException('Parent directory does not exist.')

    #     if path.exists():
    #         if path.is_file() and path.suffix == VMT_SUFFIX:
    #             raise ImportExportException('File already exists.')
    #         if path.is_dir():
    #             path /= DEFAULT_FILENAME

    #     return path.with_suffix(VMT_SUFFIX)

    @staticmethod
    def _both_instance_of(a: Any, b: Any, type: type):
        return isinstance(a, type) and isinstance(b, type)

    @staticmethod
    def _update(old_data: dict, new_data: dict) -> dict:
        for k, v in new_data.items():
            if k not in old_data:
                old_data[k] = v
            elif ImportExport._both_instance_of(old_data[k], v, dict):
                ImportExport._update(old_data[k], v)
            elif ImportExport._both_instance_of(old_data[k], v, list):
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

    def export_file(self, config: Config, games: Games, blacklist: Blacklist):
        self.data = {
            'config': config.data,
            'games': games.data,
            'blacklist': blacklist.data
        }
        self.save()