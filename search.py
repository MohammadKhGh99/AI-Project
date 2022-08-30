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


def get_random_stats(board, n):
    state = Board.Board(rows_constraints=board.rows_constraints, cols_constraints=board.cols_constraints,
                        randomly=board.randomly, size=board.size, cur_game=board.cur_game)
    states_lst = set()
    cur_k = 0
    while cur_k < n:
        r = random.randint(0, board.num_rows - 1)
        c = random.randint(0, board.num_cols - 1)
        while (r, c) in states_lst:
            r = random.randint(0, board.num_rows - 1)
            c = random.randint(0, board.num_cols - 1)
        states_lst.add((r, c))
        cur_k += 1

    for loc in states_lst:
        state.fill(loc[0], loc[1], color=random.choice(COLORS_LST_WITHOUT_WHITE))

    return state, states_lst


def search_helper(problem, actions, search_type=DFS):
    """
        Function try to fill the actions on the board, and check if it legal.
        problem: Nonogram game.
        state: the current board.
        actions: cells we want to fill in the board.
    """
    problem.board.current_row_constraint += 1
    problem.board.move_to_the_next_cell()
    get_successors = True
    for move in actions:
        # Try to fill the move on the board, and check if it legal.
        problem.board.fill(move.row, move.col, move.color)
        if not problem.board.check_move(move.col, move.row):
            get_successors = False
            problem.board.back_to_the_prev_cell()
            problem.board.filled_cells -= 1
            if search_type == DFS:
                while problem.board.current_cell.color == WHITE:
                    problem.board.fill(problem.board.current_cell.row, problem.board.current_cell.col, EMPTY)
                    problem.board.back_to_the_prev_cell()
                    problem.board.filled_cells -= 1
            else:
                problem.board.fill(problem.board.current_cell.row, problem.board.current_cell.col, EMPTY)
            break
    return get_successors


def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.
    """
    fringe = util.Stack()
    fringe.push((problem.get_start_state(), []))
    while not fringe.isEmpty():
        current = fringe.pop()
        problem.board = current[0]
        if search_helper(problem, current[1]):
            # Get the successors of the current board, if it is not the goal state.
            if problem.is_goal_state(current[0]):
                gui_helper(current[0])
                return current[0]
            for child in problem.get_successors(current[0]):
                fringe.push((child[0], child[1]))
    return -1  # No Solution


def breadth_first_search1(problem):
    """
        Search the shallowest nodes in the search tree first.
        In bfs we save a list of all moves we did,
    """
    fringe = util.Queue()
    fringe.push((problem.get_start_state(), []))
    while not fringe.isEmpty():
        # delete the previous child's actions rectangles

        current = fringe.pop()
        get_successors = True
        current[0].current_cell = Board.Cell(0, 0)

        gui_helper(current[0])

        # Reset Board
        for action in current[1][:-1]:
            current[0].fill(action.row, action.col, action.color)

        # for i in range(current[0].num_cols):
        #     for j in range(current[0].num_rows):
        #         current[0].fill(j, i, EMPTY)
        # print(current[1])
        if len(current[1]) > 0:
            for move in [current[1][-1]]:
                # Try to fill the move on the board, and check if it legal.
                current[0].fill(move.row, move.col, move.color)
                if not current[0].check_move(move.col, move.row):
                    get_successors = False
                    current[0].fill(move.row, move.col, EMPTY)
                    break
                else:
                    problem.board.move_to_the_next_cell()
        if get_successors:
            # Get the successors of the current board, if it is not the goal state.
            if problem.is_goal_state(current[0]):
                return current[0]
            current[0].moves = current[1]
            for child in problem.get_successors(current[0]):
                fringe.push((child[0], child[1]))
    return -1  # No Solution


def breadth_first_search(problem):
    problem.board.move_to_the_next_cell()
    depth = problem.board.num_cols * problem.board.num_rows
    for i in range(depth + 1):
        state = bfs_helper(problem, i)
        if state is not None:
            return state
    return None


def bfs_helper(problem, depth):
    if depth == 0:
        if problem.is_goal_state(problem.board):
            return problem.board
        return None

    for child in problem.get_successors(problem.board):
        if search_helper(problem, child[1], BFS):
            # Get the successors of the current board, if it is not the goal state.
            state = bfs_helper(problem, depth - 1)
            if state is not None:
                return state
            problem.board.back_to_the_prev_cell()
            current_row = problem.board.current_cell.row
            current_col = problem.board.current_cell.col
            problem.board.fill(current_row, current_col, EMPTY)
    return None


def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def a_star_search(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    fringe = util.PriorityQueue()
    fringe.push(StateAndActions(problem.get_start_state(), [], 0), 0)
    while not fringe.isEmpty():
        current = fringe.pop()
        problem.cost = current.cost
        gui_helper(current.state)
        if search_helper(problem, current.actions):
            # Get the successors of the current board, if it is not the goal state.
            if problem.is_goal_state(current.state):
                return current.state
            for child in problem.get_successors(current.state):
                child_cost = problem.get_cost_of_actions(child[1])
                heuristic_cost = child_cost + heuristic(child[1][0], problem)  # TODO
                fringe.push(StateAndActions(child[0], child[1], heuristic_cost), heuristic_cost)
    return -1  # No Solution


def local_beam_search_helper(problem, k_states, k):  # , value_function):
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
                move_coordinates = (successor[1][0].row, successor[1][0].col)
                if (move_coordinates in current.initial_cells) and (
                        successor[1][0].color != problem.board.board[move_coordinates[0]][move_coordinates[1]].color):
                    continue

                if search_helper(problem, successor[1]):
                    if problem.is_goal_state(problem.board):
                        gui_helper(problem.board)
                        return problem.board
                    value = (-1 * problem.board.filled_cells) + problem.get_cost_of_actions(successor[1])
                    all_successors.push(
                        StateAndActions(deepcopy(successor[0]), successor[1], value, current.initial_cells), value)
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
    # return local_beam_search_helper(problem, k_successors, k, value_function)


def local_beam_search(problem, k):  # , value_function=null_heuristic):
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
        n = problem.board.num_cols * problem.board.num_rows
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
    # legal_k_states = [StateAndActions(problem.board, [], -1 * problem.board.filled_cells, set())] #TODO for testing
    # problem.board.move_to_the_next_cell()
    return local_beam_search_helper(problem, legal_k_states, k)  # , value_function)

