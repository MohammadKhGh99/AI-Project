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
                    if self.board.board[j][i].color == EMPTY or not self.board.check_move(i, j):
                        return False
            return True
        return self.board.current_cell.row == self.board.num_rows and self.board.current_cell.col == 0
        # return self.board.current_cell.row == self.board.num_rows and self.board.current_cell.col == 0

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


# We didn't use this problem, because we got better results using the cells problem.
class NonogramConstraintsProblem(SearchProblem):
    """
        Class that defining the nonogram game as a problem. Solving it by checking row by row.
    """

    def __init__(self, board):
        self.board = board
        self.cost = 0
        self.constraints_combinations = csp.get_variables_and_domains(self.board)

    def get_start_state(self):
        return [[], 0]

    def is_goal_state(self, state):
        for i in range(self.board.num_cols):
            for j in range(self.board.num_rows):
                if self.board.board[j][i].color == EMPTY or not self.board.check_move(i, j):
                    return False
        return True

    def get_successors(self, state):
        successors = []
        for i in range(self.board.num_rows):
            if i not in self.board.filling_row_order:
                for comb in self.constraints_combinations[1][(ROWS, i)]:
                    successors.append((comb, i))
                return successors

    def get_cost_of_actions(self, actions):
        return self.cost - 1

    def do_move(self, actions):
        """
        Fill all the actions on the board, and check if it a legal fill
        actions: tuple (list of colors, row number)
        """
        get_successors = True
        i = 0
        for color in actions[0]:
            # Try to fill the move on the board, and check if it legal.
            self.board.fill(actions[1], i, color)
            if not self.board.check_move(i, actions[1], SEARCH_PROBLEMS):
                get_successors = False
                for j in range(self.board.num_cols):
                    # Empty the current row.
                    self.board.fill(actions[1], j, EMPTY)
                break
            i += 1
        if get_successors and (len(actions[0]) > 0):
            self.board.filling_row_order.append(actions[1])
        return get_successors

    def update_board(self, actions):
        """
        Empty the the current row we want fill, and all the rows we filled after it in previous moves.
        """
        if len(actions[0]) > 0:
            current_row = actions[1]
            if current_row in self.board.filling_row_order:
                index_in_list = self.board.filling_row_order.index(current_row)
                for row in self.board.filling_row_order[index_in_list:]:
                    for col in range(self.board.num_cols):
                        # Empty all cells in these rows.
                        self.board.fill(row, col, EMPTY)
                # Update the done rows list
                self.board.filling_row_order = self.board.filling_row_order[:index_in_list]


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
            self.board.fill(row_id, col_id, color, solve_type=BRUTE)
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
        self.board.fill(row_id, col_id, EMPTY, solve_type=BRUTE)
        return
