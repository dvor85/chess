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

        self.abs_x = self.board.left_offset + x * width
        self.abs_y = self.board.top_offset + y * height
        self.abs_pos = (self.abs_x, self.abs_y)
        self.pos = (x, y)
        self.color = 'light' if (x + y) % 2 == 0 else 'dark'
        self.draw_color = self.board.LIGHT_COLOR if (x + y) % 2 == 0 else self.board.DARK_COLOR
        self.highlight_color = (0, 128, 10)
        self.figure = None
        self.coord = self.get_coord()
        self.highlight = False
        self.check, self.checkmate = False, False

        self.rect = pygame.Rect(self.abs_x, self.abs_y, self.width, self.height)

    def __str__(self):
        figure = self.figure.notation if self.figure else ''
        figure = figure if self.color == 'light' else figure.lower()
        return f"{figure}{self.coord}"

    def get_coord(self):
        columns = 'abcdefgh'
        y = str(8 - self.y) if self.board.turn == 'w' else str(self.y + 1)

        return columns[self.x] + y

    def get_pos_from_coord(self, coord):
        return ('abcdefgh'.index(coord[0]), int(coord[1]) - 1)

    def draw(self, display):
        pygame.draw.rect(display, self.draw_color, self.rect)
        if self.highlight:
            pygame.draw.rect(display, self.highlight_color, self.rect, width=5)

        if self.check:
            pygame.draw.rect(display, self.board.CHECK_COLOR, self.rect, width=5)

        if self.checkmate:
            pygame.draw.rect(display, self.board.CHECK_COLOR, self.rect)

        if self.figure is not None:
            centering_rect = self.figure.img.get_rect()
            centering_rect.center = self.rect.center
            display.blit(self.figure.img, centering_rect.topleft)


