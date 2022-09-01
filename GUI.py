from tkinter import messagebox
from copy import deepcopy
from config import *
from tkinter import *


class GUI:
    """
    This class handle the gui and all its features.
    """
    def __init__(self, board=None, title="Two Colors Nonogram Game", window_width=GUI_WIDTH, window_height=GUI_HEIGHT,
                 cur_game=None):
        self.__cur_game = cur_game

        self.root = Tk()
        self.root.title(title)
        self.root.configure(background="white")
        my_title = Label(self.root, text="Two Colors Nonogram Game", font=("times new roman", 20, "bold"), bg="white",
                         fg="black")
        my_title.pack(side=TOP)
        self.canvas_width = 800
        self.canvas_height = 700
        self.root.geometry(f'{window_width}x{window_height}')

        self.canvas = Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white",
                             highlightbackground='black')
        self.canvas.place(x=10, y=40)

        # this adds a sound button to the gui, when clicked a music will be played, but we have removed it because it
        # won't play on linux, and we don't know if you will run it on linux or not so, if you're going to run
        # the program on Windows remove the hashtags to add this nice feature.

        # self.__flag = False
        # self.board = None
        # def play_sound():
        #     if not self.__flag and self.board is not None:
        #         self.__flag = True
        #         return PlaySound(r'gui_files\background_music.wav', SND_ALIAS | SND_ASYNC)
        #     else:
        #         self.__flag = False
        #         return PlaySound(None, SND_PURGE)
        # play_sound()
        # sound_icon = PhotoImage(file=r'gui_files\test.png')
        # sound_button = Button(self.root, text="sound", command=play_sound)
        # sound_button.config(height=1, width=5)
        # sound_button.place(x=950, y=1)

        self.board_rectangles_locs = []
        self.board = board

        self.create_board(board)
        self.labels = dict()

        rows_text = Text(self.canvas, bg="grey")
        rows_text.config(height=1, width=3)
        rows_text.place(x=100, y=50)

        columns_text = Text(self.canvas, bg="grey")
        columns_text.config(height=1, width=3)
        columns_text.place(x=140, y=50)

        def new_game():
            try:
                tmp1 = rows_text.get("1.0", "end-1c").replace(' ', '').strip()
                tmp2 = columns_text.get("1.0", "end-1c").replace(' ', '').strip()
                if tmp1 != '' and tmp2 != '':
                    rows_num = int(tmp1)
                    columns_num = int(tmp2)
                elif tmp1 == '' and tmp2 != '':
                    rows_num = self.__cur_game.board.num_rows
                    columns_num = int(tmp2)
                elif tmp1 != '' and tmp2 == '':
                    rows_num = int(tmp1)
                    columns_num = self.__cur_game.board.num_cols
                else:
                    rows_num = self.__cur_game.board.num_rows
                    columns_num = self.__cur_game.board.num_cols
            except Exception:
                rows_num = self.__cur_game.board.num_rows
                columns_num = self.__cur_game.board.num_cols
            self.__cur_game = self.__cur_game.new_game(self.__cur_game, size=(rows_num, columns_num))


        new_game_button = Button(self.canvas, text="new game", command=new_game)
        new_game_button.config(height=1, width=8)
        new_game_button.place(x=100, y=2)

        def clear_func():
            csps = []
            self.__cur_game.csps = []
            for label in self.labels.keys():
                self.labels[label].destroy()

            self.labels = dict()
            for chk_b in check_buttons:
                chk_b.destroy()
            self.__cur_game.board.clear_board()

        clear_button = Button(self.root, text="clear", command=clear_func)
        clear_button.config(height=1, width=5)
        clear_button.place(x=800, y=1)

        choose_label = Label(self.root, text="Choose the way to solve:", bg='white')
        choose_label.place(x=830, y=35)

        def run_brute():
            self.__cur_game.run(BRUTE)

        brute_button = Button(self.root, text="Brute Force", command=run_brute)
        brute_button.config(height=1, width=10)
        brute_button.place(x=865, y=65)

        def run_dfs():
            self.__cur_game.run(DFS)

        dfs_button = Button(self.root, text="DFS", command=run_dfs)
        dfs_button.config(height=1, width=10)
        dfs_button.place(x=865, y=125)

        def run_bfs():
            self.__cur_game.run(BFS)

        bfs_button = Button(self.root, text="BFS", command=run_bfs)
        bfs_button.config(height=1, width=10)
        bfs_button.place(x=865, y=185)

        def run_lbs():
            self.__cur_game.run(LBS, k=lbs_text_box.get("1.0", "end-1c").replace(' ', '').strip())

        lbs_text_box = Text(self.root, bg="grey")
        lbs_text_box.config(height=1, width=3)
        lbs_text_box.place(x=822, y=250)

        lbs_button = Button(self.root, text="LBS", command=run_lbs)
        lbs_button.config(height=1, width=10)
        lbs_button.place(x=865, y=245)

        self.__cur_game.csps = set()

        def add_csp(csp_to_add_or_delete):
            if csp_to_add_or_delete in self.__cur_game.csps:
                self.__cur_game.csps.remove(csp_to_add_or_delete)
            else:
                self.__cur_game.csps.add(csp_to_add_or_delete)

        check_buttons = []

        def select_csps():
            self.__cur_game.csps = set()
            mrv_check = Checkbutton(self.root, text="MRV", command=lambda: add_csp(MRV))
            mrv_check.place(x=865, y=365)

            degree_check = Checkbutton(self.root, text="DEGREE", command=lambda: add_csp(DEGREE))
            degree_check.place(x=865, y=400)

            lcv_check = Checkbutton(self.root, text="LCV", command=lambda: add_csp(LCV))
            lcv_check.place(x=865, y=435)

            fc_check = Checkbutton(self.root, text="FC", command=lambda: add_csp(FC))
            fc_check.place(x=865, y=470)

            ac_check = Checkbutton(self.root, text="AC", command=lambda: add_csp(AC))
            ac_check.place(x=865, y=505)

            run_csp_button = Button(self.root, text="Run CSP", command=run_csp)
            run_csp_button.config(height=1, width=10)
            run_csp_button.place(x=865, y=540)

            check_buttons.append(mrv_check)
            check_buttons.append(degree_check)
            check_buttons.append(lcv_check)
            check_buttons.append(fc_check)
            check_buttons.append(ac_check)
            check_buttons.append(run_csp_button)

        select_csp_button = Button(self.root, text="CSP", command=select_csps)
        select_csp_button.config(height=1, width=10)
        select_csp_button.place(x=865, y=310)

        def run_csp():
            self.__cur_game.run(CSP_P, csps=self.__cur_game.csps)

        def exit_game():
            self.root.destroy()

        exit_button = Button(self.root, text="exit", command=exit_game, background='red')
        exit_button.config(height=1, width=4)
        exit_button.place(x=5, y=1)

    def create_board(self, board):
        self.board = deepcopy(board)

        x, y = 260, 230
        tmp = min((self.canvas_height - y) // self.board.num_rows, (self.canvas_width - x) // self.board.num_cols)
        col_width, row_width = tmp, tmp

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
                row_text += str(con) + ' '
            row_text = row_text[:-1]

            self.canvas.create_text((x - 2, y + row_width // 3 + row_width * i), text=row_text, anchor='e',
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

    def timeout_msg(self):
        messagebox.showerror('Timeout', 'Timeout Reached!')

    def success_time(self, solve_type, timing):
        if solve_type in self.labels.keys():
            self.labels[solve_type].destroy()
            self.labels.pop(solve_type)

        loc = LOCS_DICT[solve_type]
        label = Label(self.root, text=str(timing), bg='light green')
        label.place(x=loc[0] - 30, y=loc[1] + 33)
        self.labels[solve_type] = label

    def failure_time(self, solve_type, timing):
        if solve_type in self.labels.keys():
            self.labels[solve_type].destroy()
            self.labels.pop(solve_type)
        loc = LOCS_DICT[solve_type]
        label = Label(self.root, text=str(timing), bg='red')
        label.place(x=loc[0] - 30, y=loc[1] + 33)
        self.labels[solve_type] = label

    def timeout_time(self, solve_type):
        if solve_type in self.labels.keys():
            self.labels[solve_type].destroy()
            self.labels.pop(solve_type)
        loc = LOCS_DICT[solve_type]
        label = Label(self.root, text="Timeout", bg='red')
        label.place(x=loc[0] - 30, y=loc[1] + 33)
        self.labels[solve_type] = label


