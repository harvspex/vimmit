from classes.data import Config
from classes.vimmit import Vimmit
from utils.cli import get_parser


def main():
    config = Config()
    systems = list(config.data['systems'].keys())
    parser = get_parser(systems)
    args = parser.parse_args()
    vimmit = Vimmit(config, args)
    vimmit.run()


if __name__ == '__main__':
    main()
