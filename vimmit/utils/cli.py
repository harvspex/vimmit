import argparse
from rich.console import Console

console = Console() # TODO: Use

# TODO: Add/Implement
# - Flag to clear seen for selected systems
# - Flag to delete selected systems
#
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
        help='games (default): import gamelists, all: import gamelists and seen data',
        nargs='?',
        choices=['games', 'all'],
        const='games',
        default=None
    )
    parser.add_argument(
        '-e', '--export',
        help='games (default): export gamelists, all: export gamelists and seen data, history: export list of seen games',
        nargs='?',
        choices=['games', 'all', 'history'],
        const='games',
        default=None
    )
    parser.add_argument(
        '-f', '--filepath',
        help='optional: filepath for import/export (default is current folder)',
        nargs='?',
        const=None, # TODO: Path.cwd() ?
        default=None
    )
    parser.add_argument(
        '--download-systems',
        help='re-download list of systems',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '--url',
        help='reset base url',
        action='store_true',
        default=False
    )
    # parser.add_argument(
    #     '-r', '--reset',
    #     help='',
    #     action='store_true',
    #     default=False
    #     # TODO: Implement
    #     # -r without -d should clear seen
    # )
    return parser.parse_args()
