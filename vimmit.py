from vimm_roller import VimmRoller
from pathlib import Path
import argparse

SYSTEMS = {'ps1', 'n64'}

def _get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='' # TODO
    )
    parser.add_argument(
        'systems',
        help='system/s to roll games for',
        choices=SYSTEMS,
        nargs='*' # TODO: support for all-system game rolls
    )
    parser.add_argument(
        '-c', '--crawl',
        help='',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '-r', '--reset',
        help='',
        action='store_true',
        default=False
    )
    return parser


def _handle_crawl(args, games_path: Path):
    from vimm_crawler import VimmCrawler
    from requests import Session
    import truststore

    truststore.inject_into_ssl()
    session = Session()
    base_url = '' # TODO
    
    for system in args.systems:
        vimm_crawler = VimmCrawler(
            session,
            base_url,
            system,
            games_path,
            args.reset,
            test_mode=True # TODO: Disable test mode
        )
        vimm_crawler.run()


def main():
    parser = _get_parser()
    args = parser.parse_args()
    cwd = Path.cwd()
    games_path = cwd / 'games.dat'
    config_path = cwd / 'config.dat'
    args.systems = {_.upper() for _ in args.systems}

    if args.crawl:
        _handle_crawl(args, games_path)

    vimm_roller = VimmRoller(args.systems, games_path)
    vimm_roller.roll()


if __name__ == '__main__':
    main()
