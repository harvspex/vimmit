from data_objects import Games, Config
from utils.format import format_system_name_and_id
from bs4 import BeautifulSoup
from requests import Session
import truststore
import posixpath
import urllib.parse

# TODO: Make async
# TODO: Loading percentage based on letter position
# TODO: Colour logging?
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

    def scrape_systems_dict(self) -> dict:
        print('Downloading systems list. Please wait...')
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
                    'bl_id': format_system_name_and_id(name, id)
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

    def _scrape_games_per_system(self, sys_vimm_id: str, games: dict, test_mode: bool=True) -> dict:
        # TODO: Disable test mode
        self._scrape_page_for_games(self._get_number_url(sys_vimm_id), games)
        r = 0 if test_mode else 26
        for i in range(r):
            letter = chr(i+65)
            self._scrape_page_for_games(self._get_letter_url(sys_vimm_id, letter), games)

        return dict(sorted(games.items(), key=lambda x: x[1]['name']))

    def scrape_games(self, games: Games, selected_systems: dict, will_reset: bool=False) -> bool:
        # TODO: Not resetting seen flag
        for sys_id, system in selected_systems.items():
            vimm_id, sys_name = system['vimm_id'], system['name']
            # TODO: why does this print sys_id in lower case?
            print(f'Downloading games list for {format_system_name_and_id(sys_name, sys_id)}. Please wait...')
            games_dict = {} if will_reset or sys_id not in games.data else games.data[sys_id]
            games_dict = self._scrape_games_per_system(vimm_id, games_dict)
            games.data[sys_id] = games_dict
            games.save()
        print('All system downloads complete!')
        return True
