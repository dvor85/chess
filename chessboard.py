import pygame
from figures.Pawn import Pawn
from figures.Bishop import Bishop
from figures.King import King
from figures.Knight import Knight
from figures.Queen import Queen
from figures.Rook import Rook
from resloader import ResLoader


class Square:

    def __init__(self, x, y, width, height, board):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.board = board

        self.abs_x = 40 + x * width
        self.abs_y = 40 + y * height
        self.abs_pos = (self.abs_x, self.abs_y)
        self.pos = (x, y)
        self.color = 'light' if (x + y) % 2 == 0 else 'dark'
        self.draw_color = (224, 179, 133) if (x + y) % 2 == 0 else (167, 96, 57)
        self.highlight_color = (0, 128, 10) if self.color == 'light' else (0, 128, 10)
        self.occupying_figure = None
        self.coord = self.get_coord()
        self.highlight = False

        self.rect = pygame.Rect(self.abs_x, self.abs_y, self.width, self.height)

    def get_coord(self):
        columns = 'abcdefgh'
        y = str(8 - self.y) if self.board.turn == 'white' else str(self.y + 1)

        return columns[self.x] + y

    def draw(self, display):
        pygame.draw.rect(display, self.draw_color, self.rect)
        if self.highlight:
            pygame.draw.rect(display, self.highlight_color, self.rect, width=5)

        if self.occupying_figure != None:
            centering_rect = self.occupying_figure.img.get_rect()
            centering_rect.center = self.rect.center
            display.blit(self.occupying_figure.img, centering_rect.topleft)


class Board:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tile_width = (width - 280) // 8
        self.tile_height = (height - 80) // 8
        self.selected_figure = None
        self.turn = 'white'
        self.current_side = self.turn[0]
#

        self.start = 'rnbqkbnr/pppppppp/3PQ3/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

        self.squares = self.generate_squares()

        self.parse_fen(self.start)
        self.setup_board()

        print(self.generate_fen())

    def parse_fen(self, fen):
        params = fen.split()
        self.position = params[0]
        if len(params) > 1:
            self.current_side = params[1]

            if len(params) == 6:
                index = 2
                self.castling = params[2]
            else:
                index = 1
            self.pawn_2go = params[index + 1]
            self.without_attack = int(params[index + 2])
            self.moves = int(params[index + 3])
#         if len(params) < 6:
#             self.position, current_side, castling, prev_pawn_2go, without_attack, moves = params

    def generate_squares(self):
        square = []
        for y in range(8):
            for x in range(8):
                square.append(Square(x, y, self.tile_width, self.tile_height, self))
        return square

    def get_square_from_pos(self, pos):
        for square in self.squares:
            if (square.x, square.y) == pos:
                return square

    def get_figure_from_pos(self, pos):
        return self.get_square_from_pos(pos).occupying_figure

    def setup_board(self):
        # iterating 2d list

        for y, row in enumerate(self.position.split('/')):
            x = 0
            irow = iter(row)
            while x < 8:
                figure = next(irow, '')
