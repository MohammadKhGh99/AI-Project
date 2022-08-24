import random
from config import *
import agent
from copy import deepcopy
import search


class Board:

    # delete - board argument, it's just for testing bro!

    def __init__(self, rows_constraints, cols_constraints, randomly=False, size=(5, 5), board=None):
        self.rows_constraints = rows_constraints
        self.cols_constraints = cols_constraints

        if not randomly:
            self.num_rows = len(self.rows_constraints)
            self.num_cols = len(self.cols_constraints)
        else:
            self.num_rows, self.num_cols = size

        self.board = board if board else [[Cell() for _ in range(self.num_cols)] for _ in range(self.num_rows)]
        # self.board = [[Cell() for _ in range(self.num_cols)] for _ in range(self.num_rows)]
        self.flipped = [[Cell() for _ in range(self.num_rows)] for _ in range(self.num_cols)]

    def fill(self, r, c, color):
        if r < self.num_rows and c < self.num_cols and self.get_cell(r, c).color == EMPTY:
            self.board[r][c].color = color
            self.flipped[c][r].color = color
            return True
        return False

    def get_cell(self, r, c, flipped=False):
        return self.board[r][c] if not flipped else self.flipped[c][r]

    def print_board(self):
        # if we got None from an agent, this means that there is no solution for the board.
        if self.board is None:
            return None
        text = ""

        # gets the longest row's length
        max_row, max_col = None, None
        m, n = 0, 0
        for row in self.rows_constraints:
            if len(row) > m:
                m = len(row)
                max_row = row
        # gets the longest column's length
        for col in self.cols_constraints:
            if len(col) > n:
                n = len(col)

        # this thing just for the design 😁.
        text += " " * (len(max_row) * 6)
        row_space = text
        text += ("-" * (6 * self.num_cols + 2)) + f"\n{row_space}"
        text += "|| "

        # adding the column constraints.
        for i in range(n - 1, -1, -1):
            for col in self.cols_constraints:
                cur = col[::-1]
                if i >= len(cur):
                    text += "    | "
                elif len(cur[i]) == 2:
                    text += f"{cur[i]}  | "
                elif len(cur[i]) == 3:
                    text += f"{cur[i]} | "

            # adding a line separator between the column constraints and the board itself.
            if i == 0:
                text += f"\n" + ("=" * (len(row_space) + self.num_cols * 6 + 2)) + f"\n{row_space}| "
            else:
                text += f"\n{row_space}" + ("-" * (self.num_cols * 6 + 2)) + f"\n{row_space}|| "
        # remove the last unnecessary '|'
        text = text[:-1]
        text = text[:len(text) - len(row_space) - 1] + "|"

        # adding the structure of each row with the current content of the board beside the rows constraints.
        for j, row in enumerate(self.rows_constraints):
            for i in range(m - 1, -1, -1):
                cur = row[::-1]
                if i >= len(cur):
                    text += "     |"
                elif len(cur[i]) == 2:
                    text += f" {cur[i]}  |"
                elif len(cur[i]) == 3:
                    text += f" {cur[i]} |"
            text += "|"
            for y in self.board[j]:
                x = str(y)
                if int(x) == EMPTY:
                    text += "     |"
                elif int(x) == WHITE:
                    text += f"  w  |"
                elif int(x) == BLACK:
                    text += f"  b  |"
                elif int(x) == RED:
                    text += f"  r  |"
            tmp = 2 + (m + self.num_cols) * 6
            text += "\n" + ("-" * tmp) + "\n|"

        return text[:-1]

    def get_first_incomplete_constraint(self, constraint_type):
        """
        Find first incomplete constraint in columns or rows constraints.
        constrain_type: on which constraints list we will work: columns or rows
        Return the coordinates of the incomplete constraints, None, if all constraints are completed
        """
        if constraint_type:
            constraints_group = self.cols_constraints
        else:
            constraints_group = self.rows_constraints

        for i in range(len(constraints_group)):
            for j in range(len(constraints_group[i])):
                if not constraints_group[i][j].completed:
                    return i, j
        return None

    def complete_constraints(self, con_i, con_j, constraint_type=COLUMNS):
        """
        Function change the status of the given constraint to completed (True)
        constraint_type: on which constraints list we will work: columns or rows.
        con_i: the index of the working constraints group.
        con_j: the index of the working constraint in the group.
        """
        if constraint_type:
            self.cols_constraints[con_i][con_j].completed = True
        else:
            self.rows_constraints[con_i][con_j].completed = True

    def fill_n_cells(self, con_i, con_j, start_index, constraint_type=COLUMNS):
        """
        Function fill the board, in a valid way. It fills n cells according to the given constraint.
        constraint_type: on which constraints list we will work: columns or rows.
        con_i: the index of the working constraints group.
        con_j: the index of the working constraint in the group.
        start_index: from where to start to fill (row/column)
        """
        child = deepcopy(self)
        if constraint_type:
            constraint = child.cols_constraints[con_i][con_j]
            for i in range(constraint.number):
                if child.fill(i + start_index, con_i, constraint.color) \
                        and agent.check_move(child, con_i, i + start_index):
                    continue
                else:
                    return None

        else:
            constraint = child.rows_constraints[con_i][con_j]
            for i in range(constraint.number):
                if child.fill(con_i, i + start_index, constraint.color) \
                        and agent.check_move(child, con_i, i + start_index):
                    continue
                else:
                    return None
        child.complete_constraints(con_i, con_j, constraint_type)
        return child


