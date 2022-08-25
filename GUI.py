# this file contains the gui code to represent our solving process.
import tkinter as tk
import time as t
# from game import *
import pygame as pg
from config import *


class GUI:
    def __init__(self, title="Nonogram", window_width=GUI_WIDTH, window_height=GUI_HEIGHT, speed=0.3):
        self.master = tk.Tk()
        self.master.title(title)
        self.canvas_width = window_width
        self.canvas_height = window_height
        self.master.geometry('{}x{}'.format(self.canvas_width, self.canvas_height)) # Size of window.
        self.speed = speed

        


# if __name__ == "__main__":
#     game = Game(colors=COLORFUL)
#     game.run()
#     gui = GUI()
#     gui.draw_board(game.board.board)
#     gui.canvas.mainloop()
