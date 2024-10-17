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
            self.board.draw()

        self.board.infopanel.draw(events, self.bot_thread is not None)

        pygame.display.update()

    def bot_move(self, qres):
        if self.bot_thread is None:
            self.bot_thread = threading.Thread(target=self.board.bot.getBestMove, args=[qres], daemon=True)
            self.bot_thread.start()

        if not qres.empty():
            self.bot_thread = None
            f, t = qres.get()
            self.board.selected_figure = self.board(f).figure
            self.board.clicked_square = self.board(t)
            return self.board.selected_figure.move(self.board.clicked_square)

    def player_move(self, events):
        mx, my = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # нажата кнопка мыши
                if event.button == 1:
                    return self.board.on_click(mx, my)

    def start_game(self):

        self.running = True
        qres = queue.Queue(maxsize=1)
        while self.running:
            res = False
            events = pygame.event.get()
            self.draw(events)

            if not self.board.game_over():
                if self.board.turn == self.board.bot_color:
#                   ход бота
                    res = self.bot_move(qres)
                else:
#                   ход игрока
                    res = self.player_move(events)

                self.board.infopanel.timers.update(self.board.turn, self.clock.get_time())

                if res:
                    print(f"Оценка позиции игрока = ", self.board.bot.evaluateBoard())
                    self.board.change_side()

                    if self.board.without_attack > 50:
                        self.board.game_over(1)
                    elif self.board.turn == 'b':
                        self.board.game_over(self.board.is_in_checkmate('b'))
                    else:
                        self.board.game_over(-self.board.is_in_checkmate('w'))

                    print(self.board._message)

            for event in events:
                # Выход
                if event.type == pygame.QUIT:
                    self.running = False

            self.clock.tick(30)


if __name__ == '__main__':
    chess = Chess()
    chess.start_game()

