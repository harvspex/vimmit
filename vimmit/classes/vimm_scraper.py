from classes.data import Games, Config
from utils.cli import console
from bs4 import BeautifulSoup
from requests import Session
from rich.progress import Progress, TaskID
import math
import truststore
import posixpath
import urllib.parse
import time
import random

# TODO: Colour printing
# TODO: Extract region priority into config?

OTHER_REGION = 'Other'
REGION_PRIORITY = {
    'USA': 1,
    'Europe': 2,
    'Australia': 3,
    'Canada': 4,
    OTHER_REGION: 5
}

class VimmScraper:
    def __init__(self, config: Config):
        truststore.inject_into_ssl()
        self.session = Session()
        self.config = config
        self.base_url = self.config.data['base_url']

    @staticmethod
    def _format_system_name_and_id(sys_name: str, sys_vimm_id: str) -> str:
        if sys_name.replace(' ', '').lower() == sys_vimm_id.lower():
            return sys_name
        return f'{sys_name} ({sys_vimm_id})'

    def scrape_systems_dict(self) -> dict:
        console.print('Downloading systems list. Please wait...')
        truststore.inject_into_ssl()
        html = self.session.get(self.base_url).text
        soup = BeautifulSoup(html, 'html.parser')
        systems = {}
        for table in soup.find_all('table'):
            for tr in table.find_all('tr'):
                tr.find('td')
                link = tr.find('a')
                id = link['href'].split('/')[-1].strip()
                name = link.text.strip()
                systems[id.lower()] = {
                    'vimm_id': id,
                    'name': name,
                    'bl_id': self._format_system_name_and_id(name, id)
                }
        return systems

    def _join_url(self, endpoint: str) -> str:
        return urllib.parse.urljoin(self.base_url, endpoint)

    def _get_number_url(self, sys_vimm_id: str) -> str:
        return self._join_url(f'?p=list&system={sys_vimm_id}&section=number')

    def _get_letter_url(self, sys_vimm_id: str, letter: str) -> str:
        return self._join_url(posixpath.join(sys_vimm_id, letter))

    def _get_game_region_priority(self, game: dict) -> int:
        try:
            return REGION_PRIORITY[game['region']]
        except KeyError:
            return REGION_PRIORITY[OTHER_REGION]

    def _handle_region(self, games_list: list[dict], new_game: dict) -> dict:
        try:
            if not games_list[-1]['name'] == new_game['name']:
                return new_game
        except IndexError:
            return new_game

        games_by_region = {self._get_game_region_priority(game): game for game in (new_game, games_list.pop())}
        return games_by_region[ min( games_by_region.keys() ) ]

    def _scrape_page_for_games(self, url: str, games_dict: dict):
        html = self.session.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')
        games_list = []

        for tr in table.find_all('tr'):
            try:
                link = tr.find('a')
                id = int(link['href'].split('/')[-1])
                image = tr.find_all('img', class_='flag')
                region = image[0]['title'] if image else OTHER_REGION
                new_game = {
                    'id': id,
                    'name': link.text,
                    'region': region,
                }
                new_game = self._handle_region(games_list, new_game)
                games_list.append(new_game)

            except TypeError:
                continue

            except ValueError:
                continue

        for game in games_list:
            if game['id'] in games_dict:
                continue

            games_dict[game['id']] = {
                'name': game['name']
            }

    @staticmethod
    def _smooth_update(
        progress: Progress,
        task_id: TaskID,
        advance_amt: float,
        delay: float
    ):
        increments = math.ceil(delay*10)
        step = advance_amt/increments
        for _ in range(increments):
            time.sleep(delay/increments)
            progress.update(task_id, advance=step)

    # TODO: Disable test mode
    def _scrape_games_per_system(
        self,
        vimm_id: str,
        games: dict,
        progress: Progress,
        task_id: TaskID,
        base_delay: float=2,
        test_mode: bool=True
    ) -> dict:
        r = 2 if test_mode else 26
        amt = 1 / (r+1) * 100
        self._scrape_page_for_games(self._get_number_url(vimm_id), games)
        self._smooth_update(progress, task_id, amt, base_delay)

        for i in range(r):
            start = time.monotonic()
            letter = chr(i+65)
            url = self._get_letter_url(vimm_id, letter)
            self._scrape_page_for_games(url, games)
            elapsed = time.monotonic() - start
            delay = max(0, base_delay - elapsed) + random.uniform(0, 0.5)
            self._smooth_update(progress, task_id, amt, delay)

        progress.update(task_id, completed=100)
        return dict(sorted(games.items(), key=lambda x: x[1]['name']))

    def scrape_games(self, games: Games, selected_systems: dict, will_reset: bool=False) -> bool:
        with Progress(console=console) as progress:
            tasks = {}
            for sys_id, system in selected_systems.items():
                task_name = system['bl_id']
                tasks[sys_id] = progress.add_task(task_name, total=100)

            for sys_id, system in selected_systems.items():
                vimm_id = system['vimm_id']
                games_dict = {} if will_reset or sys_id not in games.data else games.data[sys_id]
                games_dict = self._scrape_games_per_system(
                    vimm_id,
                    games_dict,
                    progress,
                    tasks[sys_id]
                )
                games.data[sys_id] = games_dict
                games.save()
        console.print('All downloads complete!')
        return True
