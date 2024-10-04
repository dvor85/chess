import pygame_widgets
from resloader import ResLoader
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown

_widgets_ = []


class Menu:

    def __init__(self, screen, board):
        self.screen = screen
        self.board = board
        self.width = 200
        self.font = ResLoader.get_instance().get_font(['Arial'], 20)

    def button(self, text, onclick):
        global _widgets_

        _widgets_.append(
            Button(self.screen,
                self.board.width - self.width,
                len(_widgets_) * self.board.top_offset,
                self.width,
                self.board.top_offset,
                text=text,
                inactiveColour=self.board.LIGHT_COLOR,
                hoverColour=[i - 20 for i in self.board.LIGHT_COLOR],
                pressedColour=[i - 40 for i in self.board.LIGHT_COLOR],
                textColour=self.board.DARK_COLOR,
                font=self.font,
                onClick=onclick
            )
        )

    def dropdown(self, text, choices, values, onclick):
        global _widgets_

        _widgets_.append(
            Dropdown(self.screen,
                self.board.width - self.width,
                len(_widgets_) * self.board.top_offset,
                self.width,
                self.board.top_offset,
                name=text,

                choices=choices,
                values=values,
                direction='down',
                inactiveColour=self.board.LIGHT_COLOR,
                hoverColour=[i - 20 for i in self.board.LIGHT_COLOR],
                pressedColour=[i - 40 for i in self.board.LIGHT_COLOR],
                textColour=self.board.DARK_COLOR,
                font=self.font,
                onClick=onclick
            )
        )

    def draw(self, events):
        pygame_widgets.update(events)

