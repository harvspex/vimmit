from pathlib import Path
import utils
import pandas as pd
import random


class VimmRoller:
    def __init__(
        self,
        systems: list,
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

    def roll(self):
        system = random.choice(self.systems)
        collection = utils.load_collection(self.collection_path)
        games = collection[system]
        key = random.choice(list(games.keys()))
        return games[key]

filepath = Path.cwd() / 'games.dat'
vr = VimmRoller(['PS1'], filepath)
result = vr.roll()
print(result)