import math
from abc import abstractmethod

import Board
from config import *
from typing import Dict, List
import Board


class ConstraintForVariable:
    """ Generic class to add constraints between variables"""

    def __init__(self, variables: List) -> None:
        self.variables = variables

    # Must be overridden by subclasses
    @abstractmethod
    def satisfied(self, assignment) -> bool:
        ...


class RowColumnConstraint(ConstraintForVariable):
    """ constraint such that: we are making sure a row value is satisfied between all columns"""

    def __init__(self, v1, *v2):
        super().__init__([v1, *v2])
        self.row = v1
        self.all_columns = v2  # tuple of tuples each tuple: (COLUMNS, idx)

    def satisfied(self, assignment) -> bool:
        if self.row not in assignment:
            return True

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


class CSP:
    """ a generic CSP class, that has the main things a CSP uses"""
    created_or_not = False

    def __init__(self, variables, domains, neighbors, board):
        self.variables = variables  # A list of variables
        self.domains: Dict = domains  # {var:[possible_value, ...]}
        self.neighbors: Dict = neighbors  # {var: [var,...]}
        self.constraints = {}
        self.board = board

        for variable in self.variables:
            self.constraints[variable] = []

        self.curr_domains, self.pruned = None, None
        self.csp_types = set()
        CSP.created_or_not = True

    def add_constraint(self, constraint: ConstraintForVariable) -> None:
        """ fill the constraints for the variables"""
        for variable in constraint.variables:
            self.constraints[variable].append(constraint)

    def consistent(self, variable, assignment):
        """ check if the constraints being satisfied"""
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    def consistent2(self, variable, value, other_var, other_value):
        """ if it is consistent (works), return True"""
        if value[other_var[1]] == other_value[variable[1]]:
            return True

    def assign(self, var, val, assignment):
        """ assign a value to this variable"""
        assignment[var] = val
        if var[0] == ROWS:
            for i in range(self.board.num_cols):
                self.board.fill(var[1], i, val[i], brute_force=CSP_P)
                # self.board.board[index][i].color = to_fill[i]
        elif var[0] == COLUMNS:
            for i in range(self.board.num_rows):
                self.board.fill(i, var[1], val[i], brute_force=CSP_P)
        # print(assignment)

        # TODO - MHMD - we need to fill (one assignment only!)
        if self.curr_domains:
            if FC in self.csp_types:
                self.forward_check(var, val, assignment)

    def unassign(self, var, assignment):
        """ delete the assigned value from this variable"""
        if var in assignment:
            if self.curr_domains:
                self.curr_domains[var] = self.domains[var][:]

            # unfill the wrong assignment
            if var[0] == ROWS:
                for i in range(self.board.num_cols):
                    self.board.unfill(var[1], i)
            elif var[0] == COLUMNS:
                for i in range(self.board.num_rows):
                    self.board.unfill(i, var[1])
            if Board.Board.gui is not None:
                Board.Board.gui.root.update()

            for var1 in assignment.keys():
                if var1 == var:
                    continue
                val = assignment[var1]
                if var1[0] == ROWS:
                    for i in range(self.board.num_cols):
                        if self.board.board[var1[1]][i].color == EMPTY:
                            self.board.fill(var1[1], i, val[i], brute_force=CSP_P)
                        # self.board.board[index][i].color = to_fill[i]
                elif var1[0] == COLUMNS:
                    for i in range(self.board.num_rows):
                        if self.board.board[i][var1[1]].color == EMPTY:
                            self.board.fill(i, var1[1], val[i], brute_force=CSP_P)
            # Board.Board.gui.root.update()

            del assignment[var]
            # TODO - MHMD - we need to fill all the assignments over!

    def nconflicts(self, variable, value, assignment):
        """Return the number of conflicts var=val has with other variables."""

        def conflict(var2):
            val2 = assignment.get(var2, None)
            if val2 is not None:
                temp_assignment[var2] = val2
                return not self.consistent(variable, temp_assignment)

        temp_assignment = {variable: value}
        return self.count_matching(conflict, self.neighbors[variable])

    def nconflicts2(self, var, val, assignment):
        """Return the number of conflicts var=val has with other variables."""

        def conflict(var2):
            val2 = assignment.get(var2, None)
            return val2 is not None and not self.consistent2(var, val, var2, val2)

        return self.count_matching(conflict, self.neighbors[var])

    def count_matching(self, condition, seq):
        """Returns the amount of items in seq that return true from condition"""
        return sum(1 for item in seq if condition(item))

    def backtracking_search(self, csp_types):
        """ this will initialize the backtracking as we please"""

        for csp in csp_types:
            if csp == MRV:
                self.csp_types.add(MRV)
            if csp == DEGREE:
                self.csp_types.add(DEGREE)
            if csp == LCV:
                self.csp_types.add(LCV)
            if csp == FC:
                self.csp_types.add(FC)
            if csp == AC:
                self.csp_types.add(AC)

        if FC in self.csp_types or AC in self.csp_types:
            self.curr_domains, self.pruned = {}, {}
            for v in self.variables:
                self.curr_domains[v] = self.domains[v][:]
                self.pruned[v] = []
        if AC in self.csp_types:
            self.AC3(None)
        return self.backtracking_search_rec({})

    def backtracking_search_rec(self, assignment=None):
        """ this is the recursive backtracking search"""
        # assignment is complete if every variable is assigned (our base case)
        if assignment is None:
            assignment = {}
        if len(assignment) == len(self.variables):
            return assignment

        # get the first variable in the CSP but not in the assignment
        variable = self.select_unassigned_variable(assignment)
        # get every possible domain value that are in order for this unassigned variable
        for value in self.order_domain_values(variable, assignment):
            # check if there is a conflicts between variables and assignments

            if FC in self.csp_types or self.nconflicts2(variable, value, assignment) == 0:
                # perfect! no conflict, assign the value to variable
                self.assign(variable, value, assignment)

                # backtrack baby

                result = self.backtracking_search_rec(assignment)

                # if we didn't find the result, we will end up backtracking
                if result is not None:
                    return result
                elif FC in self.csp_types:
                    # Restore prunings from previous value of var
                    for (other_variable, other_value) in self.pruned[variable]:
                        self.curr_domains[other_variable].append(other_value)
                    self.pruned[variable] = []

            # this might be a failure assigning, but don't give up, we will try again!

            self.unassign(variable, assignment)
        return None

    def select_unassigned_variable(self, assignment) -> List:
        """
        choose the unassigned variables from all the variables.
        """
        if MRV in self.csp_types or DEGREE in self.csp_types:  # MRV or DEGREE
            unassigned_variables = [v for v in self.variables if v not in assignment]
            vars_with_least_values = []
            # MRV
            if MRV in self.csp_types:
                least_values = math.inf
                for var in unassigned_variables:
                    if least_values > len(self.domains[var]):
                        least_values = len(self.domains[var])
                        vars_with_least_values = [var]
                    elif least_values == len(self.domains[var]):
                        vars_with_least_values.append(var)
            # DEGREE
            if DEGREE in self.csp_types:
                if vars_with_least_values:  # if true: MRV + DEGREE
                    unassigned_variables = vars_with_least_values
                most_constraints = -math.inf
                first_var = None
                for var in unassigned_variables:
                    if most_constraints <= len(self.constraints[var]):
                        most_constraints = len(self.constraints[var])
                        first_var = var
                return first_var
            else:  # we don't have DEGREE
                return vars_with_least_values[0]

        else:  # any other type
            for v in self.variables:
                if v not in assignment:
                    return v

    def order_domain_values(self, variable, assignment):
        """
        choose the order of the values we are going to try for variable
        """
        if self.curr_domains:  # we have FC or AC
            domain_for_var = self.curr_domains[variable]
        else:
            domain_for_var = self.domains[variable][:]

        if LCV in self.csp_types:  # LCV
            num_of_conflicts = []
            for value in domain_for_var:
                num_of_conflicts.append((value, self.nconflicts(variable, value, assignment)))
            sorted_conflicts = sorted(num_of_conflicts, key=lambda x: x[1])
            domain_for_var = [val[0] for val in sorted_conflicts]

        return domain_for_var

        # while domain_for_var:
        #     yield domain_for_var.pop()

    def forward_check(self, variable, value, assignment):
        """Do forward checking for this assignment."""
        if self.curr_domains:
            for other_variable in self.neighbors[variable]:
                if other_variable not in assignment:
                    for other_value in self.curr_domains[other_variable][:]:
                        if not self.consistent2(variable, value, other_variable, other_value):
                            self.curr_domains[other_variable].remove(other_value)
                            self.pruned[variable].append((other_variable, other_value))

    def AC3(self, queue):
        """ applying the rules of Arc Consistency"""
        if queue is None:
            queue = [(curr_var, var_neighbor) for curr_var in self.variables for var_neighbor in
                     self.neighbors[curr_var]]
        while queue:
            (curr_var, var_neighbor) = queue.pop()
            if self.remove_inconsistent_values(curr_var, var_neighbor):
                # if self.remove_inconsistent_values(var_neighbor, curr_var):
                for another_neighbor in self.neighbors[curr_var]:
                    queue.append((another_neighbor, curr_var))

    def remove_inconsistent_values(self, variable, other_variable):
        """a helper function for AC3 - Return true if we remove a value."""
        removed = False
        for value in self.curr_domains[variable][:]:
            # If variable=value conflicts with other_variable=other_value for every possible other_value, eliminate Xi=x
            if not self.curr_domains[other_variable]:
                print()
            if all(map(lambda y: not self.consistent2(variable, value, other_variable, y),
                       self.curr_domains[other_variable])):
                self.curr_domains[variable].remove(value)
                removed = True
        return removed


