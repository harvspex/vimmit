import argparse

def get_parser(systems: list) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Vimmit!'
    )
    parser.add_argument(
        'systems',
        help='system/s to roll games for',
        choices=systems,
        nargs='*'
        # TODO: support for all-system game rolls
    )
    parser.add_argument(
        '-s', '--scrape',
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
    return parser