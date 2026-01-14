from src.vimm_roller import VimmRoller
from pathlib import Path
from urllib.parse import urlparse, urlunparse
import src.utils.save_load as save_load
import argparse

SYSTEMS = {
    "Atari2600",
    "Atari5200",
    "NES",
    "SMS",
    "Atari7800",
    "TG16",
    "Genesis",
    "TGCD",
    "SNES",
    "CDi",
    "SegaCD",
    "Jaguar",
    "32X",
    "Saturn",
    "JaguarCD",
    "N64",
    "Dreamcast",
    "PS2",
    "GameCube",
    "Xbox",
    "Xbox360",
    "X360-D",
    "PS3",
    "Wii",
    "WiiWare",
    "GB",
    "Lynx",
    "GG",
    "VB",
    "GBC",
    "GBA",
    "DS",
    "PSP",
    "3DS",
}

def _get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='' # TODO
    )
    parser.add_argument(
        'systems',
        help='system/s to roll games for',
        choices=['ps1', 'n64'],
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
        # TODO: -r without -c should clear seen and blacklist
    )
    return parser


class Vimmit:
    def __init__(self, args: argparse.Namespace):
        cwd = Path.cwd()
        self.games_path = cwd / 'games.dat'
        self.config_path = cwd / 'config.dat'
        self.config = save_load.load_config(self.config_path)
        self.args = args

    def run(self):
        if self.args.crawl:
            from requests import ConnectionError
            try:
                self._handle_crawl()
            except (AttributeError, ConnectionError):
                print('That didn\'t work. Resetting base url.') # TODO: Better message
                self.config['base_url'] = None
                save_load.dump_pickle(self.config, self.config_path)
                return

        systems = {_.upper() for _ in self.args.systems}
        vimm_roller = VimmRoller(systems, self.games_path)
        vimm_roller.roll()

    @staticmethod
    def __validate_url(user_input: str, default_scheme='https') -> str:
        parsed = urlparse(user_input)

        if not parsed.scheme:
            parsed = urlparse(f"{default_scheme}://{user_input}")

        if not parsed.netloc:
            return None

        parsed = parsed._replace(path='/vault/')
        return urlunparse(parsed)

    def __handle_setup(self) -> dict:
        print('Please enter base url (hint: vimm dot net):')
        while True:
            user_input = input('>> ').strip()
            base_url = Vimmit.__validate_url(user_input)
            if not base_url:
                print('Please enter valid url:')
                continue

            self.config['base_url'] = base_url
            save_load.dump_pickle(self.config, self.config_path)
            break

    def _handle_crawl(self):
        from vimm_crawler import VimmCrawler
        from requests import Session
        import truststore

        if not self.config.get('base_url', False):
            self.__handle_setup()

        truststore.inject_into_ssl()
        session = Session()

        for system in self.args.systems:
            vimm_crawler = VimmCrawler(
                session,
                self.config['base_url'],
                system,
                self.games_path,
                self.args.reset,
                test_mode=True # TODO: Disable test mode
            )
            vimm_crawler.run()


def main():
    parser = _get_parser()
    args = parser.parse_args()
    vimmit = Vimmit(args)
    vimmit.run()


if __name__ == '__main__':
    main()
