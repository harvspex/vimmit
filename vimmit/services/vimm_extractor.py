from enum import Enum
from pathlib import Path
import shutil

from app._setup import get_input
from common.console import console
from data.config import Config
from data.games import Games

# TODO:
# - (Done, needs testing) Setup downloads folder and destination folder if needed
# - (Done) Match string similarity of seen games to games in downloads folder
#   - If extension == .zip or .7z : Extract games to dir "System/Archive Name (no suffix)/"
#   - Else: just move the file to dir "System/"
# - (Done) Flag games as moved
# - Delete archive if will_delete == True
#
# (Done) Change importer to only import game IDs, names, and (optionally) seen data
# (Don't need) Also, don't import download_path or roms_path from config
#
# TODO: Colour printing


class ArchiveSuffix(Enum):
    ZIP = '.zip'
    SEVEN_ZIP = '.7z'


class ExtractModes(Enum):
    NORMAL = 'normal'
    AUTO = 'auto'
    DELETE = 'delete'


class VimmExtractor:
    def __init__(self, config: Config, extract_modes: list):
        self.download_path = self._validate_path(config, 'downloads')
        self.roms_path = self._validate_path(config, 'roms')
        # TODO: Handle extract_modes

    @staticmethod
    def _validate_path(config: Config, key: str):
        try:
            path = Path(config.data['paths'][key])
        except KeyError:
            path = VimmExtractor._setup_path(config, key)
        if not path.is_dir():
            path = VimmExtractor._setup_path(config, key)
        return path

    @staticmethod
    def _setup_path(config: Config, key: str):
        path = get_input(
            f'Please input path to {key} folder:',
            'Please enter a valid folder path:',
            lambda path: path if Path(path).is_dir() else None
        )
        config.data['paths'][key] = path
        config.save()
        return Path(path)

    @staticmethod
    def _yield_sys_and_game(games: Games):
        for sys_id, games in games.items():
            for game_id, game in games.items():
                if game.get('seen') and not game.get('moved'):
                    yield sys_id, game_id

    def _get_filepath(self, game_name: str) -> Path | None:
        for file in self.download_path.iterdir():
            if game_name in file.name:
                return file
        return None

    def run(self, games: Games):
        for sys_id, game_id in self._yield_sys_and_game(games):
            game = games[sys_id][game_id]
            self._handle_game(sys_id, game)
            games.data[sys_id][game_id]['moved'] = True
            games.save()

    def _handle_game(self, sys_id: str, game: dict):
        game_name = game['name']
        filepath = self._get_filepath(game_name)

        if not filepath:
            console.print(
                f'WARNING: File not found for {game_name}. To extract in the future, please...' # TODO: WIP
            )
            return

        sys_folder = self.roms_path / sys_id
        if not sys_folder.is_dir():
            sys_folder.mkdir()

        if filepath.suffix not in ArchiveSuffix:
            shutil.move(filepath, sys_folder)
            return

        match filepath.suffix:
            case ArchiveSuffix.ZIP:
                ...
            case ArchiveSuffix.SEVEN_ZIP:
                ...
            case _:
                ...

        if self.will_delete_archive:
            ...