import pygame

from figures import Figure
from resloader import ResLoader


class Pawn(Figure.Figure):

    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)

        self.img = ResLoader.get_instance().getImage('images/' + color + '_pawn.png')
        self.img = pygame.transform.scale(self.img, (board.tile_width - 20, board.tile_height - 20))

        self.notation = 'P'

    def get_possible_moves(self):
        avail = []
        moves = []

        # move forward
        if self.color == 'white':
            moves.append((0, -1))
            if not self.has_moved:
                moves.append((0, -2))

        elif self.color == 'black':
            moves.append((0, 1))
            if not self.has_moved:
                moves.append((0, 2))

        for move in moves:
            new_pos = (self.x, self.y + move[1])
            if new_pos[1] < 8 and new_pos[1] >= 0:
                avail.append(self.board.get_square_from_pos(new_pos))

        return avail

    def get_moves(self):
        avail = []
        for square in self.get_possible_moves():
            if square.occupying_figure != None:
                break
            else:
                avail.append(square)

        if self.color == 'white':
            if self.x + 1 < 8 and self.y - 1 >= 0:
                square = self.board.get_square_from_pos((self.x + 1, self.y - 1))
                if square.occupying_figure != None:
                    if square.occupying_figure.color != self.color:
                        avail.append(square)
            if self.x - 1 >= 0 and self.y - 1 >= 0:
                square = self.board.get_square_from_pos((self.x - 1, self.y - 1))
                if square.occupying_figure != None:
                    if square.occupying_figure.color != self.color:
                        avail.append(square)

        elif self.color == 'black':
            if self.x + 1 < 8 and self.y + 1 < 8:
                square = self.board.get_square_from_pos((self.x + 1, self.y + 1))
                if square.occupying_figure != None:
                    if square.occupying_figure.color != self.color:
                        avail.append(square)
            if self.x - 1 >= 0 and self.y + 1 < 8:
                square = self.board.get_square_from_pos((self.x - 1, self.y + 1))
                if square.occupying_figure != None:
                    if square.occupying_figure.color != self.color:
                        avail.append(square)

        return avail

    def attacking_squares(self):
        moves = self.get_moves()
        # return the diagonal moves
        return [i for i in moves if i.x != self.x]
