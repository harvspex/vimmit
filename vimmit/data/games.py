from typing import Iterable, Hashable

from data.base_data import BaseData, DATA_DIR


class Games(BaseData):
    def __init__(self):
        super().__init__(DATA_DIR, 'games.dat')

    @staticmethod
    def clear_keys(games: Games, systems: Iterable, *keys: Hashable):
        # TODO: Test this
        keys = set(keys)
        for sys_id in systems:
            for game_id, game in games.data[sys_id].items():
                new_game = {k: v for k, v in game.items() if k not in keys}
                games.data[sys_id][game_id] = new_game

    @staticmethod
    def clear_seen(games: Games, systems: Iterable):
        return games.clear_keys(systems, 'seen', 'moved')

    def sort_games_per_system(self, sys_id):
        self.data[sys_id] = dict(sorted(self.data[sys_id].items(), key=lambda x: x[1]['name']))

    def sort_all_games(self):
        for sys_id in self.data.keys():
            self.sort_games_per_system(sys_id)