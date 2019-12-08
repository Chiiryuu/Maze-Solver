import pyautogui
import time
import random
import sys
import helperFunctions as funcs

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
dict1 = {}
keep_track_zeros = []
unexp = []

#State naming convention: -3: flagged bomb, -2: Bomb, -1: unexplored, 0: empty, 1: 1, 2:2... etc
    
def displayPlayBox(state):
    rowSize = len(state)
    colSize = len(state[0])
    rowStrings = ['']*colSize
    for i in range(rowSize):
        for j in range(colSize):
            rowStrings[j] += str(state[i][j]) + ' '
    result = ''
    for string in rowStrings:
        result += string + '\n'
        
    result = result.replace('-1','X').replace('-2','B').replace('0',' ').replace('9','?').replace('-3', 'B')
    #print(result)
    return result

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
        
    result = result.replace('-1','X').replace('-2','B').replace('0',' ').replace('9','?').replace('-3', 'B')
    print(result)
    return result

def parse_file(file_name):
    difficulty = []
    # open tbe file
    with open(file_name) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            if cnt == 1:
                if line.strip() == "EASY":
                    difficulty = 0
                elif line.strip() == "MEDIUM":
                    difficulty = 1
                elif line.strip() == "HARD":
                    difficulty = 2
                else:
                    print("Difficulty in test file not recognized")
            else:
                # get the string vals from the file and turn them into ints
                vals = line.rstrip().split(", ")
                solutionPositions.append([int(i) for i in vals] )

            line = fp.readline()
            cnt += 1
        #print(solutionPositions)

    return difficulty

def get_empty_play_box(difficulty):
    # creates an nxm array of '-1' to represent all unexplored nodes to start
    if difficulty == 0:
        playBox = [[-1 for i in range(9)] for j in range(9)]
    elif difficulty == 1:
        playBox = [[-1 for i in range(16)] for j in range(16)]
    elif difficulty == 2:
        playBox = [[-1 for i in range(30)] for j in range(16)]
    else:
        print("Error - difficult not recognized")
        playBox = None 
    return playBox

def getStateFromBoard(playBox):
    stateVal = []
    # go through the board
    for row in boxPositions:
        stateRow = []
        for pos in row:
            # get the value 
            stateRow.append(playBox[pos[0]][pos[1]])

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
                neighbors = funcs.getNeighbors(i, j, width, height)
                newState = (val, bombs, neighbors)
                stateRow.append(newState)
            state.append(stateRow)
            
    funcs.writeNeighbors(state)
        
    return state

def checkSolved(playBox):
    # we won!
    if displayPlayBox(playBox) == displayPlayBox(solutionPositions):
        return 1
    # we are alive!
    else:
        return 0

def play(difficulty, playBox):
    boxPositions.clear()
    startTime = time.time()
    guesses = 0
    #playBoxCoords = (playBox.left, playBox.top, playBox.left +  playBox.width, playBox.top + playBox.height)
    numBoxes = difficultySizes[difficulty]
    boxWidth = difficultyBoxSizes[difficulty]

    #set up box positions
    for i in range(numBoxes[0]):
        col = []
        for j in range(numBoxes[1]):
            col.append((i,j))
        boxPositions.append(col)
    

    # get position in middle of the board
    middlePositionX = numBoxes[0]//2
    middlePositionY = numBoxes[1]//2
    
    # "click" on middle position
    playBox[middlePositionY][middlePositionX] = solutionPositions[middlePositionX][middlePositionY]

   # print(displayPlayBox(playBox))
    
    state = getStateFromBoard(playBox)
    
    # print("STATE: ", state)
    #bombs = funcs.findBombs(state)
    #print('Bombs: ',bombs)
    
    #print('Safes: ',funcs.findSafes(state))
    
    #displayState(state)
    
    # set happy level to be 0 (alive)
    happyLevel = 0
        
    changed = True   
    count = 0 
    while (changed == True and happyLevel != -1):
        changed = False
        print("beggining of loop: ")
        displayState(state)
        bombs = funcs.findBombs(state)
        safes = funcs.findSafes(state)
        for bomb in bombs:
            bombPos = funcs.indexToColRow(bomb, len(state[0]) ) 
            bombLocation = boxPositions[bombPos[0]][bombPos[1]]
            print("bombLocation: ", bombLocation)
            #rclick(bombLocation[0],bombLocation[1],(playBox.left, playBox.top),clickDelay)
            playBox[bombLocation[1]][bombLocation[0]] = -3  #flag as a bomb

        
        for safe in safes:
            changed = True
            safePos = funcs.indexToColRow(safe, len(state[0]) ) 
            safeLocation = boxPositions[safePos[0]][safePos[1]]
            #click(safeLocation[0],safeLocation[1],(playBox.left, playBox.top),clickDelay)
            playBox[safeLocation[1]][safeLocation[0]] = solutionPositions[safeLocation[0]][safeLocation[1]]

            # clicked a bomb, lost 
            if playBox[safeLocation[1]][safeLocation[0]] == -2:
                happyLevel = -1

        if (changed == True):
            if happyLevel != -1:
                happyLevel = checkSolved(playBox)
            if (happyLevel == 1):
                changed = False
            else:
                #returnToOrigin( (playBox.left, playBox.top), clickDelay )
                #time.sleep(animationDelay)
                state = getStateFromBoard(playBox)
                displayState(state)
        else:
            if (guesses == 0):
                print("Guesses are required for this board.")
            guesses += 1
            choice = funcs.chooseBestGuess(state)
            choicePos = funcs.indexToColRow(choice, len(state[0]) ) 
            choiceLocation = boxPositions[choicePos[0]][choicePos[1]]
            print(choiceLocation)

            playBox[choiceLocation[1]][choiceLocation[0]] = solutionPositions[choiceLocation[0]][choiceLocation[1]]
            if playBox[choiceLocation[1]][choiceLocation[0]] == -2:
                happyLevel = -1
            #click(choiceLocation[0],choiceLocation[1],(playBox.left, playBox.top),clickDelay)
            happyLevel = checkSolved(playBox)
            if (happyLevel == 0):
                changed = True
                #time.sleep(animationDelay)
                state = getStateFromBoard(playBox)
            if (happyLevel == -1):
                break
        print("end of loop: ")
        displayState(state)
    if (happyLevel == -1):
        print("I lost... \nTotal number of guesses made: ",guesses,'\nRuntime: ',(time.time() - startTime)," seconds.\n")
        return -1
    elif happyLevel == 1:
        print("I won! :D\nTotal number of guesses made: ",guesses,"\nTime to complete: ",(time.time() - startTime)," seconds.\n")
        return 0
    else:
        print("Debugging: still alive")
