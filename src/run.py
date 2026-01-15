from data import Config, Games
from vimmit import Vimmit
from utils.cli import get_parser

def main():
    games = Games()
    config = Config()
    systems = list(config.data['systems'].keys())
    parser = get_parser(systems)
    args = parser.parse_args()
    vimmit = Vimmit(games, config, args)
    vimmit.run()


if __name__ == '__main__':
    main()