class Constraint:
    """
    This class describes the constraints cells with number, status and color (Black, Red).
    """

    def __init__(self, constraint, m=None):
        self.completed = False
        if constraint == '':
            self.number = None
        else:
            try:
                self.number = int(constraint[:-1])
            except Exception:
                # print(constraint)
                raise Exception("constraint structure should be like this")

            self.c = constraint[-1]

            if self.c.lower() not in COLORS:
                raise Exception("error in choosing color for constraint")
            else:
                self.color = BLACK if self.c.lower() == 'b' else RED

    def __str__(self):
        return str(self.number) + self.c

    def __len__(self):
        return len(self.__str__())


class Cell:
    """
    the cells of the board. each cell has a color: WHITE, Black or RED. (DEFAULT=WHITE)
    """

    def __init__(self, color=EMPTY):
        self.color = color
        self.current_state = 0  # check: idk what is this | me neither

    def __str__(self):
        return str(self.color)


class Game:
    def __init__(self, csv_file=None, rows_constraints=None, cols_constraints=None, colors=BLACK_WHITE,
                 size=(5, 5), agent=None, always_solvable=True):
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
        self.agent = agent  # check: i'm not sure what is this
        self.state = None  # check: i'm not sure what is this
        self.always_solvable = always_solvable
        self.board = None

        if csv_file:
            # create a board from csv file.

            self.__csv_building(csv_file)
        elif rows_constraints and cols_constraints:
            # create a board from a giving rows and cols constraints lists.
            # the rows constraints and columns constraints should be as the following structure:
            #       rows_constraints = ["row 1 constraint", "row 2 constraint",...,"row n constraint"]
            #       cols_constraints = ["column 1 constraint", "column 2 constraint",...,"column n constraint"]
            # this means that each one of rows_constraints and cols_constraints should be as list of strings and each
            # string is the constraint of the row in its place.

            self.__our_building(colors, rows_constraints, cols_constraints)
        else:
            # create a random board from giving size and color
            # in this situation the user or us will enter the colors of the Nonogram Game
            # (Back&White or Black&Red&White) and the dimensions of the board, the default size will be 5x5 and
            # the default colors will be Black&White.

            self.__random_building(size, colors)

        # self.__flipped = list(map(list, zip(*self.board)))

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
            expecting format to be: brw
                                    ,3b,2r-3b,1b
                                    2r,,,,
                                    3b,,,,
                                    1b-3r,,,,

        """
        with open(csv_file, 'r') as f:
            lines = f.readlines()

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
            temp_board = [[Cell(color=random.choice([WHITE, BLACK, RED])) for _ in range(self.num_cols)] for _ in
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
        colors_lst = []
        if self.colors == BLACK_WHITE:
            colors_lst = ['b']
        elif self.colors == COLORFUL:
            colors_lst = ['b', 'r']

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
        print("Brute Force")
        # self.board = agent.brute_force(self.board)
        # print(self.board.print_board())
        # print("BFS")
        nonogram_problem = agent.NonogramProblem(self.board)
        # print(search.breadth_first_search(nonogram_problem))
        print("DFS")
        print(search.depth_first_search(nonogram_problem).print_board())
        # print("A*")
        # print(search.a_star_search(problem=nonogram_problem))


if __name__ == "__main__":
    print("Hello World!")
    game = Game(csv_file='example1.csv')
    # game = Game(colors=COLORFUL)

    # import graphics
    # gui = graphics.NonogramGUI("Nonogram")
    # gui.draw_board(game.board.board)
    # gui.master.mainloop()
    print(game.board.print_board())
    game.run()
    print(game.board.print_board())
