class Figure:

    def __init__(self, pos, color, board):
        self.pos = pos
        self.x, self.y = pos
        self.color = color
        self.board = board
        self.has_moved = False

    def __str__(self):
        fig = self.notation if self.color == 'w' else self.notation.lower()
        return fig

    def move(self, to_square, force=False):
#         for i in self.board.squares:
#             i.highlight = False
#             i.check = False

        if to_square in self.get_valid_moves() or force:
            prev_square = self.board.get_square_from_pos(self.pos)
            self.pos, self.x, self.y = to_square.pos, to_square.x, to_square.y

            prev_square.figure = None
            to_square.figure = self
#             self.board.selected_figure = None
            self.has_moved = True
            self.board.pawn_2go = '-'

            if self.notation == 'P':
                # Проход пешки
                if self.y == 0 or self.y == 7:
                    from .Queen import Queen
                    to_square.figure = Queen(self.pos, self.color, self.board)
                # ход пешкой на два поля
                if abs(prev_square.y - self.y) == 2:
                    y = 5 if self.color == 'w' else 2
                    self.board.pawn_2go = self.board.get_square_from_pos((self.x, y)).coord

            # Рокировка
            if self.notation == 'K':
                if prev_square.x - self.x == 2:
                    rook = self.board.get_figure_from_pos((0, self.y))
                    rook.move(self.board.get_square_from_pos((3, self.y)), force=True)

                elif prev_square.x - self.x == -2:
                    rook = self.board.get_figure_from_pos((7, self.y))
                    rook.move(self.board.get_square_from_pos((5, self.y)), force=True)

                if self.board.castling != '-':
                    if self.color == 'w':
                        self.board.castling = self.board.castling.replace('KQ', '')
                    else:
                        self.board.castling = self.board.castling.replace('kq', '')

            if self.notation == 'R':
                if self.board.castling != '-':
                    if self.color == 'w':
                        if prev_square.x == 0:
                            self.board.castling = self.board.castling.replace('Q', '')
                        elif prev_square.x == 7:
                            self.board.castling = self.board.castling.replace('K', '')
                    else:
                        if prev_square.x == 0:
                            self.board.castling = self.board.castling.replace('q', '')
                        elif prev_square.x == 7:
                            self.board.castling = self.board.castling.replace('k', '')

            # число предыдущих ходов без взятий или движения пешек
            if to_square in self.attacking_squares() or self.notation == 'P':
                self.board.without_attack = 0
            else:
                self.board.without_attack += 1

            return True
        else:
#             self.board.selected_figure = None
            return False

    def get_moves(self):
        avail = []
        for direction in self.get_possible_moves():
            for square in direction:
                if square.figure is not None:
                    if square.figure.color == self.color:
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
            if not self.board.is_in_check(self.color, from_to=[self.pos, square.pos]):
                avail.append(square)

        return avail

    # Направление атаки одинаково для всех кроме пешки
    def attacking_squares(self):
        return self.get_moves()
