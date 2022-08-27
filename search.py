import Board
import util
from config import COLORS_DICT


def __gui_helper(board):
    Board.Board.gui.canvas.delete('rect')
    for r in range(board.num_rows):
        for c in range(board.num_cols):
            cur_color = board.board[r][c].color
            if cur_color == -1:
                board.fill(r, c, 0)
            else:
                board.fill(r, c, board.board[r][c].color)


def search_helper(problem, fringe):
    fringe.push((problem.get_start_state(), set()))
    while not fringe.isEmpty():
        # delete the previous child's actions rectangles
        Board.Board.gui.canvas.delete('rect')
        current = fringe.pop()
        # todo - block the gui for some time...
        # todo - show all the rectangles of the current child
        # Board.Board.gui.canvas.after(5000, Board.Board.gui.root.update)
        for i in range(len(current[0].rects)):
            r, c = current[0].rects[i].row, current[0].rects[i].col
            temp = Board.Board.gui.board_rectangles_locs[r][c]
            Board.Board.gui.canvas.create_rectangle(temp[0], temp[1], temp[2], temp[3],
                                                    fill=COLORS_DICT[current[0].board[r][c].__repr__()], tags='rect')
        Board.Board.gui.root.update()

        # current[0].print_board()
        if problem.is_goal_state(current[0]):
            # __gui_helper(current[0])
            return current[0]
        for child in problem.get_successors(current[0]):
            visited_coords = False
            for coord in child[1]:
                if coord in current[1]:
                    visited_coords = True
            if not visited_coords:
                # if we have a new board.
                child[1].update(current[1])
                fringe.push((child[0], child[1]))
    return -1  # Error


