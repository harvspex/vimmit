from typing import Callable

from app._delete import *
from app._get_args import get_args
from app._setup import setup
from app._systems import *
from common.console import console
from common.exceptions import *
from data.blacklist import Blacklist
from data.config import Config
from data.games import Games
from data.io.exporters import *
from data.io.importer import *
from data.io.io_utils import ExportModes
import services.vimm_roller as vimm_roller

# TODO: setup or way to install


def _handle_errors(func: Callable):
    def wrapper():
        try:
            func()
        except KeyboardInterrupt:
            console.print('Stopping Vimmit.')
            pass
        except (NoSystemsError, ImportExportError) as e:
            console.print(str(e))
        except ScrapeError:
            console.print(
                '[bold red]Download error.[/bold red][red] If the problem persists, try reseting '
                'url with --url, or redownloading systems list with --download-systems[/red]'
            )
    return wrapper


@_handle_errors
def vimmit():
    args = get_args()
    config = Config()
    games = Games()
    blacklist = Blacklist(config)

    import_arg = getattr(args, 'import')
    if import_arg:
        importer = Importer(args.filepath)
        importer.import_data(config, games, blacklist, import_arg)
        return

    if setup(config, args):
        return

    if args.export:
        match args.export:
            case ExportModes.DATA.value:
                exporter = DataExporter(args.filepath)
                exporter.export_data(config, games, blacklist)
            case ExportModes.HISTORY.value:
                exporter = HistoryExporter(args.filepath)
                exporter.export_history(config, games)
        return

    if args.show_systems:
        show_systems(config, games)
        return

    valid_systems = validate_systems(
        config,
        check_if_all_systems_selected(games, args.systems),
        config.data['systems'].keys(),
        diff_msg='The following systems were not found (will be skipped)',
        error_msg=(
            f'Please select from list of valid systems: '
            f'[orange1]{' '.join(config.data['systems'].keys())}[/orange1] '
            f'(or select all downloaded systems with [orange1]*[/orange1] )'
        )
    )
    if args.download:
        from services.vimm_scraper import VimmScraper # NOTE: lazy loading
        scraper = VimmScraper(config)
        scraper.scrape_games(games, valid_systems)
        return

    selected_systems = validate_systems(
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

    vimm_roller.roll(games, config, blacklist, selected_systems)