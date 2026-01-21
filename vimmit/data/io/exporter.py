from common.console import console
from data.base_data import BaseData
from data.blacklist import Blacklist
from data.config import Config
from data.games import Games
from data.io._validate_path import validate_export_path


class Exporter(BaseData):
    def __init__(self, filepath: str):
        self.filepath = validate_export_path(filepath)

    def export_file(self, config: Config, games: Games, blacklist: Blacklist):
        self.data = {
            'config': config.data,
            'games': games.data,
            'blacklist': blacklist.data
        }
        self.save()
        console.print(f'Exported file to: {self.filepath}')