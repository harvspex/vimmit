from vimmit import Vimmit
from exceptions import *


def main():
    vimmit = Vimmit()
    try:
        vimmit.run()
    except NoSystemsError as e:
        print(e)
    except ScrapeError:
        print('Download error. Resetting config.')
        vimmit.reset_config(reset_all=True)
    except ConnectionError:
        print('Connection error. Resetting base url.')
        vimmit.reset_config('base_url')
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
