import pygame
from chessboard import Board
import threading
import queue


class Chess():

    WINDOW_SIZE = (1080, 880)

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Шахматы')
        self.screen = pygame.display.set_mode(Chess.WINDOW_SIZE)
        self.clock = pygame.time.Clock()

        self.board = Board(self.screen, *Chess.WINDOW_SIZE)
        self.board.new_game()
        self.bot_thread = None

        self.running = False

    def draw(self, events):
        if self.bot_thread is None:
            self.screen.fill(self.board.LIGHT_COLOR)
            self.board.draw(events)

        self.board.infopanel.draw(events, self.bot_thread is not None)

        pygame.display.update()

    def start_game(self):

        self.running = True
        qres = queue.Queue(maxsize=1)
        while self.running:
            res = False
            events = pygame.event.get()
            self.draw(events)

            if not self.board.game_over:
                if self.board.turn == self.board.bot_color:
                # ход бота
                    if self.bot_thread is None:
                        self.bot_thread = threading.Thread(target=self.board.bot.getBestMove, args=[qres], daemon=True)
                        self.bot_thread.start()

                    if not qres.empty():
                        self.bot_thread = None
                        f, t = qres.get()
                        self.board.selected_figure = self.board(f).figure
                        self.board.clicked_square = self.board(t)
                        res = self.board.selected_figure.move(self.board.clicked_square)

                else:
#                   ход игрока
                    mx, my = pygame.mouse.get_pos()
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            # нажата кнопка мыши
                            if event.button == 1:
                                res = self.board.on_click(mx, my)

                self.board.infopanel.timers.update(self.board.turn, self.clock.get_time())

            if res:
                print(f"Оценка позиции {self.board.turn} = ", -self.board.bot.evaluateBoard())
                self.board.change_side()

                result = (self.board.is_in_checkmate('b'), self.board.is_in_checkmate('w'))
                if self.board.without_attack > 50:
                    result = (1, 1)

                if any(result):
                    self.game_over(result)

            for event in events:
                # Выход
                if event.type == pygame.QUIT:
                    self.game_over()
                    self.running = False

            self.clock.tick(30)

    def game_over(self, result=None):

        if result:
            self.board.game_over = True
            if 1 in result:
                self.board.message = f'Пат!'
            elif 2 in result:
                if not result.index(2):
                    self.board.message = f'Мат черным!'
                else:
                    self.board.message = f'Мат белым!'
            print(self.board.message)


if __name__ == '__main__':
    chess = Chess()
    chess.start_game()

