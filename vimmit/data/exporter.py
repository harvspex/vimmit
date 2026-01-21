from pathlib import Path

from exceptions import ImportExportException
from data.base_data import BaseData
from data.blacklist import Blacklist
from data.config import Config
from data.games import Games

# TODO: Test all

VMT_SUFFIX = '.vmt'
DEFAULT_FILENAME = 'data'


def validate_export_path(filepath: str | None) -> Path:
    if filepath is None:
        filepath = Path.cwd() / DEFAULT_FILENAME

    path = Path(filepath).expanduser()

    if not path.parent.exists():
        raise NotADirectoryError('Parent directory does not exist.')

    if path.exists():
        if path.is_file() and path.suffix == VMT_SUFFIX:
            raise FileExistsError
        if path.is_dir():
            path /= DEFAULT_FILENAME

    return path.with_suffix(VMT_SUFFIX)


class Exporter(BaseData):
    def __init__(self, filepath: str):
        try:
            self.filepath = validate_export_path(filepath)
        except:
            raise ImportExportException

    def export_file(self, config: Config, games: Games, blacklist: Blacklist):
        self.data = {
            'config': config.data,
            'games': games.data,
            'blacklist': blacklist.data
        }
        self.save()