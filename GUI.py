# this file contains the gui code to represent our solving process.
import tkinter as tk
import time as t
# from game import *
import pygame as pg
from config import *


class GUI:
    def __init__(self, input_cb):  # title="Nonogram", window_width=500, window_height=500, speed=0.3):
        self.input_cb = input_cb
        pg.init()
        self.screen = pg.display.set_mode((GUI_HEIGHT, GUI_WIDTH))
        self.timer = pg.time.Clock()
        self.screen.fill((0, 0, 0))
        # self.apple = pg.image.load(f'data/apple.png').convert()
        # self.body = pg.image.load(f'data/body.png').convert()
        # self.head = pg.image.load(f'data/head.png').convert()
        self.first_run = True
        # self.played_games = 0
        self.end_game = False

    def render(self, game):
        pass

    #     self.master = tk.Tk()
    #     self.master.title(title)
    #     self.canvas_width = window_width
    #     self.canvas_height = window_height
    #     self.master.geometry('{}x{}'.format(self.canvas_width, self.canvas_height))  # Size of window.
    #
    #     self.speed = speed
    #     self.canvas = None
    #
    # def clear(self):
    #     for widget in self.master.winfo_children():
    #         widget.destroy()
    #
    # def draw_board(self, board):
    #     self.clear()
    #     canvas = tk.Canvas(self.master, width=self.canvas_width, height=self.canvas_height)
    #     canvas.pack()
    #
    #     cell_height = self.canvas_height / len(board)
    #     cell_width = self.canvas_height / len(board[0])
    #
    #     for bY, lst in enumerate(board):
    #         for bX in range(len(lst)):
    #             cell = board[bY][bX]
    #             if cell == " ":
    #                 continue
    #             x = (bX * cell_width)
    #             y = (bY * cell_height)
    #             canvas.create_rectangle(x, y, x + cell_width, y + cell_height)
    #
    #     self.canvas = canvas
    #     # self.frameindex += 1
    #     t.sleep(self.speed)


# if __name__ == "__main__":
#     game = Game(colors=COLORFUL)
#     game.run()
#     gui = GUI()
#     gui.draw_board(game.board.board)
#     gui.canvas.mainloop()
