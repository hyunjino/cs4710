# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    start_state = problem.getStartState()
    start_node = (start_state, [])
    visted_states = set()
    print("Start:", problem.getStartState())

    adjacent_nodes = util.Stack()
    adjacent_nodes.push(start_node)

    while not (adjacent_nodes.isEmpty()):

        current_node = adjacent_nodes.pop()
        current_state = current_node[0]
        actions = current_node[1]

        if current_state not in visted_states:
            visted_states.add(current_state)

            if problem.isGoalState(current_state):
                return actions
            
            else:
                adjacents = problem.getSuccessors(current_state)
                
                for i in adjacents:
                    new_action = actions + [i[1]]
                    new_node = (i[0], new_action)
                    adjacent_nodes.push(new_node)

    return actions  

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    start_node = (start_state, [])
    visted_states = set()

    adjacent_nodes = util.Queue()
    adjacent_nodes.push(start_node)

    while not (adjacent_nodes.isEmpty()):

        current_node = adjacent_nodes.pop()
        current_state = current_node[0]
        actions = current_node[1]

        if current_state not in visted_states:
            visted_states.add(current_state)

            if problem.isGoalState(current_state):
                return actions
            
            else:
                adjacents = problem.getSuccessors(current_state)
                
                for i in adjacents:
                    new_action = actions + [i[1]]
                    new_node = (i[0], new_action)
                    adjacent_nodes.push(new_node)

    return actions  

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    start_state = problem.getStartState()
    start_node = (start_state, [], 0)
    visted_states = set()

    opened_nodes = util.PriorityQueue()
    opened_nodes.push(start_node, 0)


    while not (opened_nodes.isEmpty()):

        current_node = opened_nodes.pop()
        current_state = current_node[0]
        actions = current_node[1]
        current_cost = current_node[2]

        if current_state not in visted_states:
            visted_states.add(current_state)

            if problem.isGoalState(current_state):
                return actions
            
            else:
                adjacents = problem.getSuccessors(current_state)
                
                for i in adjacents:
                    new_action = actions + [i[1]]
                    new_cost = current_cost + i[2]
                    new_node = (i[0], new_action, new_cost)
                    opened_nodes.push(new_node, new_cost)

    return actions  

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # def manhattanHeuristic(position, problem, info={}):
    #     xy1 = position
    #     xy2 = problem.goal
    #     return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

    import searchAgents
    start_state = problem.getStartState()
    start_node = (start_state, [], 0)
    visited_states = set()

    opened_nodes = util.PriorityQueue()
    opened_nodes.push(start_node, 0)


    while not (opened_nodes.isEmpty()):

        current_node = opened_nodes.pop()
        current_state = current_node[0]
        actions = current_node[1]
        current_cost = current_node[2]

        if current_state not in visited_states:
            visited_states.add(current_state)

            if problem.isGoalState(current_state):
                return actions
            
            else:
                adjacents = problem.getSuccessors(current_state)
                
                for i in adjacents:
                    if i[0] not in visited_states:
                        new_action = actions + [i[1]]
                        new_cost = current_cost + i[2]
                        new_node = (i[0], new_action, new_cost)
                        new_heuristic = heuristic(i[0], problem)
                        opened_nodes.push(new_node, new_cost + new_heuristic)

    return actions  


    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
