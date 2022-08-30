from game import *


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        raise Exception("Not implemented.")

    def is_goal_state(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        raise Exception("Not implemented.")

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there
        """
        raise Exception("Not implemented.")

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        raise Exception("Not implemented.")


class NonogramCellsProblem(SearchProblem):
    """
        Class that defining the nonogram game as a problem. Solving it by checking cell by cell.
        BFS, DFS and A* solve this problem.
    """

    def __init__(self, board, search_type):
        self.board = board
        self.cost = 0
        self.search_type = search_type

    def get_start_state(self):
        return self.board

    def is_goal_state(self, state):
        """
            Goal state when we reach the last cell (right bottom corner),
            and we find a legal fill for it.
        """
        if self.search_type == LBS:
            for i in range(self.board.num_cols):
                for j in range(self.board.num_rows):
                    if self.board.board[j][i].color == EMPTY or not self.board.check_move(j, i):
                        return False
            return True
        return self.board.current_cell.row == self.board.num_rows and self.board.current_cell.col == 0

    def get_successors(self, state):
        """
            Successors are all the 3 possible colors: white, red and black.
            Each successor is a cell, the cell we want to fill in the board.
        """
        successors = []
        if self.search_type == DFS:
            colors = [WHITE, RED, BLACK]
        else:
            colors = [BLACK, RED, WHITE]
        if self.board.current_cell.row == self.board.num_rows:
            # We finished all the cells.
            return successors

        for color in colors:
            actions = []
            cell = Cell(self.board.current_cell.row, self.board.current_cell.col, color)
            actions.append(cell)
            successors.append((self.board, actions))
        return successors

    def get_cost_of_actions(self, actions):
        # Actions are a set of cell's coordinates we colored to get a new state.
        if actions[0].color == WHITE:
            return self.cost - 0.5
        return self.cost - 1


# No need for this class.
class BFSProblem(SearchProblem):
    """
        Class that defining the nonogram game as a problem.
    """

    def __init__(self, board):
        self.board = board

    def get_start_state(self):
        return self.board

    def is_goal_state(self, state):
        """
            Goal state when we reach the last cell (right bottom corner),
            and we find a legal fill for it.
        """
        return self.board.current_cell.row == self.board.num_rows and self.board.current_cell.col == 0

    def get_successors(self, state):
        """
            Successors are all the 3 possible colors: white, red and black.
            Each successors is a cell, the cell we want to fill in the board.
        """
        successors = []
        if self.board.current_cell.row == self.board.num_rows:
            # We finished all the cells.
            return successors

        for color in [WHITE, BLACK, RED]:
            actions = deepcopy(self.board.moves)
            cell = Cell(self.board.current_cell.row, self.board.current_cell.col, color)
            actions.append(cell)
            successors.append((self.board, actions))
        return successors

    def get_cost_of_actions(self, actions):
        # Actions are a set of cell's coordinates we colored to get a new state.
        return


class NonogramProblem(SearchProblem):
    """
        Class that defining the nonogram game as a problem.
    """

    def __init__(self, board):
        self.board = board

    def get_start_state(self):
        return self.board

    def is_goal_state(self, state):
        return (state.get_first_incomplete_constraint(COLUMNS) is None) and \
               (state.get_first_incomplete_constraint(ROWS) is None)

    def get_successors(self, state):
        successors = []
        constraint_coord = state.get_first_incomplete_constraint(ROWS)

        if constraint_coord is None:
            # We have done all the constraints
            return successors

        for start_index in range(state.num_cols):
            child = state.fill_n_cells(constraint_coord[0], constraint_coord[1], start_index, ROWS)
            if child is not None:
                actions = set()
                constraint = state.rows_constraints[constraint_coord[0]][constraint_coord[1]]
                for i in range(constraint.length):
                    actions.add((constraint_coord[0], start_index + i))  #, constraint.color))
                successors.append((child, actions))
        return successors

    def get_cost_of_actions(self, state):
        # Actions are a set of cell's coordinates we colored to get a new state.
        # Todo it looks like a heuristic function, discuss this with team.
        # cost zero.
        sum_completed_constrains = 0
        for row_con in state.rows_constraints:
            for constraint in row_con:
                if constraint.completed:
                    sum_completed_constrains += 1
        return -1 * sum_completed_constrains


# class NonogramCells(SearchProblem):
#     """
#         Class that defining the nonogram game as a problem.
#     """
#
#     def __init__(self, board):
#         self.board = board
#         self.current_cell = 0
#
#     def get_start_state(self):
#         return self.board
#
#     def is_goal_state(self, state):
#         return (state.get_first_incomplete_constraint(COLUMNS) is None) and \
#                (state.get_first_incomplete_constraint(ROWS) is None)
#
#     def get_successors(self, state):
#         successors = []
#         constraint_coord = state.get_first_incomplete_constraint(COLUMNS)
#
#         if constraint_coord is None:
#             # We have done all the constraints
#             return successors
#
#         for start_index in range(state.num_rows):
#             child = state.fill_n_cells(constraint_coord[0], constraint_coord[1], start_index, COLUMNS)
#             if child is not None:
#                 actions = set()
#                 constraint = state.cols_constraints[constraint_coord[0]][constraint_coord[1]]
#                 for i in range(constraint.length):
#                     actions.add((start_index + i, constraint_coord[0]))
#                 successors.append((child, actions))
#         return successors
#
#     def get_cost_of_actions(self, state):
#         # Actions are a set of cell's coordinates we colored to get a new state.
#         sum_completed_constrains = 0
#         for row_con in state.rows_constraints:
#             for constraint in row_con:
#                 if constraint.completed:
#                     sum_completed_constrains += 1
#         return -1 * sum_completed_constrains


# todo - fix the design and the problems that Ibraheem made

class BruteForce:
    def __init__(self, board):
        self.board = board

    def brute_force(self):
        """
        try to solve a board of nonogram by trying everything (brute force)
        """
        result = self._brute_force_helper(0, 0)
        if result:
            return self

    def _brute_force_helper(self, row_id, col_id):
        """
        this is a recursion function, we do recursion to solve it in brute force.
        """
        for color in [RED, BLACK, WHITE]:
            self.board.fill(row_id, col_id, color, brute_force=BRUTE)
            # check if this move works, if yes go to next cell.
            if self.board.check_move(col_id, row_id):
                if col_id + 1 < len(self.board.cols_constraints):
                    res = self._brute_force_helper(row_id, col_id + 1)
                    if res:
                        return res
                elif row_id + 1 < len(self.board.rows_constraints):
                    res2 = self._brute_force_helper(row_id + 1, 0)
                    if res2:
                        return res2
                else:
                    #  finished - the board is complete
                    return self
        # no color is correct
        self.board.fill(row_id, col_id, EMPTY, brute_force=BRUTE)
        return

#
# def brute_force(board):
#     """
#     try to solve a board of nonogram by trying everything (brute force)
#     """
#     result = _brute_force_helper(board, 0, 0)
#     if result:
#         return board
#
#
# def _brute_force_helper(board, row_id, col_id):
#     """
#     this is a recursion function, we do recursion to solve it in brute force.
#     """
#     for color in [RED, BLACK, WHITE]:
#         board.fill(row_id, col_id, color)
#         # check if this move works, if yes go to next cell.
#         if check_move(board, col_id, row_id):
#             if col_id + 1 < len(board.cols_constraints):
#                 res = _brute_force_helper(board, row_id, col_id + 1)
#                 if res:
#                     return res
#             elif row_id + 1 < len(board.rows_constraints):
#                 res2 = _brute_force_helper(board, row_id + 1, 0)
#                 if res2:
#                     return res2
#             else:
#                 #  finished - the board is complete
#                 return board
#     # no color is correct
#     board.fill(row_id, col_id, EMPTY)
#     return
#
#
# def check_move(board, row_id, col_id, problem_type=BRUTE_FORCE):
#     """
#     check if the move in this row_id/col_id is legit.
#     """
#     # checking for the rows
#     if not _check_move_helper_with_constraint_check(board, col_id, flipped=False, problem_type=problem_type):
#         return False
#
#     # checking for the columns (as rows)
#     if not _check_move_helper_with_constraint_check(board, row_id, flipped=True, problem_type=problem_type):
#         return False
#
#     return True
#
#
# def _check_move_helper_with_constraint_check(board, row_id, flipped=False, problem_type=BRUTE_FORCE):
#     """
#     check if the move in this row_id/col_id is legit.
#     return True if this move works and legit, false otherwise
#
#     IMPORTANT NOTE: this doesn't show that this step is correct, it just checks if it could be there.
#     """
#
#     constraints_for_row = board.rows_constraints[row_id] if not flipped else board.cols_constraints[row_id]
#     current_row = board.flipped[row_id] if flipped else board.board[row_id]
#
#     # constraint:
#     curr_constraint_id = 0
#     curr_constraint = constraints_for_row[curr_constraint_id]
#     curr_num_of_cells_to_fill = curr_constraint.length
#     curr_constraint_color = curr_constraint.color
#     curr_constraint_status = curr_constraint.completed
#
#     # the color must be for the next cell
#     must_color = EMPTY
#     # sometimes we need to block a color from next cell (example: 1b-1b - we can't put two black near each other)
#     # - white can't be forbidden
#     blocked_color = EMPTY
#
#     constraints_complete = False  # all constraints are fulfilled
#     empty_flag = False  # there is an empty cell in this row
#
#     cell_id = 0
#     while cell_id < len(current_row):
#         cell = current_row[cell_id]
#         cell_color = cell.color
#
#         if cell_color == EMPTY:  # we didn't fill it yet
#             empty_flag = True
#             blocked_color = EMPTY  # Nothing blocked after an empty cell.
#             cell_id += 1
#             continue
#
#         elif cell_color == WHITE and (must_color == WHITE or must_color == EMPTY):
#             # that's good
#             # if must color is white - that means we finished all constraints, and all remaining cells should stay white
#
#             # we reset the forbid color
#             blocked_color = EMPTY
#             cell_id += 1
#             continue
#
#         elif cell_color == curr_constraint_color and (
#                 must_color == curr_constraint_color or must_color == EMPTY) and blocked_color != curr_constraint_color:
#             if curr_constraint_status:
#                 # this constraint already filled and done, so move to next situation as we finished this status
#                 cell_id += curr_num_of_cells_to_fill
#                 curr_num_of_cells_to_fill = 0
#             else:
#                 # this constraint ain't finished yet
#                 curr_num_of_cells_to_fill -= 1
#                 cell_id += 1
#
#             # check if we need to change constraint #
#             # if we still didn't finish filling this constraint, we want the next color to be same color as the constraint:
#             if curr_num_of_cells_to_fill > 0:
#                 must_color = curr_constraint_color
#                 blocked_color = EMPTY  # nothing blocked
#
#             # if we finished filling this current constraint, we need to move to next constraint
#             elif curr_num_of_cells_to_fill == 0:
#                 must_color = EMPTY  # nothing is a must
#                 blocked_color = curr_constraint_color
#                 if not problem_type:  # if not brute force
#                     constraints_for_row[curr_constraint_id].completed = True  # Change the status for a future checks.
#
#                 # move to next constraint
#                 curr_constraint_id += 1
#                 if curr_constraint_id < len(constraints_for_row):
#                     curr_constraint = constraints_for_row[curr_constraint_id]
#                     curr_num_of_cells_to_fill = curr_constraint.length
#                     curr_constraint_color = curr_constraint.color
#
#                 else:
#                     # we finished every constraint, next cells should be white only
#                     constraints_complete = True
#                     must_color = WHITE
#             else:
#                 raise Exception("this is an impossible situation, hmmmmmm")
#
#         else:
#             return False
#
#     # maybe we finished the row but the constraints aren't finished yet! and that's a mistake:
#     # if we have Empty then no need to finish the constraints, if we don't then constraints must complete
#     if empty_flag or constraints_complete:
#         return True
#
#     return False
#
