from vimm_roller import VimmRoller
from pathlib import Path
import utils
import argparse

def _get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='' # TODO
    )
    parser.add_argument(
        'systems',
        help='system/s to roll games for',
        nargs='*'
        # TODO: support for all-system game rolls
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


def __handle_setup(config: dict) -> dict:
    from urllib.parse import urlparse

    print('First time setup: please enter base url:')
    while True:
        base_url = input('>> ')
        parsed_url = urlparse(base_url)
        if not parsed_url.scheme or not parsed_url.netloc:
            print('Please enter valid url:')
            continue

        config['base_url'] = base_url
        return config


def _handle_crawl(args, games_path: Path, config_path: Path):
    from vimm_crawler import VimmCrawler
    from requests import Session
    import truststore

    config = utils.load_config(config_path)
    if not config.get('base_url', False):
        config = __handle_setup(config)

    truststore.inject_into_ssl()
    session = Session()
    
    for system in args.systems:
        vimm_crawler = VimmCrawler(
            session,
            config['base_url'],
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
    config_path = cwd / 'config.dat'
    games_path = cwd / 'games.dat'
    args.systems = {_.upper() for _ in args.systems}

    if args.crawl:
        _handle_crawl(args, games_path, config_path)

    vimm_roller = VimmRoller(args.systems, games_path)
    vimm_roller.roll()


if __name__ == '__main__':
    main()
