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
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        minGhostDistance = min([manhattanDistance(newPos, state.getPosition()) for state in newGhostStates])

        scoreDiff = childGameState.getScore() - currentGameState.getScore()

        pos = currentGameState.getPacmanPosition()
        nearestFoodDistance = min([manhattanDistance(pos, food) for food in currentGameState.getFood().asList()])
        newFoodsDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        newNearestFoodDistance = 0 if not newFoodsDistances else min(newFoodsDistances)
        isFoodNearer = nearestFoodDistance - newNearestFoodDistance

        direction = currentGameState.getPacmanState().getDirection()
        if minGhostDistance <= 1 or action == Directions.STOP:
            return 0
        if scoreDiff > 0:
            return 8
        elif isFoodNearer > 0:
            return 4
        elif action == direction:
            return 2
        else:
            return 1


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
    Your minimax agent (Part 1)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        # Begin your code (Part 1)
        #raise NotImplementedError("To be implemented")
        
        num_of_agents = gameState.getNumAgents()
        def minimax(gameState,depth,agentIndex):
            if agentIndex >= num_of_agents:
                agentIndex = agentIndex - num_of_agents
            if (depth == 0 and agentIndex == 0) or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            
            ret = 0
            if depth == self.depth:
                MAX = -2e20
                for pacman_action in gameState.getLegalActions(agentIndex):
                    tmp = minimax(gameState.getNextState(agentIndex,pacman_action),depth-1,agentIndex+1)
                    if MAX < tmp:
                        MAX = tmp
                        ret = pacman_action
                return ret

            if agentIndex == 0:
                MAX = -2e20
                for pacman_action in gameState.getLegalActions(agentIndex):
                    MAX = max(MAX,minimax(gameState.getNextState(agentIndex,pacman_action),depth-1,agentIndex+1))
                return MAX
            else:
                MIN = 2e20
                for ghost_action in gameState.getLegalActions(agentIndex):
                    MIN = min(MIN,minimax(gameState.getNextState(agentIndex,ghost_action),depth,agentIndex+1))
                return MIN
            
        return minimax(gameState,self.depth,0)
        # End your code (Part 1)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (Part 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        # Begin your code (Part 2)
        num_of_agents = gameState.getNumAgents()
        def alpha_beta_pruning(gameState,depth,agentIndex,alpha,beta):
            if agentIndex >= num_of_agents:
                agentIndex = agentIndex - num_of_agents
            if (depth == 0 and agentIndex == 0) or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            
            ret = 0
            eval_alpha = alpha
            eval_beta = beta
            if depth == self.depth:
                MAX = -2e20
                for pacman_action in gameState.getLegalActions(agentIndex):
                    tmp = alpha_beta_pruning(gameState.getNextState(agentIndex,pacman_action),depth-1,agentIndex+1,eval_alpha,eval_beta)
                    eval_alpha = max(eval_alpha,tmp)
                    if MAX < tmp:
                        MAX = tmp
                        ret = pacman_action
                return ret

            if agentIndex == 0:
                MAX = -2e20
                eval_MAX = -2e20
                for pacman_action in gameState.getLegalActions(agentIndex):
                    tmp = alpha_beta_pruning(gameState.getNextState(agentIndex,pacman_action),depth-1,agentIndex+1,eval_alpha,eval_beta)
                    MAX = max(MAX,tmp)
                    eval_alpha = max(eval_alpha,tmp)
                    if MAX > eval_beta:
                        return MAX
                return MAX
            else:
                MIN = 2e20
                for ghost_action in gameState.getLegalActions(agentIndex):
                    if agentIndex == 1:
                        tmp = alpha_beta_pruning(gameState.getNextState(agentIndex,ghost_action),depth,agentIndex+1,eval_alpha,eval_beta)
                    else:
                        tmp = alpha_beta_pruning(gameState.getNextState(agentIndex,ghost_action),depth,agentIndex+1,eval_alpha,eval_beta)
                    eval_beta = min(eval_beta,tmp)
                    MIN = min(MIN,tmp)
                    if MIN < eval_alpha:
                        return MIN
                return MIN
            
        return alpha_beta_pruning(gameState,self.depth,0,-2e20,2e20)
        # End your code (Part 2)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (Part 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        # Begin your code (Part 3)
        #raise NotImplementedError("To be implemented")
        num_of_agents = gameState.getNumAgents()
        def expectimax(gameState,depth,agentIndex):
            if agentIndex >= num_of_agents:
                agentIndex = agentIndex - num_of_agents
            if (depth == 0 and agentIndex == 0) or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            
            ret = 0
            if depth == self.depth:
                MAX = -2e20
                for pacman_action in gameState.getLegalActions(agentIndex):
                    tmp = expectimax(gameState.getNextState(agentIndex,pacman_action),depth-1,agentIndex+1)
                    if MAX < tmp:
                        MAX = tmp
                        ret = pacman_action
                return ret

            if agentIndex == 0:
                MAX = -2e20
                for pacman_action in gameState.getLegalActions(agentIndex):
                    MAX = max(MAX,expectimax(gameState.getNextState(agentIndex,pacman_action),depth-1,agentIndex+1))
                return MAX
            else:
                MIN = 0
                expect = 1/len(gameState.getLegalActions(agentIndex))
                for ghost_action in gameState.getLegalActions(agentIndex):
                    MIN = MIN + expectimax(gameState.getNextState(agentIndex,ghost_action),depth,agentIndex+1)*expect
                return MIN
            
        return expectimax(gameState,self.depth,0)
        # End your code (Part 3)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (Part 4).
    """
    # Begin your code (Part 4)
    if currentGameState.isLose():
        return -500000000
    
    GhostStates = currentGameState.getGhostStates()
    PacmanPosition = currentGameState.getPacmanPosition()
    minGhostDistance = min([manhattanDistance(PacmanPosition, state.getPosition()) for state in GhostStates])
    score = minGhostDistance * 0.05 + 1000

    Foods = currentGameState.getFood()
    minFoodDistance = Foods.height + Foods.width
    capsule = currentGameState.getCapsules()

    eat = 0
    for x in range(0,Foods.width):
        for y in range(0,Foods.height):
            if  Foods[x][y]:
                minFoodDistance = min(minFoodDistance,manhattanDistance(PacmanPosition,[x,y]))
                eat = eat + 1

    score = score - minFoodDistance - (Foods.height+Foods.width) * eat * 50 - len(capsule) * (Foods.height+Foods.width) * 500 + currentGameState.getScore() * 0.02
    return score
    # End your code (Part 4)

# Abbreviation
better = betterEvaluationFunction
