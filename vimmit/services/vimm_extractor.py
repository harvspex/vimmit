from pathlib import Path

from common.console import console
from data.config import Config
from data.games import Games

# TODO:
# - Setup downloads folder and destination folder if needed
# - Match string similarity of seen games to games in downloads folder
#   - If extension == .zip or .7z : Extract games to dir "System/Archive Name (no suffix)/"
#   - Else: just move the file to dir "System/"
# - Flag games as extracted
# - Delete archive if will_delete == True
#
# Change importer to only import game IDs, names, and (optionally) seen data
# Also, don't import download path/roms path from config

class VimmExtractor:
    ARCHIVE_SUFFIXES = {'.7z', '.zip'}

    def __init__(self, config: Config):
        self.systems = config.data['systems']
        self.download_path = Path(config.data['downloads'])
        self.roms_path = Path(config.data['roms'])

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

    def _extract_game(self, filepath: Path, sys_id: str, game_id: str):
        ...

    def _move_game(self, filepath: Path, sys_id: str, game_id: str):
        ...

    def run(self, games: Games):
        for sys_id, game_id in self._yield_sys_and_game(games):
            self._handle_game(games, sys_id, game_id)

    def _handle_game(self, games: Games, sys_id: str, game_id: str):
        game = games[sys_id][game_id]
        game_name = game['name']
        filepath = self._get_filepath(game_name)

        if not filepath:
            # TODO: Colour
            console.print(
                f'WARNING: File not found for {game_name}. To extract in the future, please...' # TODO: WIP
            )

        elif filepath.suffix in self.ARCHIVE_SUFFIXES:
            self._extract_game()

        else:
            self._move_game()

        games.data[sys_id][game_id]['moved'] = True
        games.save()