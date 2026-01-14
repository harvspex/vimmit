import utils
from bs4 import BeautifulSoup
from pathlib import Path
from requests import Session
import posixpath
import urllib.parse

OTHER_REGION = 'Other'
REGION_PRIORITY = {
    'USA': 1,
    'Europe': 2,
    'Australia': 3,
    'Canada': 4,
    OTHER_REGION: 5
}

class VimmCrawler:
    def __init__(
        self,
        session: Session,
        base_url: str,
        system: str,
        filepath: Path,
        will_reset: bool=False,
        test_mode: bool=False
    ):
        self.session = session
        self.base_url = base_url
        self.system = system.upper()
        self.filepath = filepath
        self.will_reset = will_reset
        self.test_mode = test_mode

    def __join_url(self, endpoint: str):
        return urllib.parse.urljoin(self.base_url, endpoint)

    def __get_number_url(self):
        return self.__join_url(f'?p=list&system={self.system}&section=number')

    def __get_letter_url(self, letter: str):
        return self.__join_url(posixpath.join(self.system, letter))

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

    def __get_games(self, url: str, games_dict: dict) -> None: # NOTE: Inplace
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

    def _crawl(self, games: dict) -> dict:
        self.__get_games(self.__get_number_url(), games)
        r = 1 if self.test_mode else 26
        for i in range(r):
            letter = chr(i+65)
            self.__get_games(self.__get_letter_url(letter), games)

        return dict(sorted(games.items(), key=lambda x: x[1]['name']))

    def run(self):
        collection = utils.load_collection(self.filepath)
        games = {} if self.will_reset or self.system not in collection else collection[self.system]
        games = self._crawl(games)
        collection[self.system] = games
        utils.dump_pickle(collection, self.filepath)
