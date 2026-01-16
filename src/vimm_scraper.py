from data_objects import Games, Config
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

    @staticmethod
    def __get_blacklist_name(id: str, name: str):
        if name.replace(' ', '').lower() == id.lower():
            return name
        return f'{name} ({id})'

    def scrape_systems_list(self) -> dict:
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
                    'id': id,
                    'name': name,
                    'bl_id': self.__get_blacklist_name(id, name)
                }
        self.config.data['systems'] = systems
        self.config.save()

    def __join_url(self, endpoint: str):
        return urllib.parse.urljoin(self.base_url, endpoint)

    def __get_number_url(self, sys_id: str):
        return self.__join_url(f'?p=list&system={sys_id}&section=number')

    def __get_letter_url(self, sys_id: str, letter: str):
        return self.__join_url(posixpath.join(sys_id, letter))

    def __get_game_region_priority(self, game: dict) -> int:
        try:
            return REGION_PRIORITY[game['region']]
        except KeyError:
            return REGION_PRIORITY[OTHER_REGION]

    def __handle_region(self, games_list: list[dict], new_game: dict) -> dict:
        try:
            if not games_list[-1]['name'] == new_game['name']:
                return new_game
        except IndexError:
            return new_game

        games_by_region = {self.__get_game_region_priority(game): game for game in (new_game, games_list.pop())}
        return games_by_region[ min( games_by_region.keys() ) ]

    def __scrape_page_for_games(self, url: str, games_dict: dict) -> None: # NOTE: Inplace
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
                new_game = self.__handle_region(games_list, new_game)
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

    def __scrape_games_per_system(self, sys_id: str, games: dict, test_mode: bool=True) -> dict: # TODO: Disable test mode
        self.__scrape_page_for_games(self.__get_number_url(sys_id), games)
        r = 0 if test_mode else 26
        for i in range(r):
            letter = chr(i+65)
            self.__scrape_page_for_games(self.__get_letter_url(sys_id, letter), games)

        return dict(sorted(games.items(), key=lambda x: x[1]['name']))

    def scrape_games(
        self,
        games: Games,
        selected_systems: list[tuple],
        will_reset: bool=False
    ):
        for sys_id, sys_name in selected_systems:
            print(f'Downloading games list for {sys_name} ({sys_id}). Please wait...')
            games_dict = {} if will_reset or sys_id not in games.data else games.data[sys_id]
            games_dict = self.__scrape_games_per_system(sys_id, games_dict)
            games.data[sys_id] = games_dict
            games.save()
        print('All systems complete!')
