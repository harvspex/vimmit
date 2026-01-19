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
        # NOTE: Overwrites old data if old_data[k] is falsy
        for k, v in new_data.items():
            if k not in old_data:
                old_data[k] = v
            elif isinstance(old_data[k], dict) and isinstance(v, dict):
                ImportExport._update(old_data[k], v)
            elif isinstance(old_data[k], list) and isinstance(v, list):
                # TODO: this can degrade order and produce dupes
                old_data[k] = old_data[k] + v
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
            # TODO: Need to perform validation on data before saving
            # e.g. remove blacklist duplicates, sort
            # sort gamelists
            # sort system lists
            obj.save()

    def export_file(self, config: Config, games: Games, blacklist: Blacklist):
        self.data = {
            'config': config.data,
            'games': games.data,
            'blacklist': blacklist.data
        }
        self.save()