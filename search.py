import random
import time
from copy import deepcopy
import Board
import util
from config import *


class StateAndActions:
    """
        Class to store the state, the actions and the cost to get to this state.
        state - the state we want to store.
        actions - list of actions.
        cost - the cost of the current state.
        initial_cells - the non-empty cells from the start (for local beam search).
        This class to avoid comparing between 2 tuples when we use PriorityQueue.push().
    """

    def __init__(self, state, actions, cost, initial_cells=None):
        self.state = state
        self.actions = actions
        self.cost = cost
        self.initial_cells = initial_cells


def gui_helper(board):
    if board.gui is not None:
        bef = time.time()
        Board.Board.gui.canvas.delete('rect')
        for i in range(len(board.rects)):
            r, c = board.rects[i].row, board.rects[i].col
            temp = Board.Board.gui.board_rectangles_locs[r][c]
            Board.Board.gui.canvas.create_rectangle(temp[0], temp[1], temp[2], temp[3],
                                                    fill=COLORS_DICT[repr(board.board[r][c])], tags='rect')
        Board.Board.gui.root.update()
        Board.Board.different_time += (time.time() - bef)


def depth_first_search(problem):
    fringe = util.Stack()
    fringe.push(problem.get_start_state())
    while not fringe.isEmpty():
        current_actions = fringe.pop()  # actions to do
        problem.update_board(current_actions)  # Make board ready to be filled in this row.
        # gui_helper(problem.board)
        if problem.do_move(current_actions):
            # Get the successors of the current board, if it is not the goal state.
            if problem.is_goal_state(problem.board):
                gui_helper(problem.board)
                return problem.board
            for child in problem.get_successors(problem.board):
                fringe.push(child)
    return -1  # No Solution


def bfs_helper(problem, depth):
    if depth == 0:
        if problem.is_goal_state(problem.board):
            return problem.board
        return None

    for child in problem.get_successors(problem.board):
        if problem.do_move(child):
            # Get the successors of the current board, if it is not the goal state.
            state = bfs_helper(problem, depth - 1)
            if state is not None:
                return state
            problem.update_board(child)
            #TODO for cells problem
            # problem.board.back_to_the_prev_cell()
            # current_row = problem.board.current_cell.row
            # current_col = problem.board.current_cell.col
            # problem.board.fill(current_row, current_col, EMPTY)
    return None


def breadth_first_search(problem):
    problem.board.move_to_the_next_cell()
    depth = problem.board.num_cols * problem.board.num_rows
    for i in range(depth + 1):
        state = bfs_helper(problem, i)
        if state is not None:
            return state
    return None

def lowest_combinations_heuristic(problem):
    lowest_order = []
    for _ in range(problem.board.num_rows):
        lowest_index = problem.board.num_rows
        min_combinations = None
        for i in range(problem.board.num_rows):
            if i not in lowest_order:
                num_of_combinations = len(problem.constraints_combinations[1][(ROWS, i)])
                if min_combinations is None or num_of_combinations < min_combinations:
                    lowest_index = i
                    min_combinations = num_of_combinations
        lowest_order.append(lowest_index)
    return lowest_order

def basic_heuristic(problem):
    for row in reversed(range(problem.board.num_rows)):
        if row not in problem.board.filling_row_order:
            return row

def null_heuristic(problem):
    return [i for i in range(problem.board.num_rows)]


def a_star_search(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    fringe = only moves we want to do, on the board.
    """
    problem.heuristic_function = heuristic
    return depth_first_search(problem)
    # fringe.push(StateAndActions(problem.board, [[]], 0))
    # while not fringe.isEmpty():
    #     current = fringe.pop()
    #     gui_helper(problem.board)
    #     problem.update_board(current.actions)
    #     # Get the successors of the current board, if it is not the goal state.
    #     if problem.do_move(current.actions):
    #         if problem.is_goal_state(problem.board):
    #             return problem.board
    #         for child in problem.get_successors(current.state):
    #             fringe.push(StateAndActions(problem.board, child, 0))
    # return -1  # No Solution


def local_beam_search_helper(problem, k_states, k):
    """
    Helper function for LBS, none of the k_states is a goal state.
    """
    k_successors = k_states
    while True:
        all_successors = util.PriorityQueue()
        for current in k_successors:
            problem.board = current.state
            gui_helper(problem.board)
            for successor in problem.get_successors(current.state):
                move_coordinates = (successor[0].row, successor[0].col)
                if (move_coordinates in current.initial_cells) and (
                        successor[0].color != problem.board.board[move_coordinates[0]][move_coordinates[1]].color):
                    continue

                if problem.do_move(successor):
                    if problem.is_goal_state(problem.board):
                        gui_helper(problem.board)
                        return problem.board
                    value = problem.board.filled_cells + problem.get_cost_of_actions(successor)
                    all_successors.push(
                        StateAndActions(deepcopy(problem.board), successor, value, current.initial_cells), value)
                    problem.board.back_to_the_prev_cell()
                    problem.board.fill(problem.board.current_cell.row, problem.board.current_cell.col, EMPTY)
                    problem.board.filled_cells -= 1
        k_successors = []
        for i in range(k):
            try:
                k_successors.append(all_successors.pop())
            except IndexError:
                break
        if len(k_successors) == 0:
            return -1


def get_random_stats(board, n):
    random_state = Board.Board(rows_constraints=board.rows_constraints, cols_constraints=board.cols_constraints,
                        randomly=board.randomly, size=board.size, cur_game=board.cur_game)
    initial_cells = set()
    cur_k = 0
    while cur_k < n:
        r = random.randint(0, board.num_rows - 1)
        c = random.randint(0, board.num_cols - 1)
        color = random.choice(COLORS_LST_WITHOUT_WHITE)
        while (r, c) in initial_cells:
            r = random.randint(0, board.num_rows - 1)
            c = random.randint(0, board.num_cols - 1)
        initial_cells.add((r, c))
        cur_k += 1

    for loc in initial_cells:
        random_state.fill(loc[0], loc[1], color=random.choice(COLORS_LST_WITHOUT_WHITE))

    return random_state, initial_cells


def local_beam_search(problem, k):
    """
    Local beam search, starting with k-random states, searching for a goal state in this k states.
    If no goal state, we pick the best k-states from all successors (of starting states), and repeat.
    problem: type of our problem.
    value_function: function get a state, and give a value according the current situation.
    k_states: a list of k-states, each state is a board and the actions (coordinates of non-empty cells),
              list of StateAndActions objects.
    """
    k_states = []
    for i in range(k):
        n = int((problem.board.num_cols * problem.board.num_rows) / 4)
        random_state, initial_cells = get_random_stats(problem.board, random.randint(0, n))
        copy_state = StateAndActions(random_state, [], 0, initial_cells)
        k_states.append(copy_state)

    legal_k_states = []
    for current in k_states:
        problem.board = current.state
        current.state.move_to_the_next_cell()
        if problem.is_goal_state(current.state):
            # gui_helper(current.state)
            return current.state
        is_legal = True
        for cell in current.initial_cells:
            if not problem.board.check_move(cell[1], cell[0]):
                is_legal = False
                break
        if is_legal:
            legal_k_states.append(current)
    if len(legal_k_states) == 0:
        print("zero legal")
    return local_beam_search_helper(problem, legal_k_states, k)  # , value_function)


# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search


