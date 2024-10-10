import pygame
from config import Config
from figures.Pawn import Pawn
from figures.Bishop import Bishop
from figures.King import King
from figures.Knight import Knight
from figures.Queen import Queen
from figures.Rook import Rook
from resloader import ResLoader
import datetime
import bot


class Square:

    def __init__(self, x, y, width, height, board):

        self.x = x
        # инвертировать доску
        self.y = 7 - y if board.is_player_black else y
        self.width = width
        self.height = height
        self.board = board

        self.abs_x = self.board.left_offset + x * width
        self.abs_y = self.board.top_offset + y * height
        self.pos = (self.x, self.y)
        self.draw_color = self.board.LIGHT_COLOR if not sum(self.pos) % 2 else self.board.DARK_COLOR
        self.figure = None
        self.coord = self.board.get_coord(self.pos)
        self.highlight, self.check, self.checkmate = False, False, False

        self.rect = pygame.Rect(self.abs_x, self.abs_y, self.width, self.height)

    def __str__(self):
        return f"{self.coord}"

    def get_pos_from_coord(self, coord):
        return ('abcdefgh'.index(coord[0]), int(coord[1]) - 1)

    def draw(self, display):
        pygame.draw.rect(display, self.draw_color, self.rect)
        if self.highlight:
            pygame.draw.rect(display, self.board.HIGHLIGHT_COLOR, self.rect, width=5)

        if self.check:
            pygame.draw.rect(display, self.board.CHECK_COLOR, self.rect, width=5)

        if self.checkmate:
            pygame.draw.rect(display, self.board.CHECK_COLOR, self.rect)

        if self.figure is not None:
            centering_rect = self.figure.img.get_rect()
            centering_rect.center = self.rect.center
            display.blit(self.figure.img, centering_rect.topleft)


