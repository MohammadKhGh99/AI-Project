import util


def search_helper(problem, fringe):
    fringe.push((problem.get_start_state(), []))
    visited = set()
    while not fringe.isEmpty():
        current = fringe.pop()
        if problem.is_goal_state(current[0]):
            return current[1]
        elif current[0] not in visited:
            for child in problem.get_successors(current[0]):
                temp = current[1] + [child[1]]
                fringe.push((child[0], temp))
            visited.add(current[0])
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
    root = StateAndActions(problem.get_start_state(), [])
    fringe.push(root, 0)
    visited = set()
    while not fringe.isEmpty():
        current = fringe.pop()
        if problem.is_goal_state(current.state):
            return current.actions
        elif current.state not in visited:
            for child in problem.get_successors(current.state):
                temp = current.actions + [child[1]]
                child_cost = problem.get_cost_of_actions(current.actions) + child[2]
                heuristic_cost = child_cost + heuristic(child[0], problem)
                fringe.push(StateAndActions(child[0], temp), heuristic_cost)
            visited.add(current.state)


# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
