from data.config import Config
from data.base_data import _BaseData

from pathlib import Path


class Games(_BaseData):
    def __init__(self):
        filepath = Path.cwd() / '.data' / 'games.dat'
        super().__init__(filepath)

    def dump_history(self, config: Config, filepath: Path):
        extract_names = lambda data: [f'{game['name']}\n' for game in data.values() if game.get('seen', False)]
        history = {system: extract_names(games) for system, games in self.data.items()}
        with open(filepath, 'w') as f:
            for sys_id, games in history.items():
                bl_id = config.data['systems'][sys_id]['bl_id']
                f.write(f'# {bl_id}\n')
                f.writelines(games)
                f.write('\n')