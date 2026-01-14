from pathlib import Path
import utils.load_dump as load_dump
import random

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
        systems: list,
        collection_path: Path,
        # config_path: Path,
        # blacklist_path: Path
    ):
        self.systems_dicts = systems
        self.systems = {_['id'] for _ in systems}
        self.collection_path = collection_path
        # self.collection = utils.load_collection(collection_path)
        # self.config_path = config_path
        # self.config = utils.load_config(config_path)
        # self.blacklist_path = blacklist_path
        # self.blacklist = utils.load_blacklist(blacklist_path)

    @staticmethod
    def _game_is_allowed(game: dict) -> bool:
        return not (game.get('seen', False) or game.get('bl', False))

    def _validate_systems(self, collection: dict):
        difference = self.systems.difference(set(collection.keys()))
        self.systems -= difference

        if difference:
            print(f'The following system/s were not found and will be skipped: {" ".join(difference)}')

        if len(self.systems) < 1:
            raise NoSystemsError


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
        collection = load_dump.load_collection(self.collection_path) # TODO: handle missing filepath
        try:
            self._validate_systems(collection)
            system, games = self.get_gamelist(collection) # TODO: handle bad system value
        except NoGamesError:
            print('No games found! Try reducing your blacklist, or downloading games for a new system.')
            return
        except NoSystemsError:
            return

        game_id = random.choice(list(games.keys()))
        game = games[game_id]
        collection[system][game_id]['seen'] = True
        load_dump.dump_pickle(collection, self.collection_path)
        print(f'({system}): "{game["name"]}" {game_id}') # TODO: Fix link, improve system name