def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.
    Your search algorithm needs to return a list of actions that reaches
    the goal. Make sure to implement a graph search algorithm.
    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    print("Start:", problem.get_start_state().state)
    print("Is the start a goal?", problem.is_goal_state(problem.get_start_state()))
    print("Start's successors:", problem.get_successors(problem.get_start_state()))
    """
    "*** YOUR CODE HERE ***"
    return search_helper(problem, util.Stack())


def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    return search_helper(problem, util.Queue())


def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


class StateAndActions:
    """
        Class to store the state and the actions to get to this state.
        state - the state we want to store.
        actions - list of actions.
        This class to avoid comparing between 2 tuples when we use PriorityQueue.push().
    """

    def __init__(self, state, actions):
        self.state = state
        self.actions = actions


def a_star_search(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue()
    root = StateAndActions(problem.get_start_state(), set())
    fringe.push(root, 0)
    while not fringe.isEmpty():
        Board.Board.gui.canvas.delete('rect')

        current = fringe.pop()

        for i in range(len(current.state.rects)):
            r, c = current.state.rects[i].row, current.state.rects[i].col
            temp = Board.Board.gui.board_rectangles_locs[r][c]
            Board.Board.gui.canvas.create_rectangle(temp[0], temp[1], temp[2], temp[3],
                                                    fill=COLORS_DICT[repr(current.state.board[r][c])], tags='rect')
        Board.Board.gui.root.update()

        if problem.is_goal_state(current.state):
            # __gui_helper(current.state)
            return current.state
        for child in problem.get_successors(current.state):
            visited_coords = False
            for coord in child[1]:
                if coord in current.actions:
                    visited_coords = True
            if not visited_coords:
                child[1].update(current.actions)
                child_cost = problem.get_cost_of_actions(child[0])
                heuristic_cost = child_cost + heuristic(child[0], problem)
                fringe.push(StateAndActions(child[0], child[1]), heuristic_cost)


def local_beam_search(problem, k_states, k):
    """
    Local beam search, starting with k-random states, searching for a goal state in this k states.
    If no goal state, we pick the best k-states from all successors (of starting states), and repeat.
    problem: type of our problem.
    k_states: a list of k-states, each state is a board and the actions (coordinates of non-empty cells),
              list of StateAndActions objects.
    """
    all_successors = util.PriorityQueue()
    for current in k_states:
        if problem.is_goal_state(current.state):
            return current.state
    for current in k_states:
        for successor in problem.get_successors(current.state):
            visited_coords = False
            for coord in successor[1]:
                if coord in current.actions:
                    visited_coords = True
            if not visited_coords:
                successor[1].update(current.actions)
                priority = problem.get_cost_of_actions(successor[0])
                all_successors.push(StateAndActions(successor[0], successor[1]), priority)
            # todo Adam will check this later - he said that, also he mentioned how excited he is for the video

    k_successors = []
    for i in range(k):
        try:
            k_successors.append(all_successors.pop())
        except IndexError:
            break
    if len(k_successors) == 0:
        return None
    return local_beam_search(problem, k_successors, k)


# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search

# import util
#
#
# def search_helper(problem, fringe):
#     fringe.push((problem.get_start_state(), set()))
#     while not fringe.isEmpty():
#         current = fringe.pop()
#         if problem.is_goal_state(current[0]):
#             return current[0]
#         for child in problem.get_successors(current[0]):
#             visited_coords = False
#             for coord in child[1]:
#                 if coord in current[1]:
#                     visited_coords = True
#             if not visited_coords:
#                 # if we have a new board.
#                 child[1].update(current[1])
#                 fringe.push((child[0], child[1]))
#     return -1  # Error
#
#
# def depth_first_search(problem):
#     """
#     Search the deepest nodes in the search tree first.
#
#     Your search algorithm needs to return a list of actions that reaches
#     the goal. Make sure to implement a graph search algorithm.
#
#     To get started, you might want to try some of these simple commands to
#     understand the search problem that is being passed in:
#
#     print("Start:", problem.get_start_state().state)
#     print("Is the start a goal?", problem.is_goal_state(problem.get_start_state()))
#     print("Start's successors:", problem.get_successors(problem.get_start_state()))
#     """
#     "*** YOUR CODE HERE ***"
#     return search_helper(problem, util.Stack())
#
#
# def breadth_first_search(problem):
#     """
#     Search the shallowest nodes in the search tree first.
#     """
#     "*** YOUR CODE HERE ***"
#     return search_helper(problem, util.Queue())
#
#
# def null_heuristic(state, problem=None):
#     """
#     A heuristic function estimates the cost from the current state to the nearest
#     goal in the provided SearchProblem.  This heuristic is trivial.
#     """
#     return 0
#
#
# class StateAndActions:
#     """
#         Class to store the state and the actions to get to this state.
#         state - the state we want to store.
#         actions - list of actions.
#
#         This class to avoid comparing between 2 tuples when we use PriorityQueue.push().
#     """
#
#     def __init__(self, state, actions):
#         self.state = state
#         self.actions = actions
#
#
# def a_star_search(problem, heuristic=null_heuristic):
#     """
#     Search the node that has the lowest combined cost and heuristic first.
#     """
#     "*** YOUR CODE HERE ***"
#     fringe = util.PriorityQueue()
#     root = StateAndActions(problem.get_start_state(), set())
#     fringe.push(root, 0)
#     visited = set()
#     while not fringe.isEmpty():
#         current = fringe.pop()
#         if problem.is_goal_state(current.state):
#             return current.state
#         for child in problem.get_successors(current.state):
#             visited_coords = False
#             for coord in child[1]:
#                 if coord in current.actions:
#                     visited_coords = True
#             if not visited_coords:
#                 child[1].update(current.actions)
#                 child_cost = problem.get_cost_of_actions(child[0])
#                 heuristic_cost = child_cost + heuristic(child[0], problem)
#                 fringe.push(StateAndActions(child[0], child[1]), heuristic_cost)
#
#
# def local_beam_search(problems, k_states, k):
#     """
#     Local beam search, starting with k-random states, searching for a goal state in this k states.
#     If no goal state, we pick the best k-states from all successors (of starting states), and repeat.
#     problem: type of our problem.
#     k_states: a list of k-states, each state is a board and the actions (coordinates of non-empty cells),
#               list of StateAndActions objects.
#     """
#     all_successors = util.PriorityQueue()
#     for current in k_states:
#         if current.is_goal_state(current.state):
#             return current
#     for current in problems:
#         for successor in current.get_successors():
#             all_successors.push(successor, -1 * (successor[0].get_cost_of_actions(successor[0].cols_constraints)))
#             # todo Adam will check this later - he said that, also he mentioned how excited he is for the video
#     k_successors = []
#     for i in range(k):
#         try:
#             k_successors.append(all_successors.pop())
#         except IndexError:
#             break
#     if len(k_successors) == 0:
#         return None
#     return local_beam_search(k_successors, k)
#
#
# # Abbreviations
# bfs = breadth_first_search
# dfs = depth_first_search
# astar = a_star_search
