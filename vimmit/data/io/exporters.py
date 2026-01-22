from common.console import console
from data.base_data import BaseData
from data.blacklist import Blacklist
from data.config import Config
from data.games import Games
from data.io.io_utils import DataKeys, validate_export_path, format_filepath_message


class DataExporter(BaseData):
    def __init__(self, filepath: str):
        self.filepath = validate_export_path(filepath)

    def export_data(self, config: Config, games: Games, blacklist: Blacklist):
        self.data = {
            DataKeys.CONFIG.value: config.data,
            DataKeys.GAMES.value: games.data,
            DataKeys.BLACKLIST.value: blacklist.data
        }
        self.save()
        console.print(
            format_filepath_message('Exported file to', 'green', self.filepath)
        )


class HistoryExporter:
    def __init__(self, filepath: str):
        self.filepath = validate_export_path(filepath, 'history', '.txt')

    # TODO: refactor, and remove extra newline at end of file
    def export_history(self, config: Config, games: Games):
        extract_names = lambda data: [f'{game['name']}\n' for game in data.values() if game.get('seen', False)]
        history = {system: extract_names(games) for system, games in games.data.items()}
        history = {k: v for k, v in history.items() if v}
        with open(self.filepath, 'w') as f:
            for sys_id, games in history.items():
                bl_id = config.data['systems'][sys_id]['bl_id']
                f.write(f'# {bl_id}\n')
                f.writelines(games)
                f.write('\n')
        console.print(
            format_filepath_message('Exported history to', 'green', self.filepath)
        )