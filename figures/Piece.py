class Piece:

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

            prev_square.occupying_piece = None
            square.occupying_piece = self
            self.board.selected_piece = None
            self.has_moved = True

            # Pawn promotion
            if self.notation == 'P':
                if self.y == 0 or self.y == 7:
                    from data.classes.pieces.Queen import Queen
                    square.occupying_piece = Queen(self.pos, self.color, self.board)

            # Move rook if king castles
            if self.notation == 'K':
                if prev_square.x - self.x == 2:
                    rook = self.board.get_piece_from_pos((0, self.y))
                    rook.move(self.board.get_square_from_pos((3, self.y)), force=True)
                elif prev_square.x - self.x == -2:
                    rook = self.board.get_piece_from_pos((7, self.y))
                    rook.move(self.board.get_square_from_pos((5, self.y)), force=True)

            return True
        else:
            self.board.selected_piece = None
            return False

    def get_moves(self):
        avail = []
        for direction in self.get_possible_moves():
            for square in direction:
                if square.occupying_piece is not None:
                    if square.occupying_piece.color == self.color:
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

    # True for all pieces except pawn
    def attacking_squares(self):
        return self.get_moves()
