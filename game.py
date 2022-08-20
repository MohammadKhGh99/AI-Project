import random

#########   NOT NECESSARY !!!!!   #########
""" 
csv file should be as the following structure:
* The first line will be a list of the columns constraints.
* The second line will be a list of the rows constraints.
* The third line will contain a tuple of two dimensions (rows_number,columns_number)
*** the list of constraints should be as the following structure:
    for the columns: (in one line)
                columns                    rows
        [a,b,...,z][...]...[...]|[a,b,...,.a][...]...[...]
"""
#########   NOT NECESSARY !!!   #########


BLACK_WHITE = 0  # todo - don't know what is this, I have put it like this for stam, I don't know what it was before!

WHITE = 0
BLACK = 1
RED = 2


class Cell:
    def __init__(self, number, color):
        self.number = number
        self.color = color
        self.current_state = 0


class Game:
    def __init__(self, csv_file=None, rows=None, columns=None, colors=BLACK_WHITE, agent=None, always_solvable=True,
                 rows_constraints=None, cols_constraints=None):
        self.agent = agent
        self.state = None

        if rows and columns:
            self.rows = rows
            self.cols = columns

            # create a board from given rows and columns (as lists)
            self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

            self.rows_constraints = rows_constraints
            self.cols_constraints = cols_constraints

            # self.num_of_rows = len(rows)
            # self.num_of_cols = len(columns)
            # self.board = [[0 for c in range(self.num_of_cols)] for r in range(self.num_of_rows)]

        # todo board building from csv file here or in main?
        elif csv_file:
            # create a board from csv file
            self.__csv_building(csv_file)
        else:
            # create a random board from giving size and do it always solvable or not.
            self.__random_building()

    def __csv_building(self, csv_file):
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

    def __random_building(self):
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
