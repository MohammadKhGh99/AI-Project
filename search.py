import Board
import util
from config import *


class StateAndActions:
    """
        Class to store the state, the actions and the cost to get to this state.
        state - the state we want to store.
        actions - list of actions.
        This class to avoid comparing between 2 tuples when we use PriorityQueue.push().
    """

    def __init__(self, state, actions, cost):
        self.state = state
        self.actions = actions
        self.cost = cost


def __gui_helper(board):
    Board.Board.gui.canvas.delete('rect')
    for r in range(board.num_rows):
        for c in range(board.num_cols):
            cur_color = board.board[r][c].color
            if cur_color == -1:
                board.fill(r, c, 0)
            else:
                board.fill(r, c, board.board[r][c].color)


def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.
    """
    fringe = util.Stack()
    fringe.push((problem.get_start_state(), []))
    while not fringe.isEmpty():
        # delete the previous child's actions rectangles
        Board.Board.gui.canvas.delete('rect')
        current = fringe.pop()
        get_successors = True
        current[0].current_row_constraint += 1
        problem.board.move_to_the_next_cell()

        for move in current[1]:
            # Try to fill the move on the board, and check if it legal.
            current[0].fill(move.row, move.col, move.color)
            if not current[0].check_move(move.col, move.row):
                get_successors = False
                problem.board.back_to_the_prev_cell()
                while current[0].current_cell.color == WHITE:
                    current[0].fill(current[0].current_cell.row, current[0].current_cell.col, EMPTY)
                    problem.board.back_to_the_prev_cell()
                break

        if get_successors:
            # Get the successors of the current board, if it is not the goal state.
            if problem.is_goal_state(current[0]):
                for i in range(len(current[0].rects)):
                    r, c = current[0].rects[i].row, current[0].rects[i].col
                    temp = Board.Board.gui.board_rectangles_locs[r][c]
                    Board.Board.gui.canvas.create_rectangle(temp[0], temp[1], temp[2], temp[3],
                                                            fill=COLORS_DICT[current[0].board[r][c].__repr__()], tags='rect')
                Board.Board.gui.root.update()
                return current[0]

            for child in problem.get_successors(current[0]):
                fringe.push((child[0], child[1]))

    return -1  # No Solution


def breadth_first_search(problem):
    """
        Search the shallowest nodes in the search tree first.
        In bfs we save a list of all moves we did,
    """
    fringe = util.Queue()
    fringe.push((problem.get_start_state(), []))
    while not fringe.isEmpty():
        # delete the previous child's actions rectangles
        Board.Board.gui.canvas.delete('rect')
        current = fringe.pop()
        get_successors = True
        current[0].current_cell = Board.Cell(0, 0)
        # Reset Board
        for i in range(current[0].num_cols):
            for j in range(current[0].num_rows):
                current[0].fill(j, i, EMPTY)

        for move in current[1]:
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
                for i in range(len(current[0].rects)):
                    r, c = current[0].rects[i].row, current[0].rects[i].col
                    temp = Board.Board.gui.board_rectangles_locs[r][c]
                    Board.Board.gui.canvas.create_rectangle(temp[0], temp[1], temp[2], temp[3],
                                                            fill=COLORS_DICT[current[0].board[r][c].__repr__()], tags='rect')
                Board.Board.gui.root.update()
                return current[0]
            current[0].moves = current[1]
            for child in problem.get_successors(current[0]):
                fringe.push((child[0], child[1]))
    return -1  # No Solution


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
        # delete the previous child's actions rectangles
        Board.Board.gui.canvas.delete('rect')
        current = fringe.pop()
        get_successors = True
        multi_fill = False
        current.state.current_row_constraint += 1
        problem.board.move_to_the_next_cell()
        cells_filled = 0
        for move in current.actions:
            if multi_fill:
                problem.board.move_to_the_next_cell()
            current.state.fill(move.row, move.col, move.color)
            cells_filled += 1
            if not current.state.check_move(move.col, move.row):
                get_successors = False
                if multi_fill:
                    for i in range(cells_filled):
                        current.state.fill(current.state.current_cell.row, current.state.current_cell.col, EMPTY)
                        problem.board.back_to_the_prev_cell()
                    current.state.fill(current.state.current_cell.row, current.state.current_cell.col, EMPTY)
                else:
                    problem.board.back_to_the_prev_cell()
                    while current.state.current_cell.color == WHITE:
                        current.state.fill(current.state.current_cell.row, current.state.current_cell.col, EMPTY)
                        problem.board.back_to_the_prev_cell()

                # current[0].fill(move.row, move.col, EMPTY)
                current.state.current_row_constraint -= 1

                break
            multi_fill = True
        if get_successors:

            for i in range(len(current.state.rects)):
                r, c = current.state.rects[i].row, current.state.rects[i].col
                temp = Board.Board.gui.board_rectangles_locs[r][c]
                Board.Board.gui.canvas.create_rectangle(temp[0], temp[1], temp[2], temp[3],
                                                        fill=COLORS_DICT[current.state.board[r][c].__repr__()], tags='rect')
            Board.Board.gui.root.update()
            if problem.is_goal_state(current.state):
                return current.state
            for child in problem.get_successors(current.state):
                heuristic_cost = current.cost + heuristic(child[0], problem) - 1 # TODO
                fringe.push(StateAndActions(child[0], child[1], heuristic_cost), heuristic_cost)
    return -1


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
                priority = problem.get_cost_of_actions()
                all_successors.push(StateAndActions(successor[0], successor[1], priority), priority)
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



# def search_helper(problem, fringe):
#     fringe.push((problem.get_start_state(), set()))
#     while not fringe.isEmpty():
#         # delete the previous child's actions rectangles
#         Board.Board.gui.canvas.delete('rect')
#         current = fringe.pop()
#
#         if problem.is_goal_state(current[0]):
#             for i in range(len(current[0].rects)):
#                 r, c = current[0].rects[i].row, current[0].rects[i].col
#                 temp = Board.Board.gui.board_rectangles_locs[r][c]
#                 Board.Board.gui.canvas.create_rectangle(temp[0], temp[1], temp[2], temp[3],
#                                                         fill=COLORS_DICT[current[0].board[r][c].__repr__()], tags='rect')
#             Board.Board.gui.root.update()
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
# def search_helper_v4(problem, fringe):
#     #copy of v2
#     fringe.push((problem.get_start_state(), []))
#     while not fringe.isEmpty():
#         # delete the previous child's actions rectangles
#         Board.Board.gui.canvas.delete('rect')
#         current = fringe.pop()
#         get_successors = True
#         multi_fill = False
#         current[0].current_row_constraint += 1
#         problem.move_to_the_next_cell()
#         cells_filled = 0
#         for move in current[1]:
#             if multi_fill:
#                 problem.move_to_the_next_cell()
#             current[0].fill(move.row, move.col, move.color)
#             cells_filled += 1
#             if not current[0].check_move(move.col, move.row):
#                 get_successors = False
#                 if multi_fill:
#                     for i in range(cells_filled):
#                         current[0].fill(current[0].current_cell.row, current[0].current_cell.col, EMPTY)
#                         problem.back_to_the_prev_cell()
#                     current[0].fill(current[0].current_cell.row, current[0].current_cell.col, EMPTY)
#                 else:
#                     problem.back_to_the_prev_cell()
#                     while current[0].current_cell.color == WHITE:
#                         current[0].fill(current[0].current_cell.row, current[0].current_cell.col, EMPTY)
#                         problem.back_to_the_prev_cell()
#
#                 # current[0].fill(move[0], move[1], EMPTY)
#                 current[0].current_row_constraint -= 1
#                 break
#             multi_fill = True
#         if get_successors:
#             # for i in range(len(current[0].rects)):
#             #     r, c = current[0].rects[i].row, current[0].rects[i].col
#             #     temp = Board.Board.gui.board_rectangles_locs[r][c]
#             #     Board.Board.gui.canvas.create_rectangle(temp[0], temp[1], temp[2], temp[3],
#             #                                             fill=COLORS_DICT[current[0].board[r][c].__repr__()], tags='rect')
#             # Board.Board.gui.root.update()
#
#             if problem.is_goal_state(current[0]):
#                 return current[0]
#             for child in problem.get_successors(current[0]):
#                 fringe.push((child[0], child[1]))
#     return -1  # Error
