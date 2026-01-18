from vimmit.vimmit import Vimmit
from utils.cli import console
from utils.exceptions import NoSystemsError, ScrapeError

# TODO: setup or way to install

def main():
    vimmit = Vimmit()
    try:
        vimmit.run()
    except NoSystemsError as e:
        console.print(str(e))
    except ScrapeError:
        console.print('[red]Download error - Resetting config.[/red]')
        # TODO: should this:
        #   - reset only base url
        #   - prompt user to reset url and/or config
        vimmit.reset_config(reset_all=True)
    # TODO: This never resolves
    # except ConnectionError:
    #     console.print('[red]Connection error - Resetting base url.[/red]')
    #     vimmit.reset_config('base_url')
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
