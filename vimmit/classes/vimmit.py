from classes.data import Config
from classes.exceptions import NoSystemsError, ScrapeError
from classes.vimm_roller import VimmRoller
from classes.vimm_scraper import VimmScraper
import utils.cli as cli
from utils.cli import console
from utils.setup import input_base_url
from classes.data import *
from typing import Any, Callable

# TODO: Colour printing

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

    def _setup(self, args):
        self._update_config('base_url', input_base_url, args.url)
        self._update_config('systems', self._scrape_systems_list, args.download_systems)

    @staticmethod
    def _scrape_wrapper(func: Callable, *args, **kwargs) -> Any:
        try:
            result = func(*args, **kwargs)
        except KeyboardInterrupt:
            raise
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

    def _check_if_all_systems_selected(self, games: Games, systems: list) -> list:
        systems = set(systems)
        try:
            systems.remove('*')
            systems.update(games.data.keys())
        except KeyError:
            pass
        return list(systems)

    def _validate_systems(
        self,
        selected_systems: list,
        all_systems: list,
        diff_msg: str,
        error_msg: str
    ) -> dict:
        selected_systems_set = set(selected_systems)
        all_systems_set = set(all_systems)
        intersect = selected_systems_set.intersection(all_systems_set)
        difference = selected_systems_set.difference(all_systems_set)
        if not intersect:
            raise NoSystemsError(error_msg)
        if difference:
            console.print(f'{diff_msg}: [orange1]{' '.join(difference)}[/orange1]')
        return {k: v for k, v in self.config.data['systems'].items() if k in intersect}

    def _show_systems(self, games: Games):
        downloaded = list(games.data.keys())
        available = [_ for _ in self.config.data['systems'].keys() if _ not in downloaded]
        console.print(
            f'Downloaded systems: [green]{' '.join(downloaded)}[/green] '
            f'( [green]*[/green] to select all)\n'
            f'Available systems: [bright_cyan]{' '.join(available)}[/bright_cyan]'
        )

    def run(self):
        args = cli.get_args()
        games = Games()

        if getattr(args, 'import'):
            # TODO: WIP
            try:
                importer = ImportExport(args.filepath)
                self.config, games = importer.import_file(self.config, games)
                self.config.save()
                games.save()
            except:
                ...
                return

        self._setup(args)

        if args.show_systems:
            self._show_systems(games)
            return

        valid_systems = self._validate_systems(
            self._check_if_all_systems_selected(games, args.systems),
            self.config.data['systems'].keys(),
            diff_msg='The following systems were not found (will be skipped)',
            error_msg=(
                f'Please select from list of valid systems: '
                f'[orange1]{' '.join(self.config.data['systems'].keys())}[/orange1]\n'
                f'Or select all downloaded systems with [orange1]*[/orange1]'
            )
        )
        if args.download:
            self._scrape_games(games, valid_systems) # TODO: add will_reset

        else: # Roll game
            selected_systems = self._validate_systems(
                valid_systems.keys(),
                games.data.keys(),
                diff_msg='No games found for following systems (will be skipped)',
                error_msg=(
                    f'No games found. Try downloading gamelist for the following system/s: '
                    f'[orange1]{' '.join(valid_systems.keys())}[/orange1]'
                )
            )
            blacklist = Blacklist(self.config)
            vimm_roller = VimmRoller(games, self.config, blacklist, selected_systems)
            vimm_roller.roll()

        if args.export:
            # TODO: Handle export
            console.print(f'Exporting games data to {NotImplemented}')
            ...
