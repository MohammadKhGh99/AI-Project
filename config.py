
BLACK_WHITE = 0
COLORFUL = 1

EMPTY = -1
WHITE = 0
BLACK = 1
RED = 2  # could be COLOR

NONO_COLORS = {"bw", "wb", "bwr", "brw", "wbr", "wrb", "rbw", "rwb"}
COLORS = {'b', 'r'}
COLORS_LST = [WHITE, BLACK, RED]
COLORS_LST_WITHOUT_WHITE = [BLACK, RED]
ROWS = False
COLUMNS = True

BRUTE_FORCE = True
SEARCH_PROBLEMS = False

COMPLETE = True
NOT_COMPLETE = False

GUI_WIDTH = 1000
GUI_HEIGHT = 800

GUI_FILES_PATH = r'.\FinalProject\\gui_files'

SOUND = False

COLORS_DICT = {'w': 'white', 'b': 'black', 'r': 'red', ' ': 'white'}

BRUTE = 0
BFS = 1
DFS = 2
ASTAR = 3
CSP_P = 4
LBS = 5

ALL_ALGOS = [BRUTE, BFS, DFS, ASTAR, CSP_P]

IS_GUI = True
PRINT = False

EASY = True
HARD = False

COLORS_N_DICT = {EMPTY: ' ', WHITE: 'w', BLACK: 'b', RED: 'r'}

# BRUTE_DIM = (758, 100)
# DFS_DIM = (760, 200)
# BFS_DIM = (760, 300)
# ASTAR_DIM = (758, 400)
# CSP_DIM = (760, 500)

LOCS_DICT = {BRUTE: (865, 80), DFS: (865, 140), BFS: (865, 200), ASTAR: (865, 260), CSP_P: (865, 380), LBS: (865, 320)}

# CSP TYPES #:
MRV = 1
DEGREE = 2
LCV = 3
FC = 4
AC = 5
ALL_CSPS = {1, 2, 3, 4, 5}

PROCESS = True
FINAL = False
