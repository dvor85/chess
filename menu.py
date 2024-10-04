import pygame_widgets
from pygame_widgets.button import Button


class Menu:

    def __init__(self, screen, board):
        self.screen = screen
        self.board = board
        button = Button(
            # Mandatory Parameters
            self.screen,  # Surface to place button on
            0,  # X-coordinate of top left corner
            0,  # Y-coordinate of top left corner
            300,  # Width
            self.board.top_offset,  # Height

            # Optional Parameters
            text='Hello',  # Text to display
            fontSize=50,  # Size of font
            margin=20,  # Minimum distance between text/image and edge of button
            inactiveColour=(200, 50, 0),  # Colour of button when not being interacted with
            hoverColour=(150, 0, 0),  # Colour of button when being hovered over
            pressedColour=(0, 200, 20),  # Colour of button when being clicked
            radius=20,  # Radius of border corners (leave empty for not curved)
            onClick=lambda: print('Click')  # Function to call when clicked on
        )

    def draw(self, events):
        pygame_widgets.update(events)


class Statistic:

    def __init__(self, params):
        ...

