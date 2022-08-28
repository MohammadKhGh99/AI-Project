# this file contains the gui code to represent our solving process.
import time as t
from tkinter import messagebox
from copy import deepcopy
from config import *
from winsound import *
from tkinter import *


class GUI:
    def __init__(self, board=None, title="Two Colors Nonogram Game", window_width=GUI_WIDTH, window_height=GUI_HEIGHT,
                 cur_game=None):
        self.__cur_game = cur_game

        self.root = Tk()
        self.root.title(title)
        self.root.configure(background="grey")
        my_title = Label(self.root, text="Two Colors Nonogram Game", font=("times new roman", 20, "bold"), bg="white",
                         fg="black")
        my_title.pack(side=TOP)
        self.canvas_width = 800
        self.canvas_height = 700
        self.root.geometry(f'{window_width}x{window_height}')

        self.canvas = Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white",
                             highlightbackground='black')
        # self.canvas.pack(anchor='n', side=LEFT)
        self.canvas.place(x=10, y=40)
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

        self.labels = []

        def new_game():
            self.__cur_game = self.__cur_game.new_game(self.__cur_game)

        # def create_new_button():
        new_game_button = Button(self.canvas, text="new game", command=new_game)
        new_game_button.config(height=1, width=8)
        new_game_button.place(x=100, y=2)

        def clear_func():
            csps = []
            for label in self.labels:
                label.destroy()

            self.labels = []
            for chk_b in check_buttons:
                chk_b.destroy()
            self.__cur_game.board.clear_board()

        clear_button = Button(self.root, text="clear", command=clear_func)
        clear_button.config(height=1, width=5)
        clear_button.place(x=800, y=1)

        choose_label = Label(self.root, text="Choose the way to solve:", bg='grey')
        choose_label.place(x=830, y=50)

        def run_brute():
            self.__cur_game.run(BRUTE)

        brute_button = Button(self.root, text="Brute Force", command=run_brute)
        brute_button.config(height=1, width=10)
        brute_button.place(x=865, y=100)

        def run_dfs():
            self.__cur_game.run(DFS)

        dfs_button = Button(self.root, text="DFS", command=run_dfs)
        dfs_button.config(height=1, width=10)
        dfs_button.place(x=865, y=180)

        def run_bfs():
            self.__cur_game.run(BFS)

        bfs_button = Button(self.root, text="BFS", command=run_bfs)
        bfs_button.config(height=1, width=10)
        bfs_button.place(x=865, y=260)

        def run_astar():
            self.__cur_game.run(ASTAR)

        astar_button = Button(self.root, text="ASTAR", command=run_astar)
        astar_button.config(height=1, width=10)
        astar_button.place(x=865, y=340)

        # def exit_game():
        #     self.root.quit()
        #
        # exit_button = Button(self.root, text="exit", command=exit_game, background='red')
        # exit_button.config(height=1, width=4)
        # exit_button.place(x=5, y=1)
        csps = set()

        def add_csp(csp_to_add_or_delete):
            if csp_to_add_or_delete in csps:
                csps.remove(csp_to_add_or_delete)
            else:
                csps.add(csp_to_add_or_delete)

        check_buttons = []

        def select_csps():
            nonlocal csps
            csps = set()
            mrv_check = Checkbutton(self.root, text="MRV", command=lambda: add_csp(MRV))
            mrv_check.place(x=865, y=475)

            degree_check = Checkbutton(self.root, text="DEGREE", command=lambda: add_csp(DEGREE))
            degree_check.place(x=865, y=510)

            lcv_check = Checkbutton(self.root, text="LCV", command=lambda: add_csp(LCV))
            lcv_check.place(x=865, y=545)

            fc_check = Checkbutton(self.root, text="FC", command=lambda: add_csp(FC))
            fc_check.place(x=865, y=580)

            ac_check = Checkbutton(self.root, text="AC", command=lambda: add_csp(AC))
            ac_check.place(x=865, y=615)

            run_csp_button = Button(self.root, text="Run CSP", command=run_csp)
            run_csp_button.config(height=1, width=10)
            run_csp_button.place(x=865, y=650)

            check_buttons.append(mrv_check)
            check_buttons.append(degree_check)
            check_buttons.append(lcv_check)
            check_buttons.append(fc_check)
            check_buttons.append(ac_check)
            check_buttons.append(run_csp_button)
            # self.__cur_game.run(CSP_P)

        select_csp_button = Button(self.root, text="CSP", command=select_csps)
        select_csp_button.config(height=1, width=10)
        select_csp_button.place(x=865, y=420)

        def run_csp():
            print(csps)
            self.__cur_game.run(CSP_P, csps=csps)

        self.board_rectangles_locs = []
        self.board = None

        self.create_board(board)

    def create_board(self, board):
        self.board = deepcopy(board)

        x, y = 260, 230
        tmp = min((self.canvas_width - x) // self.board.num_rows, (self.canvas_height - y) // self.board.num_cols)
        col_width, row_width = tmp, tmp
        # create lines to create a look-like table
        for i in range(self.board.num_rows + 1):
            self.canvas.create_line(0, y + i * row_width, self.canvas_width, y + i * row_width)
        for i in range(self.board.num_cols + 1):
            self.canvas.create_line(x + i * col_width, 0, x + i * col_width, self.canvas_height)
            if i == self.board.num_cols:
                for j in range(1, 31):
                    self.canvas.create_line(x + i * col_width + 3 * j, 0, x + i * col_width + 3 * j, self.canvas_height)

        self.board_rectangles_locs = []
        for i in range(self.board.num_rows):
            row_locs = []
            for j in range(self.board.num_cols):
                x0, y0 = x + col_width * j + 2, y + row_width * i + 2
                x1, y1 = x + col_width * (j + 1) - 2, y + row_width * (i + 1) - 2
                row_locs.append((x0, y0, x1, y1))
                self.canvas.create_rectangle(x0, y0, x1, y1, fill='white')
            self.board_rectangles_locs.append(row_locs)

        for i, row_con in enumerate(self.board.rows_constraints):
            row_text = ''
            for con in row_con:
                # text = StringVar(value=str(con), )
                row_text += str(con) + ' '
            row_text = row_text[:-1]

            self.canvas.create_text((5, y + row_width // 3 + row_width * i), text=row_text, anchor='nw',
                                    font=('lucida', '9'))

        for i, col_con in enumerate(self.board.cols_constraints):
            col_text = ''
            for con in col_con:
                col_text += str(con) + '\n'
            col_text = col_text[:-1]
            n = col_text.count('\n')
            if n < 14:
                col_text = '\n' * (14 - n) + col_text
            self.canvas.create_text((x + col_width // 3 + col_width * i, 5), text=col_text, anchor='nw',
                                    font=('lucida', '9'))

    def success_msg(self):
        messagebox.showinfo('Success!', 'You Got the Solution!')

    def failed_msg(self):
        messagebox.showerror('Failed', 'You didn\'t find the solution')

    def put_time(self, solve_type, timing):
        loc = LOCS_DICT[solve_type]
        label = Label(self.root, text=str(timing), bg='light green')
        label.place(x=loc[0] - 30, y=loc[1] + 30)
        self.labels.append(label)
        # self.canvas.create_text((loc[0], loc[1] + 30), text=str(timing))