class Timers():

    def __init__(self, board, limit='15:00'):
        self.limit = limit
        self.board = board

        self.w_rect = pygame.Rect(self.board.width - 200,
                            self.board.top_offset,
                            100,
                            self.board.top_offset)
        self.b_rect = pygame.Rect(self.board.width - 100,
                            self.board.top_offset,
                            100,
                            self.board.top_offset)
        self.reset()

    def reset(self):
        self.black = datetime.datetime.strptime(self.limit, '%M:%S')
        self.white = datetime.datetime.strptime(self.limit, '%M:%S')

    def update(self, color, ms):
        if color == 'w':
            self.white -= datetime.timedelta(milliseconds=ms)
        else:
            self.black -= datetime.timedelta(milliseconds=ms)

    def text(self, color):
        if color == 'w':
            return self.white.strftime('%M:%S')
        else:
            return self.black.strftime('%M:%S')

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.w_rect)
        pygame.draw.rect(screen, (0, 0, 0), self.b_rect)
        rl = ResLoader.get_instance()

        white = rl.create_text(self.text('w'), ['Arial'], 20, color=(0, 0, 0))
        black = rl.create_text(self.text('b'), ['Arial'], 20, color=(255, 255, 255))
        screen.blits(((white, (self.w_rect.centerx - white.get_width() // 2, self.w_rect.centery - white.get_height() // 2)),
                           (black, (self.b_rect.centerx - black.get_width() // 2, self.b_rect.centery - black.get_height() // 2)))
                           )


class Board:

    DARK_COLOR = (160, 89, 50)
    LIGHT_COLOR = (224, 179, 133)
    CHECK_COLOR = (160, 10, 10)
    HIGHLIGHT_COLOR = (0, 128, 10)

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.left_offset = 40
        self.top_offset = 40
        self.tile_width = (width - 200 - 2 * self.left_offset) // 8
        self.tile_height = (height - 2 * self.top_offset) // 8
        self.cfg = Config.get()
        self.is_player_black = self.cfg.PLAYER_COLOR == 'b'
        self.bot_color = self.invert(self.is_player_black)
        self.bot = bot.Minimax(self, self.bot_color, self.cfg.DIFFICULTY)
        self.timers = Timers(self, self.cfg.TIME_LIMIT)

    def get_coord(self, pos):
        columns = 'abcdefgh'
        y = str(8 - pos[1]) if not self.is_player_black else str(pos[1] + 1)
        return columns[pos[0]] + y

    def new_game(self):
        self.game_over = 0
        self.selected_figure = None
        self.turn = 'w'
        self.castling = '-'
        self.pawn_2go = '-'
        self.without_attack = 0
        self.moves = 1

        self.parse_fen(self.cfg.START_POSITION)
        self.squares = self.generate_squares()
        self.setup_board()
        self.history = {}
        self.timers.reset()

    def save_game(self):
        self.cfg.START_POSITION = self.generate_fen()
        self.cfg.save_config()

    def change_side(self):
        self.turn = self.invert(self.turn)

    def invert(self, color):
        return 'w' if color == 'b' else 'b'

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
        y = pos[1] if not self.is_player_black else 7 - pos[1]
        return self.squares[y * 8 + pos[0]]

    def get_figure_from_pos(self, pos):
        return self.get_square_from_pos(pos).figure

    def find_squares_by_figure(self, color=None, notation=None):

        if notation is not None:
            if color:
                return [i for i in self.squares if i.figure is not None and i.figure.color == color and i.figure.notation == notation]
            else:
                return [i for i in self.squares if i.figure is not None and i.figure.notation == notation]
        else:
            if color:
                return [i for i in self.squares if i.figure is not None and i.figure.color == color]
            else:
                return [i for i in self.squares if i.figure is not None]

    def setup_board(self):
        for y, row in enumerate(self.position.split('/')):
            x = 0
            irow = iter(row)
            while x < 8:
                figure = next(irow, '')
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
        if not self.castling:
            self.castling = '-'
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

    def update_history(self, to_pos):
        move = self.history.setdefault(self.moves, {})
        move[self.turn] = str(self.selected_figure) + f'{self.get_coord(to_pos)}'
        if self.turn == 'b':
            move['fen'] = self.generate_fen()
        print(move)

    def handle_click(self, mx, my):
        x = (mx - self.left_offset) // self.tile_width
        y = (my - self.top_offset) // self.tile_height
        if self.is_player_black:
            y = 7 - y

        self.clicked_square = self.get_square_from_pos((x, y))
        if not self.clicked_square is None:
            print(self.clicked_square.pos)
            for i in self.squares:
                i.highlight = False
                i.check = False

            if not self.clicked_square.figure is None:
                if self.clicked_square.figure.color == self.turn:
                    self.selected_figure = self.clicked_square.figure
                    return

            if not self.selected_figure is None:
                return self.selected_figure.move(self.clicked_square)

    def virtual_move(self, from_to, on_moved, *args):  # from_to = [(x1, y1), (x2, y2)]
        old_square = self.get_square_from_pos(from_to[0])
        changing_figure = old_square.figure
        old_square.figure = None

        new_square = self.get_square_from_pos(from_to[1])
        new_square_old_figure = new_square.figure
        new_square.figure = changing_figure

        try:
            if callable(on_moved):
                return on_moved(*args)

        finally:
            old_square.figure = changing_figure
            new_square.figure = new_square_old_figure

    def is_in_check(self, color, from_to=None):  # from_to = [(x1, y1), (x2, y2)]

        def on_moved():
            kings = self.find_squares_by_figure(color, 'K')
            if kings:
                king_pos = kings[0].pos

            for enemy_squares in self.find_squares_by_figure('b' if color == 'w' else 'w'):
                for square in enemy_squares.figure.attacking_squares():
                    if square.pos == king_pos:
                        return True

        if from_to is not None:
            return self.virtual_move(from_to, on_moved)
        else:
            return on_moved()

    def all_valid_moves(self, color):
        return {s.figure.pos: s.figure.get_valid_moves() for s in self.find_squares_by_figure(color)}

    def is_valid_moves_exists(self, color):
        if any(self.all_valid_moves(color).values()):
            return True

    def is_in_checkmate(self, color):
        result = 0

        king = self.find_squares_by_figure(color, 'K')[0]

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

        for i, c in enumerate('87654321' if not self.is_player_black else '12345678', 1):
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
        self.timers.draw(display)

