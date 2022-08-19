#################################################################
# WRITERS : Fady omari, 212188635, Ali ali, 323955658
# EXERCISE : intro2cse ex8 2020
# DESCRIPTION: A program that solves nonograms	      .
# NOTES: intersection_row([[0, 1, -1], [-1, -1, -1]]) returns [-1, -1, -1]
#################################################################

import copy

WHITE_SPOT = 0
BLACK_SPOT = 1
UNSOLVED_SPOT = -1


def constraint_satisfactions(n, blocks):
    return constraint_satisfactions_helper(n, [0] * n, blocks, [], 0)


def constraint_satisfactions_helper(n, row, blocks, combination_list, index):
    '''backtraking function, this function returns list of lists that have all of the
     combinations of satisfactions'''

    if check_validity(row, blocks):
        combination_list.append(row[:])
        return
    if index >= n:
        return

    row[index] = WHITE_SPOT
    constraint_satisfactions_helper(n, row, blocks, combination_list, index + 1)
    row[index] = BLACK_SPOT
    constraint_satisfactions_helper(n, row, blocks, combination_list, index + 1)
    return combination_list


def row_variations(row, blocks):
    if blocks == []:
        return [[0] * len(row)]
    if row == [0] * len(row):
        return []

    if check_validity(row, blocks):
        return [row]

    new_row = row[:]
    empty_indexes = [i for i in range(len(row)) if row[i] == -1]
    ans = row_variations_helper(new_row, blocks, empty_indexes, [], 0)
    if ans == None:
        return []
    return ans


def row_variations_helper(row, blocks, empty_indexes, combination_list, index):
    '''backtraking function, this function returns list of lists that have all of the
     combinations of variations'''
    if -1 in row and combination_list != []:
        return
    if check_validity(row, blocks):
        combination_list.append(row[:])
        return
    if index >= len(empty_indexes):
        return
    row[empty_indexes[index]] = WHITE_SPOT
    row_variations_helper(row, blocks, empty_indexes, combination_list, index + 1)
    row[empty_indexes[index]] = BLACK_SPOT
    row_variations_helper(row, blocks, empty_indexes, combination_list, index + 1)
    return combination_list


def check_validity(row, blocks):

    '''this function returns True if row matches the block's requirements'''
    if row.count(1)!=sum(blocks):
        return False
    if UNSOLVED_SPOT in row:
        return False
    c = 0
    lst = []
    for num in row:
        if num == BLACK_SPOT:
            c += 1
        elif c != 0:
            lst.append(c)
            c = 0
    if c != 0:
        lst.append(c)
    if lst == blocks:
        return True
    return False


def intersection_row(rows):
    if rows==[]: return []
    lst = rows[0][:]
    for j in range(len(rows[0])):
        for i in range(len(rows) - 1):
            num1 = lst[j]
            num2 = rows[i + 1][j]
            num = intersection(num1, num2)
            lst[j] = num

    return lst


def intersection(a, b):
    '''this function makes intersections between two number according to requirements '''
    if a == b and a != UNSOLVED_SPOT:
        return a * b
    return UNSOLVED_SPOT


def build_board(constraints):
    '''this function builds a board with size of constraints, and has a -1 in every element'''
    board = []
    rows_num = len(constraints[0])
    col_num = len(constraints[1])
    for i in range(rows_num):
        one_row = []
        for j in range(col_num):
            one_row.append(UNSOLVED_SPOT)
        board.append(one_row)
    return board


def inverse(board):
    '''this function transpose rows to columns of the board'''
    new_board = []
    for j in range(len(board[0])):
        line = [board[i][j] for i in range(len(board))]
        new_board.append(line)
    return new_board


def is_board_completed(board):
    ''' returns True if board doesn't have a -1, returns False otherwise'''
    for i in range(len(board)):
        if UNSOLVED_SPOT in board[i]:
            return False
    return True



def solve_with_given_board(constraints, board):
    '''this function takes an existing board and solves it '''
    new_board = move_one_time(constraints, board)
    if new_board == None:
        return
    if new_board == board:
        return board
    board=solve_with_given_board(constraints,new_board)

    return board

def _intersection_shortcut(row, blocks):
    ''' if the row is empty , and twice the sum of constraints is less than length of the row;
    then the intersection if the variation will be the same row, there's no need to go to
     variation and intersection functions.'''
    if row.count(UNSOLVED_SPOT)==len(row) and 2*sum(blocks)<=len(row):
        return True
    return False
def _intersection_shortcut2(row, blocks):
    '''if the row is empty and the blocks is one number, so we can easily know what the intersection is.'''
    length=len(row)
    num=blocks[0]
    return row[:length-num]+[BLACK_SPOT]*(2*num-length)+row[num:]



def move_one_time(constraints, original_board):
    '''this function checks one time the rows and the columns and updates it'''
    board = copy.deepcopy(original_board)
    #cheking the rows...
    for i in range(len(board)):
        # trying to shortcut..
        if _intersection_shortcut(board[i], constraints[0][i]):
            continue
        if board[i].count(UNSOLVED_SPOT) == len(board[i]) and len(constraints[0][i]) == 1:
            board[i]=_intersection_shortcut2(board[i], constraints[0][i])
            continue
        ####
        combination_list = row_variations(board[i], constraints[0][i])
        if combination_list == []:
            return
        final_row = intersection_row(combination_list)
        board[i] = final_row

    board = inverse(board)
    '''switching rows to columns and do the same things...'''
    #checking the colmuns (which are the new rows)...
    for i in range(len(board)):
        # trying to shortcut..
        if _intersection_shortcut(board[i], constraints[1][i]):
            continue
        if board[i].count(UNSOLVED_SPOT) == len(board[i]) and len(constraints[1][i]) == 1:
            board[i]=_intersection_shortcut2(board[i], constraints[1][i])
            continue
        ####
        combination_list = row_variations(board[i], constraints[1][i])
        if combination_list == []:
            return
        final_row = intersection_row(combination_list)
        board[i] = final_row
    board = inverse(board) # returning the board to it's original shape.
    return board


def solve_easy_nonogram(constraints):
    board = build_board(constraints)
    return solve_with_given_board(constraints, board)


def solve_nonogram(constraints):
    board = build_board(constraints)
    return solve_nonogram_helper(constraints, [], board, 0)


def solve_nonogram_helper(constraints, sol_list, board, i):
    '''this function gathers all the solutions in one list called sol_list
    it's a backtracking function'''
    sol = solve_with_given_board(constraints, board)
    if sol == None:
        return
    if is_board_completed(sol):
        sol_list.append(sol)
        return sol_list
    row, col = i // len(board), i % len(board[0])
    board[row][col] = WHITE_SPOT
    solve_nonogram_helper(constraints, sol_list, board, i + 1)
    board[row][col] = BLACK_SPOT
    solve_nonogram_helper(constraints, sol_list, board, i + 1)
    board[row][col] = UNSOLVED_SPOT
    return sol_list


if __name__ == "__main__":
    print(solve_nonogram([[[1], [1]], [[1], [1]]]))


