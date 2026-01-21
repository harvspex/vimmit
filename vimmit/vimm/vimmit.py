from typing import Callable

from data.blacklist import Blacklist
from data.config import Config
from data.games import Games
from utils.cli import console, get_args
from exceptions import NoSystemsError, ScrapeError
import utils.systems as systems
from utils.setup import setup
from vimm.vimm_roller import VimmRoller
from vimm.vimm_scraper import VimmScraper
from utils.delete import *

# TODO: setup or way to install


def handle_errors(func: Callable):
    def wrapper():
        try:
            func()
        except NoSystemsError as e:
            console.print(str(e))
        except ScrapeError:
            console.print(
                '[bold red]Download error.[/bold red][red] If the problem persists, try reseting url '
                'with --url, or redownload systems with --download-systems[/red]'
            )
        except KeyboardInterrupt:
            console.print('Stopping Vimmit.')
            pass
        except:
            # TODO:
            ...
            raise
    return wrapper


@handle_errors
def vimmit():
    args = get_args()
    config = Config()
    games = Games()
    blacklist = Blacklist(config)

    if getattr(args, 'import'):
        from data.importer import Importer
        # TODO: Import WIP
        try:
            importer = Importer(args.filepath)
            importer.import_file(config, games, blacklist)
            console.print('Imported file')
        except:
            raise
            ...
            return
        return

    if setup(config, args):
        return

    if args.show_systems:
        systems.show_systems(config, games)
        return

    if args.export:
        from data.exporter import Exporter
        # TODO: Export WIP
        try:
            exporter = Exporter(args.filepath)
            exporter.export_file(config, games, blacklist)
            console.print('Exported file')
        except:
            raise
            ...
            return
        return

    valid_systems = systems.validate_systems(
        config,
        systems.check_if_all_systems_selected(games, args.systems),
        config.data['systems'].keys(),
        diff_msg='The following systems were not found (will be skipped)',
        error_msg=(
            f'Please select from list of valid systems: '
            f'[orange1]{' '.join(config.data['systems'].keys())}[/orange1] '
            f'(or select all downloaded systems with [orange1]*[/orange1] )'
        )
    )
    if args.download:
        scraper = VimmScraper(config)
        scraper.scrape_games(games, valid_systems)
        return

    selected_systems = systems.validate_systems(
        config,
        valid_systems.keys(),
        games.data.keys(),
        diff_msg='No games found for following systems (will be skipped)',
        error_msg=(
            f'No games found. Try downloading gamelist for the following system/s: '
            f'[orange1]{' '.join(valid_systems.keys())}[/orange1]'
        )
    )
    if args.clear_seen:
        print_system_list_warning('clear seen data', selected_systems)
        clear_seen_games(games, selected_systems)
        return

    if args.delete:
        print_system_list_warning('delete gamelists', selected_systems)
        delete_games(games, selected_systems)
        return

    # Roll game
    vimm_roller = VimmRoller(games, config, blacklist, selected_systems)
    vimm_roller.roll()