from vimm_roller import VimmRoller
from pathlib import Path
import utils.load_dump as load_dump
from argparse import Namespace


class Vimmit:
    def __init__(
        self,
        games_path: Path,
        config_path: Path,
        args: Namespace
    ):
        self.games_path = games_path
        self.config_path = config_path
        self.config = load_dump.load_config(config_path)
        self.args = args

    def _handle_scrape(self, systems: list):
        from vimm_scraper import VimmScraper
        from requests import Session
        import truststore

        truststore.inject_into_ssl()
        session = Session()

        for system in systems:
            print(f'Scraping for {system["name"]} ({system["id"]}) games. Please wait...')
            vimm_scraper = VimmScraper(
                session,
                self.config['base_url'],
                system['id'],
                self.games_path,
                self.args.reset,
                test_mode=True # TODO: Disable test mode
            )
            vimm_scraper.run()
        print('All systems complete!')

    def run(self):
        systems = [v for k, v in self.config['systems'].items() if k in self.args.systems]
        if not self.args.scrape:
            vimm_roller = VimmRoller(systems, self.games_path)
            vimm_roller.roll()
            return

        from requests import ConnectionError
        try:
            self._handle_scrape(systems)
        except (AttributeError, ConnectionError):
            print('That didn\'t work. Resetting base url.') # TODO: Better message
            self.config['base_url'] = None
            load_dump.dump_pickle(self.config, self.config_path)
            return
