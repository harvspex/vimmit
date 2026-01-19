from data.base_data import BaseData, DATA_DIR


class Config(BaseData):
    def __init__(self):
        super().__init__(DATA_DIR, 'config.dat')
        self.save()