from classes.vimm_roller import VimmRoller
from classes.data import *
from utils.setup import scrape_systems
from argparse import Namespace
from dataclasses import dataclass

@dataclass
class Vimmit:
    config: Config
    args: Namespace

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
        games = Games()
        blacklist = Blacklist(self.config)

        if self.args.scrape_systems:
            # TODO: Make nicer?
            self.config.data['systems'] = scrape_systems(self.config.data['base_url'])

        # TODO: Make this a set of IDs?
        selected_systems = {v['id']: v['name'] for k, v in self.config.data['systems'].items() if k in self.args.systems}

        if not self.args.download:
            vimm_roller = VimmRoller(games, self.config, blacklist, selected_systems)
            vimm_roller.roll()
            return

        from requests import ConnectionError
        try:
            self._handle_scrape(selected_systems)
        except (AttributeError, ConnectionError):
            print('That didn\'t work. Resetting base url.') # TODO: Better handling and message
            self.config['base_url'] = None
            self.config.save()
            return

        games.save()
        self.config.save()