def get_variables_and_domains(board):
    """
    get variables and domains for CSP.
    our variables: tuple: first index is boolean reffering to rows(False) or columns(True),
                   second index is row/col index.
    our domains: each combination the variable can have as a row/col
    """
    variables = []
    domains = {}
    row_constraints_list = get_constraints_boundaries(board, ROWS)
    col_constraints_list = get_constraints_boundaries(board, COLUMNS)

    # get variables and domains - rows
    for idx, dic in enumerate(row_constraints_list):
        pos_row = []
        get_all_possibilities(board.rows_constraints[idx], dic, pos_row, [WHITE] * board.num_cols, 0, 0)
        var = ROWS, idx
        variables.append(var)
        domains[var] = pos_row

    # get variables and domains - columns
    for idx, dic in enumerate(col_constraints_list):
        pos_col = []
        get_all_possibilities(board.cols_constraints[idx], dic, pos_col, [WHITE] * board.num_rows, 0, 0)
        var = COLUMNS, idx
        variables.append(var)
        domains[var] = pos_col

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
                    for j in range(constraint_length):
                        temp_curr_ans[index_to_fill + j] = constraint_color
                    index_to_fill += constraint_length

                    # we finished this constraint move to next constraint
                    get_all_possibilities(constraint_list, dict_of_blocks, final_result, temp_curr_ans,
                                          curr_constraint_idx + 1, index_to_fill)

                else:
                    # we can't fill this constraint, something is wrong, (I think this will never happen)
                    return


