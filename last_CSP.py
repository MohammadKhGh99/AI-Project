import math
from abc import abstractmethod

import Board
from config import *
from typing import Dict, List


# FAKE
class ConstraintForVariable:
    def __init__(self, variables: List) -> None:
        self.variables = variables

    # Must be overridden by subclasses
    @abstractmethod
    def satisfied(self, assignment) -> bool:
        ...


class CSP:
    def __init__(self, variables, domains, neighbors):
        self.variables = variables      # A list of variables
        self.domains: Dict = domains     # {var:[possible_value, ...]}
        self.neighbors: Dict = neighbors  # {var: [var,...]}
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

    def nconflicts(self, variable, value, assignment):
        "Return the number of conflicts var=val has with other variables."
        def conflict(var2):
            val2 = assignment.get(var2, None)

            if val2 is not None:
                temp_assignment[var2] = val2
                return not self.consistent(variable, temp_assignment)
        temp_assignment = {variable: value}
        return self.count_matching(conflict, self.neighbors[variable])

    def count_matching(self, condition, seq):
        """Returns the amount of items in seq that return true from condition"""
        return sum(1 for item in seq if condition(item))

    def cmp(self, a, b):
        return (a > b) - (a < b)

    def backtracking_search_rec(self, assignment=None):
        # assignment is complete if every variable is assigned (our base case)
        if assignment is None:
            assignment = {}
        if len(assignment) == len(self.variables):
            return assignment

        # get the first variable in the CSP but not in the assignment
        variable = self.select_unassigned_variable(assignment)

        # organize all the different values for this unassigned variable
        ordered_domain = self.order_domain_values(variable, assignment)

        # get the every possible domain value for this unassigned variable
        for value in ordered_domain:
            local_assignment = assignment.copy()
            local_assignment[variable] = value

            # if we're still consistent, we recurse (continue)
            if self.consistent(variable, local_assignment):
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
        return [v for v in self.variables if v not in assignment][0]

    def order_domain_values(self, variable, assignment):
        """
        choose the order of the values we are going to try for variable
        """
        return self.domains[variable]


class MRV_CSP(CSP):
    def select_unassigned_variable(self, assignment) -> List:
        """
        choose variable with the least amount of values
        """
        unassigned_variables = [v for v in self.variables if v not in assignment]
        least_values = math.inf
        first_var = None
        for var in unassigned_variables:
            if least_values >= len(self.domains[var]):
                least_values = len(self.domains[var])
                first_var = var
        return first_var


class degree_CSP(CSP):
    def select_unassigned_variable(self, assignment) -> List:
        """
        choose variable with the most amount of constraints
        """
        unassigned_variables = [v for v in self.variables if v not in assignment]
        most_constraints = -math.inf
        first_var = None
        for var in unassigned_variables:
            if most_constraints <= len(self.constraints[var]):
                most_constraints = len(self.constraints[var])
                first_var = var
        return first_var


class MRV_then_degree_CSP(CSP):
    def select_unassigned_variable(self, assignment) -> List:
        """
        choose variable with the least amount of values and most amount of constraints
        """
        unassigned_variables = [v for v in self.variables if v not in assignment]
        least_values = math.inf
        vars_with_least_values = []
        for var in unassigned_variables:
            if least_values > len(self.domains[var]):
                least_values = len(self.domains[var])
                vars_with_least_values = [var]
            elif least_values == len(self.domains[var]):
                vars_with_least_values.append(var)

        most_constraints = -math.inf
        first_var = None
        for var in vars_with_least_values:
            if most_constraints <= len(self.constraints[var]):
                most_constraints = len(self.constraints[var])
                first_var = var
        return first_var


class LCV_CSP(CSP):
    def order_domain_values(self, variable, assignment):
        domain_for_var = self.domains[variable].copy()
        num_of_conflicts = []
        for value in domain_for_var:
            num_of_conflicts.append((value, self.nconflicts(variable, value, assignment)))
        for conf in num_of_conflicts:
            if conf[1] >= 1:
                print()
        sorted_conflicts = sorted(num_of_conflicts, key=lambda x: x[1])
        domain_for_var = [val[0] for val in sorted_conflicts]

        while domain_for_var:
            yield domain_for_var.pop()


