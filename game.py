import itertools
import random
import sys
import time

import Board
from config import *
import agent
import csp
import search
from Board import *
import heuristics


class Game:
    first_one = True
    # times_lst = []

    def __init__(self, csv_file=None, rows_constraints=None, cols_constraints=None, size=(5, 5), always_solvable=True,
                 rows_or_cols=ROWS, gui_or_print=IS_GUI, difficulty=HARD, csps=None):
        """
        Initializing the board of the game, we have 3 different ways:
        1) from CSV file
        2) from giving lists of constraints of rows and cols
        3) as random

        the variables above:
        csv_file: if we want to build board from CSV file.
        rows_constraints and cols_constraints: if we want to build board from giving lists.
        size: if the given board is random, with specific size, then we change the size here [DEFAULT is 5x5]
        always_solvable: the random board that will be generated will be always solvable or not.
        rows_or_cols: in EASY mode, do you want to make the board easy by the rows or columns.
        gui_or_print: do you want to present the result as gui or prints on the stdout.
        difficulty: HARD will make a random board with random colors values in each cell, EASY will make an easy random
                    board that will contain some continuous random cells with the same color.
        solve_type: in which way do you want to solve the board, BRUTE, BFS, DFS, ASTAR or CSP_P.
        csps: if the way chosen was CSP_P here will be the types of csps that you want to solve the board by them.
        expected constraints format: if BLACK_WHITE: ^\d+[bB](?:-\d+[bB])*$|^\d+(?:-\d+)*$    examples: 5b-8b, 12, 5-84
                                     if COLORFUL: ^\d+[bBrR](?:-\d+[bBrR])*$    examples: 3b, 5r-15B.

        """
        self.csv_file = csv_file
        self.rows_constraints = rows_constraints
        self.cols_constraints = cols_constraints
        self.size = size
        self.always_solvable = always_solvable
        self.rows_or_cols = rows_or_cols
        self.gui_or_print = gui_or_print
        self.difficulty = difficulty
        self.board = None
        self.csps = set()
        self.times_lst = dict()
        self.ran_before = False

        if csps is not None:
            self.csps.update(set(csps))

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
            self.__our_building(rows_constraints, cols_constraints)
        else:
            """
            create a random board from giving size and color
            in this situation the user or us will enter the colors of the Nonogram Game
            (Back&White or Black&Red&White) and the dimensions of the board, the default size will be 5x5 and
            the default colors will be Black & White.
            """
            self.__random_building(size)

        if Game.first_one and gui_or_print == IS_GUI:
            Board.start_gui(self.board)
        # elif gui_or_print == PRINT:
        #     self.run(solve_type)

    @staticmethod
    def new_game(cur_game):
        Board.gui.root.destroy()
        Board.gui = None
        new_game_object = Game(csv_file=cur_game.csv_file, rows_constraints=cur_game.rows_constraints,
                               cols_constraints=cur_game.cols_constraints, size=cur_game.size,
                               always_solvable=cur_game.always_solvable, rows_or_cols=cur_game.rows_or_cols,
                               gui_or_print=cur_game.gui_or_print, difficulty=cur_game.difficulty, csps=cur_game.csps)
        if Board.gui is None:
            Board.start_gui(new_game_object.board)
        # Game.times_lst = []
        Game.first_one = True
        return new_game_object

    def __our_building(self, rows_constraints, cols_constraints):
        """
        This function build the board by our choice.
        Parameters:
            rows_constraints: the rows constraints
            cols_constraints: the cols constraints
        """
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

        lines = [line for line in all_lines if line.replace(' ', '') != '']

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
        """
        This function builds rows constraints from the given board
        """
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
        """
        This function builds columns constraints from the given board
        """
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
        """
        This function builds a board with easy mode, this means that we will see several times a continuous random
        cells with the same color, we can build easy board with this technique by rows or columns.
        """
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

    def __random_building(self, size):
        """
        building a board randomly from giving size and colors
        """
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
                # builds an easy mode board with continuous random cells with tehe same color.
                temp_board = [[Cell(r, c) for c in range(self.num_cols)] for r in range(self.num_rows)]
                if self.rows_or_cols == COLUMNS:
                    temp_cols_constraints = Game.__build_easy(self.num_cols, self.num_rows, temp_board,
                                                              temp_cols_constraints, rows_cols=COLUMNS)
                    temp_rows_constraints = self.__build_rows_constraints(temp_board, temp_rows_constraints)
                else:
                    temp_rows_constraints = Game.__build_easy(self.num_rows, self.num_cols, temp_board,
                                                              temp_rows_constraints, rows_cols=ROWS)
                    temp_cols_constraints = self.__build_cols_constraints(temp_board, temp_cols_constraints)
            else:  # HARD mode
                # builds a hard mode board, by building a fully random board then building the appropriate constraints
                # for it then empty it.
                temp_board = [[Cell(r, c, color=random.choice(COLORS_LST)) for c in range(self.num_cols)] for r in
                              range(self.num_rows)]

                # check if there is any empty column, if yes fill one cell in random way with random color
                for c in range(len(temp_board[0])):
                    all_empty = True
                    for r in range(len(temp_board)):
                        if temp_board[r][c].color != EMPTY and temp_board[r][c].color != WHITE:
                            all_empty = False
                            break
                    if all_empty:
                        row = random.randint(0, len(temp_board) - 1)
                        temp_board[row][c].color = random.choice(COLORS_LST_WITHOUT_WHITE)

                # check if there is any empty column, if yes fill one cell in random way with random color
                for r in range(len(temp_board)):
                    all_empty = True
                    for c in range(len(temp_board[0])):
                        if temp_board[r][c].color != EMPTY and temp_board[r][c].color != WHITE:
                            all_empty = False
                            break
                    if all_empty:
                        col = random.randint(0, len(temp_board[0]) - 1)
                        temp_board[r][col].color = random.choice(COLORS_LST_WITHOUT_WHITE)

                # builds the constraints
                temp_rows_constraints = self.__build_rows_constraints(temp_board, temp_rows_constraints)
                temp_cols_constraints = self.__build_cols_constraints(temp_board, temp_cols_constraints)

        self.board = Board(temp_rows_constraints, temp_cols_constraints, randomly=True, size=size, cur_game=self)

    def __build_constraints(self, m, n):
        """
        This function builds constraints for not always solvable board.
        """
        all_constraints = []

        for j in range(m):
            i = 0
            constraint_lst = []
            while i < n:
                num = random.randint(1, n - i)
                color = random.choice(COLORS_LST_WITHOUT_WHITE)

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

    def run(self, solve_type, k=1, heu=0):
        """
        This function runs the game with the given solve type.
        """
        # if this is no the first time we run this function, we clear the board.
        if not Game.first_one:
            self.board.clear_board()
            if Board.gui is not None:
                Board.gui.board = deepcopy(self.board)

        resulted_board = None
        if Game.first_one:
            Game.first_one = False

        cur_gui = self.board.gui

        Board.before_time = time.time()
        if solve_type == BRUTE:
            print("Brute Force")
            result = agent.BruteForce(self.board).brute_force()
            resulted_board = result.board if result else None
        else:
            bfs_problem = agent.NonogramCellsProblem(self.board, BFS)
            lbs_problem = agent.NonogramCellsProblem(self.board, LBS)
            dfs_problem = agent.NonogramCellsProblem(self.board, DFS)
            astar_problem = agent.NonogramCellsProblem(self.board, ASTAR)
            # bfs_problem = agent.BFSProblem(self.board)
            constraint_dfs = agent.NonogramConstraintsProblem(self.board)
            constraint_astar = agent.NonogramConstraintsProblem(self.board, search.lowest_combinations_heuristic)
            if solve_type == BFS:
                print("BFS")
                resulted_board = search.breadth_first_search(problem=bfs_problem)
            elif solve_type == DFS:
                print("DFS")
                resulted_board = search.depth_first_search(problem=constraint_dfs)
            elif solve_type == ASTAR:
                print("A*")
                resulted_board = search.a_star_search(problem=constraint_astar)
            elif solve_type == LBS:
                print("LBS")
                resulted_board = search.local_beam_search(problem=lbs_problem, k=k)
            elif solve_type == CSP_P:
                print("CSP")
                print(self.ran_before)
                resulted_board = csp.run_CSP(self.board, types_of_csps=self.csps, same_board=self.ran_before)
                self.ran_before = True

        after = time.time()
        all_time = after - Board.before_time - Board.different_time
        print(f"Time:  {all_time} Seconds")

        self.times_lst[solve_type] = [all_time]

        if self.gui_or_print == IS_GUI:
            if resulted_board is not None and type(resulted_board) is not int:
                resulted_board.print_board()
                # show time of the running algorithm
                resulted_board.gui.success_time(solve_type, all_time)
                Board.gui.success_msg()
            else:
                cur_gui.failure_time(solve_type, all_time)
                Board.gui.failed_msg()
            # to keep the window running
            Board.gui.root.mainloop()
        elif self.gui_or_print == PRINT:
            if resulted_board is not None and type(resulted_board) is not int:
                print(f"Success!\nYou Got the Solution, Time Taken: {all_time}")
                print("This is the resulted board:")
                resulted_board.print_board()
                print("End")
            else:
                print(f"Failure!\nYou didn\'t find the Solution, Time Taken: {all_time}")
                print("End")


