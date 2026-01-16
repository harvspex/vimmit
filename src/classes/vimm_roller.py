from classes.data import Blacklist, Config, Games
import random
import urllib.parse

# TODO: Implement Blacklist

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
    def _game_is_allowed(game: dict) -> bool:
        return not game.get('seen', False)

    def _validate_systems(self, systems: dict):
        systems_set = set(systems.keys())
        difference = systems_set.difference(set(self.games.data.keys()))
        self.systems = {k: v for k, v in systems.items() if k not in difference}

        if difference:
            print(f'Game data for the following system/s were not found: {" ".join(difference)}')

    def _check_blacklist(self, game: dict) -> bool:
        ...

    def _roll_system(self) -> dict:
        return self._roll_and_pop(self.systems)

    def _roll_game(self, system_id: str) -> dict:
        games = {
            id: game
            for id, game in self.games.data[system_id].items()
            if VimmRoller._game_is_allowed(game)
        }
        game = self._roll_and_pop(games)

    def roll(self):
        ...

    # def roll(self):
    #     try:
    #         self._validate_systems()
    #         sys_id, game_id = self._roll_system_and_game() # TODO: handle bad system value?
    #     except NoGamesError:
    #         print('No games found! Try reducing your blacklist, or downloading games for a new system.')
    #         return
    #     except NoSystemsError:
    #         return

    #     game_name = self.games.data[sys_id][game_id]['name']
    #     self.games.data[sys_id][game_id]['seen'] = True
    #     self.games.save()
    #     url = urllib.parse.urljoin(self.config.data['base_url'], str(game_id))
    #     print(f'{self.systems[sys_id]} ({sys_id}): "{game_name}". {url}')
