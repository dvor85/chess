import pygame
from chessboard import Board
from menu import Menu


class Chess():

    WINDOW_SIZE = (1080, 920)

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Шахматы')
        self.screen = pygame.display.set_mode(Chess.WINDOW_SIZE)
        self.clock = pygame.time.Clock()

        self.board = Board(*Chess.WINDOW_SIZE)
        self.menu = Menu(self.screen, self.board)
        self.running = False

    def draw(self):
        self.screen.fill(self.board.LIGHT_COLOR)
        self.board.draw(self.screen)
        pygame.display.update()
        self.clock.tick(30)

    def start_game(self):

        self.board.new_game()
        self.running = True
        while self.running:

            mx, my = pygame.mouse.get_pos()
            events = pygame.event.get()
            for event in events:
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

            self.menu.draw(events)
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

