from data.config import Config
from utils.cli import console
from vimm.vimm_scraper import VimmScraper
from argparse import Namespace


def _validate_url(user_input: str, default_scheme='https') -> str:
    from urllib.parse import urlparse, urlunparse

    parsed = urlparse(user_input)

    if not parsed.scheme:
        parsed = urlparse(f"{default_scheme}://{user_input}")

    if not parsed.netloc:
        return None

    parsed = parsed._replace(path='/vault/')
    return urlunparse(parsed)


def input_base_url() -> str:
    console.print('Please enter base url (hint: vimm dot net):')
    while True:
        user_input = console.input('>> ').strip()
        base_url = _validate_url(user_input)
        if not base_url:
            console.print('Please enter valid url:')
            continue

        return base_url


def _scrape_systems_list(config: Config) -> dict:
    scraper = VimmScraper(config)
    return scraper.scrape_systems_dict()


def setup(config: Config, args: Namespace) -> bool:
    results = (
        config.update('base_url', input_base_url, args.url),
        config.update('systems', _scrape_systems_list, args.download_systems)
    )
    did_update_config = True in results
    if did_update_config:
        config.save()
    return did_update_config