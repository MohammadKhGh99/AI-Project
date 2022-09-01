import time

from GUI import GUI
from config import *
from typing import List


class Cell:
    """
    the cells of the board. each cell has a color: WHITE, Black or RED. (DEFAULT=WHITE)
    """

    def __init__(self, row_id, col_id, color=EMPTY):
        self.color = color
        self.row = row_id
        self.col = col_id

    def __str__(self):
        return str(self.color)

    def __repr__(self):
        if self.color == EMPTY:
            return ' '
        elif self.color == WHITE:
            return 'w'
        elif self.color == BLACK:
            return 'b'
        elif self.color == RED:
            return 'r'


class Constraint:
    """
    This class describes the constraints cells with number, status and color (Black, Red).
    """

    def __init__(self, constraint):
        if constraint.replace(' ', '') == '':  # empty constraint
            raise Exception("Empty Constraint Situation Not Implemented!")
        try:
            self.length = int(constraint[:-1])
        except Exception:
            raise Exception("constraint structure should not be like this")

        c = constraint[-1]

        if c.lower() not in COLORS:
            raise Exception("error in choosing color for constraint")
        else:
            self.color = BLACK if c.lower() == 'b' else RED

        self.completed = False

    def __str__(self):
        return str(self.length) + COLORS_N_DICT[self.color]

    def __len__(self):
        return len(self.__str__())


