import json
from pathlib import Path


class Config:
    __instance = None
    __settings_f = Path(__file__).with_name('settings.json')

    @classmethod
    def get(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def __init__(self):
        # self.START_CONFIG = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        # self.START_CONFIG = 'rnbqkbnr/2pp1ppp/8/pp2p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq b6 0 4'
        # self.START_CONFIG = 'rnbqkbnr/pppp2p1/8/1N2pp1p/4P3/8/PPPP1PPP/R1BQKBNR w KQkq h6 0 1'
        # self.START_CONFIG = 'rnb1kbnr/ppqp2p1/8/4pP1p/8/8/PPPP1PPP/R1BQKBNR b KQkq - 0 2'
        # self.START_CONFIG = 'rnbq1bnr/2p5/1p2Q3/p2P2p1/1P1P1PPp/3N3P/P1P3k1/RNB1K2R b KQ f3 0 15'
        self.START_POSITION = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        self.PLAYER_COLOR = 'w'
        self.DIFFICULTY = 3
        self.TIME_LIMIT = '15:00'

        self.__load_config()

    def __str__(self):
        return str(self.__dict__)

    def __load_config(self):
        if Config.__settings_f.is_file():
            with Config.__settings_f.open('r') as fp:
                data = json.load(fp)
                self.__dict__.update(data)

    def save_config(self):

        with Config.__settings_f.open('w') as fp:
            json.dump(self.__dict__, fp, indent=4, sort_keys=True)

