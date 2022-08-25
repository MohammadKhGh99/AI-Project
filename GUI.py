# this file contains the gui code to represent our solving process.
import time as t
from tkinter import messagebox

from config import *
from winsound import *
from tkinter import *


class GUI:
    def __init__(self, board=None, title="Nonogram", window_width=GUI_WIDTH, window_height=GUI_HEIGHT, speed=0.3):
        self.root = Tk()
        self.root.title(title)
        self.root.configure(background="grey")
        my_title = Label(self.root, text="Nonogram Game", font=("times new riman", 20, "bold"), bg="grey", fg="black")
        my_title.pack(side=TOP)
        self.canvas_width = window_width - 100
        self.canvas_height = window_height - 50
        self.root.geometry(f'{window_width}x{window_height}')  # Size of window.

        self.canvas = Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="grey")
        # self.canvas.create_line(0, 200, self.canvas_width, 200)
        # self.canvas.create_line(200, 0, 200, self.canvas_height)
        self.canvas.pack(anchor='n', side=LEFT)
        # self.canvas.place(relx=GUI_WIDTH // 2)#, rely=(GUI_HEIGHT // 2) - 100)

        self.speed = speed

        flag = False

        def play_sound():
            nonlocal flag
            if not flag:
                flag = True
                return PlaySound(r'gui_files\background_music.wav', SND_ALIAS | SND_ASYNC)
            else:
                flag = False
                return PlaySound(None, SND_PURGE)

        # sound_icon = PhotoImage(file=r'gui_files\test.png')

        sound_button = Button(self.root, text="sound", command=play_sound)
        sound_button.config(height=1, width=5)
        sound_button.place(x=950, y=1)
        self.board = None

    # def set_board(self, board):
        self.board = board

    # def draw_lines(self):
        row_width = (self.canvas_height - 200) // self.board.num_rows
        col_width = (self.canvas_width - 200) // self.board.num_cols

        # row_len = self.canvas_width - 200
        # col_len = self.canvas_height - 200

        # create lines to create a look-like table
        for i in range(self.board.num_rows):
            self.canvas.create_line(0, 200 + i * row_width, self.canvas_width, 200 + i * row_width)
        for i in range(self.board.num_cols):
            self.canvas.create_line(200 + i * col_width, 0, 200 + i * col_width, self.canvas_height)

        # board_labels = []
        # con_labels, con_labels = [], []
        # for i in range(self.board.num_rows):
        #     row_labels = []
        #     for j in range(self.board.num_cols):
        #         # label = Label(self.root, borderwidth=5, bg="white")
        #         # cur_x = 200 + i * col_width + col_width // 2
        #         # cur_y = 200 + i * row_width + row_width // 2
        #         # label.pack(padx=cur_x, pady=cur_y)
        #         row_labels.append(Label(self.canvas, borderwidth=1, bg="white"))
        #     board_labels.append(row_labels)

        row_width = (self.canvas_height - 200) // self.board.num_rows
        col_width = (self.canvas_width - 200) // self.board.num_cols
        self.board_rectangles_locs = []
        for i in range(self.board.num_rows):
            row_locs = []
            for j in range(self.board.num_cols):
                x0, y0 = 200 + col_width * j + 2, 200 + row_width * i + 2
                x1, y1 = 200 + col_width * (j + 1) - 2, 200 + row_width * (i + 1) - 2
                row_locs.append((x0, y0, x1, y1))
            self.board_rectangles_locs.append(row_locs)

    # def get_cells_locs(self):
    #
    #     return board_rectangles_locs

    def finish_msg(self):
        messagebox.showinfo('game', 'You Got the Solution!')
