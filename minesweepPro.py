import pyautogui
import time
import random
import sys
from PIL import Image, ImageGrab

#Close program if you go to (0,0)
#  https://pyautogui.readthedocs.io/en/latest/cheatsheet.html
#image = cv2.cvtColor(np.array(pyautogui.screenshot(region=(0, 0, 1300, 750))), cv2.COLOR_BGR2GRAY)


pyautogui.FAILSAFE = True
difficultyNames = ['Easy','Medium','Hard']
difficultyPics = ['easy.png', 'medium.png', 'hard.png']
difficulty = -1
                    #Width, height
difficultySizes = [(9,9),(16,16),(30,16)]
difficultyBoxSizes = [16,16,16]
difficultyBombs = [10,40,99]
boxPositions = []
solutionPositions = []
uiHeight=52

#State naming convention: -2: Bomb, -1: unexplored, 0: empty, 1: 1, 2:2... etc

#animationDelay=0.85
animationDelay=0
clickDelay = 0

def returnToOrigin(origin, delay=0):
        pass
        #pyautogui.moveTo(origin[0], origin[1], duration=delay)
    
def click(x,y,origin, delay=0):
        if (delay > 0):
            pyautogui.moveTo(x, y, duration=delay)
        pyautogui.click(x,y) #button='right'
        pyautogui.click(x,y)
        #if (delay > 0):
            #pyautogui.moveTo(origin[0], origin[1], duration=delay)
        #pyautogui.moveTo(origin[0], origin[1])   
        
def rclick(x,y,origin, delay=0):
        if (delay > 0):
            pyautogui.moveTo(x, y, duration=delay)
        pyautogui.click(x,y, button='right')
        #if (delay > 0):
            #pyautogui.moveTo(origin[0], origin[1], duration=delay)
        #pyautogui.moveTo(origin[0], origin[1])   
        
def displayState(state):
    rowSize = len(state)
    colSize = len(state[0])
    rowStrings = ['']*colSize
    for i in range(rowSize):
        for j in range(colSize):
            rowStrings[j] += str(state[i][j][0]) + ' '
    result = ''
    for string in rowStrings:
        result += string + '\n'
        
    result = result.replace('-1','X').replace('-2','B').replace('0',' ').replace('9','?')
    print(result)

def colRowToIndex(col, row, height):
    if (col < 0 or row < 0 or row >= height):
        return -1
    return col*height + row
    
def indexToColRow(index, height):
    col = index // height
    row = index % height
    return (col, row)
    
