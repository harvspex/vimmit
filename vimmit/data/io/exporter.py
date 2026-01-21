from enum import Enum

from common.console import console
from data.base_data import BaseData
from data.blacklist import Blacklist
from data.config import Config
from data.games import Games
from data.io._validate_path import validate_export_path


class ExportModes(Enum):
    DATA = 'data'
    HISTORY = 'history'


# TODO: colour printing
# TODO: alternate validate_export_filepath for export_history mode
class Exporter(BaseData):
    def __init__(self, filepath: str):
        self.filepath = validate_export_path(filepath)

    def export_data(self, config: Config, games: Games, blacklist: Blacklist):
        self.data = {
            'config': config.data,
            'games': games.data,
            'blacklist': blacklist.data
        }
        self.save()
        console.print(f'Exported file to: {self.filepath}')

    def export_history(self, config: Config, games: Games):
        extract_names = lambda data: [f'{game['name']}\n' for game in data.values() if game.get('seen', False)]
        history = {system: extract_names(games) for system, games in games.data.items()}
        with open(self.filepath, 'w') as f:
            for sys_id, games in history.items():
                bl_id = config.data['systems'][sys_id]['bl_id']
                f.write(f'# {bl_id}\n')
                f.writelines(games)
                f.write('\n')