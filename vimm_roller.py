from pathlib import Path
from enum import Enum
import utils
import random

# class Mode(Enum):
#     SYSTEM = 'game'
#     GAME = 'game'


class NoGamesError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class VimmRoller:
    def __init__(
        self,
        systems: set,
        collection_path: Path,
        # config_path: Path,
        # blacklist_path: Path
    ):
        self.systems = systems
        self.collection_path = collection_path
        # self.collection = utils.load_collection(collection_path)
        # self.config_path = config_path
        # self.config = utils.load_config(config_path)
        # self.blacklist_path = blacklist_path
        # self.blacklist = utils.load_blacklist(blacklist_path)

    @staticmethod
    def _game_is_allowed(game: dict) -> bool:
        return not (game.get('seen', False) or game.get('bl', False))

    def get_gamelist(self, collection: dict) -> dict:
        while True:
            system = random.choice(list(self.systems))
            self.systems.remove(system)
            subset = {
                id: game
                for id, game in collection[system].items()
                if VimmRoller._game_is_allowed(game)
            }
            if subset:
                return system, subset
            if not self.systems:
                raise NoGamesError

    def roll(self):
        collection = utils.load_collection(self.collection_path) # TODO: handle missing filepath
        try:
            system, games = self.get_gamelist(collection) # TODO: handle bad system value
        except NoGamesError:
            ...

        game_id = random.choice(list(games.keys()))
        game = games[game_id]
        print(f'{system} {game["name"]} {game_id}')


filepath = Path.cwd() / 'games.dat'
vr = VimmRoller(['PS1'], filepath)
vr.roll()