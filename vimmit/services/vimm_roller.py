from typing import Any
import random
import urllib.parse

from data.blacklist import Blacklist
from data.config import Config
from data.games import Games
from common.console import console
from common.exceptions import NoGamesError, NoSystemsError


def _roll_dict_key(_dict: dict) -> Any:
    return random.choice(list(_dict.keys()))

def _game_is_unseen(game: dict) -> bool:
    return not game.get('seen', False)

def _check_blacklist(blacklist: Blacklist, bl_id: str, game_name: str) -> bool:
    for phrase in blacklist.data[bl_id]:
        if phrase in game_name:
            return True
    return False

def _game_is_blacklisted(config: Config, blacklist: Blacklist, sys_id: str, game: dict) -> bool:
    game_name = game['name'].lower()
    bl_id = config.data['systems'][sys_id]['bl_id']
    return _check_blacklist(blacklist, blacklist.ALL_SYSTEMS, game_name) \
        or _check_blacklist(blacklist, bl_id, game_name)

def _roll_system(selected_systems: dict) -> str:
    if not selected_systems:
        raise NoSystemsError('No new games! Try a new system, or reduce your blacklist.')

    key = _roll_dict_key(selected_systems)
    return key, selected_systems.pop(key)

def _roll_game(games: Games, config: Config, blacklist: Blacklist, sys_id: str) -> tuple:
    games = {
        id: game
        for id, game in games.data[sys_id].items()
        if _game_is_unseen(game)
    }
    while len(games) > 0:
        key = _roll_dict_key(games)
        game = games.pop(key)
        if not _game_is_blacklisted(config, blacklist, sys_id, game):
            return key, game
    raise NoGamesError

def roll(games: Games, config: Config, blacklist: Blacklist, selected_systems: dict):
    while True:
        sys_id, system = _roll_system(selected_systems)
        try:
            game_id, game = _roll_game(games, config, blacklist, sys_id)
            break
        except NoGamesError:
            continue

    url = urllib.parse.urljoin(config.data['base_url'], str(game_id))
    console.print(f'[green][{system['bl_id']}][/green] [bold]{game['name']}[/bold] → [magenta]{url}[/magenta]')
    games.data[sys_id][game_id]['seen'] = True
    games.save()