def get_constraints_boundaries(board, constraint_type):
    """
    fill a list with dictionaries of constraints, each dictionary contain a row or a column with its constraint
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
    making constraints and neighbors between variables
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

    for col_idx in range(len(board.cols_constraints)):
        temp_variable = (COLUMNS, col_idx)
        neighbors[temp_variable] = rows_constraints
        # constraints.append(RowColumnConstraint(temp_variable, *rows_constraints))

    return constraints, neighbors


# -----------------------


def run_CSP(board, types_of_csps=None):
    # if not CSP.created_or_not:
    variables, domains = get_variables_and_domains(board)
    the_constraints, neighbors = get_constrains_and_neighbors(board)
    our_csp = CSP(variables, domains, neighbors, board)

    for con in the_constraints:
        our_csp.add_constraint(con)

    print(types_of_csps)

    # MRV, DEGREE, LCV, FC, AC, ALL_CSPS
    if types_of_csps is None:
        types_of_csps = {AC}
    res = our_csp.backtracking_search(types_of_csps)
    if res:
        print_result(res, str("Normal"))

    return our_csp.board


# ------------------------

def test_all_new(game):
    board = game.board
    variables, domains = get_variables_and_domains(board)
    the_constraints, neighbors = get_constrains_and_neighbors(board)

    dict_all = select_all_csps()
    new_dict_all = {}
    for k, v in dict_all.items():
        new_dict_all[k] = (v, CSP(variables, domains, neighbors, board))

    for con in the_constraints:
        for value in new_dict_all.values():
            value[1].add_constraint(con)

    all_csps_results = []
    for type_of_csp, csp in new_dict_all.items():
        # TODO - time start
        res = csp[1].backtracking_search(csp[0])
        # TODO - time finish
        if res:
            all_csps_results.append(print_result(res, type_of_csp))
        else:
            print("------------------------------------------")
            print("None results: " + type_of_csp)

    first_set = all_csps_results[0]
    for second_set in all_csps_results:
        ans = first_set.symmetric_difference(second_set)
        if ans:
            print(first_set)
            print()
            print(second_set)
            break
    else:
        print("all correct")


def select_csp_types(csp):
    result = set()
    # individuals:
    if csp == MRV:
        result.add(MRV)
    if csp == DEGREE:
        result.add(DEGREE)
    if csp == LCV:
        result.add(LCV)
    if csp == FC:
        result.add(FC)
    if csp == AC:
        result.add(AC)

    return result


def csp_names(csp_set):
    ans = ""
    for csp in csp_set:
        if csp == MRV:
            ans += "MRV "
        if csp == DEGREE:
            ans += "DEGREE "
        if csp == LCV:
            ans += "LCV "
        if csp == FC:
            ans += "FC "
        if csp == AC:
            ans += "AC "
    return ans


def select_all_csps():
    # all_things_test2 = []
    all_things_test = dict()

    # NO CSP
    # all_things_test.append({0})
    all_things_test["Normal"] = list({0})
    # individuals:
    for csp1 in ALL_CSPS:
        curr_1 = select_csp_types(csp1)
        for csp2 in ALL_CSPS:
            curr_2 = curr_1.union(select_csp_types(csp2))
            if len(curr_2) < 2:
                continue
            for csp3 in ALL_CSPS:
                curr_3 = curr_2.union(select_csp_types(csp3))
                if len(curr_3) < 3:
                    continue
                for csp4 in ALL_CSPS:
                    curr_4 = curr_3.union(select_csp_types(csp4))
                    if len(curr_4) < 4:
                        continue
                    all_things_test[csp_names(curr_4)] = list(curr_4)
                all_things_test[csp_names(curr_3)] = list(curr_3)
            all_things_test[csp_names(curr_2)] = list(curr_2)
        all_things_test[csp_names(curr_1)] = list(curr_1)

    all_things_test["ALL"] = ALL_CSPS
    return all_things_test


def print_result(dic, type_of_csp):
    print("------------------------------------------")
    sorted_dic = dict(sorted(dic.items()))
    rows = []
    cols = []
    for k, v in sorted_dic.items():
        if k[0] == ROWS:
            rows.append(v)
        else:
            cols.append(v)

    # print(type_of_csp + ":")

    rows_from_cols = []
    for v in zip(*cols):
        rows_from_cols.append(v)

    first_set = set(map(tuple, rows))
    second_set = set(map(tuple, rows_from_cols))
    ans = first_set.symmetric_difference(second_set)
    if ans:
        print(type_of_csp)
        print()
        print("ROWS")
        for s in rows:
            print(*s)
        print("COLUMNS")
        for d in rows_from_cols:
            print(*d)
        return type_of_csp
    else:
        print(type_of_csp + ": Perfect!")
        return first_set
