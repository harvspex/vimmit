import argparse
from rich.console import Console

console = Console() # TODO: Use

# TODO: Add and implement options
# - Support for all (downloaded) system game rolls with `*` arg
# - Re-scrape systems
# - Import/export from file. Existing data wins conflicts
# - Mode to roll games per game rather than per system?
# - Reset config (or at least base url)
# - Add flag to show list of systems (scrapes if necessary, no roll)
# - delay time (between requests)

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Vimmit! ✌️🤮 "The Retro Game Randomiser"'
    )
    parser.add_argument(
        'systems',
        help='system/s to roll games for (separated by spaces)',
        nargs='*'
    )
    parser.add_argument(
        '-d', '--download',
        help='download gamelists for selected systems',
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
        '-ds', '--download-systems',
        help='re-download list of systems',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '-u', '--url',
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
