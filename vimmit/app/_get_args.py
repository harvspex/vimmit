import argparse

from data.io.io_utils import ImportModes, ExportModes

# TODO: Add and implement
# - Delay time (between requests)
# - Mode to roll games per combined system gameslists, rather than per system


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Vimmit! ✌️🤮 "The Retro Game Randomiser"'
    )
    parser.add_argument(
        'systems',
        help='system/s to roll games for (separated by spaces), or * to select all available systems',
        nargs='*'
    )
    parser.add_argument(
        '-d', '--download',
        help='download gamelists for selected systems',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '-s', '--show-systems', '--systems',
        help='show list of downloaded and available systems',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '-i', '--import',
        help=(
            f'[{ImportModes.GAMES.value}] (default): import systems and gamelists. '
            f'[{ImportModes.SEEN.value}]: import games plus seen data (seen games won\'t be rolled). '
            f'[{ImportModes.BLACKLIST.value}]: import blacklist data. '
            f'[{ImportModes.ALL.value}]: import all'
        ),
        nargs='?',
        choices=[_.value for _  in ImportModes],
        const=ImportModes.GAMES.value,
        default=None
    )
    parser.add_argument(
        '-e', '--export',
        help=(
            f'[{ExportModes.DATA.value}] (default): export system, game and blacklist data. '
            f'[{ExportModes.HISTORY.value}]: export list of seen games '
        ),
        nargs='?',
        choices=[_.value for _  in ExportModes],
        const=ExportModes.DATA.value,
        default=None
    )
    parser.add_argument(
        '-f', '--filepath',
        help='optional: filepath for import/export (default: ./vimmit.vmt)',
        nargs='?',
        const=None,
        default=None
    )
    parser.add_argument(
        '--clear-seen',
        help='clear seen data for selected systems (games can be rerolled)',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '--delete',
        help='delete gamelist for selected systems',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '--download-systems',
        help='redownload list of systems',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '--url',
        help='reset base url',
        action='store_true',
        default=False
    )
    return parser.parse_args()