# class degree_then_MRV_CSP(CSP):
#     def select_unassigned_variable(self, assignment) -> List:
#         """
#         choose variable with the most amount of constraints and least amount of values
#         """
#         unassigned_variables = [v for v in self.variables if v not in assignment]
#         least_values = math.inf
#         vars_with_least_values = []
#         for var in unassigned_variables:
#             if least_values > len(self.domains[var]):
#                 least_values = len(self.domains[var])
#                 vars_with_least_values = [var]
#             elif least_values == len(self.domains[var]):
#                 vars_with_least_values.append(var)
#
#         most_constraints = -math.inf
#         first_var = None
#         for var in vars_with_least_values:
#             if most_constraints <= len(self.constraints[var]):
#                 most_constraints = len(self.constraints[var])
#                 first_var = var
#         return [first_var]


def get_variables_and_domains(board):
    """
    get variables and domains for CSP.
    our variables: tuple: first index is boolean reffering to rows(False) or columns(True), second index is row/col index.
    our domains: each combination the variable can have as a row/col
    """
    variables = []
    domains = {}
    row_constraints_list = get_constraints_boundaries(board, ROWS)
    col_constraints_list = get_constraints_boundaries(board, COLUMNS)

    # get variables and domains - rows
    possibilities_rows = []
    for idx, dic in enumerate(row_constraints_list):
        pos_row = []
        get_all_possibilities(board.rows_constraints[idx], dic, pos_row, [WHITE] * board.num_cols, 0, 0)
        var = ROWS, idx
        variables.append(var)
        domains[var] = pos_row
        # possibilities_rows.append(pos_row)

    # get variables and domains - columns
    possibilities_cols = []
    for idx, dic in enumerate(col_constraints_list):
        pos_col = []
        get_all_possibilities(board.cols_constraints[idx], dic, pos_col, [WHITE] * board.num_rows, 0, 0)
        var = COLUMNS, idx
        variables.append(var)
        domains[var] = pos_col
        # possibilities_cols.append(pos_col)

    # return variables, domains
    return variables, domains


def get_all_possibilities(constraint_list, dict_of_blocks, final_result, curr_ans, curr_constraint_idx, index_to_fill):
    """
    get all possible LEGIT row/column filled line by the constraints
    """
    if index_to_fill >= len(curr_ans):
        # we finished
        final_result.append(curr_ans)
        return
    elif curr_constraint_idx >= len(constraint_list):
        # we finished all the constraints, fill the rest with white cells
        while index_to_fill < len(curr_ans):
            curr_ans[index_to_fill] = WHITE
            index_to_fill += 1
        final_result.append(curr_ans)
        return
    else:
        # we need to fill some colors (constraints)
        constraint_length = constraint_list[curr_constraint_idx].length
        constraint_color = constraint_list[curr_constraint_idx].color

        block_first_last_position = dict_of_blocks[constraint_list[curr_constraint_idx]]
        block_possible_positions = list(range(block_first_last_position[0], block_first_last_position[1] + 1))
        old_index_to_fill = index_to_fill
        for position in block_possible_positions:
            temp_curr_ans = curr_ans.copy()
            index_to_fill = old_index_to_fill
            if position > 0 and temp_curr_ans[position - 1] == constraint_color:
                continue
            if position < index_to_fill:
                continue
            else:
                # fill white cells before constraint
                num_white_cells = position - index_to_fill
                for i in range(num_white_cells):
                    temp_curr_ans[index_to_fill + i] = WHITE
                index_to_fill += num_white_cells

                if index_to_fill + constraint_length - 1 <= len(temp_curr_ans) - 1:
                    # fill the constraint
                    # check the -1 maybe it's wrong like this
                    for j in range(constraint_length):
                        temp_curr_ans[index_to_fill + j] = constraint_color
                    index_to_fill += constraint_length

                    # we finished this constraint move to next constraint
                    get_all_possibilities(constraint_list, dict_of_blocks, final_result, temp_curr_ans, curr_constraint_idx + 1, index_to_fill)

                else:
                    # we can't fill this constraint, something is wrong, (I think this will never happen)
                    return


