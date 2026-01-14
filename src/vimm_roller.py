from pathlib import Path
import utils.load_dump as load_dump
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
        systems: dict,
        collection_path: Path,
        config_path: Path,
        # blacklist_path: Path
    ):
        self.systems_dict = systems
        self.systems_set = {_['id'] for _ in systems.values()}
        self.collection_path = collection_path
        self.config_path = config_path
        # self.blacklist_path = blacklist_path
        # self.blacklist = utils.load_blacklist(blacklist_path)

    @staticmethod
    def _game_is_allowed(game: dict) -> bool:
        return not (game.get('seen', False) or game.get('bl', False))

    def _validate_systems(self, collection: dict):
        difference = self.systems_set.difference(set(collection.keys()))
        self.systems_set -= difference

        if difference:
            print(f'The following system/s were not found and will be skipped: {" ".join(difference)}')

        if len(self.systems_set) < 1:
            raise NoSystemsError


    def get_gamelist(self, collection: dict) -> dict:
        while True:
            system_id = random.choice(list(self.systems_set))
            self.systems_set.remove(system_id)
            subset = {
                id: game
                for id, game in collection[system_id].items()
                if VimmRoller._game_is_allowed(game)
            }
            if subset:
                return system_id, subset
            if not self.systems_set:
                raise NoGamesError

    def roll(self):
        collection = load_dump.load_collection(self.collection_path) # TODO: handle missing filepath
        try:
            self._validate_systems(collection)
            system_id, games = self.get_gamelist(collection) # TODO: handle bad system value
        except NoGamesError:
            print('No games found! Try reducing your blacklist, or downloading games for a new system.')
            return
        except NoSystemsError:
            return

        config = load_dump.load_config(self.config_path)
        game_id = random.choice(list(games.keys()))
        game = games[game_id]
        collection[system_id][game_id]['seen'] = True
        load_dump.dump_pickle(collection, self.collection_path)
        url = urllib.parse.urljoin(config['base_url'], str(game_id))
        print(f'{self.systems_dict[system_id.lower()]["name"]} ({system_id}): "{game["name"]}". {url}') # TODO: Improve system name
        # TODO: Make this nicer
