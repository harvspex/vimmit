from typing import Callable

from rich.columns import Columns

from data.blacklist import Blacklist
from data.config import Config
from data.games import Games
from data.import_export import ImportExport
from utils.cli import console, get_args
from utils.exceptions import NoSystemsError
from utils.setup import input_base_url
from vimmit.vimm_roller import VimmRoller
from vimmit.vimm_scraper import VimmScraper


class Vimmit:
    def __init__(self):
        self.config = Config()

    def _scrape_systems_list(self) -> dict:
        scraper = VimmScraper(self.config)
        return scraper.scrape_systems_dict()

    def _setup(self, args) -> bool:
        results = (
            self.config.update('base_url', input_base_url, args.url),
            self.config.update('systems', self._scrape_systems_list, args.download_systems)
        )
        if True in results:
            blacklist = Blacklist(self.config)
            self.config.save()
            return True
        return False

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
        # TODO (maybe): Force equal number of columns for both
        format_name = lambda sys_id, colour: (
            f'[{colour}]{sys_id}[/{colour}] ({self.config.data['systems'][sys_id]['name']})'
        )
        get_columns = lambda systems, colour: Columns(
            [format_name(_, colour) for _ in systems], column_first=True, equal=True, expand=True
        )
        print_columns = lambda systems, title, colour: (
            console.print(f'[bold {colour}]{title}[/bold {colour}]'),
            console.print(get_columns(systems, colour))
        )
        downloaded = list(games.data.keys())
        available = [_ for _ in self.config.data['systems'].keys() if _ not in downloaded]
        print_columns(downloaded, 'Downloaded systems:', 'green')
        console.print()
        print_columns(available, 'Available systems:','bright_cyan')

    @staticmethod
    def _delete_wrapper(games: Games, func: Callable, systems: list, message: str):
        console.print(
            f'[bold red]WARNING: [/bold red][red]{message}[/red][orange1]'
            f'{' '.join(systems)}[/orange1]'
        )
        console.print(f'Enter "delete" to confirm, or anything else to cancel:')
        user_input = console.input('>> ')
        if not user_input.strip().lower() == 'delete':
            return
        func(systems)
        games.save()

    def run(self):
        args = get_args()
        games = Games()

        if self._setup(args):
            return

        if args.show_systems:
            self._show_systems(games)
            return

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
            return

        if args.export:
            # TODO: Handle export
            ...
            return

        valid_systems = self._validate_systems(
            self._check_if_all_systems_selected(games, args.systems),
            self.config.data['systems'].keys(),
            diff_msg='The following systems were not found (will be skipped)',
            error_msg=(
                f'Please select from list of valid systems: '
                f'[orange1]{' '.join(self.config.data['systems'].keys())}[/orange1] '
                f'(or select all downloaded systems with [orange1]*[/orange1] )'
            )
        )
        if args.download:
            scraper = VimmScraper(self.config)
            scraper.scrape_games(games, valid_systems) # TODO: add will_reset
            return

        selected_systems = self._validate_systems(
            valid_systems.keys(),
            games.data.keys(),
            diff_msg='No games found for following systems (will be skipped)',
            error_msg=(
                f'No games found. Try downloading gamelist for the following system/s: '
                f'[orange1]{' '.join(valid_systems.keys())}[/orange1]'
            )
        )

        if args.clear_seen:
            self._delete_wrapper(
                games,
                games.clear_seen,
                selected_systems.keys(),
                'You are about to clear seen data for the following system/s: '
            )
            return

        if args.delete:
            self._delete_wrapper(
                games,
                games.clear,
                selected_systems.keys(),
                'You are about to delete gamelists for the following system/s: ',
            )
            return

        # Roll game
        blacklist = Blacklist(self.config)
        vimm_roller = VimmRoller(games, self.config, blacklist, selected_systems)
        vimm_roller.roll()