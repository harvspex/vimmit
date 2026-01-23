from pathlib import Path

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

class VimmExtractor:
    ARCHIVE_SUFFIXES = {'.7z', '.zip'}

    def __init__(self, config: Config):
        self.systems = config.data['systems']
        self.download_path = Path(config.data['downloads'])
        self.roms_path = Path(config.data['roms'])

    @staticmethod
    def _match_game_from_filename(seen_games: dict, filename: str) -> tuple:
        for sys_id in seen_games:
            for game_id, game in seen_games[sys_id].items():
                if game['name'] in filename:
                    return sys_id, game_id
        return None, None


    def _handle_extract(self, filepath: Path, sys_id: str, game_id: str):
        ...


    def _handle_move(self, filepath: Path, sys_id: str, game_id: str):
        ...


    def _move_or_extract(self, filepath: Path, sys_id: str, game_id: str):
        if filepath.suffix in self.ARCHIVE_SUFFIXES:
            self._handle_extract()
        else:
            self._handle_move()


    def extract_games(self, games: Games):
        seen_games = ...

        for file in self.download_path.iterdir():        
            sys_id, game_id = self._match_game_from_filename(seen_games, file.name)
            if None in (sys_id, game_id):
                continue

            self._move_or_extract(file, sys_id, game_id)

            # TODO: If users don't download, or manually move some games, this will result in a 
            # growing list of game names that get checked, but never set to 'moved'=True
            #
            # Could warn user that games have been flagged as moved but not actually moved
            # and user needs to rerun an arg like --force-recheck if they download it in the future
            games.data[sys_id][game_id]['moved'] = True