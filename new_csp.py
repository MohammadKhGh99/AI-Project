import Board

def get_needed_data(board: Board):
    m = board.num_rows
    n = board.num_cols
    o = len(game.COLORS_LST_WITHOUT_WHITE)
    b_r = []        # number of blocks in row i
    s_r = []        # sizes of all blocks in row i
    c_r = []        # colors of all blocks in row i

    b_c = []        # number of blocks in col i
    s_c = []        # sizes of all blocks in col i
    c_c = []        # colors of all blocks in col i

    # todo didn't write e and l yet
    # todo the way to fill them, we check the size of blocks before us: thats e,and sum with our length that's l

    # fill data in lists above
    for r in board.rows_constraints:
        b_r.append(len(r))
        sizes_r = []
        colors_r = []
        for k in r:
            sizes_r.append(k.length)
            colors_r.append(k.color)
        s_r.append(sizes_r)
        c_r.append(colors_r)
    for c in board.cols_constraints:
        b_c.append(len(c))
        sizes_c = []
        colors_c = []
        for k in c:
            sizes_c.append(k.length)
            colors_c.append(k.color)
        s_c.append(sizes_c)
        c_c.append(colors_c)


def get_variables_and_domains(board):
    """
    get variables and domains for CSP.
    """
    variables = []
    domains = {}

    # get constraint most left position (Row)
    for row_constraints in board.rows_constraints:
        for constraint in row_constraints:
            value = [0, 1]
            variables.append(constraint)
            domains[constraint] = value

    # get constraint most top position (Column)
    for col_constraints in board.cols_constraints:
        for constraint in col_constraints:
            value = [0, 1]
            variables.append(constraint)
            domains[constraint] = value

    all_colors = [_ for _ in range(len(board.COLORS_LST))]
    # get all cells in board
    for row in board.board:
        for cell in row:

            variables.append(cell)
            domains[cell] = all_colors

    return variables, domains
