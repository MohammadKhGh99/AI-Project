from config import *

def heuristic(action, problem):
    current_row = problem.board.current_cell.row

    # Count the number of red and black cells in the current row.
    black_in_row = 0
    red_in_row = 0
    for cell in problem.board.board[current_row]:
        if cell.color == BLACK:
            black_in_row += 1
        elif cell.color == RED:
            red_in_row += 1
    black_in_row = 1 if black_in_row == 0 else black_in_row
    red_in_row = 1 if red_in_row == 0 else red_in_row

    # Count the number of total red and total black in the current row constraints.
    black_in_constraint = 0
    red_in_constraint = 0
    for constraint in problem.board.rows_constraints[current_row]:
        if constraint.color == BLACK:
            black_in_constraint += constraint.length
        elif constraint.color == RED:
            red_in_constraint += constraint.length

    black_value = black_in_constraint / black_in_row
    red_value = red_in_constraint / red_in_row

    # if black_value == red_value and black_value == 1:
    #     black_value = 10000
    #     red_value = 10000

    if action.color == BLACK:
        return -1 * black_value
    elif action.color == RED:
        return -1 * red_value
    else:
        return 0
