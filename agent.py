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
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        raise Exception("Not implemented.")

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        raise Exception("Not implemented.")


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
        constraint_coord = state.get_first_incomplete_constraint(COLUMNS)

        if constraint_coord is None:
            # We done all the constraints
            return successors

        for start_index in range(state.num_rows):
            child = state.fill_n_cells(constraint_coord[0], constraint_coord[1], start_index, COLUMNS)
            if child is not None:
                constraint = self.board.cols_constraints[constraint_coord[0]][constraint_coord[1]]
                successors.append((child, constraint, abs(constraint.number - state.num_rows)))

        return successors

    def get_cost_of_actions(self, actions):
        # Action is the number of cells we colored to get a new state.
        return sum(action.number for action in actions if action.completed)


from game import *


# todo - fix the design and the problems that Ibraheem made

def brute_force(board):
    """
    try to solve a board of nonogram by trying everything (brute force)
    """
    result = _brute_force_helper(board, 0, 0)
    if result:
        return board


def _brute_force_helper(board, row_id, col_id):
    """
    this is a recursion function, we do recursion to solve it in brute force.
    """
    for color in [RED, BLACK, WHITE]:
        board.fill(row_id, col_id, color)
        # check if this move works, if yes go to next cell.
        if check_move(board, col_id, row_id):
            if col_id + 1 < len(board.cols_constraints):
                res = _brute_force_helper(board, row_id, col_id + 1)
                if res:
                    return res
            elif row_id + 1 < len(board.rows_constraints):
                res2 = _brute_force_helper(board, row_id + 1, 0)
                if res2:
                    return res2
            else:
                #  finished - the board is complete
                return board
    # no color is correct
    board.fill(row_id, col_id, EMPTY)
    return


def check_move(board, row_id, col_id, brute_force=True):
    """
    check if the move in this row_id/col_id is legit.
    """
    # checking for the rows
    if not _check_move_helper_with_constraint_check(board, col_id, flipped=False, brute_force=brute_force):
        return False

    # checking for the columns (as rows)
    if not _check_move_helper_with_constraint_check(board, row_id, flipped=True, brute_force=brute_force):
        return False

    return True


def _check_move_helper_with_constraint_check(board, row_id, flipped=False, brute_force=True):
    """
    check if the move in this row_id/col_id is legit.
    return True if this move works and legit, false otherwise

    IMPORTANT NOTE: this doesn't show that this step is correct, it just checks if it could be there.
    """

    constraints_for_row = board.rows_constraints[row_id] if not flipped else board.cols_constraints[row_id]
    current_row = board.flipped[row_id] if flipped else board.board[row_id]

    # constraint:
    curr_constraint_id = 0
    curr_constraint = constraints_for_row[curr_constraint_id]
    curr_num_of_cells_to_fill = curr_constraint.number
    if curr_num_of_cells_to_fill is None:
        return True
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
            # if must color is white - that means we finished all constraints, and all remaining cells should stay white

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
            # if we still didn't finish filling this constraint, we want the next color to be same color as the constraint:
            if curr_num_of_cells_to_fill > 0:
                must_color = curr_constraint_color
                blocked_color = EMPTY  # nothing blocked

            # if we finished filling this current constraint, we need to move to next constraint
            elif curr_num_of_cells_to_fill == 0:
                must_color = EMPTY  # nothing is a must
                blocked_color = curr_constraint_color
                if not brute_force:
                    constraints_for_row[curr_constraint_id].completed = True  # Change the status for a future checks.

                # move to next constraint
                curr_constraint_id += 1
                if curr_constraint_id < len(constraints_for_row):
                    curr_constraint = constraints_for_row[curr_constraint_id]
                    curr_num_of_cells_to_fill = curr_constraint.number
                    curr_constraint_color = curr_constraint.color

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