def main():
    # All combinations of all the csp's types
    combs = []
    for i in range(1, len(ALL_CSPS) + 1):
        combs.append(list(itertools.combinations(ALL_CSPS, i)))

    print("\nTwo Colors Nonogram Game - Wellcome!\n")
    # size, rows_or_cols, difficulty, csps
    print("\nTesting the Algorithms with 5x5 random board...\n")


    # Finding which one of the algorithms is the fastest one in finding out that there is no solution.
    print("\nNot Solvable:\n")
    not_solvable_boards = []
    for _ in range(10):
        csps = {}
        my_game = Game(size=(5, 5), difficulty=HARD, csps=csps, gui_or_print=PRINT)
        for solve_type in ALL_ALGOS:
            for _ in range(5):
                my_game.run(solve_type)
            print(f"Didn\'t Find Solution in Average Time is {sum(my_game.times_lst[solve_type])} Seconds for {solve_type}\n")

    # todo - make easy mode just for large board like 8x8 or 10x10
    # Which of the algorithms is the fastest one in finding the solution if the board made as the rows are easy.
    print("\nEasy Mode (By Rows):\n")
    csps = {}
    my_game = Game(size=(8, 8), difficulty=EASY, csps=csps, rows_or_cols=ROWS, gui_or_print=PRINT)
    for solve_type in ALL_ALGOS:
        for _ in range(5):
            my_game.run(solve_type)
        print(f"Average Time for {solve_type} is {sum(my_game.times_lst[solve_type])} Seconds\n")

    # Which of the algorithms is the fastest one in finding the solution if the board made as the columns are easy.
    print("\nEasy Mode (By Columns):\n")
    csps = {}
    my_game = Game(size=(8, 8), difficulty=EASY, csps=csps, rows_or_cols=COLUMNS, gui_or_print=PRINT)
    for solve_type in ALL_ALGOS:
        for _ in range(5):
            my_game.run(solve_type)
        print(f"Average Time for {solve_type} is {sum(my_game.times_lst[solve_type])} Seconds\n")

    # Which of the algorithms is the fastest one in finding the solution if the board made as hard to solve.
    print("\nHard Mode:\n")
    csps = {}
    my_game = Game(size=(5, 5), difficulty=HARD, csps=csps, gui_or_print=PRINT)
    for solve_type in ALL_ALGOS:
        for _ in range(5):
            my_game.run(solve_type)
        print(f"Average Time for {solve_type} is {sum(my_game.times_lst[solve_type])} Seconds\n")

    print("Now we will test larger boards with hard mode and different csps:\n")
    # Sizes
    print("\n7x7 Board:\n")
    csps = {}
    my_game = Game(size=(7, 7), difficulty=HARD, csps=csps, gui_or_print=PRINT)
    for solve_type in ALL_ALGOS:
        for _ in range(5):
            my_game.run(solve_type)
        print(f"Average Time for {solve_type} is {sum(my_game.times_lst[solve_type])} Seconds\n")

    print("\n8x8 Board:\n")
    csps = {}
    my_game = Game(size=(8, 8), difficulty=HARD, csps=csps, gui_or_print=PRINT)
    for solve_type in ALL_ALGOS:
        for _ in range(5):
            my_game.run(solve_type)
        print(f"Average Time for {solve_type} is {sum(my_game.times_lst[solve_type])} Seconds\n")


if __name__ == "__main__":
    # print("Hello World!")
    # main()

    # game = Game(colors=COLORFUL, size=(9, 9), difficulty=HARD, gui_or_print=IS_GUI)
    game = Game( size=(20, 20), difficulty=EASY, gui_or_print=PRINT)
    # game = Game(csv_file='example1.csv', gui_or_print=IS_GUI)
    # game = Game(difficulty=HARD, size=(7, 7), gui_or_print=IS_GUI, csps=ALL_CSPS)
    game.run(ASTAR)
    # Brute Force can solve up to 31x31 boards - the others will come to maximum recursion depth Error
    # game = Game(colors=COLORFUL, size=(7, 7), difficulty=HARD, gui_or_print=IS_GUI, solve_type=BRUTE)

    # game.run(solve_type=CSP_P)
