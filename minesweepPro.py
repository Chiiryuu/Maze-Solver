import pyautogui
import time
import random
import sys
from PIL import Image, ImageGrab
import fileInput as fileHelper
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
    
def getStateFromBoard(playBox, boxWidth):
    playBoxCoords = (playBox.left, playBox.top, playBox.left +  playBox.width, playBox.top + playBox.height)
    image = ImageGrab.grab(playBoxCoords)
    pixelSpace = image.load()
    #Optional; used for testing
    #image.save('initial-state.png')
    stateVal = []
    #print(boxPositions)
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
                neighbors = funcs.getNeighbors(i, j, width, height)
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
    funcs.writeNeighbors(state)        
        
        
    return state


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
    
    print("STATE: ", state)
    #print('Bombs: ',bombs)
    
    
    
    print('Safes: ',funcs.findSafes(state))
    
    #displayState(state)
    
    #print(state)
    
    happyLevel = 0
    
    ratio = 0
        
    changed = True    
    while (changed == True and happyLevel != -1):
        changed = False
        #displayState(state)
        bombs = funcs.findBombs(state)
        safes = funcs.findSafes(state)
        for bomb in bombs:
            bombPos = funcs.indexToColRow(bomb, len(state[0]) ) 
            bombLocation = boxPositions[bombPos[0]][bombPos[1]]
            rclick(bombLocation[0],bombLocation[1],(playBox.left, playBox.top),clickDelay)
        
        for safe in safes:
            changed = True
            safePos = funcs.indexToColRow(safe, len(state[0]) ) 
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
            choice = funcs.chooseBestGuess(state)
            choicePos = funcs.indexToColRow(choice, len(state[0]) ) 
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

    # count the arguments
    arguments = len(sys.argv) - 1
    mustWin = False
    
    if arguments == 1 and sys.argv[1] != '-win':
        print("file input")
        difficulty = fileHelper.parse_file(sys.argv[1])
        playBox = fileHelper.get_empty_play_box(difficulty)
        fileHelper.play(difficulty, playBox)

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
            result = -1
            while (result == -1):
                result = play(difficulty, playBox)
                if (mustWin == False):
                    result = 0
                if (result == -1):
                    pyautogui.press('f2')
            

        input("Press enter to exit.\n")

    # output usage statement to tell user how to run program if incorrect args passed
    else:
        print("ERROR - wrong number of input arguments entered.")
        print("Usage 1 (no input arguments): python minesweeperPro.py")
        print("USage 2 (1 input argument): python minesweeperPro.py -win")
        print("Usage 2 (1 input arguement): python minesweeperPro.py testFile.txt")