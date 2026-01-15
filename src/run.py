from vimmit import Vimmit
from utils.setup import handle_setup
from utils.cli import get_parser
import utils.save_load as save_load
from pathlib import Path

def main():
    data_dir = Path.cwd() / '.data'
    games_path = data_dir / 'games.dat'
    config_path = data_dir / 'config.dat'
    config = save_load.load_config(config_path)

    handle_setup(config)
    save_load.dump_pickle(config, config_path)

    systems = list(config['systems'].keys())
    parser = get_parser(systems)
    args = parser.parse_args()

    vimmit = Vimmit(games_path, config_path, args)
    vimmit.run()


if __name__ == '__main__':
    main()
