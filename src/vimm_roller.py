from data_objects import Blacklist, Config, Games
from utils.format import format_system_name_and_id
import random
import urllib.parse


class NoGamesError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class NoSystemsError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


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
        self.selected_systems = self._validate_systems(selected_systems)

    @staticmethod
    def _roll_dict_key(_dict: dict):
        return random.choice(list(_dict.keys()))

    @staticmethod
    def _game_is_unseen(game: dict) -> bool:
        return not game.get('seen', False)

    def _validate_systems(self, selected_systems: dict) -> dict:
        selected_systems_set = set(selected_systems.keys())
        downloaded_systems = set(self.games.data.keys())
        intersect = selected_systems_set.intersection(downloaded_systems)
        difference = selected_systems_set.difference(downloaded_systems)
        if difference:
            print(f'Game data for the following system/s were not found and will be skipped: {" ".join(difference)}')
        return {k: v for k, v in self.config.data['systems'].items() if k in intersect}

    def _check_blacklist(self, bl_id: str, game_name: str) -> bool:
        for phrase in self.blacklist.data[bl_id]:
            if phrase in game_name:
                return True
        return False

    def _game_is_blacklisted(self, sys_id: str, game: dict) -> bool:
        bl_id = self.config.data['systems'][sys_id]['bl_id']
        game_name = game['name']
        return self._check_blacklist(self.blacklist.ALL_SYSTEMS, game_name) \
            or self._check_blacklist(bl_id, game_name)

    def _roll_system(self) -> str:
        if len(self.selected_systems) < 1:
            raise NoSystemsError

        key = self._roll_dict_key(self.selected_systems)
        return key, self.selected_systems.pop(key)

    def _roll_game(self, sys_id: str) -> dict:
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
        if len(self.selected_systems) < 1:
            return

        while True:
            try:
                sys_id, system = self._roll_system()
            except NoSystemsError:
                print('No new games! Try a new system, or reduce your blacklist.')
                return
            try:
                game_id, game = self._roll_game(sys_id)
                break
            except NoGamesError:
                continue

        url = urllib.parse.urljoin(self.config.data['base_url'], str(game_id))
        print(f'{format_system_name_and_id(system['name'], system['vimm_id'])}: "{game['name']}". {url}')
        self.games.data[sys_id][game_id]['seen'] = True
        self.games.save()
