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
        A* and DFS solve this problem.
    """

    def __init__(self, board):
        self.board = board
        self.cost = 0

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
            Each successor is a cell, the cell we want to fill in the board.
        """
        successors = []

        if self.board.current_cell.row == self.board.num_rows:
            # We finished all the cells.
            return successors

        for color in [WHITE, RED, BLACK]:
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
        Each successor is a cell, the cell we want to fill in the board.
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
