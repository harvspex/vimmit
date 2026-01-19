from pathlib import Path

from data.config import Config
from data.base_data import BaseData, DATA_DIR


class Games(BaseData):
    def __init__(self):
        super().__init__(DATA_DIR, 'games.dat')

    def dump_history(self, config: Config, filepath: Path):
        extract_names = lambda data: [f'{game['name']}\n' for game in data.values() if game.get('seen', False)]
        history = {system: extract_names(games) for system, games in self.data.items()}
        with open(filepath, 'w') as f:
            for sys_id, games in history.items():
                bl_id = config.data['systems'][sys_id]['bl_id']
                f.write(f'# {bl_id}\n')
                f.writelines(games)
                f.write('\n')

    def clear_seen(self, systems: list):
        for sys in systems:
            for game in self.data[sys].values():
                if game.get('seen', False):
                    del game['seen']

    def sort_games_per_system(self, sys_id):
        self.data[sys_id] = dict(sorted(self.data[sys_id].items(), key=lambda x: x[1]['name']))

    def sort_all_games(self):
        for sys_id in self.data.keys():
            self.sort_games_per_system(sys_id)