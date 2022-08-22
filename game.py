import random
from config import *
import agent


# rows and columns constraints
# board list of lists
# fill cell
class Board:
    def __init__(self, rows_constraints, cols_constraints, randomly=False, size=(5, 5)):
        self.rows_constraints = rows_constraints
        self.cols_constraints = cols_constraints
        if not randomly:
            self.num_rows = len(self.rows_constraints)
            self.num_cols = len(self.cols_constraints)
        else:
            self.num_rows, self.num_cols = size
        self.board = [[Cell() for _ in range(self.num_cols)] for _ in range(self.num_rows)]
        self.flipped = [[Cell() for _ in range(self.num_rows)] for _ in range(self.num_cols)]

    def fill(self, r, c, color):
        self.board[r][c].color = color
        self.flipped[c][r].color = color

    def get_cell(self, r, c, flipped=False):
        return self.board[r][c] if not flipped else self.flipped[c][r]


# todo - add True and False if holds or not
class Constraint:
    """
    This class describes the constraints cells with number and color (Black, Red).
    """
    def __init__(self, constraint):
        self.status = False

        try:
            self.number = int(constraint[:-1])
        except Exception:
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
        # self.c = ""
        # if self.color == EMPTY:
        #     self.c = " "
        # elif self.color == WHITE:
        #     self.c = "w"
        # elif self.color == BLACK:
        #     self.c = "b"
        # elif self.color == RED:
        #     self.c = "r"
        self.current_state = 0  # check: idk what is this | me neither

    def __str__(self):
        return str(self.color)


class Game:
    def __init__(self, csv_file=None, rows_constraints=None, cols_constraints=None, colors=BLACK_WHITE,
                 size=(5, 5), agent=None):
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
        self.state = None   # check: i'm not sure what is this

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

        temp_rows_constraints = rows_constraints
        temp_cols_constraints = cols_constraints

        # remove the '-' between each constraint and put it in a cell in a list of a row constraints.
        temp_rows_constraints = [list(map(lambda x: Constraint(x), row.split('-'))) for row in temp_rows_constraints]

        # remove the '-' between each constraint and put it in a cell in a list of a column constraints.
        temp_cols_constraints = [list(map(lambda x: Constraint(x), col.split('-'))) for col in temp_cols_constraints]

        # self.num_of_rows = len(rows_constraints)
        # self.num_of_cols = len(cols_constraints)

        self.board = Board(temp_rows_constraints, temp_cols_constraints)

        # self.board = [[Cell() for _ in range(self.num_of_cols)] for _ in range(self.num_of_rows)]

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
        # print(lines[1][1:])
        temp_cols_constraints = list(map(lambda x: x.split('-'), lines[1][1:].strip().split(',')))
        temp_cols_constraints = list(map(lambda l: [Constraint(x) for x in l], temp_cols_constraints))

        # self.cols_constraints = temp_cols_constraints

        # take the third row and so on in csv file, the rows constraints and put each constraint in a list in a
        # list of rows constraints.
        temp_rows_constraints = list(map(lambda x: x[:x.index(',')].split('-'), lines[2:]))
        temp_rows_constraints = list(map(lambda l: [Constraint(x) for x in l], temp_rows_constraints))

        # self.rows_constraints = temp_rows_constraints
        #
        # self.num_of_rows = len(self.rows_constraints)
        # self.num_of_cols = len(self.cols_constraints)

        # build the board as empty board.# build the board as empty board.
        self.board = Board(temp_rows_constraints, temp_cols_constraints)

        # self.board = [[Cell() for _ in range(self.num_of_cols)] for _ in range(self.num_of_rows)]

    def __random_building(self, size, colors):
        """
                building a board randomly from giving size and colors
                """
        self.colors = colors
        # self.num_of_rows = size[0]
        # self.num_of_cols = size[1]

        # build the board as empty board.# build the board as empty board.
        # self.board = [[Cell() for _ in range(self.num_of_cols)] for _ in range(self.num_of_rows)]

        # build the random constraints of columns and rows.
        temp_rows_constraints = self.__build_constraints(size[0], random.randint(1, size[1]))
        temp_cols_constraints = self.__build_constraints(size[1], random.randint(1, size[0]))

        self.board = Board(temp_rows_constraints, temp_cols_constraints, randomly=True, size=size)

    # @staticmethod
    def __build_constraints(self, n, m):
        all_constraints = []
        colors_lst = []
        if self.colors == BLACK_WHITE:
            colors_lst = ['b']
        elif self.colors == COLORFUL:
            colors_lst = ['b', 'r']

        for j in range(n):
            i = 0
            constraint_lst = []
            while i < m:
                num = random.randint(1, m - i)
                color = random.choice(colors_lst)

                # if the current color is the same as the previous color and there is no room for it,
                # we should try again and choose another color or number of colored cells by this color.
                if len(constraint_lst) >= 1 and constraint_lst[-1].color == color:
                    if i + num + 1 >= m:
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

    def print_board(self):
        # if we got None from an agent, this means that there is no solution for the board.
        if self.board.board is None:
            return None
        text = ""

        # gets the longest row's length
        max_row, max_col = None, None
        m, n = 0, 0
        for row in self.board.rows_constraints:
            if len(row) > m:
                m = len(row)
                max_row = row
        # gets the longest column's length
        for col in self.board.cols_constraints:
            if len(col) > n:
                n = len(col)

        # this thing just for the design 😁.
        text += " " * (len(max_row) * 6)
        row_space = text
        text += ("-" * (6 * self.board.num_cols + 2)) + f"\n{row_space}"
        text += "|| "

        # adding the column constraints.
        for i in range(n):
            for col in self.board.cols_constraints:
                if i >= len(col):
                    text += "    | "
                elif len(col[i]) == 2:
                    text += (str(col[i]) + "  | ")
                elif len(col[i]) == 3:
                    text += (str(col[i]) + " | ")

            # adding a line separator between the column constraints and the board itself.
            if i == 0:
                text += f"\n" + ("=" * (len(row_space) + self.board.num_cols * 6 + 2)) + f"\n{row_space}| "
            else:
                text += f"\n{row_space}" + ("-" * (self.board.num_cols * 6 + 2)) + f"\n{row_space}|| "
        # remove the last unnecessary '|'
        text = text[:-1]
        text = text[:len(text) - len(row_space) - 1] + "|"

        # adding the structure of each row with the current content of the board beside the rows constraints.
        for j, row in enumerate(self.board.rows_constraints):
            for i in range(m):
                if i >= len(row):
                    text += "     |"
                elif len(row[i]) == 2:
                    text += f" {row[i]}  |"
                elif len(row[i]) == 3:
                    text += f" {row[i]} |"
            text += "|"
            for y in self.board.board[j]:
                x = str(y)
                if int(x) == EMPTY:
                    text += "     |"
                elif int(x) == WHITE:
                    text += f"  w  |"
                elif int(x) == BLACK:
                    text += f"  b  |"
                elif int(x) == RED:
                    text += f"  r  |"
            tmp = 2 + (m + self.board.num_cols) * 6
            text += "\n" + ("-" * tmp) + "\n|"

        return text[:-1]

    def run(self):
        # runs the brute force algorithm on the board.
        self.board.board = agent.brute_force(self.board.rows_constraints, self.board.cols_constraints, self.board.board)


if __name__ == "__main__":
    print("Hello World!")
    game = Game(csv_file="example1.csv")

    game.run()
    print(game.print_board())

