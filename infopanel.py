import pygame
import datetime
from resloader import ResLoader
from menu import Menu


class Timers():

    def __init__(self, board, top, limit='15:00'):
        self.limit = limit
        self.board = board
        self.top = top
        self.screen = board.screen
        self.w_rect = pygame.Rect(self.board.width - self.board.panel_width,
                            self.top,
                            self.board.panel_width // 2,
                            self.board.top_offset)
        self.b_rect = pygame.Rect(self.board.width - self.board.panel_width // 2,
                            self.top,
                            self.board.panel_width // 2,
                            self.board.top_offset)
        self.reset()

    def height(self):
        return self.w_rect.height

    def reset(self):
        self.black = datetime.datetime.strptime(self.limit, '%M:%S')
        self.white = datetime.datetime.strptime(self.limit, '%M:%S')

    def update(self, color, ms):
        if color == 'w':
            self.white -= datetime.timedelta(milliseconds=ms)
        else:
            self.black -= datetime.timedelta(milliseconds=ms)

    def text(self, color):
        if color == 'w':
            return self.white.strftime('%M:%S')
        else:
            return self.black.strftime('%M:%S')

    def draw(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.w_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.b_rect)
        rl = ResLoader.get_instance()

        white = rl.create_text(self.text('w'), ['Arial'], 20, color=(0, 0, 0))
        black = rl.create_text(self.text('b'), ['Arial'], 20, color=(255, 255, 255))
        self.screen.blits(((white, (self.w_rect.centerx - white.get_width() // 2, self.w_rect.centery - white.get_height() // 2)),
                           (black, (self.b_rect.centerx - black.get_width() // 2, self.b_rect.centery - black.get_height() // 2)))
                           )


class InfoPanel:

    def __init__(self, board):
        self.board = board

        self.screen = board.screen
        self.left = board.width - board.panel_width
        self.width = board.panel_width

        self.panel = pygame.Rect(self.left, 0, self.width, board.height)

        self.menu = Menu(self.board)
        self.bottom = self.menu.height()

        self.timers = Timers(self.board, self.bottom, self.board.cfg.TIME_LIMIT)
        self.bottom += self.timers.height()
        self.history_height = 0

    def draw_history(self):
        rl = ResLoader.get_instance()
        y = self.bottom + 10
        for m, h in self.board.history.items():
            h['y'] = y

            if 'w' in h:
                m_text = rl.create_text(f"{m}.", ['Arial'], 16, color=self.board.DARK_COLOR, bold=True)
                self.screen.blit(m_text, (self.panel.left + 10,
                                      h['y']))

                w_text = rl.create_text(f"{h['w']}", ['Arial'], 16, color=self.board.DARK_COLOR, bold=True)
                self.screen.blit(w_text, (self.panel.centerx - self.width // 4 - w_text.get_width() // 2,
                                      h['y']))

                if 'b' in h:
                    b_text = rl.create_text(f"{h['b']}", ['Arial'], 16, color=self.board.DARK_COLOR, bold=True)
                    self.screen.blit(b_text, (self.panel.centerx + self.width // 4 - b_text.get_width() // 2,
                                          h['y']))
                y += m_text.get_height()

        self.history_height = y

    def draw_message(self, text=None):
        if text:
            rl = ResLoader.get_instance()
            msg = rl.create_text(text, ['Arial'], 20, color=(200, 0, 0), bold=True)
            self.screen.blit(msg, (self.panel.centerx - msg.get_width() // 2,
                                    self.history_height))

    def draw(self, events):
        self.menu.draw(events)
        self.timers.draw()
        self.draw_history()
        self.draw_message(self.board.message)
        pygame.draw.rect(self.screen, self.board.DARK_COLOR, self.panel, width=5)

