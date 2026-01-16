import argparse

# TODO: Add and implement options
# - Support for all (downloaded) system game rolls with `*` arg
# - Re-scrape systems
# - Import/export from file. Existing data wins conflicts
# - Mode to roll games per game rather than per system?
# - Reset config (or at least base url)

def get_parser(systems: list) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Vimmit!'
    )
    parser.add_argument(
        'systems',
        help='system/s to roll games for',
        choices=systems,
        nargs='*'
    )
    parser.add_argument(
        '-d', '--download',
        help='',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '-e', '--export',
        help='',
        action='store_true',
        default=False
        # TODO: Accept filepath as arg
        # default=None,
        # nargs='?'
    )
    parser.add_argument(
        '-ss', '--scrape-systems',
        help='',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '-r', '--reset',
        help='',
        action='store_true',
        default=False
        # TODO: -r without -c should clear seen and blacklist
    )
    parser.add_argument(
        '-u', '--url',
        help='',
        action='store_true',
        default=False
    )
    return parser