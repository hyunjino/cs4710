# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        value = successorGameState.getScore()
        # check if successor is win or loss
        if successorGameState.isWin():
            return 1000000
        elif successorGameState.isLose():
            return -1000000

        if(action == Directions.STOP):
            value -= 100
        
        #if successor means eating food
        if successorGameState.getNumFood() < currentGameState.getNumFood():
            value += 300
        else: 
            value -= 100

        #if it means getting closer to food
        # closestFoodDist = 1000000
        # closestFoodPos = currentGameState.getFood()[0]

        # for i in currentGameState.getFood():
        #     dist = util.manhattanDistance(currentGameState.getPacmanPosition(), i)
        #     if dist < closestFoodDist:
        #         closestFoodDist = dist
        #         closestFoodPos = i

        # if util.manhattanDistance(newPos, closestFoodPos) < closestFoodDist:
        #     value += 300

        

        #if successor position is the same position as a ghost that is not scared vs one that is scared
        for i in newGhostStates:
            if newPos == i.getPosition():
                if i.scaredTimer == 0:
                    return -1000000
                else:
                    return 1000000

        

        return value

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def performMinimax(depth, agentIndex, gameState):
            #if node is terminal or depth = 0
            if (gameState.isWin() or gameState.isLose() or depth == 0):
                return self.evaluationFunction(gameState), ""

            if agentIndex == 0:
                return maxValue(depth, agentIndex, gameState)
            # agent is a ghost
            else:
                return minValue(depth, agentIndex, gameState)

        def maxValue(depth, agentIndex, gameState):
            value = -1000000
            bestAction = ""
            actions = gameState.getLegalActions(agentIndex)
            for i in actions:
                child = gameState.generateSuccessor(agentIndex, i)
                util = performMinimax(depth, agentIndex + 1, child)[0]
                if util > value:
                    value = util
                    bestAction = i
            return value, bestAction
        
        def minValue(depth, agentIndex, gameState):
            nextAgent = agentIndex + 1
            nextDepth = depth

            #if all ghosts have gone, make next agent pacman and go down a depth
            if nextAgent == gameState.getNumAgents():
                nextAgent = 0
                nextDepth -= 1

            value = 1000000
            actions = gameState.getLegalActions(agentIndex)
            for i in actions:
                child = gameState.generateSuccessor(agentIndex, i)
                value = min(value, performMinimax(nextDepth, nextAgent, child)[0])
            return value, ""

        return performMinimax(self.depth, 0, gameState)[1]
    

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def performAlphaBeta(depth, agentIndex, gameState, alpha, beta):
            #if node is terminal or depth = 0
            if (gameState.isWin() or gameState.isLose() or depth == 0):
                return self.evaluationFunction(gameState), ""

            if agentIndex == 0:
                return maxValue(depth, agentIndex, gameState, alpha, beta)
            # agent is a ghost
            else:
                return minValue(depth, agentIndex, gameState, alpha, beta)

        def maxValue(depth, agentIndex, gameState, alpha, beta):
            value = -1000000
            bestAction = ""
            actions = gameState.getLegalActions(agentIndex)
            for i in actions:
                child = gameState.generateSuccessor(agentIndex, i)
                util = performAlphaBeta(depth, agentIndex + 1, child, alpha, beta)[0]
                alpha = max(alpha, util)
                if util > value:
                    value = util
                    bestAction = i
                if value > beta:
                    return value, bestAction
            return value, bestAction
        
        def minValue(depth, agentIndex, gameState, alpha, beta):
            nextAgent = agentIndex + 1
            nextDepth = depth

            #if all ghosts have gone, make next agent pacman and go down a depth
            if nextAgent == gameState.getNumAgents():
                nextAgent = 0
                nextDepth -= 1

            value = 1000000
            actions = gameState.getLegalActions(agentIndex)
            for i in actions:
                child = gameState.generateSuccessor(agentIndex, i)
                value = min(value, performAlphaBeta(nextDepth, nextAgent, child, alpha, beta)[0])
                beta = min(beta, value)
                if value < alpha:
                    return value, ""
            return value, ""

        return performAlphaBeta(self.depth, 0, gameState, -100000, 1000000)[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def performExpectiMax(depth, agentIndex, gameState):
            #if node is terminal or depth = 0
            if (gameState.isWin() or gameState.isLose() or depth == 0):
                return self.evaluationFunction(gameState), ""

            if agentIndex == 0:
                return maxValue(depth, agentIndex, gameState)
            # agent is a ghost
            else:
                return expValue(depth, agentIndex, gameState)

        def maxValue(depth, agentIndex, gameState):
            value = -1000000
            bestAction = ""
            actions = gameState.getLegalActions(agentIndex)
            for i in actions:
                child = gameState.generateSuccessor(agentIndex, i)
                util = performExpectiMax(depth, agentIndex + 1, child)[0]
                if util > value:
                    value = util
                    bestAction = i
            return value, bestAction
        
        def expValue(depth, agentIndex, gameState):

            actions = gameState.getLegalActions(agentIndex)
            numActions = len(actions)
            value = 0
            prob = 1.0 / numActions
            for i in actions:
                nextAgent = agentIndex + 1
                nextDepth = depth

                #if all ghosts have gone, make next agent pacman and go down a depth
                if nextAgent == gameState.getNumAgents():
                    nextAgent = 0
                    nextDepth -= 1

                
                child = gameState.generateSuccessor(agentIndex, i)
                value += prob * performExpectiMax(nextDepth, nextAgent, child)[0]
            return value, ""

        return performExpectiMax(self.depth, 0, gameState)[1]

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <accumulate score based on the following positive factors:
    how close pacman is to food
    how far pacman is from ghost
    how close pacman is to a scared ghost (within a certain distance and scaredtime)
    how close pacman is to a capsule
    if the move will win the game
    if the move will lose the game>
    """
    "*** YOUR CODE HERE ***"

    pacmanPos = currentGameState.getPacmanPosition()
    foodPos = currentGameState.getFood().asList()
    capPos = currentGameState.getCapsules()
    ghostPos = currentGameState.getGhostPositions()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    score = 1000 * currentGameState.getScore()
    foodScore = 0
    ghostScore = 0
    totalScore = 0
    # check if successor is win or loss
    if currentGameState.isWin():
        return 1000000
    elif currentGameState.isLose():
        return -1000000

    #the more food and the farther they r, the lesser the score
    for i in foodPos:
        foodScore += 100 / manhattanDistance(pacmanPos, i) 

    for i in capPos:
        foodScore += 30 / manhattanDistance(pacmanPos, i) 

    for i in range(len(ghostStates)):
        if ghostStates[i].scaredTimer > 0:
            ghostScore += 1/(((manhattanDistance(pacmanPos, ghostPos[i])) * scaredTimes[i])+1)
        elif ghostStates[i].scaredTimer == 0:
            ghostScore += manhattanDistance(pacmanPos, ghostPos[i])
                     

    
        totalScore = score + foodScore + ghostScore
    return totalScore

# Abbreviation
better = betterEvaluationFunction
