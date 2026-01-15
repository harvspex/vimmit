from classes.vimm_roller import VimmRoller
from classes.data import *
from argparse import Namespace
from dataclasses import dataclass

@dataclass
class Vimmit:
    games: Games
    config: Config
    args: Namespace

    def _handle_blacklist(self, systems: dict):
        blacklist = Blacklist()
        old_hash = self.config.data['bl_hash']

        if old_hash != blacklist.get_hash():
            # TODO: WIP
            ...

    def _handle_scrape(self, systems: dict):
        from classes.vimm_scraper import VimmScraper
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
            self._handle_blacklist(systems)
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
