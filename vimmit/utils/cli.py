import argparse

from rich.console import Console

console = Console(highlight=False)

# TODO (maybe): Add and implement
# - Delay time (between requests)
# - Mode to roll games per game rather than per system?

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Vimmit! ✌️🤮 "The Retro Game Randomiser"'
    )
    parser.add_argument(
        'systems',
        help='system/s to roll games for (separated by spaces), or * to select all available systems',
        nargs='*'
    )
    parser.add_argument(
        '-d', '--download',
        help='download gamelists for selected systems',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '-s', '--show-systems', '--systems',
        help='show list of downloaded and available systems',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '-i', '--import',
        help=(
            f'[games] (default): import systems and gamelists'
            f'. [seen]: import games plus seen data (seen games won\'t be rolled)'
            f'. [blacklist]: import blacklist data'
            f'. [all]: import all'
        ),
        nargs='?',
        choices=['games', 'all'], # TODO add: 'seen', 'blacklist',
        const='games',
        default=None
    )
    parser.add_argument(
        '-e', '--export',
        help=(
            f'[data] (default): export system, game and blacklist data'
            f'. [history]: export list of seen games '
        ),
        nargs='?',
        choices=['data', 'history'],
        const='data',
        default=None
    )
    parser.add_argument(
        '-f', '--filepath',
        # TODO: Update default filepath
        help='optional: filepath for import/export (default: current_folder/vimmit.vmt)',
        nargs='?',
        const=None,
        default=None
    )
    parser.add_argument(
        '--clear-seen',
        help='clear seen data for selected systems (games can be rerolled)',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '--delete',
        help='delete gamelist for selected systems',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '--download-systems',
        help='redownload list of systems',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '--url',
        help='reset base url',
        action='store_true',
        default=False
    )
    return parser.parse_args()
