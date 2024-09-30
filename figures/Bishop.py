import pygame

from .Piece import Piece


class Bishop(Piece):

    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)

        self.img = pygame.image.load('images/' + color + '_bishop.png')
        self.img = pygame.transform.scale(self.img, (board.tile_width - 20, board.tile_height - 20))

        self.notation = 'B'

    def get_possible_moves(self):
        avail = []

        moves_ne = []
        for i in range(1, 8):
            if self.x + i > 7 or self.y - i < 0:
                break
            moves_ne.append(self.board.get_square_from_pos((self.x + i, self.y - i)))
        avail.append(moves_ne)

        moves_se = []
        for i in range(1, 8):
            if self.x + i > 7 or self.y + i > 7:
                break
            moves_se.append(self.board.get_square_from_pos((self.x + i, self.y + i)))
        avail.append(moves_se)

        moves_sw = []
        for i in range(1, 8):
            if self.x - i < 0 or self.y + i > 7:
                break
            moves_sw.append(self.board.get_square_from_pos((self.x - i, self.y + i)))
        avail.append(moves_sw)

        moves_nw = []
        for i in range(1, 8):
            if self.x - i < 0 or self.y - i < 0:
                break
            moves_nw.append(self.board.get_square_from_pos((self.x - i, self.y - i)))
        avail.append(moves_nw)

        return avail
