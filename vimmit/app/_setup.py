from data.config import Config
from common.console import console


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
    console.print('Please enter base url (hint: vimm dot net):')
    while True:
        user_input = console.input('>> ').strip()
        base_url = _validate_url(user_input)
        if not base_url:
            console.print('Please enter valid url:')
            continue
        return base_url


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