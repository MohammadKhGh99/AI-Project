from GUI import GUI
from config import *
from typing import List
from copy import deepcopy
import agent
import sys
import time


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
        # todo - add the situation if the constraint is empty or not?
        if constraint.replace(' ', '') == '':
            raise Exception("Empty Constraint Situation Not Implemented!")

        try:
            self.length = int(constraint[:-1])
        except Exception:
            raise Exception("constraint structure should be like this")

        c = constraint[-1]

        if c.lower() not in COLORS:
            raise Exception("error in choosing color for constraint")
        else:
            self.color = BLACK if c.lower() == 'b' else RED

        # todo choose one of those
        self.completed = False

    def __str__(self):
        c = 'b' if self.color == BLACK else 'r'
        return str(self.length) + c
        # return (str(self.length) + 'b') if self.color == BLACK else (str(self.length) + 'r')

    def __len__(self):
        return len(self.__str__())


class Board:
    gui = None

    def __init__(self, rows_constraints: List[List[Constraint]], cols_constraints: List[List[Constraint]],
                 randomly=False, size=(5, 5)):
        self.rows_constraints = rows_constraints
        self.cols_constraints = cols_constraints
        self.to_print = ""
        self.cells_locations = []
        self.randomly = randomly
        self.size = size
        self.current_cell = Cell(0, -1)
        self.current_row_constraint = -1
        self.moves = []


        # todo - add a list of the cells of the child's actions rectangles
        self.rects = []

        if not self.randomly:
            self.num_rows = len(self.rows_constraints)
            self.num_cols = len(self.cols_constraints)
        else:
            self.num_rows, self.num_cols = self.size

        self.board = [[Cell(r, c) for c in range(self.num_cols)] for r in range(self.num_rows)]
        # todo i guess now to have same cells we need to flip this board manually - DONE (I think?)
        self.flipped = [[Cell(c, r) for r in range(self.num_rows)] for c in range(self.num_cols)]
        self.to_print = self.init_board_print()
        # Board.gui = GUI.GUI(board=self)

    @staticmethod
    def start_gui(board):
        Board.gui = GUI(board=board)

    def fill(self, r, c, color, brute_force=SEARCH_PROBLEMS):
        # time.sleep(0.1)
        # sys.stdout.flush()
        if r < self.num_rows and c < self.num_cols:
            self.board[r][c].color = color
            self.flipped[c][r].color = color
            Board.gui.board.board[r][c].color = color
            cur = self.cells_locations[r][c]
            # I found that this way is faster
            self.to_print = self.to_print[:cur] + self.board[r][c].__repr__() + self.to_print[cur + 1:]

            # time.sleep(0.1)
            # Board.gui.canvas.delete('rect')

            if brute_force:
                temp = Board.gui.board_rectangles_locs[r][c]
                Board.gui.canvas.create_rectangle(temp[0], temp[1], temp[2], temp[3],
                                                  fill=COLORS_DICT[self.board[r][c].__repr__()], tags='rect')
                Board.gui.root.update()
            self.rects.append(self.board[r][c])

            # self.print_board()
            return True
        return False

    def fill_n_cells(self, con_i, con_j, start_index, constraint_type=ROWS):
        """
        Function fill the board, in a valid way. It fills n cells according to the given constraint.
        constraint_type: on which constraints list we will work: columns or rows.
        con_i: the index of the working constraints group.
        con_j: the index of the working constraint in the group.
        start_index: from where to start to fill (row/column)
        """
        #TODO remove if we decided to not use it.
        child = deepcopy(self)
        if not constraint_type:
            constraint = child.rows_constraints[con_i][con_j]
            for i in range(start_index):
                # Assign the cells that must be white.
                if child.get_cell(con_i, i).color == EMPTY:
                    child.fill(con_i, i, WHITE)
            for i in range(constraint.length):
                if child.fill(con_i, i + start_index, constraint.color) \
                        and child.check_move(i + start_index, con_i, problem_type=SEARCH_PROBLEMS):
                    continue
                else:
                    return None
        child.complete_constraints(con_i, con_j, constraint_type)
        # Board.gui.canvas.delete('rect')
        return child

    def get_cell(self, r, c, flipped=False):
        return self.board[r][c] if not flipped else self.flipped[c][r]

    def init_board_print(self):
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

        constraints_for_row = self.rows_constraints[row_id] if not flipped else self.cols_constraints[row_id]
        current_row = self.flipped[row_id] if flipped else self.board[row_id]

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
                        constraints_for_row[
                            curr_constraint_id].completed = True  # Change the status for a future checks.

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

    def get_first_incomplete_constraint(self, constraint_type):
        """
        Find first incomplete constraint in columns or rows constraints.
        constrain_type: on which constraints list we will work: columns or rows
        Return the coordinates of the incomplete constraints, None, if all constraints are completed
        """
        constraints_group = self.cols_constraints if constraint_type else self.rows_constraints
        #TODO remove if we decided to not use it.
        for i in range(len(constraints_group)):
            for j in range(len(constraints_group[i])):
                if not constraints_group[i][j].completed:
                    return i, j
        return None

    def get_next_row_constraint(self):
        #TODO remove if we decided to not use it.
        i = 0
        for row_con in range(len(self.rows_constraints)):
            previous_constraint = -1
            for constraint in self.rows_constraints[row_con]:
                if i == self.current_row_constraint:
                    if self.current_cell.row != row_con:
                        self.current_cell = self.get_cell(row_con, previous_constraint + 1)
                    return constraint
                i += 1
                previous_constraint += constraint.length
        return None

    def complete_constraints(self, con_i, con_j, constraint_type=COLUMNS):
        """
        Function change the status of the given constraint to completed (True)
        constraint_type: on which constraints list we will work: columns or rows.
        con_i: the index of the working constraints group.
        con_j: the index of the working constraint in the group.
        """
        #TODO remove if we decided to not use it.
        if constraint_type:
            self.cols_constraints[con_i][con_j].completed = True
        else:
            self.rows_constraints[con_i][con_j].completed = True

    def back_to_the_prev_cell(self):
        """This function change the current cell backward"""
        new_col = self.current_cell.col - 1
        new_row = self.current_cell.row
        if new_col == -1:
            new_col = self.num_cols - 1
            new_row -= 1
        try:
            self.current_cell = self.get_cell(new_row, new_col)
        except IndexError:
            self.current_cell = Cell(new_row, new_col)

    def move_to_the_next_cell(self):
        """This function change the current cell forward."""
        new_col = self.current_cell.col + 1
        new_row = self.current_cell.row
        if new_col == self.num_cols:
            new_col = 0
            new_row += 1
        try:
            self.current_cell = self.get_cell(new_row, new_col)
        except IndexError:
            self.current_cell = Cell(new_row, new_col)