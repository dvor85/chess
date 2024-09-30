import pygame
from figures.Pawn import Pawn
from figures.Bishop import Bishop
from figures.King import King
from figures.Knight import Knight
from figures.Queen import Queen
from figures.Rook import Rook


class Square:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.abs_x = x * width
        self.abs_y = y * height
        self.abs_pos = (self.abs_x, self.abs_y)
        self.pos = (x, y)
        self.color = 'light' if (x + y) % 2 == 0 else 'dark'
        self.draw_color = (189, 189, 189) if (x + y) % 2 == 0 else (73, 73, 73)
        self.highlight_color = (100, 149, 83) if self.color == 'light' else (0, 128, 10)
        self.occupying_piece = None
        self.coord = self.get_coord()
        self.highlight = False

        self.rect = pygame.Rect(self.abs_x, self.abs_y, self.width, self.height)

    def get_coord(self):
        columns = 'abcdefgh'
        return columns[self.x] + str(self.y + 1)

    def draw(self, display):
        if self.highlight:
            pygame.draw.rect(display, self.highlight_color, self.rect)
        else:
            pygame.draw.rect(display, self.draw_color, self.rect)

        if self.occupying_piece != None:
            centering_rect = self.occupying_piece.img.get_rect()
            centering_rect.center = self.rect.center
            display.blit(self.occupying_piece.img, centering_rect.topleft)


class Board:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tile_width = width // 8
        self.tile_height = height // 8
        self.selected_piece = None
        self.turn = 'white'

        # try making it chess.board.fen()
        self.config = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
#         self.config = [
#             ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
#             ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
#             ['', '', '', '', '', '', '', ''],
#             ['', '', '', '', '', '', '', ''],
#             ['', '', '', '', '', '', '', ''],
#             ['', '', '', '', '', '', '', ''],
#             ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
#             ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
#         ]

        self.squares = self.generate_squares()

        self.setup_board()

    def generate_squares(self):
        square = []
        for y in range(8):
            for x in range(8):
                square.append(
                    Square(x, y, self.tile_width, self.tile_height)
                )
        return square

    def get_square_from_pos(self, pos):
        for square in self.squares:
            if (square.x, square.y) == pos:
                return square

    def get_piece_from_pos(self, pos):
        return self.get_square_from_pos(pos).occupying_piece

    def setup_board(self):
        # iterating 2d list
        for y, row in enumerate(self.config.split('/')):
            for x, piece in enumerate(list(row)):
                square = self.get_square_from_pos((x, y))

                # looking inside contents, what piece does it have
                if piece in 'Rr':
                    square.occupying_piece = Rook((x, y), 'black' if piece == 'r' else 'white', self)
                # as you notice above, we put `self` as argument, or means our class Board

                elif piece in 'Nn':
                    square.occupying_piece = Knight((x, y), 'black' if piece == 'n' else 'white', self)

                elif piece in 'Bb':
                    square.occupying_piece = Bishop((x, y), 'black' if piece == 'b' else 'white', self)

                elif piece in 'Qq':
                    square.occupying_piece = Queen((x, y), 'black' if piece == 'q' else 'white', self)

                elif piece in 'Kk':
                    square.occupying_piece = King((x, y), 'black' if piece == 'k' else 'white', self)

                elif piece in 'Pp':
                    square.occupying_piece = Pawn((x, y), 'black' if piece == 'p' else 'white', self)

    def handle_click(self, mx, my):
        x = mx // self.tile_width
        y = my // self.tile_height
        clicked_square = self.get_square_from_pos((x, y))

        if self.selected_piece is None:
            if clicked_square.occupying_piece is not None:
                if clicked_square.occupying_piece.color == self.turn:
                    self.selected_piece = clicked_square.occupying_piece

        elif self.selected_piece.move(clicked_square):
            self.turn = 'white' if self.turn == 'black' else 'black'

        elif clicked_square.occupying_piece is not None:
            if clicked_square.occupying_piece.color == self.turn:
                self.selected_piece = clicked_square.occupying_piece

    def is_in_check(self, color, board_change=None):  # board_change = [(x1, y1), (x2, y2)]
        output = False
        king_pos = None

        changing_piece = None
        old_square = None
        new_square = None
        new_square_old_piece = None

        if board_change is not None:
            for square in self.squares:
                if square.pos == board_change[0]:
                    changing_piece = square.occupying_piece
                    old_square = square
                    old_square.occupying_piece = None
            for square in self.squares:
                if square.pos == board_change[1]:
                    new_square = square
                    new_square_old_piece = new_square.occupying_piece
                    new_square.occupying_piece = changing_piece

        pieces = [i.occupying_piece for i in self.squares if i.occupying_piece is not None]

        if changing_piece is not None:
            if changing_piece.notation == 'K':
                king_pos = new_square.pos
        if king_pos == None:
            for piece in pieces:
                if piece.notation == 'K' and piece.color == color:
                        king_pos = piece.pos
        for piece in pieces:
            if piece.color != color:
                for square in piece.attacking_squares():
                    if square.pos == king_pos:
                        output = True

        if board_change is not None:
            old_square.occupying_piece = changing_piece
            new_square.occupying_piece = new_square_old_piece

        return output

    def is_in_checkmate(self, color):
        output = False

        for piece in [i.occupying_piece for i in self.squares]:
            if piece != None:
                if piece.notation == 'K' and piece.color == color:
                    king = piece

        if king.get_valid_moves() == []:
            if self.is_in_check(color):
                output = True

        return output

    def draw(self, display):
        if self.selected_piece is not None:
            self.get_square_from_pos(self.selected_piece.pos).highlight = True
            for square in self.selected_piece.get_valid_moves():
                square.highlight = True

        for square in self.squares:
            square.draw(display)
