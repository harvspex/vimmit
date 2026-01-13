import pandas as pd

class GameRoller:
    def __init__(
        self,
        filename: str
    ):
        self.filename = filename
        self.df = pd.read_csv(filename)
