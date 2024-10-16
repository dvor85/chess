import pygame
from pathlib import Path


class ResLoader:

    __instance = None

    def __init__(self):
        self._cached_fonts = {}
        self._cached_text = {}
        self._cached_images = {}

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def getImage(self, path):
        return self._cached_images.setdefault(Path(path).name, pygame.image.load(path))

    def make_font(self, fonts, size, bold=False):
        available = pygame.font.get_fonts()
        # get_fonts() returns a list of lowercase spaceless font names
        choices = map(lambda x:x.lower().replace(' ', ''), fonts)
        for choice in choices:
            if choice in available:
                return pygame.font.SysFont(choice, size, bold=bold)
        return pygame.font.Font(None, size)

    def get_font(self, font_preferences, size, bold=False):
        key = str(font_preferences) + '|' + str(size) + str(bold)
        font = self._cached_fonts.get(key, None)
        if font is None:
            font = self.make_font(font_preferences, size, bold)
            self._cached_fonts[key] = font
        return font

    def create_text(self, text, fonts, size, color, bold=False):
        key = '|'.join(map(str, (fonts, size, color, bold, text)))
        image = self._cached_text.get(key, None)
        if image is None:
            font = self.get_font(fonts, size, bold)
            image = font.render(text, True, color)
            self._cached_text[key] = image
        return image
