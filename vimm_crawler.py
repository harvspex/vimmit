from bs4 import BeautifulSoup
from dataclasses import dataclass
from pathlib import Path
from requests import Session
import pandas as pd
import posixpath
import urllib.parse

@dataclass
class VimmCrawler:
    session: Session
    base_url: str
    system: str
    filepath: Path
    will_reset: bool=False
    test_mode: bool=False

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
                image = tr.find_all('img', class_='flag')
                image = image[0] if image else None
                id = int(link['href'].split('/')[-1])
                rows.append((id, link.text, image['title'], 0, 0))

            except TypeError:
                continue

            except ValueError:
                continue

        return pd.DataFrame(rows)

    def _format(self, games: list):
        # TODO: add bias based on string similarity
        # remove redundant copies of game (e.g. non-US version)
        df = pd.DataFrame(games)

        if not self.will_reset:
            old_df = pd.read_csv(self.filepath, header=None)
            df = (
                pd.concat([old_df, df], ignore_index=True)
                .drop_duplicates(subset=[0], keep="first")
            )

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

    def _dump(self, df: pd.DataFrame):
        print(len(df))
        with open(self.filepath, 'w', newline='') as f:
            df.to_csv(f, index=False, header=False)

    def run(self):
        games = self._crawl()
        games = self._format(games)
        self._dump(games)
