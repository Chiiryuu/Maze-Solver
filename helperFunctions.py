import random
import fileInput as fileHelper

def colRowToIndex(col, row, height):
    """ This function is used to take in a (col,row) pair along 
        with the height of the playBox and converts the (col,row)
        pair to an index
    """
    if (col < 0 or row < 0 or row >= height):
        return -1
    return col*height + row
    
def indexToColRow(index, height):
    """ This function is used to take in an index along with the
        height of the playBox and converts the index to a (col,row)
        pair/
    """
    col = index // height
    row = index % height
    return (col, row)
    
def getNeighbors(col, row, width, height):
    """ This function is used to get all of the neighbors
        of a certain (col,row) pair.
    """
    neighbors = []
    min = -1
    max = width * height
    
    neighbor = colRowToIndex(col-1, row-1, height)
    if (neighbor > min and neighbor < max):
        neighbors.append((9, neighbor))
    
    neighbor = colRowToIndex(col-1, row, height)
    if (neighbor > min and neighbor < max):
        neighbors.append((9, neighbor))
        
    neighbor = colRowToIndex(col-1, row+1, height)
    if (neighbor > min and neighbor < max):
        neighbors.append((9, neighbor))
        
    neighbor = colRowToIndex(col, row-1, height)
    if (neighbor > min and neighbor < max):
        neighbors.append((9, neighbor))
        
    neighbor = colRowToIndex(col, row+1, height)
    if (neighbor > min and neighbor < max):
        neighbors.append((9, neighbor))
        
    neighbor = colRowToIndex(col+1, row-1, height)
    if (neighbor > min and neighbor < max):
        neighbors.append((9, neighbor))
    
    neighbor = colRowToIndex(col+1, row, height)
    if (neighbor > min and neighbor < max):
        neighbors.append((9, neighbor))
        
    neighbor = colRowToIndex(col+1, row+1, height)
    if (neighbor > min and neighbor < max):
        neighbors.append((9, neighbor))

    return neighbors
    
def displayState(state):
    """ This function is used to display the state of the
        program. It takes in the stae with is a 2d array of
        state tuples. 
    """
    rowSize = len(state)
    colSize = len(state[0])
    rowStrings = ['']*colSize
    for i in range(rowSize):
        for j in range(colSize):
            rowStrings[j] += str(state[i][j][0]) + ' '
    result = ''
    for string in rowStrings:
        result += string + '\n'
        
    result = result.replace('-1','X').replace('-2','B').replace('0',' ').replace('9','?').replace('-3', 'F')
    print(result)
    return result

def getUnknowns(state):
    """ Get a list of all of the unknowns in a state. It checks for the value
        being -1, and if it is -1 then it will appent the index to the unknown
        list.
    """
    unknowns = []
    height = len(state[0])
    for i in range(len(state)):
            for j in range(height):
                val = state[i][j][0]
                if (val == -1):
                    unknowns.append(colRowToIndex(i,j,height))
    return unknowns

def chooseBestGuessV1(state):
    """ Version 1 of the choose best guess function.
    """
    guessList = []
    unknownsToBombs = 0
    for i in range(len(state)):
            for j in range(len(state[i])):  
                val = state[i][j][0]
                
                if (val == -1 or val == -2):
                    val = 5
                
                unknowns = []
                bombs = state[i][j][1]
                difference = val-bombs
                
                neighbors = state[i][j][2]
                for neighbor in neighbors:
                    if (neighbor[0] == -1):
                        unknowns.append(neighbor[1])
                localVal = len(unknowns) - difference
                if (localVal > unknownsToBombs):
                    unknownsToBombs = localVal
                    guessList = unknowns
                if (localVal == unknownsToBombs):
                    guessList.extend(unknowns)
    #This is done because completely unknown squares are assigned a strange weight
    return random.choice(guessList)

