import pygame
from chessboard import Board
from menu import Menu


class Chess():

    WINDOW_SIZE = (1080, 880)

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Шахматы')
        self.screen = pygame.display.set_mode(Chess.WINDOW_SIZE)
        self.clock = pygame.time.Clock()

        self.board = Board(*Chess.WINDOW_SIZE)
        self.menu = Menu(self.screen, self.board)
        self.menu.button('Новая игра', self.board.new_game)
        self.menu.dropdown("Играть за ...", ['Белых', 'Чёрных'], ('w', 'b'), lambda: 1)

        self.running = False

    def draw(self, events):
        self.screen.fill(self.board.LIGHT_COLOR)
        self.board.draw(self.screen)
        self.menu.draw(events)
        pygame.display.update()

    def start_game(self):

        self.board.new_game()
        self.running = True
        while self.running:
            res = False
            events = pygame.event.get()
            self.draw(events)

            if not self.board.game_over and self.board.turn == self.board.bot_color:
                f, t = self.board.bot.getBestMove()
                self.board.selected_figure = self.board.get_figure_from_pos(f)
                self.board.clicked_square = self.board.get_square_from_pos(t)

                res = self.board.selected_figure.move(self.board.clicked_square)

            else:

                mx, my = pygame.mouse.get_pos()
                for event in events:
                    # Выход
                    if event.type == pygame.QUIT:
                        self.game_over()
                        self.running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        # нажата кнопка мыши
                        if event.button == 1:
                            res = self.board.handle_click(mx, my)

            if res:
                to_pos = self.board.clicked_square.pos
                self.board.update_history(to_pos)

                if self.board.turn == 'b':
                    self.board.moves += 1
                self.board.change_side()
                self.board.selected_figure = None

            result = (self.board.is_in_checkmate('b'), self.board.is_in_checkmate('w'))
            if any(result):
                self.game_over(result)

            # Доска
            self.draw(events)
            self.clock.tick(30)

    def game_over(self, result=None):

        if result:
            self.board.game_over = result
            message = 'Начать новую игру?'
            if 1 in result:
                message = f'Пат! \n{message}'
            elif 2 in result:
                if not result.index(2):
                    message = f'Мат черным! \n{message}'
                else:
                    message = f'Мат белым! \n{message}'
            print(message)


if __name__ == '__main__':
    chess = Chess()
    chess.start_game()