#             for x, figure in enumerate(list(row)):
                square = self.get_square_from_pos((x, y))
                if figure.isdigit():
                    x += int(figure)
                else:
                    if figure in 'Rr':
                        square.occupying_figure = Rook((x, y), 'black' if figure == 'r' else 'white', self)

                    elif figure in 'Nn':
                        square.occupying_figure = Knight((x, y), 'black' if figure == 'n' else 'white', self)

                    elif figure in 'Bb':
                        square.occupying_figure = Bishop((x, y), 'black' if figure == 'b' else 'white', self)

                    elif figure in 'Qq':
                        square.occupying_figure = Queen((x, y), 'black' if figure == 'q' else 'white', self)

                    elif figure in 'Kk':
                        square.occupying_figure = King((x, y), 'black' if figure == 'k' else 'white', self)

                    elif figure in 'Pp':
                        square.occupying_figure = Pawn((x, y), 'black' if figure == 'p' else 'white', self)
                    x += 1

    def generate_fen(self):
        fen = []
        for y in range(8):
            row = ''
            skip = 0
            for x in range(8):
                figure = self.get_figure_from_pos((x, y))
                if figure is not None:
                    if skip > 0:
                        row += str(skip)
                        skip = 0
                    if figure.color == 'white':
                        row += figure.notation
                    else:
                        row += figure.notation.lower()
                else:
                    skip += 1

            if skip > 0:
                row += str(skip)
            fen.append(row)
        return '/'.join(fen)

    def history(self):
        print(self.position)
        print(self.pawn_2go)

    def handle_click(self, mx, my):
        x = (mx - 40) // self.tile_width
        y = (my - 40) // self.tile_height
        clicked_square = self.get_square_from_pos((x, y))

        if clicked_square is not None:
            if self.selected_figure is None:
                if clicked_square.occupying_figure is not None:
                    if clicked_square.occupying_figure.color == self.turn:
                        self.selected_figure = clicked_square.occupying_figure

            elif self.selected_figure.move(clicked_square):
                self.turn = 'white' if self.turn == 'black' else 'black'
                self.history()

            elif clicked_square.occupying_figure is not None:
                if clicked_square.occupying_figure.color == self.turn:
                    self.selected_figure = clicked_square.occupying_figure

    def is_in_check(self, color, board_change=None):  # board_change = [(x1, y1), (x2, y2)]
        output = False
        king_pos = None

        changing_figure = None
        old_square = None
        new_square = None
        new_square_old_figure = None

        if board_change is not None:
            for square in self.squares:
                if square.pos == board_change[0]:
                    changing_figure = square.occupying_figure
                    old_square = square
                    old_square.occupying_figure = None
            for square in self.squares:
                if square.pos == board_change[1]:
                    new_square = square
                    new_square_old_figure = new_square.occupying_figure
                    new_square.occupying_figure = changing_figure

        figures = [i.occupying_figure for i in self.squares if i.occupying_figure is not None]

        if changing_figure is not None:
            if changing_figure.notation == 'K':
                king_pos = new_square.pos
        if king_pos == None:
            for figure in figures:
                if figure.notation == 'K' and figure.color == color:
                        king_pos = figure.pos
        for figure in figures:
            if figure.color != color:
                for square in figure.attacking_squares():
                    if square.pos == king_pos:
                        output = True

        if board_change is not None:
            old_square.occupying_figure = changing_figure
            new_square.occupying_figure = new_square_old_figure

        return output

    def is_in_checkmate(self, color):
        output = False

        for figure in [i.occupying_figure for i in self.squares]:
            if figure != None:
                if figure.notation == 'K' and figure.color == color:
                    king = figure

        if king.get_valid_moves() == []:
            if self.is_in_check(color):
                output = True

        return output

    def draw_coords(self, display):
        DARK_COLOR = (160, 89, 50)
        LIGHT_COLOR = (224, 179, 133)
        border = pygame.Rect(40, 40, self.tile_width * 8, self.tile_height * 8)
        pygame.draw.rect(display, DARK_COLOR, border, width=5)

        border = pygame.Rect(0, 0, 80 + self.tile_width * 8, 80 + self.tile_height * 8)
        pygame.draw.rect(display, LIGHT_COLOR, border, width=40)

        for i, c in enumerate('abcdefgh', 1):
            text = ResLoader.get_instance().create_text(c, ['Arial'], 20, color=DARK_COLOR)
            display.blit(text, (40 + i * self.tile_width - (self.tile_width + text.get_width()) // 2, 40 + self.tile_height * 8 + text.get_height() // 2))

        for i, c in enumerate('87654321', 1):
            text = ResLoader.get_instance().create_text(c, ['Arial'], 20, color=DARK_COLOR)
            display.blit(text, (20 - text.get_width() // 2, 40 + i * self.tile_height - (self.tile_height + text.get_height()) // 2,))

    def draw(self, display):

        if self.selected_figure is not None:
            self.get_square_from_pos(self.selected_figure.pos).highlight = True
            for square in self.selected_figure.get_valid_moves():
                square.highlight = True

        for square in self.squares:
            square.draw(display)

        self.draw_coords(display)

