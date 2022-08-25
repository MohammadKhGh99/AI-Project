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

        self.current_state = 0  # check: idk what is this | me neither

        # i'll try if this help me: OK
        self.row = row_id
        self.col = col_id

    def __str__(self):
        return str(self.color)


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

        # self.status = NOT_COMPLETE

    def __str__(self):
        c = 'b' if self.color == BLACK else 'r'
        return str(self.length) + c
        # str_comp = "T" if self.completed else "F"
        # return str(self.number) + self.c + str_comp

    def __len__(self):
        return len(self.__str__())


class Board:

    # delete - board argument, it's just for testing bro!
    def __init__(self, rows_constraints: List[List[Constraint]], cols_constraints: List[List[Constraint]],
                 randomly=False, size=(5, 5), board=None):
        self.rows_constraints = rows_constraints
        self.cols_constraints = cols_constraints

        if not randomly:
            self.num_rows = len(self.rows_constraints)
            self.num_cols = len(self.cols_constraints)
        else:
            self.num_rows, self.num_cols = size

        self.board = board if board else [[Cell(r, c) for c in range(self.num_cols)] for r in range(self.num_rows)]
        # todo i guess now to have same cells we need to flip this board manually
        self.flipped = [[Cell(c, r) for r in range(self.num_rows)] for c in range(self.num_cols)]

    def fill(self, r, c, color):
        time.sleep(1)
        sys.stdout.flush()
        if r < self.num_rows and c < self.num_cols:
            self.board[r][c].color = color
            self.flipped[c][r].color = color
            print(self.print_board())
            return True
        return False

    # todo - BEFORE MERGING WITH ADAM
    # def fill_n_cells(self, con_i, con_j, start_index, constraint_type=COLUMNS):
    #     """
    #     Function fill the board, in a valid way. It fills n cells according to the given constraint.
    #     constraint_type: on which constraints list we will work: columns or rows.
    #     con_i: the index of the working constraints group.
    #     con_j: the index of the working constraint in the group.
    #     start_index: from where to start to fill (row/column)
    #     """
    #     child = deepcopy(self)
    #     child.complete_constraints(constraint_type, con_i, con_j)
    #     if constraint_type:
    #         constraint = child.cols_constraints[con_i][con_j]
    #         for i in range(constraint.length):
    #             if agent.check_move(child, i + start_index, con_i):
    #                 child.fill(i + start_index, con_i, constraint.color)
    #             else:
    #                 break
    #     else:
    #         constraint = child.rows_constraints[con_i][con_j]
    #         for i in range(constraint.length):
    #             if agent.check_move(child, con_i, i + start_index):
    #                 child.fill(con_i, i + start_index, constraint.color)
    #             else:
    #                 break
    #     return child

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
            for i in range(start_index):
                # Assign the cells that must be white.
                if child.get_cell(i, con_i).color == EMPTY:
                    child.fill(i, con_i, WHITE)

            for i in range(constraint.length):
                if child.fill(i + start_index, con_i, constraint.color) \
                        and agent.check_move(child, con_i, i + start_index):
                    continue
                else:
                    return None
        # Todo make it support the row constrains
        # else:
        #     constraint = child.rows_constraints[con_i][con_j]
        #     for i in range(constraint.number):
        #         if child.fill(con_i, i + start_index, constraint.color) \
        #                 and agent.check_move(child, con_i, i + start_index):
        #             continue
        #         else:
        #             return None
        #     for i in range(start_index):
        #         # Assign the cells that must be white.
        #         if child.get_cell(con_i, i).color == EMPTY:
        #             child.fill(con_i, i, WHITE)
        child.complete_constraints(con_i, con_j, constraint_type)
        return child

    def switch_empty_to(self):
        pass

    def get_cell(self, r, c, flipped=False):
        return self.board[r][c] if not flipped else self.flipped[c][r]

    def print_board(self):
        # if we got None from an agent, this means that there is no solution for the board.
        # if self.board is None:
        #     return None
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
        # if constraint_type:
        constraints_group = self.cols_constraints if constraint_type else self.rows_constraints
        # else:
        #     constraints_group = self.rows_constraints

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

