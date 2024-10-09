class Minimax:

    def __init__(self, board, color, depth):
        self.board = board
        self.depth = depth
        self.color = color
        self.player_color = board.cfg.PLAYER_COLOR

        self.pawnEval = [
                [6.0, 7.0, 7.0, 7.5, 7.5, 7.0, 7.0, 6.0],
                [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
                [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
                [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
                [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
                [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
                [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            ]

        self.knightEval = [
                [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
                [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
                [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
                [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
                [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
                [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
                [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
                [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
            ]

        self.bishopEval = [
                [ -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
                [ -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
                [ -1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
                [ -1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
                [ -1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
                [ -1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
                [ -1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
                [ -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
            ]

        self.rookEval = [
                [  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [  0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
                [ -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                [ -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                [ -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                [ -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                [ -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                [  0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]
            ]

        self.evalQueen = [
                [ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
                [ -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
                [ -1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
                [ -0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
                [  0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
                [ -1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
                [ -1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
                [ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
            ]

        self.kingEval = [
                [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                [ -2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
                [ -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
                [  2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
                [  2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]
            ]

    def getFigureValue(self, figure):
        if figure is None:
            return 0
        x, y = figure.pos

        def getAbsoluteValue():
            if figure.notation == 'P':
                return 1 + (self.pawnEval[y][x] if figure.color == self.player_color else self.pawnEval[7 - y][x])
            elif figure.notation == 'R':
                return 5 + (self.rookEval[y][x] if figure.color == self.player_color else self.rookEval[7 - y][x])
            elif figure.notation == 'N':
                return 3 + self.knightEval[y][x]
            elif figure.notation == 'B':
                return 3 + (self.bishopEval[y][x] if figure.color == self.player_color else self.bishopEval[7 - y][x])
            elif figure.notation == 'Q':
                return 9 + self.evalQueen[y][x];
            elif figure.notation == 'K':
                return 900 + (self.kingEval[y][x] if figure.color == self.player_color else  self.kingEval[7 - y][x])

        absoluteValue = getAbsoluteValue()
        return absoluteValue if figure.color == self.player_color else -absoluteValue

    def evaluateBoard(self, color):
        return sum(self.getFigureValue(s.figure) for s in self.board.find_squares_by_figure(color))

    def minimaxRoot (self, depth, is_maximazing):
        color = self.color if is_maximazing else self.player_color
        all_moves = self.board.all_valid_moves(color)
        bestMove = -9999
        bestMoveFound = None, None

        for f_pos, squares in all_moves.items():
            for square in squares:
                new_pos = square.pos
                value = self.board.virtual_move([f_pos, new_pos], self.minimax, depth - 1, -10000, 10000, not is_maximazing)

                if (value >= bestMove):
                    bestMove = value
                    bestMoveFound = f_pos, new_pos;

        return bestMoveFound;

    def minimax (self, depth, alpha, beta, is_maximazing):

        def hook():
            if is_maximazing:
                return  max(bestMove, self.minimax(depth - 1, alpha, beta, not is_maximazing))
            else:
                return  min(bestMove, self.minimax(depth - 1, alpha, beta, not is_maximazing))

        color = self.color if is_maximazing else self.player_color

        if depth == 0:
            return -self.evaluateBoard(color)

        bestMove = -9999 if is_maximazing else 9999

        all_moves = self.board.all_valid_moves(color)
        for f_pos, squares in all_moves.items():
            for square in squares:
                if is_maximazing:
                    bestMove = self.board.virtual_move([f_pos, square.pos], hook)
                    alpha = max(alpha, bestMove);
                    if (beta <= alpha):
                        return bestMove

                else:
                    bestMove = self.board.virtual_move([f_pos, square.pos], hook)
                    beta = min(beta, bestMove);
                    if (beta <= alpha):
                        return bestMove

        return bestMove

    def getBestMove(self):
        return self.minimaxRoot(self.depth, True)

    def doBestMove(self):
        f, t = self.getBestMove()
        figure = self.board.get_figure_from_pos(f)
        to_square = self.board.get_square_from_pos(t)
        return figure.move(to_square)

