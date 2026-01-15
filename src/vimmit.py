from vimm_roller import VimmRoller
from pathlib import Path
from argparse import Namespace
import hashlib
from data import Config, Games
from dataclasses import dataclass

@dataclass
class Vimmit:
    games: Games
    config: Config
    args: Namespace

    # def __init_blacklist(self):
    #     ...

    # def _handle_blacklist(self, systems: dict):
    #     GLOBAL = 'Global'

    #     blacklist_path = Path.cwd() / 'blacklist.txt'
    #     if not Path.is_file(blacklist_path):
    #         Path.touch(blacklist_path)

    #     old_hash = self.config['bl_hash']
    #     with open(blacklist_path, 'rb') as f:
    #         current_hash = hashlib.md5(f.read()).hexdigest()

    #     if old_hash != current_hash:
    #         with open(blacklist_path, 'r') as f:
    #             blacklist = yaml.safe_load(f)

    #         if blacklist is None:
    #             blacklist = {}

    #         if GLOBAL not in blacklist:
    #             blacklist[GLOBAL] = []

    #         for system in self.config['systems'].values():
    #             sys_name = system['name']
    #             sys_id = system['id']
    #             name = f'{sys_name} ({sys_id})'
    #             if name not in blacklist:
    #                 blacklist[name] = []

    #         # TODO: WIP

    #         with open(blacklist_path, 'w') as f:
    #             yaml.safe_dump(blacklist, f)

    def _handle_scrape(self, systems: dict):
        from vimm_scraper import VimmScraper
        from requests import Session
        import truststore

        truststore.inject_into_ssl()
        session = Session()

        for sys_id, sys_name in systems.items():
            print(f'Downloading games list for {sys_name} ({sys_id}). Please wait...')
            vimm_scraper = VimmScraper(
                self.games,
                self.config,
                session,
                sys_id,
                self.args.reset,
                test_mode=True # TODO: Disable test mode
            )
            vimm_scraper.run()
        print('All systems complete!')

    def run(self):
        systems = {v['id']: v['name'] for k, v in self.config.data['systems'].items() if k in self.args.systems}

        if not self.args.download:
            # self._handle_blacklist(systems)
            vimm_roller = VimmRoller(self.games, self.config, systems)
            vimm_roller.roll()
            return

        from requests import ConnectionError
        try:
            self._handle_scrape(systems)
        except (AttributeError, ConnectionError):
            print('That didn\'t work. Resetting base url.') # TODO: Better handling and message
            self.config['base_url'] = None
            self.config.save()
            return
