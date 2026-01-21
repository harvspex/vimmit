from data.config import Config
from data.games import Games
from common.console import console
from common.exceptions import NoSystemsError


def check_if_all_systems_selected(games: Games, systems: list) -> list:
    systems = set(systems)
    try:
        systems.remove('*')
        systems.update(games.data.keys())
    except KeyError:
        pass
    return list(systems)


def show_systems(config: Config, games: Games):
    from rich.columns import Columns # NOTE: lazy loading
    # TODO (maybe): Force equal number of columns for both
    format_name = lambda sys_id, colour: (
        f'[{colour}]{sys_id}[/{colour}] ({config.data['systems'][sys_id]['name']})'
    )
    get_columns = lambda systems, colour: Columns(
        [format_name(_, colour) for _ in systems], column_first=True, equal=True, expand=True
    )
    print_columns = lambda systems, title, colour: (
        console.print(f'[bold {colour}]{title}[/bold {colour}]'),
        console.print(get_columns(systems, colour))
    )
    downloaded = list(games.data.keys())
    available = [_ for _ in config.data['systems'].keys() if _ not in downloaded]
    print_columns(downloaded, 'Downloaded systems:', 'green')
    console.print()
    print_columns(available, 'Available systems:','bright_cyan')


def validate_systems(
    config: Config,
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
    return {k: v for k, v in config.data['systems'].items() if k in intersect}