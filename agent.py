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
            # We have done all the constraints
            return successors

        for start_index in range(state.num_rows):
            child = state.fill_n_cells(constraint_coord[0], constraint_coord[1], start_index, COLUMNS)
            if child is not None:
                actions = set()
                constraint = state.cols_constraints[constraint_coord[0]][constraint_coord[1]]
                for i in range(constraint.length):
                    actions.add((start_index + i, constraint_coord[0]))
                successors.append((child, actions))
        return successors

    def get_cost_of_actions(self, state):
        # Actions are a set of cell's coordinates we colored to get a new state.
        #Todo it looks like a heuristc function, discucss this with team.
        # cost zero.
        sum_completed_constrains = 0
        for row_con in state.rows_constraints:
            for constraint in row_con:
                if constraint.completed:
                    sum_completed_constrains += 1
        return -1 * sum_completed_constrains

class NonogramCells(SearchProblem):
    """
        Class that defining the nonogram game as a problem.
    """
    def __init__(self, board):
        self.board = board
        self.current_cell = 0

    def get_start_state(self):
        return self.board

    def is_goal_state(self, state):
        return (state.get_first_incomplete_constraint(COLUMNS) is None) and \
               (state.get_first_incomplete_constraint(ROWS) is None)

    def get_successors(self, state):
        successors = []
        constraint_coord = state.get_first_incomplete_constraint(COLUMNS)

        if constraint_coord is None:
            # We have done all the constraints
            return successors

        for start_index in range(state.num_rows):
            child = state.fill_n_cells(constraint_coord[0], constraint_coord[1], start_index, COLUMNS)
            if child is not None:
                actions = set()
                constraint = state.cols_constraints[constraint_coord[0]][constraint_coord[1]]
                for i in range(constraint.length):
                    actions.add((start_index + i, constraint_coord[0]))
                successors.append((child, actions))
        return successors

    def get_cost_of_actions(self, state):
        # Actions are a set of cell's coordinates we colored to get a new state.
        sum_completed_constrains = 0
        for row_con in state.rows_constraints:
            for constraint in row_con:
                if constraint.completed:
                    sum_completed_constrains += 1
        return -1 * sum_completed_constrains

class BruteForce:

    def __init__(self, board):
        self.board = board

    def brute_force(self):
        """
        try to solve a board of nonogram by trying everything (brute force)
        """
        result = self._brute_force_helper( 0, 0)
        if result:
            return self

    def _brute_force_helper(self, row_id, col_id):
        """
        this is a recursion function, we do recursion to solve it in brute force.
        """
        for color in [RED, BLACK, WHITE]:
            self.board.fill(row_id, col_id, color)
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
        self.board.fill(row_id, col_id, EMPTY)
        return