def chooseBestGuessV2(state, numBombs):
    """ Version 2 of the choose best guess function
    """
    guessList = []
    frontier = []
    unknownsToBombs = 0
    totalCombinations = 0
    frontierValues = {}
    height = len(state[0])
    for i in range(len(state)):
            for j in range(height):  
                val = state[i][j][0]
                neighbors = state[i][j][2]
                if (val > 0):
                    onFrontier=False
                    numNeighbors = 0
                    for neighbor in neighbors:
                        if (neighbor[0] == -1):
                            onFrontier = True
                            numNeighbors = numNeighbors + 1
                    if (onFrontier):
                        frontier.append((i,j,numNeighbors))
                        
    for member in frontier:
        object = state[member[0]][member[1]]
        neighbors = object[2]
        unknownNeighbors = member[2]
        bombs = state[i][j][1]
        difference = object[0]-object[1]
        for neighbor in neighbors:
                neighborPos =  indexToColRow(neighbor[1], height)
                neighborObject = state[neighborPos[0]][neighborPos[1]]
                if (neighborObject[0] == -1):
                    val = frontierValues.get(neighbor[1], (0,0))
                    frontierValues[neighbor[1]] = (val[0] + difference, val[1] + unknownNeighbors)
    max = 1.0
    for key in frontierValues:
        val = frontierValues[key]
        val = val[0] / val[1]
        #print("val: ",val,", max: ",max,"val > max: ",val > max)
        if (val < max):
            guessList = []
            guessList.append(key)
            max = val
        elif (abs(val - max) < 0.01):
            guessList.append(key)
    #print("Choosing 1 of ",len(guessList)," best guesses...")   
    #print(frontierValues)

                     
    #print("Frontier: ",len(frontier),", Bombs:",numBombs)
    #This is done because completely unknown squares are assigned a strange weight
    
    #guess = random.choice(frontier)
    #guess = colRowToIndex(guess[0], guess[1], height)
    #return guess
    return (random.choice(guessList), max)

def writeNeighbors(state):
    """ This function is used to go through the current
        state of the board and see if anything has changed
        for the neighbors or number of bombs.
    """
    height = len(state[0])
    for i in range(len(state)):
            for j in range(len(state[i])):  
                val = state[i][j][0]
                bombs = state[i][j][1]
                neighbors = state[i][j][2]
                newNeighbors = []
                for k in range(len(neighbors)):
                    #print(neighbors[k])
                    neigborPos = indexToColRow(neighbors[k][1], height) 
                    neighborState = state[neigborPos[0]][neigborPos[1]]
                    if neighborState[0] == -2:
                        bombs+=1
                    elif neighborState[0] != 0:
                        newNeighbors.append((neighborState[0], neighbors[k][1]))
                state[i][j] = newState = (val, bombs, newNeighbors)
    
def findBombs(state):
    """ Function for finding the bombs in the state and 
        their locations.  
    """
    newBombs = []
    
    for i in range(len(state)):
            for j in range(len(state[i])):
                unknowns = []
                val = state[i][j][0]
                bombs = state[i][j][1]
                neighbors = state[i][j][2]
                for neighbor in neighbors:
                    if (neighbor[0] == -1):
                        unknowns.append(neighbor[1])
                if (val - bombs == len(unknowns)):
                    for unknown in unknowns:
                        if (not unknown in newBombs):
                            newBombs.append(unknown)
                    for k in reversed(range(len(neighbors))):
                        if (neighbors[k][1] in unknowns):
                            neighbors.pop(k)
                    bombs = bombs + len(unknowns)
                    state[i][j] = (val, bombs, neighbors)
                    
            for bomb in newBombs:
                bombPos = indexToColRow(bomb, len(state[0]) ) 
                state[bombPos[0]][bombPos[1]] = (-2, 0, [])
    writeNeighbors(state)
    return newBombs
    
def findSafes(state):
    """ This function is used to check the current
        state for locations that are safe to move 
        to (not a bomb)
    """
    safes = []
    
    for i in range(len(state)):
            for j in range(len(state[i])):
                unknowns = []
                val = state[i][j][0]
                bombs = state[i][j][1]
                neighbors = state[i][j][2]
                for neighbor in neighbors:
                    if (neighbor[0] == -1):
                        unknowns.append(neighbor[1])
                if (val - bombs == 0):
                    for unknown in unknowns:
                        if (not unknown in safes):
                            safes.append(unknown)
                    for k in reversed(range(len(neighbors))):
                        if (neighbors[k][1] in unknowns):
                            neighbors.pop(k)
                    state[i][j] = (val, bombs, neighbors)
    writeNeighbors(state)
    return safes