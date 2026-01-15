from data import Config, Games
from dataclasses import dataclass
from pathlib import Path
import random
import urllib.parse

# TODO: Implement Blacklist

class NoGamesError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class NoSystemsError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


@dataclass
class VimmRoller:
    games: Games
    config: Config
    systems: dict

    @staticmethod
    def _game_is_allowed(game: dict) -> bool:
        return not (game.get('seen', False) or game.get('bl', False))

    def _validate_systems(self):
        systems_set = set(self.systems.keys())
        difference = systems_set.difference(set(self.games.data.keys()))
        self.systems = {k: v for k, v in self.systems.items() if k not in difference}

        if difference:
            print(f'The following system/s were not found and will be skipped: {" ".join(difference)}')

        if len(systems_set) < 1:
            raise NoSystemsError

    def _roll_system_and_game(self) -> dict:
        system_list = list(self.systems.keys())
        while True:
            if not system_list:
                raise NoGamesError
            choice = random.randint(0, len(system_list) - 1)
            system_id = system_list.pop(choice)
            subset = {
                id: game
                for id, game in self.games.data[system_id].items()
                if VimmRoller._game_is_allowed(game)
            }
            if subset:
                game_id = random.choice(list(subset.keys()))
                return system_id, game_id

    def roll(self):
        try:
            self._validate_systems()
            sys_id, game_id = self._roll_system_and_game() # TODO: handle bad system value?
        except NoGamesError:
            print('No games found! Try reducing your blacklist, or downloading games for a new system.')
            return
        except NoSystemsError:
            return

        game_name = self.games.data[sys_id][game_id]['name']
        self.games.data[sys_id][game_id]['seen'] = True
        self.games.save()
        url = urllib.parse.urljoin(self.config.data['base_url'], str(game_id))
        print(f'{self.systems[sys_id]} ({sys_id}): "{game_name}". {url}')
