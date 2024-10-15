from figures import Figure


class Pawn(Figure.Figure):

    def __init__(self, pos, color, board):
        self.notation = 'P'
        super().__init__(pos, color, board)
        self.has_moved = 1 < self.y < 6

    def get_possible_moves(self):
        avail = []
        moves = []

        # move forward
        if self.color == 'w':
            moves.append((0, -1))
            if not self.has_moved:
                moves.append((0, -2))

        elif self.color == 'b':
            moves.append((0, 1))
            if not self.has_moved:
                moves.append((0, 2))

        for move in moves:
            if 8 > self.y + move[1] >= 0:
                avail.append(self.board((self.x, self.y + move[1])))

        return avail

    def get_moves(self):
        avail = []
        for square in self.get_possible_moves():
            if square.figure is not None:
                break
            else:
                avail.append(square)

        if self.color == 'w':
            if self.x + 1 < 8 and self.y - 1 >= 0:
                square = self.board((self.x + 1, self.y - 1))
                if square.figure is not None:
                    if square.figure.color != self.color:
                        avail.append(square)
            if self.x - 1 >= 0 and self.y - 1 >= 0:
                square = self.board((self.x - 1, self.y - 1))
                if square.figure is not None:
                    if square.figure.color != self.color:
                        avail.append(square)

        elif self.color == 'b':
            if self.x + 1 < 8 and self.y + 1 < 8:
                square = self.board((self.x + 1, self.y + 1))
                if square.figure is not None:
                    if square.figure.color != self.color:
                        avail.append(square)
            if self.x - 1 >= 0 and self.y + 1 < 8:
                square = self.board((self.x - 1, self.y + 1))
                if square.figure is not None:
                    if square.figure.color != self.color:
                        avail.append(square)

        return avail

    def attacking_squares(self):
        # атака по диагонали
        return [i for i in self.get_moves() if i.x != self.x]
