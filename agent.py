from game import *

class Constraint:
    def __init__(self, constraint):
        self.number = int(constraint[:-1])
        self.color = constraint[-1]



# todo maybe we should put transpose version of the board in the initialize, and when we fill cell, make sure we fill it too


def brute_force(row_con, col_con, board):
    """
    try to solve a board of nonogram by trying everything
    """
    result = _brute_force_helper(row_con, col_con, board, 0, 0)
    if result:
        return board


def _brute_force_helper(row_con, col_con, board, row_id, col_id):
    for color in [RED, BLACK, WHITE]:
        board[row_id][col_id].color = color
        if __check_move(row_con, col_con, board, row_id, col_id):
            if row_id + 1 < len(row_con):
                return _brute_force_helper(row_con, col_con, board, row_id + 1, col_id)
            elif col_id + 1 < len(col_id):
                return _brute_force_helper(row_con, col_con, board, 0, col_id + 1)
            else:
                #  finished - the board is complete
                return board
    return None


def __check_move(row_con, col_con, board, row_id, col_id):
    """
    check if the move in this row_id/col_id is legit.
    """

    if not __check_move_helper(row_con, board, row_id):
        return False

    flipped = __invert_board(board)
    if not __check_move_helper(col_con, flipped, col_id):
        return False

    return True


def __check_move_helper(row, board, row_id):
    """
    check if the move in this row_id/col_id is legit.
    return True if this move works and legit, false otherwise

    IMPORTANT NOTE: this doesn't show that this step is correct, it just checks if it could be here
    """

    constrain: list[Constraint] = row[row_id]
    current_row = board[row_id]

    # constraint:
    curr_constraint_id = 0
    curr_constraint = constrain[curr_constraint_id]
    curr_num_of_cells_to_fill = curr_constraint.number
    curr_constraint_color = curr_constraint.color

    must_color = NO_COLOR  # the color of the next cell should be
    forbid_color = NO_COLOR  # sometimes we need to block a color from next cell (example: 1b-1b - we can't put two black near each other) - white can't be forbidden

    for cell in current_row:
        cell_color = cell.color

        if cell_color == WHITE and must_color == (WHITE or NO_COLOR):
            # that's good
            # if must color is white - that means we finished all constrains, and all remaining cells should stay white
            continue  # check, just that?

        elif cell_color == curr_constraint_color and must_color == (curr_constraint_color or NO_COLOR) and forbid_color != curr_constraint_color:
            # that's good, check if we need to change constrain
            curr_num_of_cells_to_fill -= 1

            # if we still didn't finish filling this constraint, we want the next color to be same color as the constraint:
            if curr_num_of_cells_to_fill > 0:
                must_color = curr_constraint_color
                forbid_color = NO_COLOR

            # if we finished filling this current constraint, we need to move to next constraint
            elif curr_num_of_cells_to_fill == 0:
                must_color = NO_COLOR
                forbid_color = curr_constraint_color

                if curr_constraint_id + 1 < len(constrain):
                    # we finished every constrain, next cells should be white only
                    must_color = WHITE

                # move to next constraint
                else:
                    curr_constraint_id += 1
                    curr_constraint = constrain[curr_constraint_id]
                    curr_num_of_cells_to_fill = curr_constraint.number
                    curr_constraint_color = curr_constraint.color
            else:
                raise Exception("this is an impossible situation, hmmmmmm")

        else:
            return False
    return True


def __invert_board(board):
    """
    transpose the board
    """
    return list(map(list, zip(*board)))


