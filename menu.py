import pygame_widgets
import pygame
from datetime import datetime
from resloader import ResLoader
from resloader import ResLoader
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown

_widgets_ = []


class Menu:

    def __init__(self, board):
        global _widgets_
        self.screen = board.screen
        self.board = board
        self.width = board.panel_width
        self.font = ResLoader.get_instance().get_font(['Arial'], 14)

        _widgets_.append(self.button_new_game())
        _widgets_.append(self.button_save_config())

    def height(self):
        return _widgets_[-1].getHeight()

    def button_new_game(self):

        return Button(self.screen,
                self.board.width - self.width,
                0,
                self.width // 2,
                self.board.top_offset,
                text='Новая игра',
                inactiveColour=self.board.LIGHT_COLOR,
                hoverColour=[i - 20 for i in self.board.LIGHT_COLOR],
                pressedColour=[i - 40 for i in self.board.LIGHT_COLOR],
                textColour=self.board.DARK_COLOR,
                font=self.font,
                onClick=self.board.new_game
            )

    def button_save_config(self):

        return Button(self.screen,
                self.board.width - self.width // 2,
                0,
                self.width // 2,
                self.board.top_offset,
                text='Сохранить',
                inactiveColour=self.board.LIGHT_COLOR,
                hoverColour=[i - 20 for i in self.board.LIGHT_COLOR],
                pressedColour=[i - 40 for i in self.board.LIGHT_COLOR],
                textColour=self.board.DARK_COLOR,
                font=self.font,
                onClick=self.board.save_game
            )

    def init_timers(self, time='15:00'):
        white = pygame.Rect(self.board.width - 200,
                            self.board.top_offset + 20,
                            100,
                            self.board.top_offset)
        black = pygame.Rect(self.board.width - 100,
                            self.board.top_offset + 20,
                            100,
                            self.board.top_offset)

        pygame.draw.rect(self.screen, (255, 255, 255), white)
        pygame.draw.rect(self.screen, (0, 0, 0), black)

        w_text = ResLoader.get_instance().create_text(time, ['Arial'], 20, color=(255, 255, 255))
        b_text = ResLoader.get_instance().create_text(time, ['Arial'], 20, color=(0, 0, 0))
        self.screen.blits(((w_text, (black.centerx - w_text.get_width() // 2, black.centery - w_text.get_height() // 2)),
                           (b_text, (white.centerx - b_text.get_width() // 2, white.centery - b_text.get_height() // 2)))
                           )

#     def dropdown(self, text, choices, values, onclick):
#         global _widgets_
#
#         _widgets_.append(
#             Dropdown(self.screen,
#                 self.board.width - self.width,
#                 len(_widgets_) * self.board.top_offset,
#                 self.width,
#                 self.board.top_offset,
#                 name=text,
#
#                 choices=choices,
#                 values=values,
#                 direction='down',
#                 inactiveColour=self.board.LIGHT_COLOR,
#                 hoverColour=[i - 20 for i in self.board.LIGHT_COLOR],
#                 pressedColour=[i - 40 for i in self.board.LIGHT_COLOR],
#                 textColour=self.board.DARK_COLOR,
#                 font=self.font,
#                 onClick=onclick
#             )
#         )

    def draw(self, events):
        pygame_widgets.update(events)

