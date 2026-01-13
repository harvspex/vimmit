from bs4 import BeautifulSoup
from pathlib import Path
from requests import Session
import pandas as pd
import posixpath
import urllib.parse

class VimmCrawler:
    def __init__(
        self,
        session: Session,
        base_url: str,
        system: str,
        test_mode: bool=False
    ):
        self.session = session
        self.base_url = base_url
        self.system = system.upper()
        self.test_mode = test_mode

    def _join_url(self, endpoint: str):
        return urllib.parse.urljoin(self.base_url, endpoint)

    def _get_number_url(self):
        return self._join_url(f'?p=list&system={self.system}&section=number')

    def _get_letter_url(self, letter: str):
        return self._join_url(posixpath.join(self.system, letter))

    def _get_games(self, url: str) -> pd.DataFrame:
        html = self.session.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')
        rows = []

        for tr in table.find_all('tr'):
            try:
                link = tr.find('a')
                if link is None:
                    continue

                image = tr.find_all('img', class_='flag')
                image = image[0] if image else None
                rows.append((link.text, link['href'], image['title']))

            except TypeError:
                continue

        return self._format_rows(rows)

    @staticmethod
    def _format_rows(games: list):
        df = pd.DataFrame(games)
        # TODO: add bias based on string similarity
        # remove redundant copies of game (e.g. non-US version)
        return df

    def _crawl(self):
        games = pd.DataFrame()
        begins_with_number = self._get_games(self._get_number_url())
        games = pd.concat((games, begins_with_number))

        r = 1 if self.test_mode else 26
        for i in range(r):
            begins_with_letter = self._get_games(self._get_letter_url(chr(i+65)))
            games = pd.concat((games, begins_with_letter))

        return games.reset_index(drop=True)

    @staticmethod
    def _dump(filepath: Path, df: pd.DataFrame):
        with open(filepath, 'w', newline='') as f:
            df.to_csv(f, header=False)

    def run(self, filepath: Path):
        games = self._crawl()
        self._dump(filepath, games)
