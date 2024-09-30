import pygame

from .Piece import Piece


class Rook(Piece):

    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)

        self.img = pygame.image.load('images/' + color + '_rook.png')
        self.img = pygame.transform.scale(self.img, (board.tile_width - 20, board.tile_height - 20))

        self.notation = 'R'

    def get_possible_moves(self):
        avail = []

        moves_north = []
        for y in range(self.y)[::-1]:
            moves_north.append(self.board.get_square_from_pos((self.x, y)))
        avail.append(moves_north)

        moves_east = []
        for x in range(self.x + 1, 8):
            moves_east.append(self.board.get_square_from_pos((x, self.y)))
        avail.append(moves_east)

        moves_south = []
        for y in range(self.y + 1, 8):
            moves_south.append(self.board.get_square_from_pos((self.x, y)))
        avail.append(moves_south)

        moves_west = []
        for x in range(self.x)[::-1]:
            moves_west.append(self.board.get_square_from_pos((x, self.y)))
        avail.append(moves_west)

        return avail
