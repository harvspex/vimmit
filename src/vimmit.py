from data_objects import Config
from exceptions import NoSystemsError, ScrapeError
from vimm_roller import VimmRoller
from vimm_scraper import VimmScraper
from utils.cli import get_args
from utils.setup import input_base_url
from data_objects import *
from typing import Callable

class Vimmit:
    def __init__(self):
        self.config = Config()

    def reset_config(self, *keys: str, reset_all: bool=False):
        if reset_all:
            self.config.data.clear()
        for key in keys:
            self.config.data[key] = None
        self.config.save()

    def _update_config(self, key: str, func: Callable, will_run: bool=False):
        if not self.config.data.get(key, False) or will_run:
            self.config.data[key] = func()
            self.config.save()

    @staticmethod
    def _scrape_wrapper(func: Callable, *args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except:
            raise ScrapeError
        if not result:
            raise ScrapeError
        return result

    def _scrape_systems_list(self) -> dict:
        scraper = VimmScraper(self.config)
        return self._scrape_wrapper(scraper.scrape_systems_dict)

    def _scrape_games(self, games: Games, systems: dict):
        scraper = VimmScraper(self.config)
        return self._scrape_wrapper(scraper.scrape_games, games, systems)

    def validate_systems(
        self,
        selected_systems: list,
        all_systems: list,
        difference_message: str
    ) -> dict:
        selected_systems_set = set(selected_systems)
        downloaded_systems = set(all_systems)
        intersect = selected_systems_set.intersection(downloaded_systems)
        difference = selected_systems_set.difference(downloaded_systems)
        if not intersect:
            raise NoSystemsError(
                f'Please select a valid system:\n{' '.join(self.config.data['systems'].keys())}'
            )
        if difference:
            print(f'{difference_message}: {' '.join(difference)}')
        return {k: v for k, v in self.config.data['systems'].items() if k in intersect}

    def run(self):
        args = get_args()

        # Setup
        self._update_config('base_url', input_base_url, args.url)
        self._update_config('systems', self._scrape_systems_list, args.scrape_systems)

        games = Games()

        valid_systems = self.validate_systems(
            args.systems,
            self.config.data['systems'].keys(),
            'The following systems were not found and will be skipped',
        )
        if args.download:
            self._scrape_games(games, valid_systems)

        else: # Roll game
            selected_systems = self.validate_systems(
                valid_systems.keys(),
                games.data.keys(),
                'No games found for following systems (will be skipped)',
            )
            blacklist = Blacklist(self.config)
            vimm_roller = VimmRoller(games, self.config, blacklist, selected_systems)
            vimm_roller.roll()

        if args.export:
            games.dump_json()