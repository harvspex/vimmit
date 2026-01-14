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
        self.systems = systems
        self.collection_path = collection_path
        self.config_path = config_path
        # self.blacklist_path = blacklist_path
        # self.blacklist = utils.load_blacklist(blacklist_path)

    @staticmethod
    def _game_is_allowed(game: dict) -> bool:
        return not (game.get('seen', False) or game.get('bl', False))

    def _validate_systems(self, collection: dict):
        systems_set = set(self.systems.keys())
        difference = systems_set.difference(set(collection.keys()))
        self.systems = {k: v for k, v in self.systems.items() if k not in difference}

        if difference:
            print(f'The following system/s were not found and will be skipped: {" ".join(difference)}')

        if len(systems_set) < 1:
            raise NoSystemsError

    def _roll_system_and_game(self, collection: dict) -> dict:
        system_list = list(self.systems.keys())
        while True:
            choice = random.randint(0, len(system_list) - 1)
            system_id = system_list.pop(choice)
            subset = {
                id: game
                for id, game in collection[system_id].items()
                if VimmRoller._game_is_allowed(game)
            }
            if subset:
                game_id = random.choice(list(subset.keys()))
                return system_id, game_id
            if not system_list:
                raise NoGamesError

    def roll(self):
        collection = load_dump.load_collection(self.collection_path) # TODO: handle missing filepath
        try:
            self._validate_systems(collection)
            sys_id, game_id = self._roll_system_and_game(collection) # TODO: handle bad system value
        except NoGamesError:
            print('No games found! Try reducing your blacklist, or downloading games for a new system.')
            return
        except NoSystemsError:
            return

        config = load_dump.load_config(self.config_path)
        collection[sys_id][game_id]['seen'] = True
        load_dump.dump_pickle(collection, self.collection_path)
        game_name = collection[sys_id][game_id]['name']
        url = urllib.parse.urljoin(config['base_url'], str(game_id))
        print(f'{self.systems[sys_id]} ({sys_id}): "{game_name}". {url}')
