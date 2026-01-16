from classes.data import Blacklist, Config, Games
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
        systems: dict
    ):
        self.games = games
        self.config = config
        self.blacklist = blacklist
        self.systems = self._validate_systems(systems)

    @staticmethod
    def _roll_and_pop(_dict: dict):
        key = random.choice(list(_dict.keys()))
        return _dict.pop(key)

    @staticmethod
    def _game_is_unseen(game: dict) -> bool:
        return not game.get('seen', False)

    def _validate_systems(self, systems: dict):
        systems_set = set(systems.keys())
        difference = systems_set.difference(set(self.games.data.keys()))
        systems = {k: v for k, v in systems.items() if k not in difference}
        if difference:
            print(f'Game data for the following system/s were not found: {" ".join(difference)}')
        return systems

    def _check_blacklist(self, bl_id: str, game_name: str) -> bool:
        for phrase in self.blacklist.data[bl_id]:
            if phrase in game_name:
                return True
        return False

    def _game_is_blacklisted(self, sys_id: str, game: dict) -> bool:
        bl_id = self.systems[sys_id]['bl_id']
        game_name = game['name']
        return self._check_blacklist(self.blacklist.ALL_SYSTEMS, game_name) \
            or self._check_blacklist(bl_id, game_name)

    def _roll_system(self) -> dict:
        return self._roll_and_pop(self.systems)

    def _roll_game(self, sys_id: str) -> dict:
        games = {
            id: game
            for id, game in self.games.data[sys_id].items()
            if VimmRoller._game_is_unseen(game)
        }
        while True:
            game = self._roll_and_pop(games)
            if not self._game_is_blacklisted(sys_id, game):
                return game

    def roll(self):
        system = self._roll_system()
        sys_id = system['id']
        game = self._roll_game(system['id'])
        game_id = game['id']
        self.games.data[sys_id][game_id]['seen'] = True
        url = urllib.parse.urljoin(self.config.data['base_url'], str(game_id))
        print(f'{self.systems[sys_id]} ({sys_id}): "{game['name']}". {url}')
