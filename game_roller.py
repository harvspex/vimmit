from pathlib import Path
import utils
import random


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


    def pre(self):
        # TODO: check if blacklist hash changed
        # if yes, reapply blacklist
        # filter non-blacklisted, non-seen games
        # if list is empty, reroll new system
        ...


    def roll(self):
        # TODO: WIP
        system = random.choice(list(self.systems))
        collection = utils.load_collection(self.collection_path) # TODO: handle missing filepath
        games = collection[system] # TODO: handle missing system
        game_id = random.choice(list(games.keys()))
        game = games[game_id]
        print(f'{system} {game["name"]} {game_id}')


filepath = Path.cwd() / 'games.dat'
vr = VimmRoller(['PS1'], filepath)
vr.roll()