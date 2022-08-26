# this file contains the gui code to represent our solving process.
import time as t
from tkinter import messagebox
from copy import deepcopy
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
        self.canvas_height = window_height - 40
        self.root.geometry(f'{window_width}x{window_height}')  # Size of window.

        self.canvas = Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="grey")
        # self.canvas.create_line(0, 200, self.canvas_width, 200)
        # self.canvas.create_line(200, 0, 200, self.canvas_height)
        self.canvas.pack(anchor='n', side=BOTTOM)
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
        sound_button.place(x=850, y=1)

        # def set_board(self, board):
        self.board = deepcopy(board)

        x, y = 260, 230

        # def draw_lines(self):
        row_width = (self.canvas_width - x) // self.board.num_rows
        col_width = (self.canvas_height - y) // self.board.num_cols

        tmp = min(row_width, col_width)

        col_width, row_width = tmp, tmp

        # row_len = self.canvas_width - 200
        # col_len = self.canvas_height - 200

        print(row_width)

        # create lines to create a look-like table
        for i in range(self.board.num_rows + 1):
            self.canvas.create_line(0, y + i * row_width, self.canvas_width, y + i * row_width)
        for i in range(self.board.num_cols + 1):
            self.canvas.create_line(x + i * col_width, 0, x + i * col_width, self.canvas_height)

        # max_col, max_row = 0, 0
        # for row in self.board.rows_constraints:
        #     if len(row) > max_row:
        #         max_row = len(row)
        # # gets the longest column's length
        # for col in self.board.cols_constraints:
        #     if len(col) > max_col:
        #         max_col = len(col)

        # row_width_con = 200 // max_row
        # col_width_con = 200 // max_col

        # for row in range(max_row):
        #     self.canvas.create_line(0 + row * row_width, 200, 0 + row * row_width, self.canvas_height, dash=(3, 1))
        # for col in range(max_col):
        #     self.canvas.create_line(200, 0 + col * col_width, self.canvas_height, 0 + col * col_width, dash=(3, 1))

        # row_width = (self.canvas_height - 200) // self.board.num_rows
        # col_width = (self.canvas_width - 200) // self.board.num_cols
        self.board_rectangles_locs = []
        for i in range(self.board.num_rows):
            row_locs = []
            for j in range(self.board.num_cols):
                x0, y0 = x + col_width * j + 2, y + row_width * i + 2
                x1, y1 = x + col_width * (j + 1) - 2, y + row_width * (i + 1) - 2
                row_locs.append((x0, y0, x1, y1))
                self.canvas.create_rectangle(x0, y0, x1, y1)
            self.board_rectangles_locs.append(row_locs)

        print(self.board_rectangles_locs)

        for i, row_con in enumerate(self.board.rows_constraints):
            row_text = ''
            for con in row_con:
                row_text += str(con) + ' '
            # row_text = row_text * 15
            row_text = row_text[:-1]
            # if len(row_text) < 80:
            #     row_text = ' ' * (80 - len(row_text)) + row_text

            self.canvas.create_text((5, y + row_width // 3 + row_width * i), text=row_text, anchor='nw', font=('lucida', '9'))
        for i, col_con in enumerate(self.board.cols_constraints):
            col_text = ''
            for con in col_con:
                col_text += str(con) + '\n'
            # col_text = col_text * 15
            col_text = col_text[:-1]
            n = col_text.count('\n')
            if n < 14:
                col_text = '\n' * (14 - n) + col_text

            self.canvas.create_text((x + col_width // 3 + col_width * i, 5), text=col_text, anchor='nw', font=('lucida', '9'))

    def success_msg(self):
        messagebox.showinfo('Success!', 'You Got the Solution!')

    def failed_msg(self):
        messagebox.showerror('Failed', 'You didn\'t find the solution')
