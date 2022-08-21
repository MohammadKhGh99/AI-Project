import random
from config import *


class Cell:
    """
    the cells of the board. each cell has a color: WHITE, Black or RED. (DEFAULT=WHITE)
    """
    def __init__(self, color=WHITE):
        self.color = color
        self.current_state = 0  # check: idk what is this


class Game:
    def __init__(self, csv_file=None, rows_constraints=None, cols_constraints=None, colors=BLACK_WHITE,
                 size=(5, 5), always_solvable=True, agent=None):
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
        always_solvable: this will give us if the random board should have a solution or maybe.

        expected constraints format: if BLACK_WHITE: ^\d+[bB](?:-\d+[bB])*$|^\d+(?:-\d+)*$     examples: 5b-8b, 12, 5-84
                                     if COLORFUL: ^\d+[bBrR](?:-\d+[bBrR])*$    examples: 3b, 5r-15B.

        """
        self.agent = agent  # check: i'm not sure what is this
        self.state = None   # check: i'm not sure what is this

        if csv_file:
            # create a board from csv file.
            self.__csv_building(csv_file)

        elif rows_constraints and cols_constraints:
            # create a board from a giving rows and cols constraints lists.
            self.num_of_rows = len(rows_constraints)
            self.num_of_cols = len(cols_constraints)

            self.board = [[0 for _ in range(self.num_of_cols)] for _ in range(self.num_of_rows)]

        else:
            # create a random board from giving size and do it as: always_solvable or not.
            self.__random_building(colors, size, always_solvable)

    def __csv_building(self, csv_file):
        """
        building the board from a csv file
        expecting format to be: ,3b,2r-3b,1b
                                2r,,,,
                                3b,,,,
                                1b-3r,,,,

        """
        with open(csv_file, 'r') as f:
            lines = f.readlines()

        def convert(c):
            color = c[-1]
            number = int(c[:-1])

            # todo - Cell or make a new class called constraint cell ??
            cell = Cell(number, color)
            return cell

        temp_cols_constraints = list(map(lambda x: x.split('-'), lines[0][4:].strip().split(',')))
        temp_cols_constraints = list(map(lambda l: [convert(x) for x in l], temp_cols_constraints))

        self.cols_constraints = temp_cols_constraints

        temp_rows_constraints = list(map(lambda x: x[:x.index(',')].split('-'), lines[1:]))
        temp_rows_constraints = list(map(lambda l: [convert(x) for x in l], temp_rows_constraints))

        self.rows_constraints = temp_rows_constraints

        self.rows = len(self.rows_constraints)
        self.cols = len(self.cols_constraints)

        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def __random_building(self, colors, size, always_solvable):

        if size:

        self.rows = random.randint(1, 25)
        self.cols = random.randint(1, 25)

        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        self.rows_constraints = Game.__build_constraints(random.randint(1, self.rows), random.randint(1, self.cols))
        self.cols_constraints = Game.__build_constraints(random.randint(1, self.cols), random.randint(1, self.rows))

    @staticmethod
    def __build_constraints(n, m):
        rlst = []
        for j in range(n):
            i = 0
            lst = []
            while i < m:
                num = random.randint(1, m - i)
                color = random.choice(['b', 'r'])
                if len(lst) > 1 and lst[-1][-1] == color:
                    if i + num + 1 >= m:
                        continue

                lst.append(str(num) + color)

                if len(lst) > 1:
                    if lst[-2][-1] == color:
                        i += (num + 1)
                    else:
                        i += num
                else:
                    i += num
            rlst.append(lst)
        return rlst


if __name__ == "__main__":
    print("Hello World!")



    # with open('example1.csv', 'r') as f:
    #     lines = f.readlines()
    #
    #
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