class Board:

    DARK_COLOR = (160, 89, 50)
    LIGHT_COLOR = (224, 179, 133)
    CHECK_COLOR = (160, 10, 10)

    def __init__(self, width, height, start):
        self.width = width
        self.height = height
        self.left_offset = 40
        self.top_offset = 40
        self.tile_width = (width - 200 - 2 * self.left_offset) // 8
        self.tile_height = (height - 2 * self.top_offset) // 8
        self.selected_figure = None

        self.start = start
        self.turn = 'w'
        self.castling = '-'
        self.pawn_2go = '-'
        self.without_attack = 0
        self.moves = 1

        self.squares = self.generate_squares()

        self.parse_fen(self.start)
        self.setup_board()

    def parse_fen(self, fen):
        params = fen.split()
        self.position = params[0]
        if len(params) > 1:
            self.turn = params[1]
            self.castling = params[2]
            self.pawn_2go = params[3]
            self.without_attack = int(params[4])
            self.moves = int(params[5])

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
        return self.get_square_from_pos(pos).figure

    def find_squares_from_figure(self, color, notation=None):
        if notation is not None:
            return [i for i in self.squares if i.figure is not None and i.figure.color == color and i.figure.notation == notation]
        else:
            return [i for i in self.squares if i.figure is not None and i.figure.color == color]

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
                    color = 'b' if figure in 'rnbqkp' else 'w'
                    if figure in 'Rr':
                        square.figure = Rook((x, y), color, self)

                    elif figure in 'Nn':
                        square.figure = Knight((x, y), color, self)

                    elif figure in 'Bb':
                        square.figure = Bishop((x, y), color, self)

                    elif figure in 'Qq':
                        square.figure = Queen((x, y), color, self)

                    elif figure in 'Kk':
                        square.figure = King((x, y), color, self)

                    elif figure in 'Pp':
                        square.figure = Pawn((x, y), color, self)
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
                    if figure.color == 'w':
                        row += figure.notation
                    else:
                        row += figure.notation.lower()
                else:
                    skip += 1

            if skip > 0:
                row += str(skip)
            fen.append(row)
        return '/'.join(fen) + f" {self.turn} {self.castling} {self.pawn_2go} {self.without_attack} {self.moves}"

    def history(self):
        print(self.generate_fen())

    def handle_click(self, mx, my):
        x = (mx - self.left_offset) // self.tile_width
        y = (my - self.top_offset) // self.tile_height
        clicked_square = self.get_square_from_pos((x, y))
        if clicked_square is not None:
            if self.selected_figure is None:
                if clicked_square.figure is not None:
                    if clicked_square.figure.color == self.turn:
                        self.selected_figure = clicked_square.figure

            elif self.selected_figure.move(clicked_square):
                # Ход
                if self.turn == 'b':
                    self.moves += 1

                if not self.castling:
                    self.castling = '-'

                self.turn = 'w' if self.turn == 'b' else 'b'
                self.history()

            elif clicked_square.figure is not None:
                if clicked_square.figure.color == self.turn:
                    self.selected_figure = clicked_square.figure

    def is_in_check(self, color, board_change=None):  # board_change = [(x1, y1), (x2, y2)]
        result = False
        king_pos = None

        changing_figure = None
        old_square = None
        new_square = None
        new_square_old_figure = None

        if board_change is not None:
            old_square = self.get_square_from_pos(board_change[0])
            changing_figure = old_square.figure
            old_square.figure = None

            new_square = self.get_square_from_pos(board_change[1])
            new_square_old_figure = new_square.figure
            new_square.figure = changing_figure

        figures = [i.figure for i in self.squares if i.figure is not None]

        if changing_figure is not None:
            if changing_figure.notation == 'K':
                king_pos = new_square.pos

        if king_pos is None:
            king_pos = self.find_squares_from_figure(color, 'K')[0].pos

        for figure in figures:
            if figure.color != color:
                for square in figure.attacking_squares():
                    if square.pos == king_pos:
                        result = True

        if board_change is not None:
            old_square.figure = changing_figure
            new_square.figure = new_square_old_figure

        return result

    def is_valid_moves_exists(self, color):
        my_squares = self.find_squares_from_figure(color)
        for square in my_squares:
            if any(square.figure.get_valid_moves()):
                return True

    def is_in_checkmate(self, color):
        result = 0

        king = self.find_squares_from_figure(color, 'K')[0]

        if not self.is_valid_moves_exists(color):
            if self.is_in_check(color):
                result = 2
                king.checkmate = True
            else:
                result = 1
        elif self.is_in_check(color):
            king.check = True

        return result

    def draw_coords(self, display):

        border = pygame.Rect(self.left_offset, self.top_offset, self.tile_width * 8, self.tile_height * 8)
        pygame.draw.rect(display, self.DARK_COLOR, border, width=5)

        border = pygame.Rect(0, 0, 2 * self.left_offset + self.tile_width * 8, 2 * self.top_offset + self.tile_height * 8)
        pygame.draw.rect(display, self.DARK_COLOR, border, width=5)

        for i, c in enumerate('abcdefgh', 1):
            text = ResLoader.get_instance().create_text(c, ['Arial'], 20, color=self.DARK_COLOR)
            display.blit(text, (self.left_offset + i * self.tile_width - (self.tile_width + text.get_width()) // 2,
                                self.top_offset + self.tile_height * 8 + text.get_height() // 2))
            display.blit(text, (self.left_offset + i * self.tile_width - (self.tile_width + text.get_width()) // 2,
                                (self.top_offset - text.get_height()) // 2))

        for i, c in enumerate('87654321', 1):
            text = ResLoader.get_instance().create_text(c, ['Arial'], 20, color=self.DARK_COLOR)
            display.blit(text, ((self.left_offset - text.get_width()) // 2,
                                self.top_offset + i * self.tile_height - (self.tile_height + text.get_height()) // 2))
            display.blit(text, (self.left_offset + self.tile_width * 8 + (self.left_offset - text.get_width()) // 2,
                                self.top_offset + i * self.tile_height - (self.tile_height + text.get_height()) // 2))

    def draw(self, display):

        if self.selected_figure is not None:
            self.get_square_from_pos(self.selected_figure.pos).highlight = True
            for square in self.selected_figure.get_valid_moves():
                square.highlight = True

        for square in self.squares:
            square.draw(display)

        self.draw_coords(display)

