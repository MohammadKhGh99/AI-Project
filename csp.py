# CSP
import game
from game import *

from abc import abstractmethod
from typing import Dict, List


# --------------------------#


# FAKE
class ConstraintForVariable:
    def __init__(self, variables: List) -> None:
        self.variables = variables

    # Must be overridden by subclasses
    @abstractmethod
    def satisfied(self, assignment) -> bool:
        ...


class CSP:
    def __init__(self, variables, domains):
        self.variables = variables
        self.domains: Dict = domains
        self.constraints = {}
        for variable in self.variables:
            self.constraints[variable] = []

    def add_constraint(self, constraint: ConstraintForVariable) -> None:
        for variable in constraint.variables:
            self.constraints[variable].append(constraint)

    def consistent(self, variable, assignment):
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    def backtracking_search_rec(self, assignment=None):
        # assignment is complete if every variable is assigned (our base case)
        if assignment is None:
            assignment = {}
        if len(assignment) == len(self.variables):
            return assignment

        # get all variables in the CSP but not in the assignment
        unassigned: List = self.select_unassigned_variable(assignment)

        # organize all the different values in the unassigned variables
        ordered_unassigned = self.order_domain_values(unassigned, assignment)

        # get the every possible domain value of the first unassigned variable
        first = ordered_unassigned[0]
        for value in self.domains[first]:
            local_assignment = assignment.copy()
            local_assignment[first] = value

            # if we're still consistent, we recurse (continue)
            if self.consistent(first, local_assignment):
                # local_assignment[first] = value
                result = self.backtracking_search_rec(local_assignment)
                # if we didn't find the result, we will end up backtracking
                if result is not None:
                    return result
        return None

    def select_unassigned_variable(self, assignment) -> List:
        """
        choose the unassigned variables from all the variables.
        """
        # todo, this function need to get override by different CSP, to choose the best variable
        return [v for v in self.variables if v not in assignment]

    def order_domain_values(self, unassigned, assignment):
        """
        choose the order of the values we are going to try for variable
        """
        return unassigned


# ----------

# in board - we can use shakra's constraints complete thing
def is_board_filled(board):
    for row in board.board:
        for cell in row:
            if cell.color == EMPTY:
                return False
    return True


def get_variables_and_domains(board):
    """
    get variables and domains for CSP.
    """
    variables = []
    domains = {}

    # get constraint most left position (Row)
    for row_constraints in board.rows_constraints:
        for constraint in row_constraints:
            value = list(range(board.num_cols - constraint.length + 1))
            variables.append(constraint)
            domains[constraint] = value

    # get constraint most top position (Column)
    for col_constraints in board.cols_constraints:
        for constraint in col_constraints:
            value = list(range(board.num_rows - constraint.length + 1))
            variables.append(constraint)
            domains[constraint] = value

    all_colors = [_ for _ in range(len(COLORS_LST))]
    # get all cells in board
    for row in board.board:
        for cell in row:

            variables.append(cell)
            domains[cell] = all_colors

    return variables, domains


def get_constrains(board):
    """
    get the constraints for the CSP of a giving board of nonogram game
    """
    # row blocks:
    constraints = []
    for row_constraints in board.rows_constraints:
        k = 0
        while k < len(row_constraints) - 1:
            if row_constraints[k].color == row_constraints[k + 1].color:
                constraints.append(RowBlockEqualConstraint(row_constraints[k], row_constraints[k + 1]))
            else:
                constraints.append(RowBlockNotEqualConstraint(row_constraints[k], row_constraints[k + 1]))
            k += 1

    # col blocks
    for col_constraints in board.cols_constraints:
        k = 0
        while k < len(col_constraints) - 1:
            if col_constraints[k].color == col_constraints[k + 1].color:
                constraints.append(ColBlockEqualConstraint(col_constraints[k], col_constraints[k + 1]))
            else:
                constraints.append(ColBlockNotEqualConstraint(col_constraints[k], col_constraints[k + 1]))
            k += 1


    # Rows color contained check
    i = 0
    while i < board.num_rows:  # 3amodi
        j = 0
        while j < board.num_cols:  # ofoke
            if board.rows_constraints[i]:
                constraints.append(RowColorContained(board.board[i][j], *board.rows_constraints[i]))
            j += 1
        i += 1

    # Cols color contained check
    i = 0
    while i < board.num_rows:  # 3amodi
        j = 0
        while j < board.num_cols:  # ofoke
            if board.cols_constraints[j]:
                constraints.append(ColColorContained(board.board[i][j], *board.cols_constraints[j]))
            j += 1
        i += 1

    return constraints


