from typing import Any
import random
import urllib.parse

from data.blacklist import Blacklist
from data.config import Config
from data.games import Games
from utils.cli import console
from utils.exceptions import NoGamesError, NoSystemsError


class VimmRoller:
    def __init__(
        self,
        games: Games,
        config: Config,
        blacklist: Blacklist,
        selected_systems: dict
    ):
        self.games = games
        self.config = config
        self.blacklist = blacklist
        self.selected_systems = selected_systems

    @staticmethod
    def _roll_dict_key(_dict: dict) -> Any:
        return random.choice(list(_dict.keys()))

    @staticmethod
    def _game_is_unseen(game: dict) -> bool:
        return not game.get('seen', False)

    def _check_blacklist(self, bl_id: str, game_name: str) -> bool:
        for phrase in self.blacklist.data[bl_id]:
            if phrase in game_name:
                return True
        return False

    def _game_is_blacklisted(self, sys_id: str, game: dict) -> bool:
        bl_id = self.config.data['systems'][sys_id]['bl_id']
        game_name = game['name'].lower()
        return self._check_blacklist(self.blacklist.ALL_SYSTEMS, game_name) \
            or self._check_blacklist(bl_id, game_name)

    def _roll_system(self) -> str:
        if not self.selected_systems:
            raise NoSystemsError('No new games! Try a new system, or reduce your blacklist.')

        key = self._roll_dict_key(self.selected_systems)
        return key, self.selected_systems.pop(key)

    def _roll_game(self, sys_id: str) -> tuple:
        games = {
            id: game
            for id, game in self.games.data[sys_id].items()
            if VimmRoller._game_is_unseen(game)
        }
        while len(games) > 0:
            key = self._roll_dict_key(games)
            game = games.pop(key)
            if not self._game_is_blacklisted(sys_id, game):
                return key, game
        raise NoGamesError

    def roll(self):
        while True:
            sys_id, system = self._roll_system()
            try:
                game_id, game = self._roll_game(sys_id)
                break
            except NoGamesError:
                continue

        url = urllib.parse.urljoin(self.config.data['base_url'], str(game_id))
        console.print(f'[green][{system['bl_id']}][/green] [bold]{game['name']}[/bold] → [magenta]{url}[/magenta]')
        self.games.data[sys_id][game_id]['seen'] = True
        self.games.save()
