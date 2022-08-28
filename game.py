import random
import sys
import time

import Board
from config import *
import agent
import csp
import search
from Board import *


class Game:
    first_one = True

    def __init__(self, csv_file=None, rows_constraints=None, cols_constraints=None, colors=BLACK_WHITE,
                 size=(5, 5), always_solvable=True, rows_or_cols=ROWS, gui_or_print=IS_GUI, difficulty=EASY,
                 solve_type=BRUTE):
        """
        Initializing the board of the game, we have 3 different ways:
        1) from CSV file
        2) from giving lists of constraints of rows and cols
        3) as random

        the variables above:
        csv_file: if we want to build board from CSV file.
        rows_constraints and cols_constraints: if we want to build board from giving lists.
        colors: we have two options - BLACK_WHITE: black and white board (two colors) [DEFAULT option]
                                    - COLORFUL: red, black and white board (three colors)
        size: if the given board is random, with specific size, then we change the size here [DEFAULT is 5x5]

        expected constraints format: if BLACK_WHITE: ^\d+[bB](?:-\d+[bB])*$|^\d+(?:-\d+)*$    examples: 5b-8b, 12, 5-84
                                     if COLORFUL: ^\d+[bBrR](?:-\d+[bBrR])*$    examples: 3b, 5r-15B.

        """
        self.csv_file = csv_file
        self.rows_constraints = rows_constraints
        self.cols_constraints = cols_constraints
        self.colors = colors
        self.size = size
        self.always_solvable = always_solvable
        self.rows_or_cols = rows_or_cols
        self.gui_or_print = gui_or_print
        self.difficulty = difficulty
        self.board = None

        if self.csv_file:
            """
            create a board from csv file.
            in the first line: a variation of the colors 'b' 'r' 'w' or just 'b' 'w'
            the second line: the columns constraints.
            the other lines: the rows constraints
            example:
            expecting format to be: [brw]|[bwr]|[wrb]|[wbr]|[rbw]|[rwb]
                                    ,3b,2r-3b,1b
                                    2r,,,,
                                    3b,,,,
                                    1b-3r,,,,
            """
            self.__csv_building(csv_file)
        elif rows_constraints and cols_constraints:
            """ 
            create a board from a giving rows and cols constraints lists.
            the rows constraints and columns constraints should be as the following structure:
                   rows_constraints = ["row 1 constraint", "row 2 constraint",...,"row n constraint"]
                   cols_constraints = ["column 1 constraint", "column 2 constraint",...,"column n constraint"]
            this means that each one of rows_constraints and cols_constraints should be as list of strings and each
            string is the constraint of the row in its place.
            """
            self.__our_building(colors, rows_constraints, cols_constraints)
        else:
            """
            create a random board from giving size and color
            in this situation the user or us will enter the colors of the Nonogram Game
            (Back&White or Black&Red&White) and the dimensions of the board, the default size will be 5x5 and
            the default colors will be Black & White.
            """
            self.__random_building(size, colors)

        if Game.first_one and gui_or_print == IS_GUI:
            Board.start_gui(self.board)
        elif gui_or_print == PRINT:
            self.run(solve_type)

    @staticmethod
    def new_game(cur_game):
        Board.gui.root.destroy()
        # Board.gui.canvas.delete('all')
        # print(Game.first_one)
        new_game_object = Game(csv_file=cur_game.csv_file, rows_constraints=cur_game.rows_constraints,
                               cols_constraints=cur_game.cols_constraints, colors=cur_game.colors, size=cur_game.size,
                               always_solvable=cur_game.always_solvable, rows_or_cols=cur_game.rows_or_cols,
                               gui_or_print=cur_game.gui_or_print, difficulty=cur_game.difficulty)
        if Board.gui is None:
            Board.start_gui(new_game_object.board)
        # Board.gui.create_board(new_game_object.board)
        Game.first_one = True
        return new_game_object

    def __our_building(self, colors, rows_constraints, cols_constraints):
        """
        This function build the board by our choice.
        Parameters:
            colors: the colors of the Nonogram Game.
            rows_constraints: the rows constraints
            cols_constraints: the cols constraints
        """
        self.colors = colors

        # remove the '-' between each constraint and put it in a cell in a list of a row constraints.
        temp_rows_constraints = [list(map(lambda x: Constraint(x), row.split('-'))) for row in rows_constraints]

        # remove the '-' between each constraint and put it in a cell in a list of a column constraints.
        temp_cols_constraints = [list(map(lambda x: Constraint(x), col.split('-'))) for col in cols_constraints]

        # build a new empty board with the given constraints.
        self.board = Board(temp_rows_constraints, temp_cols_constraints, cur_game=self)

    def __csv_building(self, csv_file):
        """
            building the board from a csv file
        """
        with open(csv_file, 'r') as f:
            all_lines = f.readlines()

        # todo - this tries to take just the lines that have something in them and not empty lines.
        # check - so check it !
        lines = [line for line in all_lines if line.replace(' ', '') != '']

        self.colors = lines[3:6]

        # take the second row in csv file, the columns constraints and put each constraint in a list in a
        # list of columns constraints.
        temp_cols_constraints = list(map(lambda x: x.split('-'), lines[1][1:].strip().split(',')))
        temp_cols_constraints = list(map(lambda l: [Constraint(x) for x in l], temp_cols_constraints))

        # take the third row and so on in csv file, the rows constraints and put each constraint in a list in a
        # list of rows constraints.
        temp_rows_constraints = list(map(lambda x: x[:x.index(',')].split('-'), lines[2:]))
        temp_rows_constraints = list(map(lambda l: [Constraint(x) for x in l], temp_rows_constraints))

        # build the board as empty board.# build the board as empty board.
        self.board = Board(temp_rows_constraints, temp_cols_constraints, cur_game=self)

    def __build_rows_constraints(self, temp_board, temp_rows_constraints):
        for row in range(self.num_rows):
            seq = 1
            row_constraints = []
            for col in range(self.num_cols):
                if temp_board[row][col].color != WHITE:
                    cur_color = COLORS_N_DICT[temp_board[row][col].color]
                    if col < self.num_cols - 1:
                        if temp_board[row][col].color == temp_board[row][col + 1].color:
                            seq += 1
                        else:
                            row_constraints.append(Constraint(str(seq) + cur_color))
                            seq = 1
                    else:
                        row_constraints.append(Constraint(str(seq) + cur_color))
            temp_rows_constraints.append(row_constraints)
        return temp_rows_constraints

    def __build_cols_constraints(self, temp_board, temp_cols_constraints):
        for col in range(self.num_cols):
            seq = 1
            col_constraints = []
            for row in range(self.num_rows):
                if temp_board[row][col].color != WHITE:
                    cur_color = COLORS_N_DICT[temp_board[row][col].color]
                    if row < self.num_rows - 1:
                        if temp_board[row][col].color == temp_board[row + 1][col].color:
                            seq += 1
                        else:
                            col_constraints.append(Constraint(str(seq) + cur_color))
                            seq = 1
                    else:
                        col_constraints.append(Constraint(str(seq) + cur_color))
            temp_cols_constraints.append(col_constraints)
        return temp_cols_constraints

    @staticmethod
    def __build_easy(m, n, temp_board, temp_constraints, rows_cols=ROWS):
        for i in range(m):
            con_lst = []
            j = 0
            while j < n:
                ran_len = random.randint(1, n - j)
                color = random.choice(COLORS_LST_WITHOUT_WHITE)
                for k in range(j, j + ran_len):
                    if rows_cols == ROWS:
                        temp_board[i][k].color = color
                    else:
                        temp_board[k][i].color = color
                if j + ran_len < n:
                    if rows_cols == ROWS:
                        temp_board[i][j + ran_len].color = WHITE
                    else:
                        temp_board[j + ran_len][i].color = WHITE
                j += (ran_len + 1)
                con_lst.append(Constraint(str(ran_len) + COLORS_N_DICT[color]))
            temp_constraints.append(con_lst)
        return temp_constraints

    def __random_building(self, size, colors):
        """
                building a board randomly from giving size and colors
                """
        self.colors = colors
        self.num_rows = size[0]
        self.num_cols = size[1]

        # build the board as empty board.# build the board as empty board.

        if not self.always_solvable:
            # build the random constraints of columns and rows.
            temp_rows_constraints = self.__build_constraints(size[0], random.randint(1, size[1]))
            temp_cols_constraints = self.__build_constraints(size[1], random.randint(1, size[0]))
        else:
            # build an always solvable board, then build its constraints.
            temp_rows_constraints, temp_cols_constraints = [], []

            if self.difficulty == EASY:
                temp_board = [[Cell(r, c) for c in range(self.num_cols)] for r in range(self.num_rows)]
                if self.rows_or_cols == COLUMNS:
                    temp_cols_constraints = Game.__build_easy(self.num_cols, self.num_rows, temp_board,
                                                              temp_cols_constraints, rows_cols=COLUMNS)
                    temp_rows_constraints = self.__build_rows_constraints(temp_board, temp_rows_constraints)
                else:
                    temp_rows_constraints = Game.__build_easy(self.num_rows, self.num_cols, temp_board,
                                                              temp_rows_constraints, rows_cols=ROWS)
                    temp_cols_constraints = self.__build_cols_constraints(temp_board, temp_cols_constraints)
            else:
                temp_board = [[Cell(r, c, color=random.choice(COLORS_LST)) for c in range(self.num_cols)] for r in
                              range(self.num_rows)]

                for c in range(len(temp_board[0])):
                    all_empty = True
                    for r in range(len(temp_board)):
                        if temp_board[r][c].color != EMPTY:
                            all_empty = False
                            break
                    if all_empty:
                        r = random.randint(0, len(temp_board))
                        temp_board[r][c].color = random.choice(COLORS_LST_WITHOUT_WHITE)

                temp_rows_constraints = self.__build_rows_constraints(temp_board, temp_rows_constraints)
                temp_cols_constraints = self.__build_cols_constraints(temp_board, temp_cols_constraints)

        self.board = Board(temp_rows_constraints, temp_cols_constraints, randomly=True, size=size, cur_game=self)

    def __build_constraints(self, m, n):
        all_constraints = []
        colors_lst = ['b']
        if self.colors == COLORFUL:
            colors_lst.append('r')

        for j in range(m):
            i = 0
            constraint_lst = []
            while i < n:
                num = random.randint(1, n - i)
                color = random.choice(colors_lst)

                # if the current color is the same as the previous color and there is no room for it,
                # we should try again and choose another color or number of colored cells by this color.
                if len(constraint_lst) >= 1 and constraint_lst[-1].color == color:
                    if i + num + 1 >= n:
                        continue

                constraint_lst.append(Constraint(str(num) + color))

                if len(constraint_lst) > 1:
                    # if the current color is the same as the previous color, we should add to the i the same number
                    # plus 1 because a white cell should be between these two constraints.
                    if constraint_lst[-2].color == color:
                        i += (num + 1)
                    else:
                        i += num
                else:
                    i += num
            all_constraints.append(constraint_lst)
        return all_constraints

    def run(self, solve_type, csps=None):
        # runs the brute force algorithm on the board.
        # print(Game.first_one)
        if not Game.first_one:
            self.board.clear_board()
            if Board.gui is not None:
                Board.gui.board = deepcopy(self.board)

        # Board.start_gui(self.board)
        resulted_board = None
        if Game.first_one:
            Game.first_one = False
        Board.before_time = time.time()
        # before = time.time()
        if solve_type == BRUTE:
            print("Brute Force")
            result = agent.BruteForce(self.board).brute_force()
            resulted_board = result.board if result else None
        else:
            nonogram_problem = agent.NonogramProblem(self.board)
            if solve_type == BFS:
                print("BFS")
                resulted_board = search.breadth_first_search(problem=nonogram_problem)
            elif solve_type == DFS:
                print("DFS")
                # self.board.print_board()
                resulted_board = search.depth_first_search(problem=nonogram_problem)
            elif solve_type == ASTAR:
                print("A*")
                # self.board.print_board()
                resulted_board = search.a_star_search(problem=nonogram_problem)
            elif solve_type == CSP_P:
                print("CSP")
                # self.board.print_board()
                resulted_board = csp.run_CSP(self.board, types_of_csps=csps)

        after = time.time()

        all_time = after - Board.before_time - Board.different_time
        print(f"Time:  {all_time}")

        # show time of the running algorithm
        # self.board.gui.put_time(solve_type, after - before)

        if self.gui_or_print:
            # gui_helper(self.board, solve_type)
            if resulted_board is not None and type(resulted_board) is not int:
                resulted_board.gui.put_time(solve_type, all_time)
                Board.gui.success_msg()
            else:
                Board.gui.failed_msg()
            Board.gui.root.mainloop()
        else:
            if resulted_board is not None and type(resulted_board) is not int:
                print(f"Success!\nYou Got the Solution, Time Taken: {all_time}")
                print("This is the resulted board:")
                resulted_board.print_board()
                print("End")
            else:
                print(f"Failure!\nYou didn\'t find the Solution, Time Taken: {all_time}")
                print("End")
        # Game.first_one = False


