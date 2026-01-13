from pathlib import Path
import pandas as pd


def _init_blacklist(blacklist_path: Path) -> set:
    with open(blacklist_path, 'r') as f:
        return set([_.lower().strip() for _ in f.readlines() if _])


def _get_non_blacklist_game(games: pd.DataFrame, blacklist: set) -> pd.DataFrame:
    # TODO: This can result in an infinite loop
    # Better approach:
    # - Hash blacklist file
    # - If hash different from last time, recheck database, and flag blacklisted games
    # - Sample game from updated database

    seeking = True
    while seeking:
        game = games.sample()
        title = game.iloc[0][1].lower()

        for substring in blacklist:
            print(f'{substring} in {title}: {substring in title}')

            if substring in title:
                print('substring in title')
                break
            
            seeking = False

    return game


def roll_game(games_path: Path, blacklist_path: Path):
    blacklist = _init_blacklist(blacklist_path)
    games = pd.read_csv(games_path, header=None)
    game = _get_non_blacklist_game(games, blacklist)
    print(game)


roll_game('psx_a.csv', 'blacklist.txt')