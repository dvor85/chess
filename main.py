import pygame

from chessboard import Board

pygame.init()

WINDOW_SIZE = (800, 800)
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()
board = Board(*WINDOW_SIZE)
pygame.display.set_caption('Шахматы')


def draw(display):
    display.fill('white')
    board.draw(display)
    pygame.display.flip()
    clock.tick(60)


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
        if board.is_in_checkmate('black'):  # Черным мат
            ...
#             print('White wins!')
#             running = False
        elif board.is_in_checkmate('white'):  # Белым мат
            ...
#             print('Black wins!')
#             running = False
        # Доска
        draw(screen)
