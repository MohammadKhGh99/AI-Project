class Nonogram:
    def __init__(self, csv_file=None, rows=None, columns=None, colors=BLACK_AND_WHITE, size=(5, 5), always_solvable=True):
        if csv_file:
            # create a board from csv file
            # todo init row and col
            pass
        elif rows and columns:
            # create a board from rows and columns given
            self.rows = rows
            self.cols = columns

            self.num_of_rows = len(rows)
            self.num_of_cols = len(columns)
            self.board = [[0 for c in range(self.num_of_cols)] for r in range(self.num_of_rows)]

            pass
        else:
            # create a random board from giving size and do it always solvable or not.
            # todo init row and col

            pass
