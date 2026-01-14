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

    def _handle_crawl(self):
        from vimm_crawler import VimmCrawler
        from requests import Session
        import truststore

        if not self.config.get('base_url', False):
            self.__handle_setup()

        truststore.inject_into_ssl()
        session = Session()

        for system in self.args.systems:
            vimm_crawler = VimmCrawler(
                session,
                self.config['base_url'],
                system,
                self.games_path,
                self.args.reset,
                test_mode=True # TODO: Disable test mode
            )
            vimm_crawler.run()

    def run(self):
        if self.args.crawl:
            from requests import ConnectionError
            try:
                self._handle_crawl()
            except (AttributeError, ConnectionError):
                print('That didn\'t work. Resetting base url.') # TODO: Better message
                self.config['base_url'] = None
                load_dump.dump_pickle(self.config, self.config_path)
                return

        systems = {self.config['systems'][system]['id'] for system in self.args.systems}
        vimm_roller = VimmRoller(systems, self.games_path)
        vimm_roller.roll()