def gui_helper(board, solve_type):
    # if solve_type == BRUTE:
    # Board.gui.canvas.delete('rect')
    for r in range(board.num_rows):
        for c in range(board.num_cols):
            time.sleep(0.1)
            temp = Board.gui.board_rectangles_locs[r][c]
            Board.gui.canvas.create_rectangle(temp[0], temp[1], temp[2], temp[3],
                                              fill=COLORS_DICT[repr(board.board[r][c])], tags='rect')
            Board.gui.root.update()
    # elif solve_type == DFS or solve_type == BFS or solve_type == ASTAR:
    #     for cell in Board.moves:
    #         # r, c = move
    #         r, c = cell.row, cell.col
    #         # time.sleep(0.1)
    #         temp = Board.gui.board_rectangles_locs[r][c]
    #         Board.gui.canvas.create_rectangle(temp[0], temp[1], temp[2], temp[3],
    #                                           fill=COLORS_DICT[repr(board.board[r][c])], tags='rect')
    #         Board.gui.root.update()


def main():
    print("\nTwo Colors Nonogram Game - Wellcome!\n")
    # inputs = sys.argv[1:]
    # todo - what about letting the user enter constraints?

    print("Testing the Algorithms with 5x5 random board...\n")
    print("Not Always Solvable:\n")
    my_game = Game(colors=COLORFUL, size=(5, 5), always_solvable=False, gui_or_print=PRINT)
    for solve_type in ALL_ALGOS:
        my_game.run(solve_type)

    print("Always Solvable:\n")
    print("Easy Mode (By Rows):")

    # game = Game(colos=COLORFUL, size=(5, 5), )


if __name__ == "__main__":
    # print("Hello World!")
    # main()


    # game = Game(colors=COLORFUL, size=(9, 9), difficulty=HARD, gui_or_print=IS_GUI)
    # game = Game(colors=COLORFUL, size=(20, 20), difficulty=HARD, gui_or_print=IS_GUI)
    # game = Game(csv_file='example1.csv')
    game = Game(colors=COLORFUL, difficulty=HARD)

    # Brute Force can solve up to 31x31 boards - the others will come to maximum recursion depth Error
    # game = Game(colors=COLORFUL, size=(7, 7), difficulty=HARD, gui_or_print=IS_GUI, solve_type=BRUTE)

    # game.run(solve_type=CSP_P)
