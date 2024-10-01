import pygame

from figures import Figure


class King(Figure.Figure):

    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)

        self.img = pygame.image.load('images/' + color + '_king.png')
        self.img = pygame.transform.scale(self.img, (board.tile_width - 20, board.tile_height - 20))

        self.notation = 'K'

    def get_possible_moves(self):
        avail = []
        moves = [
            (0, -1),  # north
            (1, -1),  # ne
            (1, 0),  # east
            (1, 1),  # se
            (0, 1),  # south
            (-1, 1),  # sw
            (-1, 0),  # west
            (-1, -1),  # nw
        ]

        for move in moves:
            new_pos = (self.x + move[0], self.y + move[1])
            if (
                new_pos[0] < 8 and
                new_pos[0] >= 0 and
                new_pos[1] < 8 and
                new_pos[1] >= 0
            ):
                avail.append([self.board.get_square_from_pos(new_pos)])

        return avail

    def can_castle(self):
        if self.board.castling != '-':

            if self.color == 'w':
                if 'Q' in self.board.castling:
                    if not any(self.board.get_figure_from_pos((i, 7)) for i in range(1, 4)):
                        return 'Q'

                if 'K' in self.board.castling:
                    if not any(self.board.get_figure_from_pos((i, 7)) for i in range(5, 7)):
                        return 'K'

            else:
                if 'q' in self.board.castling:
                    if not any(self.board.get_figure_from_pos((i, 0)) for i in range(1, 4)):
                        return 'q'

                if 'k' in self.board.castling:
                    if not any(self.board.get_figure_from_pos((i, 0)) for i in range(5, 7)):
                        return 'k'

        return '0'

    def get_valid_moves(self):
        avail = []
        for square in self.get_moves():
            if not self.board.is_in_check(self.color, board_change=[self.pos, square.pos]):
                avail.append(square)

        if self.can_castle() in 'Qq':
            avail.append(self.board.get_square_from_pos((self.x - 2, self.y)))
        if self.can_castle() in 'Kk':
            avail.append(self.board.get_square_from_pos((self.x + 2, self.y)))

        return avail
