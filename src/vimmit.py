from vimm_roller import VimmRoller
from vimm_scraper import VimmScraper
from utils.cli import get_parser
from utils.setup import input_base_url
from data_objects import *
from typing import Callable
# from requests import ConnectionError

class Vimmit:
    def __init__(self):
        self.config = Config()

    def __add_if_not_in(self, key: str, func: Callable, *args, **kwargs):
        if not self.config.data.get(key, False):
            self.config.data[key] = func(*args, **kwargs)

    def __setup(self):
        self.__add_if_not_in('base_url', input_base_url)
        self.__add_if_not_in('systems', self.__scrape_systems_list)
        self.config.save()

    def __scrape_systems_list(self):
        scraper = VimmScraper(self.config)
        scraper.scrape_systems_list()

    def __scrape_games(self, games: Games, systems: dict):
        scraper = VimmScraper(self.config)
        scraper.scrape_games(games, systems)

    def run(self):
        self.__setup()
        systems = list(self.config.data['systems'].keys())
        parser = get_parser(systems)
        args = parser.parse_args()

        if args.scrape_systems:
            self.__scrape_systems_list()

        games = Games()
        blacklist = Blacklist(self.config)
        selected_systems = {k: v for k, v in self.config.data['systems'].items() if k in args.systems}

        if not args.download:
            vimm_roller = VimmRoller(games, self.config, blacklist, selected_systems)
            vimm_roller.roll()
            return

        self.__scrape_games(games, selected_systems)

        if args.export:
            games.dump_json()

        # try:
        #     self._handle_scrape(selected_systems)
        # except (AttributeError, ConnectionError) as e:
        #     print(e)
        #     # print('That didn\'t work. Resetting base url.') # TODO: Better handling and message
        #     self.config.data['base_url'] = None
        #     self.config.save()
        #     return