def checkHappyLevel(playBox):
    basePos = [playBox.width//2, 17]
    
    playBoxCoords = (playBox.left, playBox.top, playBox.left +  playBox.width, playBox.top + playBox.height)
    image = ImageGrab.grab(playBoxCoords)
    pixelSpace = image.load()
    
    #5- win 
    #10 - lose
    #12 - ok
    
    midPix = pixelSpace[basePos[0],basePos[1]+5]
    if (midPix[0] < 10 and midPix[1] < 10 and midPix[2] < 10):
        #print("We won!")
        return 1
        
    midPix = pixelSpace[basePos[0],basePos[1]+10]
    if (midPix[0] < 10 and midPix[1] < 10 and midPix[2] < 10):
        #print("We died...")
        return -1
    
    midPix = pixelSpace[basePos[0],basePos[1]+12]
    if (midPix[0] < 10 and midPix[1] < 10 and midPix[2] < 10):
        #print("We're alive")
        return 0
    
    print("Unknown happy level")
    return -2

def getPlayBox():
    for i in range(len(difficultyPics)):
        #print('Searching for',difficultyNames[i])
        playBox = pyautogui.locateOnScreen(difficultyPics[i])
        #print(playBox)
        if (playBox != None):
            return (i,playBox)
    print("ERROR: Could not find playing field!")
    return (3,None)
    
def getNeighbors(col, row, width, height):
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
    
def chooseBestGuess(state):
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
    
def getStateFromBoard(playBox, boxWidth):
    playBoxCoords = (playBox.left, playBox.top, playBox.left +  playBox.width, playBox.top + playBox.height)
    image = ImageGrab.grab(playBoxCoords)
    pixelSpace = image.load()
    #Optional; used for testing
    #image.save('initial-state.png')
    stateVal = []
    for row in boxPositions:
        stateRow = []
        for pos in row:
            midPix = pixelSpace[pos[0]-playBox.left,pos[1]-playBox.top]
            if (midPix[0] < 5 and midPix[1] < 5 and midPix[2] < 5):
                stateRow.append(-2)
            elif (midPix[0] > 190 and midPix[1] > 190 and midPix[2] > 190):
                topPix = pixelSpace[pos[0]-playBox.left,pos[1]-playBox.top-(boxWidth//2)]
                #print('\t',topPix)
                if (topPix[0] > 250 and topPix[1] > 250 and topPix[2] > 250):
                    stateRow.append(-1)
                else:
                    stateRow.append(0)
            elif (midPix[0] < 10 and midPix[1] < 10 and midPix[2] > 250):
                stateRow.append(1)
            elif (midPix[0] < 10 and midPix[1] > 125 and midPix[2] < 10):
                stateRow.append(2)
            elif (midPix[0] > 250 and midPix[1] < 10 and midPix[2] < 10):
                stateRow.append(3)
            elif (midPix[0] < 10 and midPix[1] < 10 and midPix[2] > 120):
                stateRow.append(4)
            elif (midPix[0] < 30 and midPix[1] > 90 and midPix[2] > 90):
                stateRow.append(6)
            elif (midPix[0] > 70 and midPix[1] < 10 and midPix[2] < 10):
                stateRow.append(5)
            else:
                print(midPix)
                stateRow.append(9)
        stateVal.append(stateRow)
        
    width = len(stateVal)
    height = len(stateVal[0])
        
        
    state = []
        
        
    for i in range(len(stateVal)):
            stateRow = []
            for j in range(len(stateVal[i])):
                val = stateVal[i][j]
                #print(val)
                bombs = 0
                neighbors = getNeighbors(i, j, width, height)
                #index = colRowToIndex(i,j,height)
                #pos = indexToColRow(index, height)
                #print(pos, ', ',index)
                #state[pos[0]][pos[1]] = index
                #state[i][j] = i*height + j
                newState = (val, bombs, neighbors)
                stateRow.append(newState)
                #print(state[i][j])
            state.append(stateRow)
            
        #print(state,'\n')
    writeNeighbors(state)        
        
        
    return state

def writeNeighbors(state):
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


def play(difficulty, playBox):
    boxPositions.clear()
    startTime = time.time()
    guesses = 0
    playBoxCoords = (playBox.left, playBox.top, playBox.left +  playBox.width, playBox.top + playBox.height)
    numBoxes = difficultySizes[difficulty]
    boxWidth = difficultyBoxSizes[difficulty]
    basePosition = (playBox.left, playBox.top)
    middleBaseBox = (playBox.left + boxWidth//2, playBox.top + uiHeight + boxWidth//2)
    for i in range(numBoxes[0]):
        col = []
        xPos = middleBaseBox[0] + boxWidth*i
        for j in range(numBoxes[1]):
            yPos = middleBaseBox[1] + boxWidth*j
            col.append((xPos,yPos))
        boxPositions.append(col)
    
    middleBox = boxPositions[numBoxes[0]//2 -1][numBoxes[1]//2 -1]
    
    click(middleBox[0],middleBox[1],(playBox.left, playBox.top),clickDelay)
    
    #Needed for particles to fade
    returnToOrigin( (playBox.left, playBox.top), clickDelay )
    time.sleep(animationDelay)
    
    state = getStateFromBoard(playBox, boxWidth)
    
    #print(state)
    
    
    #print('Bombs: ',bombs)
    
    
    
    #print('Safes: ',safes)
    
    #displayState(state)
    
    #print(state)
    
    happyLevel = 0
    
    ratio = 0
        
    changed = True    
    while (changed == True and happyLevel != -1):
        changed = False
        #displayState(state)
        bombs = findBombs(state)
        safes = findSafes(state)
        for bomb in bombs:
            bombPos = indexToColRow(bomb, len(state[0]) ) 
            bombLocation = boxPositions[bombPos[0]][bombPos[1]]
            rclick(bombLocation[0],bombLocation[1],(playBox.left, playBox.top),clickDelay)
        
        for safe in safes:
            changed = True
            safePos = indexToColRow(safe, len(state[0]) ) 
            safeLocation = boxPositions[safePos[0]][safePos[1]]
            click(safeLocation[0],safeLocation[1],(playBox.left, playBox.top),clickDelay)
        if (changed == True):
            happyLevel = checkHappyLevel(playBox)
            if (happyLevel == 1):
                changed = False
            else:
                returnToOrigin( (playBox.left, playBox.top), clickDelay )
                time.sleep(animationDelay)
                state = getStateFromBoard(playBox, boxWidth)
        else:
            if (guesses == 0):
                print("Guesses are required for this board.")
            guesses += 1
            choice = chooseBestGuess(state)
            choicePos = indexToColRow(choice, len(state[0]) ) 
            choiceLocation = boxPositions[choicePos[0]][choicePos[1]]
            click(choiceLocation[0],choiceLocation[1],(playBox.left, playBox.top),clickDelay)
            happyLevel = checkHappyLevel(playBox)
            if (happyLevel == 0):
                changed = True
                time.sleep(animationDelay)
                state = getStateFromBoard(playBox, boxWidth)
            if (happyLevel == -1):
                break

    if (happyLevel == -1):
        print("I lost... \nTotal number of guesses made: ",guesses,'\nRuntime: ',(time.time() - startTime)," seconds.\n")
        return -1
    else:
        print("I won! :D\nTotal number of guesses made: ",guesses,"\nTime to complete: ",(time.time() - startTime)," seconds.\n")
        return 0
        
       

if __name__ == "__main__":
        print("Initializing Minesweeper Program")

        # count the arguments
        arguments = len(sys.argv) - 1
        mustWin = False
        # if no input arg passed in, look for windows exe for minesweeper
        if arguments == 1 and sys.argv[1] == '-win':
            mustWin = True
            print('Repeat until win has been enabled. This is dangerous. Move mouse to top left of screen to close program.')
        result = (3,None)
        while (result[0] == 3):
            result = getPlayBox()
        difficulty = result[0]
        playBox = result[1]
        
        if (playBox != None):
            print('Detected Difficulty:',difficultyNames[difficulty],'\n')
            result = -1
            while (result == -1):
                result = play(difficulty, playBox)
                if (mustWin == False):
                    result = 0
                if (result == -1):
                    pyautogui.press('f2')
                    
            '''try:
                play(difficulty, playBox)
            except:
                print('Triggered Failsafe')
                exit()'''
            

        input("Press enter to exit.\n")
