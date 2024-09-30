class Figure:

    def __init__(self, pos, color, board):
        self.pos = pos
        self.x, self.y = pos
        self.color = color
        self.board = board
        self.has_moved = False

    def move(self, square, force=False):
        for i in self.board.squares:
            i.highlight = False

        if square in self.get_valid_moves() or force:
            prev_square = self.board.get_square_from_pos(self.pos)
            self.pos, self.x, self.y = square.pos, square.x, square.y

            prev_square.occupying_figure = None
            square.occupying_figure = self
            self.board.selected_figure = None
            self.has_moved = True

            if self.notation == 'P':
                # Проход пешки
                if self.y == 0 or self.y == 7:
                    from .Queen import Queen
                    square.occupying_figure = Queen(self.pos, self.color, self.board)
                # ход пешкой на два поля
                if abs(prev_square.y - self.y) == 2:
                    y = 5 if self.board.turn == 'white' else 2
                    self.board.pawn_2go = self.board.get_square_from_pos((self.x, y)).coord
                else:
                    self.board.pawn_2go = '-'

            # Рокировка
            if self.notation == 'K':
                if prev_square.x - self.x == 2:
                    rook = self.board.get_figure_from_pos((0, self.y))
                    rook.move(self.board.get_square_from_pos((3, self.y)), force=True)
                elif prev_square.x - self.x == -2:
                    rook = self.board.get_figure_from_pos((7, self.y))
                    rook.move(self.board.get_square_from_pos((5, self.y)), force=True)

            return True
        else:
            self.board.selected_figure = None
            return False

    def get_moves(self):
        avail = []
        for direction in self.get_possible_moves():
            for square in direction:
                if square.occupying_figure is not None:
                    if square.occupying_figure.color == self.color:
                        break
                    else:
                        avail.append(square)
                        break
                else:
                    avail.append(square)
        return avail

    def get_valid_moves(self):
        avail = []
        for square in self.get_moves():
            if not self.board.is_in_check(self.color, board_change=[self.pos, square.pos]):
                avail.append(square)

        return avail

    # Направление атаки одинаково для всех кроме пешки
    def attacking_squares(self):
        return self.get_moves()
