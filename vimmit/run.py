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
        console.print(
            '[bold red]Download error.[/bold red][red] If the problem persists, try reseting url '
            'with --url, or redownload systems with --download-systems[/red]'
        )
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
