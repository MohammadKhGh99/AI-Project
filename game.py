import random
import re

from config import *


class Constraint:
    """
    This class describes the constraints cells with number and color (Black, Red).
    """
    def __init__(self, constraint):
        try:
            self.number = int(constraint[:-1])
            self.color = constraint[-1]
        except Exception:
            raise Exception("constraint structure should be like this")

        if self.color not in COLORS:
            raise Exception("error in choosing color for constraint")

    def __str__(self):
        return str(self.number) + self.color

    def __len__(self):
        return len(self.__str__())


class Cell:
    """
    the cells of the board. each cell has a color: WHITE, Black or RED. (DEFAULT=WHITE)
    """
    def __init__(self, color=WHITE):
        self.color = color
        self.current_state = 0  # check: idk what is this | me neither

    def __str__(self):
        return self.color


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
            if colors.lower() not in NONO_COLORS:
                raise Exception("error in choosing the colors of the Nongram")

            self.colors = colors

            self.rows_constraints = rows_constraints
            self.cols_constraints = cols_constraints

            self.rows_constraints = [list(map(lambda x: Constraint(x), row.split('-'))) for row in self.rows_constraints]
            self.cols_constraints = [list(map(lambda x: Constraint(x), col.split('-'))) for col in self.cols_constraints]

            self.num_of_rows = len(rows_constraints)
            self.num_of_cols = len(cols_constraints)

            self.board = [[Cell() for _ in range(self.num_of_cols)] for _ in range(self.num_of_rows)]

        else:
            # create a random board from giving size and color
            self.__random_building(size)

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

        temp_cols_constraints = list(map(lambda x: x.split('-'), lines[1][4:].strip().split(',')))
        temp_cols_constraints = list(map(lambda l: [Constraint(x) for x in l], temp_cols_constraints))

        self.cols_constraints = temp_cols_constraints

        temp_rows_constraints = list(map(lambda x: x[:x.index(',')].split('-'), lines[2:]))
        temp_rows_constraints = list(map(lambda l: [Constraint(x) for x in l], temp_rows_constraints))

        self.rows_constraints = temp_rows_constraints

        self.num_of_rows = len(self.rows_constraints)
        self.num_of_cols = len(self.cols_constraints)

        self.board = [[Cell() for _ in range(self.num_of_cols)] for _ in range(self.num_of_rows)]

    def __random_building(self, size):
        """
        building a board randomly from giving size and colors
        """
        self.num_of_rows = size[0]
        self.num_of_cols = size[1]

        self.board = [[Cell() for _ in range(self.num_of_cols)] for _ in range(self.num_of_rows)]

        self.rows_constraints = Game.__build_constraints(self.num_of_rows, random.randint(1, self.num_of_cols))
        self.cols_constraints = Game.__build_constraints(self.num_of_cols, random.randint(1, self.num_of_rows))

    @staticmethod
    def __build_constraints(n, m):
        all_constraints = []
        for j in range(n):
            i = 0
            constraint_lst = []
            while i < m:
                num = random.randint(1, m - i)
                color = random.choice(['b', 'r'])
                if len(constraint_lst) >= 1 and constraint_lst[-1].color == color:
                    if i + num + 1 >= m:
                        continue

                constraint_lst.append(Constraint(str(num) + color))

                if len(constraint_lst) > 1:
                    if constraint_lst[-2].color == color:
                        i += (num + 1)
                    else:
                        i += num
                else:
                    i += num
            all_constraints.append(constraint_lst)
        return all_constraints

    # def print_board(self):
    #     text = ""
    #
    #     max_row, max_col = None, None
    #     m, n = 0, 0
    #     for row in self.rows_constraints:
    #         if len(row) > m:
    #             m = len(row)
    #             max_row = row
    #     for col in self.cols_constraints:
    #         if len(col) > n:
    #             n = len(col)
    #             max_col = col
    #
    #     for _ in max_row:
    #         text += " " * (3 + 1)
    #     row_space = text
    #     text += "| "
    #     # text -= " "
    #
    #     # text += " " * m
    #     for i in range(n - 1, -1, -1):
    #         for col in self.cols_constraints:
    #             if i >= len(col):
    #                 text += "    | "
    #             elif len(col[i]) == 2:
    #                 text += (str(col[i]) + "  | ")
    #             elif len(col[i]) == 3:
    #                 text += (str(col[i]) + " | ")
    #
    #         text += f"\n{row_space}" + ("-" * 91) + f"\n{row_space}| "
    #     text = text[:len(text) - len(row_space) - 2]
    #
    #     for row in self.rows_constraints:
    #         # text += "|"
    #         for i in range(m - 1, -1, -1):
    #             if i >= len(row):
    #                 text += "    | "
    #             elif len(row[i]) == 2:
    #                 text += f" {row[i]}  | "
    #             elif len(row[i]) == 3:
    #                 text += f" {row[i]} |"
    #         text += ("  w  |" * self.num_of_cols) + "\n" + ("-" * 91) + "\n| "
    #
    #     return text
    #

if __name__ == "__main__":
    print("Hello World!")
    game = Game(size=(15, 15))
    print(game.print_board())





    # with open('example1.csv', 'r') as f:
    #     lines = f.readlines()
    # print(lines[0][3:6])

    # def convert(c):
    #     color = c[-1]
    #     number = int(c[:-1])
    #     cell = Cell(number, color)
    #     return cell
    #
    #
    # cols_constraints = list(map(lambda x: x.split('-'), lines[0][4:].strip().split(',')))
    # cols_constraints = list(map(lambda l: [convert(x) for x in l], cols_constraints))
    #
    # rows_constraints = list(map(lambda x: x[:x.index(',')].split('-'), lines[1:]))
    # rows_constraints = list(map(lambda l: [convert(x) for x in l], rows_constraints))
    # # rows_constraints = list
    #
    # # print([[(x.number, x.color) for x in r] for r in rows_constraints])
    # # print([[(x.number, x.color) for x in r] for r in cols_constraints])
    # #
    #
    # # rows = len(rows_constraints)
    # # cols = len(cols_constraints)
    #
    # rows = random.randint(1, 25)
    # cols = random.randint(1, 25)
    #
    # rand_rows = random.randint(1, rows)
    # rand_cols = random.randint(1, cols)
    #
    # clst = []
    # for j in range(cols):
    #     i = 0
    #     lst = []
    #     while i < rows:
    #         num = random.randint(1, rows - i)
    #         color = random.choice(['b', 'r'])
    #         if len(lst) > 1 and lst[-1][-1] == color:
    #             if i + num + 1 >= rows:
    #                 continue
    #         lst.append(str(num) + color)
    #         # if num == rows:
    #         #     break
    #         if len(lst) > 1:
    #             if lst[-2][-1] == color:
    #                 i += (num + 1)
    #             else:
    #                 i += num
    #         else:
    #             i += num
    #     clst.append(lst)
    #
    # rlst = []
    # for j in range(rows):
    #     i = 0
    #     lst = []
    #     while i < cols:
    #         num = random.randint(1, cols - i)
    #         color = random.choice(['b', 'r'])
    #         if len(lst) > 1 and lst[-1][-1] == color:
    #             if i + num + 1 >= cols:
    #                 continue
    #         lst.append(str(num) + color)
    #         # if num == cols:
    #         #     break
    #         if len(lst) > 1:
    #             if lst[-2][-1] == color:
    #                 i += (num + 1)
    #             else:
    #                 i += num
    #         else:
    #             i += num
    #     rlst.append(lst)
    #
    # print(f"({rows}, {cols})")
    #
    # print(rlst)
    # print(clst)
