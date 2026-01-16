from data_objects import Config
from vimmit import Vimmit
from cli import get_parser


def main():
    config = Config()
    systems = list(config.data['systems'].keys())
    parser = get_parser(systems)
    args = parser.parse_args()
    vimmit = Vimmit(config, args)
    vimmit.run()


if __name__ == '__main__':
    main()
