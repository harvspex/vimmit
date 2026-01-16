from data_objects import Blacklist, Config, Games
import random
import urllib.parse

class VimmRoller:
    def __init__(
        self,
        games: Games,
        config: Config,
        blacklist: Blacklist,
        selected_systems: list[tuple]
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

    def _validate_systems(self, selected_systems: list[tuple]):
        # TODO: Fix
        selected_systems = {_[0] for _ in selected_systems}
        downloaded_systems = set(self.games.data.keys())
        union = selected_systems.union(downloaded_systems)
        difference = selected_systems.difference(downloaded_systems)
        if difference:
            print(f'Game data for the following system/s were not found: {" ".join(difference)}')

        return {k: v for k, v in self.config.data['systems'].items() if k in union}

    def _check_blacklist(self, bl_id: str, game_name: str) -> bool:
        for phrase in self.blacklist.data[bl_id]:
            if phrase in game_name:
                return True
        return False

    def _game_is_blacklisted(self, sys_id: str, game: dict) -> bool:
        bl_id = self.selected_systems[sys_id]['bl_id']
        game_name = game['name']
        return self._check_blacklist(self.blacklist.ALL_SYSTEMS, game_name) \
            or self._check_blacklist(bl_id, game_name)

    def _roll_system(self) -> str:
        key = self._roll_dict_key(self.selected_systems)
        return key, self.selected_systems.pop(key)

    def _roll_game(self, sys_id: str) -> dict:
        games = {
            id: game
            for id, game in self.games.data[sys_id].items()
            if VimmRoller._game_is_unseen(game)
        }
        while True:
            key = self._roll_dict_key(games)
            game = games.pop(key)
            if not self._game_is_blacklisted(sys_id, game):
                return game

    def roll(self):
        try:
            sys_id, sys_name = self._roll_system()
        except IndexError:
            print('No systems')
            return
        game = self._roll_game(sys_id)
        game_id = game['id']
        self.games.data[sys_id][game_id]['seen'] = True
        url = urllib.parse.urljoin(self.config.data['base_url'], str(game_id))
        print(f'{sys_name} ({sys_id}): "{game['name']}". {url}')
