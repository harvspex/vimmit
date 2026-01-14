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

    def _handle_scrape(self, systems: dict):
        from vimm_scraper import VimmScraper
        from requests import Session
        import truststore

        truststore.inject_into_ssl()
        session = Session()

        for sys_id, sys_name in systems.items():
            print(f'Downloading games list for {sys_name} ({sys_id}). Please wait...')
            vimm_scraper = VimmScraper(
                session,
                self.config['base_url'],
                sys_id,
                self.games_path,
                self.args.reset,
                test_mode=True # TODO: Disable test mode
            )
            vimm_scraper.run()
        print('All systems complete!')

    def run(self):
        systems = {v['id']: v['name'] for k, v in self.config['systems'].items() if k in self.args.systems}
        if not self.args.download:
            vimm_roller = VimmRoller(systems, self.games_path, self.config_path)
            vimm_roller.roll()
            return

        from requests import ConnectionError
        try:
            self._handle_scrape(systems)
        except (AttributeError, ConnectionError):
            print('That didn\'t work. Resetting base url.') # TODO: Better handling and message
            self.config['base_url'] = None
            load_dump.dump_pickle(self.config, self.config_path)
            return
