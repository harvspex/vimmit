from data_objects import Config
from exceptions import NoSystemsError
from vimm_roller import VimmRoller
from vimm_scraper import VimmScraper
from utils.cli import get_args
from utils.setup import input_base_url
from data_objects import *
from typing import Callable
from requests import ConnectionError

class Vimmit:
    def __init__(self):
        self.config = Config()

    def _update_config(self, key: str, func: Callable, will_run: bool=False):
        if not self.config.data.get(key, False) or will_run:
            self.config.data[key] = func()
            self.config.save()

    def _scrape_systems_list(self) -> dict:
        scraper = VimmScraper(self.config)
        return scraper.scrape_systems_dict()

    def _scrape_games(self, games: Games, systems: dict):
        scraper = VimmScraper(self.config)
        scraper.scrape_games(games, systems)

    def validate_systems(self, selected_systems: list, all_systems: list, message: str) -> dict:
        selected_systems_set = set(selected_systems)
        downloaded_systems = set(all_systems)
        intersect = selected_systems_set.intersection(downloaded_systems)
        difference = selected_systems_set.difference(downloaded_systems)

        if difference:
            print(f'{message}: {" ".join(difference)}')

        if not intersect:
            raise NoSystemsError

        return {k: v for k, v in self.config.data['systems'].items() if k in intersect}

    def _run(self):
        args = get_args()

        # Setup
        self._update_config('base_url', input_base_url, args.url)
        self._update_config('systems', self._scrape_systems_list, args.scrape_systems)

        games = Games()

        if args.download:
            selected_systems = self.validate_systems(
                args.systems,
                self.config.data['systems'].keys(),
                'The following systems were not found and will be skipped'
            )
            self._scrape_games(games, selected_systems)

        else: # Roll game
            selected_systems = self.validate_systems(
                args.systems,
                games.data.keys(),
                'No games found for following systems (will be skipped)'
            )
            blacklist = Blacklist(self.config)
            vimm_roller = VimmRoller(games, self.config, blacklist, selected_systems)
            vimm_roller.roll()

        if args.export:
            games.dump_json()

    def run(self):
        try:
            self._run()
        except NoSystemsError:
            return
        except ConnectionError:
            # TODO:
            # - handle bad url
            # - handle incorrect url
            # - Better handling and message
            print('That didn\'t work. Resetting base url.')
            self.config.data['base_url'] = None
            self.config.save()
            return
        except TypeError as e:
            print(e)
            ...
        except AttributeError as e:
            print(e)
            ...
        except KeyboardInterrupt as e:
            print(e)
            ...