def get_constraints_boundaries(board, constraint_type):
    """
    fill a list with dictionaries of constraints, each dictionary contain a row or a column with it's constraint
    that it's value is a list of the range this constraint could possibly be in
    """
    if constraint_type == ROWS:
        constraint_is = board.rows_constraints
        limit_of_board = board.num_cols
    else:
        constraint_is = board.cols_constraints
        limit_of_board = board.num_rows

    all_positions_for_constraint_list = []
    for constraints_list in constraint_is:
        possible_positions = dict((block, [EMPTY, EMPTY]) for block in constraints_list)
        # fill smallest_most_left_pixel
        old_con_color = EMPTY
        old_cluster_finish_pos = 0
        for con in constraints_list:
            if con.color == old_con_color:
                old_cluster_finish_pos += 1
            possible_positions[con][0] = old_cluster_finish_pos
            old_cluster_finish_pos += con.length
            old_con_color = con.color

        # fill largest_most_left_pixel
        old_con_color = EMPTY
        old_cluster_end_pos = limit_of_board
        for con_reverse in reversed(constraints_list):
            if con_reverse.color == old_con_color:
                old_cluster_end_pos -= 1

            old_cluster_end_pos -= con_reverse.length
            possible_positions[con_reverse][1] = old_cluster_end_pos
            # old_cluster_end_pos = con_reverse.largest_most_left_pixel
            old_con_color = con_reverse.color

        all_positions_for_constraint_list.append(possible_positions)

    return all_positions_for_constraint_list


def get_constrains_and_neighbors(board):
    """
    making constraints between variables
    """
    neighbors = {}
    columns_constraints = []
    rows_constraints = []
    constraints = []
    for col_idx in range(len(board.cols_constraints)):
        temp_variable = (COLUMNS, col_idx)
        columns_constraints.append(temp_variable)
        neighbors[temp_variable] = []

    for row_idx in range(len(board.rows_constraints)):
        temp_variable = (ROWS, row_idx)
        rows_constraints.append(temp_variable)
        constraints.append(RowColumnConstraint(temp_variable, *columns_constraints))
        neighbors[temp_variable] = columns_constraints

    # todo, I feel we don't need this, but we keep it for now
    for col_idx in range(len(board.cols_constraints)):
        temp_variable = (COLUMNS, col_idx)
        constraints.append(RowColumnConstraint(temp_variable, *rows_constraints))
        neighbors[temp_variable] = rows_constraints

    return constraints, neighbors

def run_CSP_last(game):
    board = game.board
    variables, domains = get_variables_and_domains(board)
    the_constraints, neighbors = get_constrains_and_neighbors(board)
    our_csp = CSP(variables, domains, neighbors)
    our_csp_mrv = MRV_CSP(variables, domains, neighbors)
    our_csp_lcv = LCV_CSP(variables, domains, neighbors)
    for con in the_constraints:
        our_csp.add_constraint(con)
        our_csp_mrv.add_constraint(con)

    test = our_csp.backtracking_search_rec()
    test2 = our_csp_mrv.backtracking_search_rec()
    test3 = our_csp_lcv.backtracking_search_rec()
    print()



class RowColumnConstraint(ConstraintForVariable):
    def __init__(self, v1, *v2):
        super().__init__([v1, *v2])
        self.row = v1
        self.all_columns = v2    # tuple of tuples each tuple: (COLUMNS, idx)

    def satisfied(self, assignment) -> bool:
        if self.row not in assignment:
            return True
        #####################################3
        ##            DELETE                ##
        if self.row == (COLUMNS, 0):
            print()
        all_assigned_columns = []
        for col in self.all_columns:
            if col in assignment:
                all_assigned_columns.append(col)

        if not all_assigned_columns:
            return True

        for column in all_assigned_columns:
            if assignment[column][self.row[1]] != assignment[self.row][column[1]]:
                return False
        return True
