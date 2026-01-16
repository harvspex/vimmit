from vimm_roller import VimmRoller
from data_objects import *
from setup import scrape_systems
from argparse import Namespace
from dataclasses import dataclass

@dataclass
class Vimmit:
    config: Config
    args: Namespace

    def run(self):
        if self.args.scrape_systems:
            # TODO: Make nicer?
            self.config.data['systems'] = scrape_systems(self.config.data['base_url'])
            self.config.save()

        games = Games()
        blacklist = Blacklist(self.config)

        # TODO: Make this a set of IDs?
        selected_systems = {v['id']: v['name'] for k, v in self.config.data['systems'].items() if k in self.args.systems}

        if not self.args.download:
            vimm_roller = VimmRoller(games, self.config, blacklist, selected_systems)
            vimm_roller.roll()
            return

        from requests import ConnectionError
        try:
            self._handle_scrape(selected_systems)
        except (AttributeError, ConnectionError) as e:
            print(e)
            # print('That didn\'t work. Resetting base url.') # TODO: Better handling and message
            self.config.data['base_url'] = None
            self.config.save()
            return

        games.save()
        self.config.save()
