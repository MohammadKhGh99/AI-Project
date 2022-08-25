import util


def search_helper(problem, fringe):
    fringe.push((problem.get_start_state(), set()))
    while not fringe.isEmpty():
        current = fringe.pop()
        if problem.is_goal_state(current[0]):
            return current[0]
        for child in problem.get_successors(current[0]):
            check_coords = False
            for coord in child[1]:
                if coord in current[1]:
                    check_coords = True
            if not check_coords:
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
    visited = set()
    while not fringe.isEmpty():
        current = fringe.pop()
        if problem.is_goal_state(current.state):
            return current.state
        elif current.state not in visited:
            for child in problem.get_successors(current.state):
                child[1].update(current.actions)
                child_cost = problem.get_cost_of_actions(current.actions) + child[2]
                heuristic_cost = child_cost + heuristic(child[0], problem)
                fringe.push(StateAndActions(child[0], child[1]), heuristic_cost)
            visited.add(current.state)


def local_beam_search(k_problems, k):
    """
    Local beam search, starting with k-random stats, searching for a goal state in this k states.
    If no goal state, we pick the best k-stats from all successors (of starting states), and repeat.
    """
    all_successors = util.PriorityQueue()
    for problem in k_problems:
        if problem.is_goal_state():
            return problem
    for problem in k_problems:
        for successor in problem.get_successors():
            all_successors.push(successor, -1 * (successor[0].get_cost_of_actions(successor[0].cols_constraints)))
            # todo Adam will check this later - he said that, also he mentioned how excited he is for the video
    k_successors = []
    for i in range(k):
        try:
            k_successors.append(all_successors.pop())
        except IndexError:
            break
    if len(k_successors) == 0:
        return None
    return local_beam_search(k_successors, k)


# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
