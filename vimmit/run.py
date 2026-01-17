from classes.vimmit import Vimmit
from classes.exceptions import *
from rich.console import Console

# TODO: setup or way to install

def main():
    console = Console()
    vimmit = Vimmit()
    try:
        vimmit.run()
    except NoSystemsError as e:
        console.print(str(e))
    except ScrapeError:
        console.print('[red]Download error - Resetting config.[/red]')
        vimmit.reset_config(reset_all=True)
    except ConnectionError:
        console.print('[red]Connection error - Resetting base url.[/red]')
        vimmit.reset_config('base_url')
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
