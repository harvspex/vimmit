from typing import Callable

from data.config import Config
from common.console import console


def get_input(msg: str, retry_msg: str, validator: Callable, *args, **kwargs) -> str:
    console.print(msg)
    while True:
        user_input = console.input('>> ').strip()
        user_input = validator(user_input, *args, **kwargs)
        if not user_input:
            console.print(retry_msg)
            continue
        return user_input


def _validate_url(user_input: str, default_scheme='https') -> str:
    from urllib.parse import urlparse, urlunparse # NOTE: lazy loading
    parsed = urlparse(user_input)
    if not parsed.scheme:
        parsed = urlparse(f"{default_scheme}://{user_input}")
    if not parsed.netloc:
        return None
    parsed = parsed._replace(path='/vault/')
    return urlunparse(parsed)


def _input_base_url() -> str:
    return get_input(
        'Please enter base url (hint: vimm dot net):',
        'Please enter valid url:',
        _validate_url
    )


def _scrape_systems(config: Config) -> dict:
    from services.vimm_scraper import VimmScraper # NOTE: lazy loading
    scraper = VimmScraper(config)
    return scraper.scrape_systems_dict()


def setup(config: Config, args) -> bool:
    results = (
        config.update('base_url', args.url, _input_base_url),
        config.update('systems', args.download_systems, _scrape_systems, config)
    )
    did_update_config = True in results
    if did_update_config:
        config.save()
    return did_update_config