from game import *


# todo - fix the design and the problems that Ibraheem made

def brute_force(row_con, col_con, board):
    """
    try to solve a board of nonogram by trying everything (brute force)
    """
    result = _brute_force_helper(row_con, col_con, board, 0, 0)
    if result:
        return board


def _brute_force_helper(row_con, col_con, board, row_id, col_id):
    """
    this is a recursion function, we do recursion to solve it in brute force.
    """
    for color in [RED, BLACK, WHITE]:
        board[row_id][col_id].color = color
        # check if this move works, if yes go to next cell.
        if check_move(row_con, col_con, board, col_id, row_id):
            if col_id + 1 < len(col_con):
                res = _brute_force_helper(row_con, col_con, board, row_id, col_id + 1)
                if res:
                    return res
            elif row_id + 1 < len(row_con):
                res2 = _brute_force_helper(row_con, col_con, board, row_id + 1, 0)
                if res2:
                    return res2
            else:
                #  finished - the board is complete
                return board
    # no color is correct
    board[row_id][col_id].color = EMPTY
    return


def check_move(row_con, col_con, board, row_id, col_id):
    """
    check if the move in this row_id/col_id is legit.
    """
    # checking for the rows
    if not _check_move_helper_with_constrain_check(row_con, board, col_id):
        return False

    flipped = __invert_board(board)
    # checking for the columns (as rows)
    if not _check_move_helper_with_constrain_check(col_con, flipped, row_id):
        return False

    return True


def _check_move_helper_with_constrain_check(row, board, row_id):
    """
    check if the move in this row_id/col_id is legit.
    return True if this move works and legit, false otherwise

    IMPORTANT NOTE: this doesn't show that this step is correct, it just checks if it could be there.
    """

    constraints_for_row: list[Constraint] = row[row_id]
    current_row = board[row_id]

    # constraint:
    curr_constraint_id = 0
    curr_constraint = constraints_for_row[curr_constraint_id]
    curr_num_of_cells_to_fill = curr_constraint.number
    curr_constraint_color = curr_constraint.color
    curr_constraint_status = curr_constraint.status

    must_color = EMPTY  # the color must be for the next cell
    blocked_color = EMPTY  # sometimes we need to block a color from next cell (example: 1b-1b - we can't put two black near each other) - white can't be forbidden

    constraints_complete = False  # all constraints are fulfilled
    empty_flag = False  # there is an empty cell in this row

    cell_id = 0
    while cell_id < len(current_row):
        cell = current_row[cell_id]
        cell_color = cell.color

        if cell_color == EMPTY:  # we didn't fill it yet
            empty_flag = True
            cell_id += 1
            continue

        elif cell_color == WHITE and (must_color == WHITE or must_color == EMPTY):
            # that's good
            # if must color is white - that means we finished all constrains, and all remaining cells should stay white

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

                # move to next constraint
                curr_constraint_id += 1
                if curr_constraint_id < len(constraints_for_row):
                    curr_constraint = constraints_for_row[curr_constraint_id]
                    curr_num_of_cells_to_fill = curr_constraint.number
                    curr_constraint_color = curr_constraint.color

                else:
                    # we finished every constrain, next cells should be white only
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


# def __check_move_helper(row, board, row_id):
#     """
#     check if the move in this row_id/col_id is legit.
#     return True if this move works and legit, false otherwise
#
#     IMPORTANT NOTE: this doesn't show that this step is correct, it just checks if it could be there.
#     """
#
#     constraints_for_row: list[Constraint] = row[row_id]
#     current_row = board[row_id]
#
#     # constraint:
#     curr_constraint_id = 0
#     curr_constraint = constraints_for_row[curr_constraint_id]
#     curr_num_of_cells_to_fill = curr_constraint.number
#     curr_constraint_color = curr_constraint.color
#
#     must_color = EMPTY  # the color must be for the next cell
#     blocked_color = EMPTY  # sometimes we need to block a color from next cell (example: 1b-1b - we can't put two black near each other) - white can't be forbidden
#
#     constraints_complete = False
#     empty_flag = False  # there is an empty cell in this row
#     for cell in current_row:
#         cell_color = cell.color
#         if cell_color == EMPTY:  # we didn't fill it yet
#             empty_flag = True
#             continue
#         elif cell_color == WHITE and (must_color == WHITE or must_color == EMPTY):
#             # that's good
#             # if must color is white - that means we finished all constrains, and all remaining cells should stay white
#
#             # we reset the forbid color
#             blocked_color = EMPTY
#             continue
#
#         elif cell_color == curr_constraint_color and (must_color == curr_constraint_color or must_color == EMPTY) and blocked_color != curr_constraint_color:
#             # that's good, check if we need to change constrain
#             curr_num_of_cells_to_fill -= 1
#
#             # if we still didn't finish filling this constraint, we want the next color to be same color as the constraint:
#             if curr_num_of_cells_to_fill > 0:
#                 must_color = curr_constraint_color
#                 blocked_color = EMPTY  # nothing blocked
#
#             # if we finished filling this current constraint, we need to move to next constraint
#             elif curr_num_of_cells_to_fill == 0:
#                 must_color = EMPTY  # nothing is a must
#                 blocked_color = curr_constraint_color
#
#                 # move to next constraint
#                 curr_constraint_id += 1
#                 if curr_constraint_id < len(constraints_for_row):
#                     curr_constraint = constraints_for_row[curr_constraint_id]
#                     curr_num_of_cells_to_fill = curr_constraint.number
#                     curr_constraint_color = curr_constraint.color
#
#                 else:
#                     # we finished every constrain, next cells should be white only
#                     must_color = WHITE
#             else:
#                 raise Exception("this is an impossible situation, hmmmmmm")
#
#         else:
#             return False
#
#     # maybe we finished the row but the constraints aren't finished yet! and that's a mistake:
#     # if we have Empty then no need to finish the constraints, if we don't then constraints must complete
#
#     if empty_flag   :
#         return True
#
#     return False


def __invert_board(board):
    """
    transpose the board
    """
    return list(map(list, zip(*board)))
