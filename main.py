import pygame

from chessboard import Board


class Chess():

    WINDOW_SIZE = (1080, 880)

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Шахматы')
        self.screen = pygame.display.set_mode(Chess.WINDOW_SIZE)
        self.clock = pygame.time.Clock()
#         self.start = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        self.start = 'rnbqkbnr/2pp1ppp/1p6/p3p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 0 4'
#         self.start = 'rnbqkbnr/2pp1ppp/8/pp2p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq b6 0 4'
#         self.start = 'rnbqkbnr/pppp2p1/8/1N2pp1p/4P3/8/PPPP1PPP/R1BQKBNR w KQkq h6 0 1'
#         self.start = 'rnb1kbnr/ppqp2p1/8/4pP1p/8/8/PPPP1PPP/R1BQKBNR b KQkq - 0 2'
#         self.start = 'rnbq1bnr/2p5/1p2Q3/p2P2p1/1P1P1PPp/3N3P/P1P3k1/RNB1K2R b KQ f3 0 15'
        self.board = Board(*Chess.WINDOW_SIZE, self.start)
        self.running = False

    def draw(self):
        self.screen.fill(self.board.LIGHT_COLOR)
        self.board.draw(self.screen)
        pygame.display.update()
        self.clock.tick(30)

    def start_game(self):

        self.board = Board(*Chess.WINDOW_SIZE, self.start)
        self.running = True
        while self.running:

            mx, my = pygame.mouse.get_pos()
            for event in pygame.event.get():
                # Выход
                if event.type == pygame.QUIT:
                    self.end_game()
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # нажата кнопка мыши
                    if event.button == 1:
                        self.board.handle_click(mx, my)

            result = (self.board.is_in_checkmate('b'), self.board.is_in_checkmate('w'))
            if any(result):
                self.end_game(result)

            # Доска
            self.draw()

    def end_game(self, result=None):

        if result is not None:
            message = 'Начать новую игру?'
            if 1 in result:
                message = f'Пат! \n{message}'
            elif 2 in result:
                if not result.index(2):
                    message = f'Мат черным! \n{message}'
                else:  # белым мат
                    message = f'Мат белым! \n{message}'
            print(message)


if __name__ == '__main__':
    chess = Chess()
    chess.start_game()

