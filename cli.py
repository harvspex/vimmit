import argparse

DEFAULT_FILEPATH=''


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='lexiconizer: count words and find neighbours'
    )
    parser.add_argument(
        'system',
        help='system for which to roll games',
        choices=['ps1', 'n64'],
        # nargs='*' # TODO: support for multi-system game rolls
    )
    parser.add_argument(
        '-f', '--filepath',
        help='filepath for game data',
        default=DEFAULT_FILEPATH,
        const=DEFAULT_FILEPATH,
        nargs='?'
    )
    # parser.add_argument(
    #     '-b', '--blacklist',
    #     help='',
    #     action='store_true'
    # )
    # parser.add_argument(
    #     '-c', '--crawl',
    #     help='',
    #     action='store_true'
    # )
    # parser.add_argument(
    #     '-r', '--reset',
    #     help='',
    #     action='store_true'
    # )

    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    ...