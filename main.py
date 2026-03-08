import pygame as pg
from copy import deepcopy
import time


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 20
        self.koef = 0.5

        self.is_can_redraw = True
        self.is_stop_play = False
        self.running = True
        self.render()

    def render(self):
        pg.init()
        pg.display.set_caption('Инициализация поля')
        self.screen = pg.display.set_mode((800, 800))
        while self.running:
            self.check_event()
        pg.quit()

    def check_event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 4:
                self.koef = min(self.koef, self.koef - 0.05)
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 5:
                self.koef = min(self.koef, self.koef + 0.05)
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.get_click(*event.pos)
            cond = ((event.type == pg.KEYDOWN and event.key == pg.K_SPACE) or
                    (event.type == pg.MOUSEBUTTONDOWN and event.button == 3))
            if self.is_can_redraw and cond:
                self.is_stop_play = False
                self.is_can_redraw = False
                self.next_move()
            elif cond:
                self.is_can_redraw = True
                self.is_stop_play = True
        if self.is_can_redraw:
            self.draw()

    def get_click(self, x, y):
        if self.is_can_redraw:
            if (self.left <= x <= self.left + self.cell_size * self.width) and \
                    (self.top <= y <= self.top + self.cell_size * self.height):
                coord_x = (x - self.left) // self.cell_size
                coord_y = (y - self.top) // self.cell_size
                self.redraw_cell(coord_x, coord_y)

    def redraw_cell(self, coord_x, coord_y):
        self.board[coord_y][coord_x] = abs(self.board[coord_y][coord_x] - 1)

    def draw(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.board[y][x]:
                    pg.draw.rect(self.screen, (0, 255, 0),
                                 ((self.left + x * self.cell_size, self.top + y * self.cell_size),
                                  (self.cell_size, self.cell_size)))
                else:
                    pg.draw.rect(self.screen, (0, 0, 0),
                                 ((self.left + x * self.cell_size + 1, self.top + y * self.cell_size + 1),
                                  (self.cell_size - 2, self.cell_size - 2)))
                    pg.draw.rect(self.screen, (255, 255, 255),
                                 ((self.left + x * self.cell_size, self.top + y * self.cell_size),
                                  (self.cell_size, self.cell_size)), 1)
        pg.display.flip()

    def next_move(self):
        pass


class Life(Board):
    def __init__(self, width, height):
        super().__init__(width, height)

    def next_move(self):
        while self.running:
            self.check_event()
            if not self.is_stop_play:
                board = deepcopy(self.board)
                for y in range(len(self.board)):
                    for x in range(len(self.board[y])):
                        cnt_feel, cnt_empty = 0, 0
                        if 0 < x < self.width - 1:
                            for y_cell in range(y - 1, y + 2):
                                if 0 <= y_cell <= self.height - 1:
                                    cnt_feel += (self.board[y_cell][x - 1] + self.board[y_cell][x + 1])
                                    cnt_empty += (2 - self.board[y_cell][x - 1] - self.board[y_cell][x + 1])
                        elif x == 0:
                            for y_cell in range(y - 1, y + 2):
                                if 0 <= y_cell <= self.height - 1:
                                    cnt_feel += self.board[y_cell][x + 1]
                                    cnt_empty += (1 - self.board[y_cell][x + 1])
                        else:
                            for y_cell in range(y - 1, y + 2):
                                if 0 <= y_cell <= self.height - 1:
                                    cnt_feel += self.board[y_cell][x - 1]
                                    cnt_empty += (1 - self.board[y_cell][x - 1])

                        if 0 < y < self.height - 1:
                            cnt_feel += (self.board[y - 1][x] + self.board[y + 1][x])
                            cnt_empty += (2 - self.board[y - 1][x] - self.board[y + 1][x])
                        elif y == 0:
                            cnt_feel += self.board[y + 1][x]
                            cnt_empty += (1 - self.board[y + 1][x])
                        else:
                            cnt_feel += self.board[y - 1][x]
                            cnt_empty += (1 - self.board[y - 1][x])

                        if self.board[y][x] == 1:
                            if cnt_feel not in (2, 3):
                                board[y][x] = 0
                        else:
                            if cnt_feel == 3:
                                board[y][x] = 1
                self.rewrite_board(board)
                self.draw()
                time.sleep(self.koef)


    def rewrite_board(self, board):
        self.board = board[:]


Life(39, 39)
