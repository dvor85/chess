from figures import Figure


class Knight(Figure.Figure):

    def __init__(self, pos, color, board):
        self.notation = 'N'
        super().__init__(pos, color, board)

    def get_possible_moves(self):
        avail = []
        moves = [
            (1, -2),
            (2, -1),
            (2, 1),
            (1, 2),
            (-1, 2),
            (-2, 1),
            (-2, -1),
            (-1, -2)
        ]

        for move in moves:
            new_pos = (self.x + move[0], self.y + move[1])
            if (0 <= new_pos[0] < 8 and 0 <= new_pos[1] < 8):
                avail.append([self.board.get_square_from_pos(new_pos)])

        return avail
