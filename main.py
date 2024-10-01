import pygame

from chessboard import Board

pygame.init()

WINDOW_SIZE = (1080, 880)
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()
board = Board(*WINDOW_SIZE)
pygame.display.set_caption('Шахматы')


def draw(display):
    display.fill(board.LIGHT_COLOR)
    board.draw(display)
    pygame.display.update()
    clock.tick(30)


if __name__ == '__main__':
    running = True
    while running:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            # Выход
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # нажата кнопка мыши
                if event.button == 1:
                    board.handle_click(mx, my)
        result = (board.is_in_checkmate('b'), board.is_in_checkmate('w'))
        if 1 in result:  # Пат
            ...
        elif 2 in result:
            if not result.index(2):  # Черным мат
                ...
            else:  # белым мат
                ...
        elif result[1] == 2:  # Пат
            ...

        # Доска
        draw(screen)