class Board:
    gui = None
    before_time = 0
    different_time = 0

    def __init__(self, rows_constraints: List[List[Constraint]], cols_constraints: List[List[Constraint]],
                 randomly=False, size=(5, 5), cur_game=None):
        # the constraints to build the board from them
        self.rows_constraints = rows_constraints
        self.cols_constraints = cols_constraints
        # this variable contain the shape of the board if we want ot print it
        self.to_print = ""
        # locations of board's cells in the print variable above to assign them if they have changed.
        self.cells_locations = []
        # if the board is created randomly
        self.randomly = randomly
        # the size of the board (rows, columns)
        self.size = size
        # the current game of the current board
        self.cur_game = cur_game

        self.current_cell = Cell(0, -1)
        self.current_row_constraint = -1
        self.filled_cells = 0
        # list of the created rectangles in the gui
        self.rects = []

        # if the current board is not created randomly
        if not self.randomly:
            self.num_rows = len(self.rows_constraints)
            self.num_cols = len(self.cols_constraints)
        else:  # if the current board is created randomly
            self.num_rows, self.num_cols = self.size

        # the board to fill
        self.board = [[Cell(r, c) for c in range(self.num_cols)] for r in range(self.num_rows)]
        # the flipped version of th board to fill (rows as columns and columns as rows, helping us with checking)
        self.flipped = [[Cell(c, r) for r in range(self.num_rows)] for c in range(self.num_cols)]

        self.to_print = self.init_board_print()

    @staticmethod
    def start_gui(board):
        """
        This function starts the gui
        """
        Board.gui = GUI(board=board, cur_game=board.cur_game)
        Board.gui.root.mainloop()

    def clear_board(self):
        """
        this function clear everything in the current board
        """
        if Board.gui is not None:
            Board.gui.canvas.delete('rect')
        Board.different_time = 0
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                self.board[r][c].color = EMPTY
                self.flipped[c][r].color = EMPTY
                self.current_cell = Cell(0, -1)
                self.current_row_constraint = -1
                self.filled_cells = 0
                if Board.gui:
                    Board.gui.board.board[r][c].color = EMPTY
                    Board.gui.board.cells_locations = []
                    Board.gui.board.init_board_print()
                    Board.gui.board.rects = []
                self.cells_locations = []
                self.init_board_print()
                self.rects = []

        for row_con in self.rows_constraints:
            for con in row_con:
                con.completed = False
        for col_con in self.cols_constraints:
            for con in col_con:
                con.completed = False

    def unfill(self, r, c):
        """
        This function unfill the given location in the current board
        """
        if r < self.num_rows and c < self.num_cols:
            self.board[r][c].color = EMPTY
            self.flipped[c][r].color = EMPTY
            if Board.gui:
                Board.gui.board.board[r][c].color = EMPTY

            # adding the correct color char to the appropriate place in to_print variable.
            cur = self.cells_locations[r][c]

            # I found that this way is faster
            self.to_print = self.to_print[:cur] + ' ' + self.to_print[cur + 1:]

            # adding the cell to the gui.
            if Board.gui is not None:
                before = time.time()
                # if we want some delay
                # time.sleep(0.1)
                temp = Board.gui.board_rectangles_locs[r][c]
                Board.gui.canvas.create_rectangle(temp[0], temp[1], temp[2], temp[3], fill='white', tags='rect')
                # this done to not include the gui time in the final time of the running algorithm
                Board.different_time += (time.time() - before)

            # removing the cell from the gui
            if Board.gui is not None:
                self.rects.remove(self.board[r][c])

            return True
        return False

    def fill(self, r, c, color, solve_type):
        """
        This function fills the give location in the current board
        """
        if r < self.num_rows and c < self.num_cols:
            if self.board[r][c].color == EMPTY:
                self.filled_cells += 1
            self.board[r][c].color = color
            self.flipped[c][r].color = color
            if Board.gui:
                Board.gui.board.board[r][c].color = color
            cur = self.cells_locations[r][c]
            # I found that this way is faster
            self.to_print = self.to_print[:cur] + repr(self.board[r][c]) + self.to_print[cur + 1:]

            if (solve_type == BRUTE or solve_type == CSP_P or solve_type == BFS) and Board.gui is not None and Board.gui.canvas is not None:
                before = time.time()
                # if we want some delay
                # time.sleep(0.1)
                temp = Board.gui.board_rectangles_locs[r][c]
                Board.gui.canvas.create_rectangle(temp[0], temp[1], temp[2], temp[3],
                                                  fill=COLORS_DICT[repr(self.board[r][c])], tags='rect')
                Board.gui.root.update()
                # this done to not include the gui time in the final time of the running algorithm
                Board.different_time += (time.time() - before)

            if Board.gui is not None:
                self.rects.append(self.board[r][c])
            return True
        return False

    def fill_row_col(self, i, row_or_col):
        """
        This function takes a row or column and fill it in the same time, used by csp
        """
        if row_or_col == ROWS:  # row
            for j in range(self.num_cols):
                loc = Board.gui.board_rectangles_locs[i][j]
                Board.gui.canvas.create_rectangle(loc, fill=COLORS_DICT[repr(self.board[i][j])], tags='rect')
        else:  # column
            for j in range(self.num_rows):
                loc = Board.gui.board_rectangles_locs[j][i]
                Board.gui.canvas.create_rectangle(loc, fill=COLORS_DICT[repr(self.board[j][i])], tags='rect')
        Board.gui.root.update()

    def init_board_print(self):
        """
        This function initializes the print variable in the current board, adds the places of the constraints,
        just for printing.
        """
        self.to_print = ""

        # gets the longest row's length
        max_row = None
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
        self.to_print += " " * (len(max_row) * 6)
        row_space = self.to_print
        self.to_print += ("-" * (6 * self.num_cols + 2)) + f"\n{row_space}"
        self.to_print += "|| "

        # adding the column constraints.
        for i in range(n - 1, -1, -1):
            for j, col in enumerate(self.cols_constraints):
                cur = col[::-1]
                if i >= len(cur):
                    self.to_print += "    | "
                elif len(cur[i]) == 2:
                    self.to_print += f"{cur[i]}  | "
                elif len(cur[i]) == 3:
                    self.to_print += f"{cur[i]} | "
                if j == self.num_cols - 1:
                    self.to_print = self.to_print[:-1]

            # adding a line separator between the column constraints and the board itself.
            if i == 0:
                self.to_print += f"\n" + ("=" * (len(row_space) + self.num_cols * 6 + 2)) + f"\n{row_space}| "
            else:
                self.to_print += f"\n{row_space}" + ("-" * (self.num_cols * 6 + 2)) + f"\n{row_space}|| "
        # remove the last unnecessary '|'
        self.to_print = self.to_print[:-1]
        self.to_print = self.to_print[:len(self.to_print) - len(row_space) - 1] + "|"

        # adding the structure of each row with the current content of the board beside the rows constraints.

        for j, row in enumerate(self.rows_constraints):
            for i in range(m - 1, -1, -1):
                cur = row[::-1]
                if i >= len(cur):
                    self.to_print += "     |"
                elif len(cur[i]) == 2:
                    self.to_print += f" {cur[i]}  |"
                elif len(cur[i]) == 3:
                    self.to_print += f" {cur[i]} |"

            self.to_print += "|"
            lst = []
            for i, y in enumerate(self.board[j]):
                x = str(y)
                if int(x) == EMPTY:
                    self.to_print += "     |"
                elif int(x) == WHITE:
                    self.to_print += f"  w  |"
                elif int(x) == BLACK:
                    self.to_print += f"  b  |"
                elif int(x) == RED:
                    self.to_print += f"  r  |"
                else:
                    raise Exception("the board should be filled just with -1, 0, 1 and 2")
                lst.append(len(self.to_print) - 4)
            self.cells_locations.append(lst)
            tmp = 2 + (m + self.num_cols) * 6
            self.to_print += "\n" + ("-" * tmp) + "\n|"
        return self.to_print[:-1]

    def print_board(self):
        """
        This function prints the board, after filling the empty places with white color.
        """
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                cur = self.cells_locations[r][c]
                if self.to_print[cur] == ' ':
                    self.to_print = self.to_print[:cur] + 'w' + self.to_print[cur + 1:]
        print(self.to_print)

    def check_move(self, row_id, col_id, problem_type=BRUTE_FORCE):
        """
        check if the move in this row_id/col_id is legit.
        """
        # checking for the rows
        if not self._check_move_helper_with_constraint_check(col_id, flipped=False, problem_type=problem_type):
            return False

        # checking for the columns (as rows)
        if not self._check_move_helper_with_constraint_check(row_id, flipped=True, problem_type=problem_type):
            return False

        return True

    def _check_move_helper_with_constraint_check(self, row_id, flipped=False, problem_type=BRUTE_FORCE):
        """
        check if the move in this row_id/col_id is legit.
        return True if this move works and legit, false otherwise
        IMPORTANT NOTE: this doesn't show that this step is correct, it just checks if it could be there.
        """
        if flipped:
            constraints_for_row = self.cols_constraints[row_id]
        else:
            constraints_for_row = self.rows_constraints[row_id]

        if flipped:
            current_row = self.flipped[row_id]
        else:
            current_row = self.board[row_id]

        # constraint:
        curr_constraint_id = 0
        curr_constraint = constraints_for_row[curr_constraint_id]
        curr_num_of_cells_to_fill = curr_constraint.length
        curr_constraint_color = curr_constraint.color
        curr_constraint_status = curr_constraint.completed

        # the color must be for the next cell
        must_color = EMPTY
        # sometimes we need to block a color from next cell (example: 1b-1b - we can't put two black near each other)
        # - white can't be forbidden
        blocked_color = EMPTY

        constraints_complete = False  # all constraints are fulfilled
        empty_flag = False  # there is an empty cell in this row

        cell_id = 0
        while cell_id < len(current_row):
            cell = current_row[cell_id]
            cell_color = cell.color

            if cell_color == EMPTY:  # we didn't fill it yet
                empty_flag = True
                blocked_color = EMPTY  # Nothing blocked after an empty cell.
                cell_id += 1
                continue

            elif cell_color == WHITE and (must_color == WHITE or must_color == EMPTY):
                # that's good
                # if must_color is white -
                # that means we finished all constraints, and all remaining cells should stay white

                # we reset the forbid color
                blocked_color = EMPTY
                cell_id += 1
                continue

            elif cell_color == curr_constraint_color and (
                    must_color == curr_constraint_color or must_color == EMPTY) and blocked_color != curr_constraint_color:
                if curr_constraint_status:
                    # this constraint already filled and done, so move to next situation as we finished this status
                    cell_id += curr_num_of_cells_to_fill
                    curr_num_of_cells_to_fill = 0
                else:
                    # this constraint ain't finished yet
                    curr_num_of_cells_to_fill -= 1
                    cell_id += 1

                # check if we need to change constraint #
                # if we still didn't finish filling this constraint,
                # we want the next color to be same color as the constraint:
                if curr_num_of_cells_to_fill > 0:
                    must_color = curr_constraint_color
                    blocked_color = EMPTY  # nothing blocked

                # if we finished filling this current constraint, we need to move to next constraint
                elif curr_num_of_cells_to_fill == 0:
                    must_color = EMPTY  # nothing is a must
                    blocked_color = curr_constraint_color
                    if not problem_type:  # if not brute force
                        # Change the status for a future checks.
                        constraints_for_row[curr_constraint_id].completed = True

                    # move to next constraint
                    curr_constraint_id += 1
                    if curr_constraint_id < len(constraints_for_row):
                        curr_constraint = constraints_for_row[curr_constraint_id]
                        curr_num_of_cells_to_fill = curr_constraint.length
                        curr_constraint_color = curr_constraint.color
                        curr_constraint_status = constraints_for_row[curr_constraint_id].completed

                    else:
                        # we finished every constraint, next cells should be white only
                        constraints_complete = True
                        must_color = WHITE
                else:
                    raise Exception("this is an impossible situation, hmmmmmm")

            else:
                return False

        # maybe we finished the row but the constraints aren't finished yet! and that's a mistake:
        # if we have Empty then no need to finish the constraints, if we don't then constraints must complete
        if empty_flag or constraints_complete:
            return True

        return False

    def back_to_the_prev_cell(self):
        """
        This function change the current cell backward
        """
        new_col = self.current_cell.col - 1
        new_row = self.current_cell.row
        if new_col == -1:
            new_col = self.num_cols - 1
            new_row -= 1
        try:
            self.current_cell = self.board[new_row][new_col]
        except IndexError:
            self.current_cell = Cell(new_row, new_col)

    def move_to_the_next_cell(self):
        """
        This function change the current cell forward.
        """
        new_col = self.current_cell.col + 1
        new_row = self.current_cell.row
        if new_col == self.num_cols:
            new_col = 0
            new_row += 1
        try:
            self.current_cell = self.board[new_row][new_col]
        except IndexError:
            self.current_cell = Cell(new_row, new_col)
