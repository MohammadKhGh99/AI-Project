import random
from config import *
import agent
import csp
import search
import GUI
from Board import *


class Game:
    def __init__(self, csv_file=None, rows_constraints=None, cols_constraints=None, colors=BLACK_WHITE,
                 size=(5, 5), my_agent=None, always_solvable=True):
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
        self.agent = my_agent
        self.always_solvable = always_solvable
        self.state = None
        self.board = None
        # self.gui = None

        if csv_file:
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
        self.board = Board(temp_rows_constraints, temp_cols_constraints)

    def __csv_building(self, csv_file):
        """
            building the board from a csv file
        """
        with open(csv_file, 'r') as f:
            all_lines = f.readlines()

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
        self.board = Board(temp_rows_constraints, temp_cols_constraints)

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
            temp_board = [[Cell(r, c, color=random.choice([WHITE, BLACK, RED])) for c in range(self.num_cols)] for r in
                          range(self.num_rows)]
            temp_rows_constraints, temp_cols_constraints = [], []
            for row in range(self.num_rows):
                seq = 1
                row_constraints = []
                for col in range(self.num_cols):
                    if temp_board[row][col].color != WHITE:
                        cur_color = 'b' if temp_board[row][col].color == BLACK else 'r'
                        if col < self.num_cols - 1:
                            if temp_board[row][col].color == temp_board[row][col + 1].color:
                                seq += 1
                            else:
                                row_constraints.append(Constraint(str(seq) + cur_color))
                                seq = 1
                        else:
                            row_constraints.append(Constraint(str(seq) + cur_color))
                temp_rows_constraints.append(row_constraints)

            for col in range(self.num_cols):
                seq = 1
                col_constraints = []
                for row in range(self.num_rows):
                    if temp_board[row][col].color != WHITE:
                        cur_color = 'b' if temp_board[row][col].color == BLACK else 'r'
                        if row < self.num_rows - 1:
                            if temp_board[row][col].color == temp_board[row + 1][col].color:
                                seq += 1
                            else:
                                col_constraints.append(Constraint(str(seq) + cur_color))
                                seq = 1
                        else:
                            col_constraints.append(Constraint(str(seq) + cur_color))
                temp_cols_constraints.append(col_constraints)

        self.board = Board(temp_rows_constraints, temp_cols_constraints, randomly=True, size=size)

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

    def run(self):
        # runs the brute force algorithm on the board.
        # agent.BruteForce(self.board).brute_force().board.print_board()
        # print("Brute Force")
        # self.board = agent.brute_force(self.board)
        # self.board.print_board()
        # print("BFS")
        nonogram_problem = agent.NonogramProblem(self.board)
        # print(search.breadth_first_search(nonogram_problem).print_board())
        # print(search.breadth_first_search(nonogram_problem))
        # print("DFS")
        # print(search.depth_first_search(nonogram_problem).print_board())
        # print(search.depth_first_search(nonogram_problem))
        print("A*")
        self.board = search.a_star_search(problem=nonogram_problem)
        # self.board.print_board()
        # Board.gui = GUI.GUI(self.board)
        # self.gui.canvas.mainloop()
        # Board.gui.root.mainloop()
        # Board.gui.finish_msg()


if __name__ == "__main__":
    print("Hello World!")

    game = Game(colors=COLORFUL, size=(1, 7))
    # game = Game(colors=COLORFUL, size=(3, 3))
    # game = Game(colors=COLORFUL, size=(5, 5))
    # game = Game(colors=COLORFUL, size=(15, 15))

    csp.run_CSP(game.board)
    game.run()

