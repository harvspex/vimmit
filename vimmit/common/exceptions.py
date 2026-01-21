class NoSystemsError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class ScrapeError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class NoGamesError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class ImportExportError(Exception):
    def __init__(self, *args):
        super().__init__(*args)