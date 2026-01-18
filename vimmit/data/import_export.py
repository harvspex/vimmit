from pathlib import Path

from data.base_data import _BaseData
from data.config import Config
from data.games import Games


class ImportExport(_BaseData):
    # TODO: Handle Read Exceptions?
    # TODO (maybe): Import blacklist?

    def __init__(self, filepath):
        self.filepath = self._validate_filepath(filepath)

    @staticmethod
    def _validate_filepath(filepath: str=None):
        if filepath is None:
            return Path.cwd() / 'vimmit.vmt'
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