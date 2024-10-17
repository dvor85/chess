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
        self.START_POSITION = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        self.PLAYER_COLOR = 'w'
        self.DIFFICULTY = 3
        self.TIME_LIMIT = 15

        self.__load_config()

    def __str__(self):
        return str(self.__dict__)

    def __load_config(self):
        if Config.__settings_f.is_file():
            with Config.__settings_f.open('r') as fp:
                self.__dict__.update(json.load(fp))

    def save_config(self):
        with Config.__settings_f.open('w') as fp:
            json.dump(self.__dict__, fp, indent=4, sort_keys=True)

