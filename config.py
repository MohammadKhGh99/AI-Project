
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
LBS = 4
CSP_P = 5

ALGOS_DICT = {BRUTE: "Brute Force", BFS: "BFS", DFS: "DFS", ASTAR: "A*", LBS: "LBS", CSP_P: "CSP"}

ALL_ALGOS = [BRUTE, BFS, DFS, LBS, CSP_P]

IS_GUI = True
PRINT = False

EASY = True
HARD = False

COLORS_N_DICT = {EMPTY: ' ', WHITE: 'w', BLACK: 'b', RED: 'r'}

LOCS_DICT = {BRUTE: (865, 65), DFS: (865, 125), BFS: (865, 185), LBS: (865, 245), CSP_P: (865, 310)}

# CSP TYPES #:
MRV = 1
DEGREE = 2
LCV = 3
FC = 4
AC = 5
ALL_CSPS = {1, 2, 3, 4, 5}


NULL_HEU = 0
OUR_HEU = 1

ALGOS_SYS_DICT = {"brute": BRUTE, "bfs": BFS, "dfs": DFS, "astar": ASTAR, "lbs": LBS, "csp": CSP_P}
