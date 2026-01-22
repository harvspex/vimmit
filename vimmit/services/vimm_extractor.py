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

ARCHIVE_SUFFIXES = {'.7z', '.zip'}


def _match_game_from_filename(seen_games: dict, filename: str) -> tuple:
    for sys_id in seen_games:
        for game_id, game in seen_games[sys_id].items():
            if game['name'] in filename:
                return sys_id, game_id
    return None, None


def _handle_extract():
    ...


def _handle_move():
    ...


def _move_or_extract():
    ...


def extract_games(config: Config, games: Games):
    download_path = Path(config.data['downloads'])
    roms_path = Path(config.data['roms'])
    seen_games = ...
    
    for file in download_path.iterdir():        
        sys_id, game_id = _match_game_from_filename(seen_games, file.name)
        if None in (sys_id, game_id):
            continue

        ...