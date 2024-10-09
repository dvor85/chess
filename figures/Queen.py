from figures import Figure


class Queen(Figure.Figure):

    def __init__(self, pos, color, board):
        self.notation = 'Q'
        super().__init__(pos, color, board)

    def get_possible_moves(self):
        avail = []

        moves_north = []
        for y in range(self.y)[::-1]:
            moves_north.append(self.board.get_square_from_pos((self.x, y)))
        avail.append(moves_north)

        moves_ne = []
        for i in range(1, 8):
            if self.x + i > 7 or self.y - i < 0:
                break
            moves_ne.append(self.board.get_square_from_pos((self.x + i, self.y - i)))
        avail.append(moves_ne)

        moves_east = []
        for x in range(self.x + 1, 8):
            moves_east.append(self.board.get_square_from_pos((x, self.y)))
        avail.append(moves_east)

        moves_se = []
        for i in range(1, 8):
            if self.x + i > 7 or self.y + i > 7:
                break
            moves_se.append(self.board.get_square_from_pos((self.x + i, self.y + i)))
        avail.append(moves_se)

        moves_south = []
        for y in range(self.y + 1, 8):
            moves_south.append(self.board.get_square_from_pos((self.x, y)))
        avail.append(moves_south)

        moves_sw = []
        for i in range(1, 8):
            if self.x - i < 0 or self.y + i > 7:
                break
            moves_sw.append(self.board.get_square_from_pos((self.x - i, self.y + i)))
        avail.append(moves_sw)

        moves_west = []
        for x in range(self.x)[::-1]:
            moves_west.append(self.board.get_square_from_pos((x, self.y)))
        avail.append(moves_west)

        moves_nw = []
        for i in range(1, 8):
            if self.x - i < 0 or self.y - i < 0:
                break
            moves_nw.append(self.board.get_square_from_pos((self.x - i, self.y - i)))
        avail.append(moves_nw)

        return avail
