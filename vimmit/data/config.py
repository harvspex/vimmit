from argparse import Namespace

from data.base_data import BaseData, DATA_DIR
from utils.cli import console
from vimm.vimm_scraper import VimmScraper


class Config(BaseData):
    def __init__(self):
        super().__init__(DATA_DIR, 'config.dat')

    @staticmethod
    def _validate_url(user_input: str, default_scheme='https') -> str:
        from urllib.parse import urlparse, urlunparse
        parsed = urlparse(user_input)
        if not parsed.scheme:
            parsed = urlparse(f"{default_scheme}://{user_input}")
        if not parsed.netloc:
            return None
        parsed = parsed._replace(path='/vault/')
        return urlunparse(parsed)

    @staticmethod
    def _input_base_url() -> str:
        console.print('Please enter base url (hint: vimm dot net):')
        while True:
            user_input = console.input('>> ').strip()
            base_url = Config._validate_url(user_input)
            if not base_url:
                console.print('Please enter valid url:')
                continue
            return base_url

    def _scrape_systems_list(self) -> dict:
        scraper = VimmScraper(self)
        return scraper.scrape_systems_dict()

    def setup(self, args: Namespace) -> bool:
        results = (
            self.update('base_url', self._input_base_url, args.url),
            self.update('systems', self._scrape_systems_list, args.download_systems)
        )
        did_update_config = True in results
        if did_update_config:
            self.save()
        return did_update_config