############
# ALL CONSTRAINTS FOR CSP OF BOARD
#############
class RowColorContained(ConstraintForVariable):
    def __init__(self, v1, *v2):
        super().__init__([v1, *v2])
        self.cell_i_j: Cell = v1  # Cell
        self.tuple_constraints_i_k = v2  # Tuple Constraint

    def satisfied(self, assignment) -> bool:
        if self.cell_i_j not in assignment:
            return True
        assigned_constraints = [con for con in self.tuple_constraints_i_k if con in assignment]
        if not assigned_constraints:
            return True

        # list of constraints
        #Old mostly wrong
        # intersection = []
        # for ass_con in assigned_constraints:
        #     if (assignment[ass_con] <= self.cell_i_j.col) and (self.cell_i_j.col < ass_con.length + assignment[ass_con]):
        #         intersection.append(ass_con)
        #         if ass_con.color == assignment[self.cell_i_j]:
        #             return True
        #
        # for ass_con in assigned_constraints:
        #     if ass_con.color != assignment[self.cell_i_j]:
        #         if (assignment[ass_con] > self.cell_i_j.col) or (self.cell_i_j.col >= ass_con.length + assignment[ass_con]):
        #             return True
        # return False      #todo not that sure about it - i know we assigned all constraints before cells - so for the iff
        #-------------------------------------------------#
        #TRY 1
        negation = []
        for ass_con in assigned_constraints:
            if ass_con.color == assignment[self.cell_i_j]:
                if (assignment[ass_con] <= self.cell_i_j.col) and (self.cell_i_j.col < ass_con.length + assignment[ass_con]):
                    return True
            else:
                if (assignment[ass_con] > self.cell_i_j.col) or (self.cell_i_j.col >= ass_con.length + assignment[ass_con]):
                    negation.append(ass_con)

        return len(negation) == len(assigned_constraints)

        #______________________________________________
        # TRY 2
        # negation = []
        # for ass_con in assigned_constraints:
        #     if ass_con.color == assignment[self.cell_i_j] and (assignment[ass_con] <= self.cell_i_j.col) and (
        #                 self.cell_i_j.col < ass_con.length + assignment[ass_con]):
        #             return True
        #     else:
        #             negation.append(ass_con)
        #
        # return len(negation) == len(assigned_constraints)


class ColColorContained(ConstraintForVariable):
    def __init__(self, v1, *v2):
        super().__init__([v1, *v2])
        self.cell_i_j: Cell = v1  # Cell
        self.tuple_constraints_j_k = v2  # Tuple Constraint

    def satisfied(self, assignment) -> bool:
        if self.cell_i_j not in assignment:
            return True
        assigned_constraints = [con for con in self.tuple_constraints_j_k if con in assignment]
        if not assigned_constraints:
            return True
        #
        # # list of constraints
        # for ass_con in assigned_constraints:
        #     if (assignment[ass_con] <= self.cell_i_j.row) and (self.cell_i_j.row < ass_con.length + assignment[ass_con]):
        #         if ass_con.color == assignment[self.cell_i_j]:
        #             return True
        #     else:
        #         if ass_con.color != assignment[self.cell_i_j]:
        #             return True
        # return False     #todo not that sure about it - i know we assigned all constraints before cells - so for the iff

        # TRY 2
        negation = []
        for ass_con in assigned_constraints:
            if ass_con.color == assignment[self.cell_i_j] and (assignment[ass_con] <= self.cell_i_j.row) and (
                        self.cell_i_j.row < ass_con.length + assignment[ass_con]):
                return True
            else:
                if (assignment[ass_con] > self.cell_i_j.row) or (self.cell_i_j.row >= ass_con.length + assignment[ass_con]):
                    negation.append(ass_con)

        return len(negation) == len(assigned_constraints)


class RowBlockEqualConstraint(ConstraintForVariable):
    def __init__(self, v1, v2):
        super().__init__([v1, v2])
        self.r_i_k = v1
        self.r_i_k_1 = v2

    def satisfied(self, assignment) -> bool:
        if self.r_i_k not in assignment or self.r_i_k_1 not in assignment:
            return True
        return self.r_i_k.length + assignment[self.r_i_k] < assignment[self.r_i_k_1]


class RowBlockNotEqualConstraint(ConstraintForVariable):
    def __init__(self, v1, v2):
        super().__init__([v1, v2])
        self.r_i_k = v1
        self.r_i_k_1 = v2

    def satisfied(self, assignment) -> bool:
        if self.r_i_k not in assignment or self.r_i_k_1 not in assignment:
            return True
        return self.r_i_k.length + assignment[self.r_i_k] <= assignment[self.r_i_k_1]


class ColBlockEqualConstraint(ConstraintForVariable):
    def __init__(self, v1, v2):
        super().__init__([v1, v2])
        self.c_i_k = v1
        self.c_i_k_1 = v2

    def satisfied(self, assignment) -> bool:
        if self.c_i_k not in assignment or self.c_i_k_1 not in assignment:
            return True
        return self.c_i_k.length + assignment[self.c_i_k] < assignment[self.c_i_k_1]


class ColBlockNotEqualConstraint(ConstraintForVariable):
    def __init__(self, v1, v2):
        super().__init__([v1, v2])
        self.c_i_k = v1
        self.c_i_k_1 = v2

    def satisfied(self, assignment) -> bool:
        if self.c_i_k not in assignment or self.c_i_k_1 not in assignment:
            return True
        return self.c_i_k.length + assignment[self.c_i_k] <= assignment[self.c_i_k_1]


def run_CSP(board):
    # for r in range(board.num_rows):
    #     for c in range(board.num_cols):
    #         board.fill(r, c, WHITE)
    variables, domains = get_variables_and_domains(board)
    our_csp = CSP(variables, domains)
    the_constraints = get_constrains(board)
    for con in the_constraints:
        our_csp.add_constraint(con)

    test = our_csp.backtracking_search_rec()
    if test:
        test2 = our_csp.backtracking_search_rec()
        print()