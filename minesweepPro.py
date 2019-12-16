import pyautogui
import time
import sys
from PIL import Image, ImageGrab
import fileInput as fileHelper
import helperFunctions as funcs

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

animationDelay=0
clickDelay = 0

def returnToOrigin(origin, delay=0):
        pass
    
def click(x,y,origin, delay=0):
    ''' This function is used to move the mouse
        to the x,y coordinate passed into the 
        function, and then clicking there.
    '''
    if (delay > 0):
        pyautogui.moveTo(x, y, duration=delay)
    pyautogui.click(x,y) #button='right'
    pyautogui.click(x,y)   
        
def rclick(x,y,origin, delay=0):
    """ This function is used to do a right clikc
        to flag areas as bombs. It moves to the
        x,y coordinate passed into the function
        and then clicks it with the right button
        parameter.
    """
    if (delay > 0):
        pyautogui.moveTo(x, y, duration=delay)
    pyautogui.click(x,y, button='right')  
    
def checkHappyLevel(playBox):
    """ This function is used to check the "happy level" on the
        windows executable. The "happy level" tells us when the
        game is won, lost or if it is still going on.
    """
    basePos = [playBox.width//2, 17]
    
    playBoxCoords = (playBox.left, playBox.top, playBox.left +  playBox.width, playBox.top + playBox.height)
    image = ImageGrab.grab(playBoxCoords)
    pixelSpace = image.load()
    
    #5- win 
    midPix = pixelSpace[basePos[0],basePos[1]+5]
    if (midPix[0] < 10 and midPix[1] < 10 and midPix[2] < 10):
        #print("We won!")
        return 1
       
    #10 - lose 
    midPix = pixelSpace[basePos[0],basePos[1]+10]
    if (midPix[0] < 10 and midPix[1] < 10 and midPix[2] < 10):
        #print("We died...")
        return -1
    
    #12 - ok
    midPix = pixelSpace[basePos[0],basePos[1]+12]
    if (midPix[0] < 10 and midPix[1] < 10 and midPix[2] < 10):
        #print("We're alive")
        return 0
    
    print("Unknown happy level")
    return -2

def getPlayBox():
    """ This function is used to capture an image on the
        screen and get the playBox from it.
    """
    for i in range(len(difficultyPics)):
        playBox = pyautogui.locateOnScreen(difficultyPics[i])

        if (playBox != None):
            return (i,playBox)
    print("ERROR: Could not find playing field!")
    return (3,None)
    
def getStateFromBoard(playBox, boxWidth):
    """ This function is used for getting the state from the 
        board. It grabs the image of the minesweeper program
        and then does processing on the pixels to get what values 
        are present on the board.
    """
    playBoxCoords = (playBox.left, playBox.top, playBox.left +  playBox.width, playBox.top + playBox.height)
    image = ImageGrab.grab(playBoxCoords)
    pixelSpace = image.load()

    stateVal = []

    for row in boxPositions:
        stateRow = []
        for pos in row:
            midPix = pixelSpace[pos[0]-playBox.left,pos[1]-playBox.top]
            if (midPix[0] < 5 and midPix[1] < 5 and midPix[2] < 5):
                stateRow.append(-2)
            elif (midPix[0] > 190 and midPix[1] > 190 and midPix[2] > 190):
                topPix = pixelSpace[pos[0]-playBox.left,pos[1]-playBox.top-(boxWidth//2)]
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
                stateRow.append(9)
        stateVal.append(stateRow)
        
    width = len(stateVal)
    height = len(stateVal[0])
             
    state = []
        
    for i in range(len(stateVal)):
            stateRow = []
            for j in range(len(stateVal[i])):
                val = stateVal[i][j]
                bombs = 0
                neighbors = funcs.getNeighbors(i, j, width, height)
                newState = (val, bombs, neighbors)
                stateRow.append(newState)
            state.append(stateRow)

    funcs.writeNeighbors(state)        
        
    return state


def play(difficulty, playBox, guessFunction = funcs.chooseBestGuessV3):
    """ This function is used to play the minesweeper game
        for the windows executable method. 
    """
    # set the variables to initiale values
    boxPositions.clear()
    startTime = time.time()
    guesses = 0
    numBombs = difficultyBombs[difficulty]

    # get the playbox coordinates and info for middle box
    playBoxCoords = (playBox.left, playBox.top, playBox.left +  playBox.width, playBox.top + playBox.height)
    numBoxes = difficultySizes[difficulty]
    boxWidth = difficultyBoxSizes[difficulty]
    basePosition = (playBox.left, playBox.top)
    middleBaseBox = (playBox.left + boxWidth//2, playBox.top + uiHeight + boxWidth//2)

    # build up boxPositions
    for i in range(numBoxes[0]):
        col = []
        xPos = middleBaseBox[0] + boxWidth*i
        for j in range(numBoxes[1]):
            yPos = middleBaseBox[1] + boxWidth*j
            col.append((xPos,yPos))
        boxPositions.append(col)
    
    # calculate the middle box position
    middleBox = boxPositions[numBoxes[0]//2 -1][numBoxes[1]//2 -1]
    
    # click on the middle box
    click(middleBox[0],middleBox[1],(playBox.left, playBox.top),clickDelay)
    
    # Needed for particles to fade
    returnToOrigin( (playBox.left, playBox.top), clickDelay )
    time.sleep(animationDelay)
    
    # get current state 
    state = getStateFromBoard(playBox, boxWidth)

    # set the condition variables for the while loop
    happyLevel = 0    
    ratio = 1
    changed = True    
    while (changed == True and happyLevel != -1 and numBombs > 0):
        changed = False
 
        # find the bombs and safe locations
        bombs = funcs.findBombs(state)
        safes = funcs.findSafes(state)

        # go through all bombs
        for bomb in bombs:
            # get new number of unknown bombs
            numBombs = numBombs - 1

            # get the location of the bomb
            bombPos = funcs.indexToColRow(bomb, len(state[0]) ) 
            bombLocation = boxPositions[bombPos[0]][bombPos[1]]

            # right click to flag the location as a bomb
            rclick(bombLocation[0],bombLocation[1],(playBox.left, playBox.top),clickDelay)

            # if the number of unknown bombs is zero, get the new set of safe locations
            if (numBombs == 0):
                #print("All bombs successfully flagged!")
                safes = funcs.getUnknowns(state)
        
        # go through all the safe locations
        for safe in safes:
            changed = True
            safePos = funcs.indexToColRow(safe, len(state[0]) ) 
            safeLocation = boxPositions[safePos[0]][safePos[1]]

            # click on the safe location
            click(safeLocation[0],safeLocation[1],(playBox.left, playBox.top),clickDelay)
        if (changed == True):
            # check if we have solved minsweeper yet
            happyLevel = checkHappyLevel(playBox)
            if (happyLevel == 1):
                changed = False
            else:
                # move to origin and get new state
                returnToOrigin( (playBox.left, playBox.top), clickDelay )
                time.sleep(animationDelay)
                state = getStateFromBoard(playBox, boxWidth)

        # otherwise we need guesses to solve
        else:
            #if (guesses == 0):
               #print("Guesses are required for this board.")
            guesses += 1
            guess = guessFunction(state, numBombs)
            choice = guess[0]
            ratio = guess[1]
            choicePos = funcs.indexToColRow(choice, len(state[0]) ) 
            choiceLocation = boxPositions[choicePos[0]][choicePos[1]]

            # click on the guess location
            click(choiceLocation[0],choiceLocation[1],(playBox.left, playBox.top),clickDelay)

            # check if solved yet
            happyLevel = checkHappyLevel(playBox)
            if (happyLevel == 0):
                changed = True
                #time.sleep(animationDelay)
                state = getStateFromBoard(playBox, boxWidth)
            if (happyLevel == -1):
                break
    #funcs.displayState(state)
    runTime = (time.time() - startTime)
    returnVal = 0
    if (happyLevel == 1):
        returnVal = 1
        numBombs = 0
    
    return (returnVal, guesses, numBombs, ratio, runTime)
    
def tupleToCSVLine(tuple):
    resultText = ''
    for i in range(len(tuple)):
        resultText += str(tuple[i])
        if (i+1 == len(tuple)):
            resultText+='\n'
        else:
            resultText+=','
    return resultText
    
def getData(difficulty, playBox, trials=100):
    guessFunctions = [funcs.chooseBestGuessV0, funcs.chooseBestGuessV1, funcs.chooseBestGuessV2, funcs.chooseBestGuessV3]
    
    for functionIndex in range(len(guessFunctions)):
    
        listOfResults = []
        avgResult = [0,0,0,0,0]
        print('Getting data for Guess Algorithm v'+str(functionIndex)+', difficulty '+difficultyNames[difficulty])
        for i in range(trials):
            pyautogui.press('f2')
            result = play(difficulty, playBox,guessFunctions[functionIndex])
            #print(result)
            listOfResults.append(result)
            for i in range(len(result)):
                avgResult[i] = avgResult[i] + result[i]
            
        for i in range(len(avgResult)):
            avgResult[i] = avgResult[i] / trials
        
        dataDump = open('data/guess-v'+str(functionIndex)+'-'+difficultyNames[difficulty]+'.csv','w')
        dataDump.write('success,guesses,bombs,confidence,runtime\n')
    
        for result in listOfResults:
            resultText = tupleToCSVLine(result)
            dataDump.write(resultText)
        
        #dataDump.write( ',,,,\n')
        dataDump.write( tupleToCSVLine(avgResult) )
        dataDump.close()
    input("Data collection complete!\nPress enter to exit.\n")

if __name__ == "__main__":

    print("Initializing Minesweeper Program")

    # count the arguments
    arguments = len(sys.argv) - 1

    # count the arguments
    arguments = len(sys.argv) - 1
    mustWin = False
    
    if arguments > 0 and sys.argv[1] == '-data':
        trials = 100
        if arguments == 2:
            trials = int(sys.argv[2])
        result = (3,None)
        while (result[0] == 3):
            result = getPlayBox()
        difficulty = result[0]
        playBox = result[1]
        if (playBox != None):
            print('Collecting data on',trials,'trials for:',difficultyNames[difficulty],'\n')
            getData(difficulty, playBox, trials)
        
    
    elif arguments == 1 and sys.argv[1] != '-win':
        print("file input")
        difficulty, solutionPositions = fileHelper.parse_file(sys.argv[1])
        playBox = fileHelper.get_empty_play_box(difficulty)
        fileHelper.play(difficulty, playBox, solutionPositions)

    elif arguments == 0 or (arguments == 1 and sys.argv[1] == '-win'):
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
            result = (0,0,0,0,0)
            while (result[0] == 0):
                result = play(difficulty, playBox)
                if (result[0] == 0):
                    print("I lost... \nChance of that spot being a bomb: ",(result[3]*100),"%\nTotal number of guesses made: ",result[1],'\nRuntime: ',result[4]," seconds.\n")
                else:
                    print("I won! :D\nTotal number of guesses made: ",result[1],"\nTime to complete: ",result[4]," seconds.\n")
                if (mustWin == False):
                    result = (1,0,0,0,0)
                if (result[0] == 0):
                    pyautogui.press('f2')
            

        input("Press enter to exit.\n")

    # output usage statement to tell user how to run program if incorrect args passed
    else:
        print("ERROR - wrong number of input arguments entered.")
        print("Usage 1 (no input arguments): python minesweeperPro.py")
        print("USage 2 (1 input argument): python minesweeperPro.py -win")
        print("Usage 2 (1 input arguement): python minesweeperPro.py testFile.txt")