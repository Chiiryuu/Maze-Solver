import pyautogui
import time
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

animationDelay=0.85

def click(x,y,origin, delay=0):
    try:
        if (delay > 0):
            pyautogui.moveTo(x, y, duration=delay)
        pyautogui.click(x,y) #button='right'
        pyautogui.click(x,y)
        if (delay > 0):
            pyautogui.moveTo(origin[0], origin[1], duration=delay)
        pyautogui.moveTo(origin[0], origin[1])   
    except:
        print('Triggered Failsafe')
        exit()
        
def displayState(state):
    rowSize = len(state)
    colSize = len(state[0])
    rowStrings = ['']*colSize
    for i in range(rowSize):
        for j in range(colSize):
            rowStrings[j] += str(state[i][j]) + ' '
    result = ''
    for string in rowStrings:
        result += string + '\n'
        
    result = result.replace('-1','X').replace('-2','B').replace('0',' ').replace('9','?')
    print(result)
    

def getPlayBox():
    for i in range(len(difficultyPics)):
        print('Searching for',difficultyNames[i])
        playBox = pyautogui.locateOnScreen(difficultyPics[i])
        print(playBox)
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
    state = []
    for row in boxPositions:
        stateRow = []
        for pos in row:
            midPix = pixelSpace[pos[0]-playBox.left,pos[1]-playBox.top]
            if (midPix[0] > 190 and midPix[1] > 190 and midPix[2] > 190):
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
            else:
                print(midPix)
                stateRow.append(9)
                #print(midPix)
                #boxSpace = (pos[0]-boxWidth//2,pos[1]-boxWidth//2,pos[0]+boxWidth//2, pos[1]+boxWidth//2)
                #boxPic = ImageGrab.grab(boxSpace)
               #boxPic.save('%s,%s.png' % (pos[0],pos[1]))
            
            '''
            if (midPix[2] > 200):
                stateRow.append(1)
            elif (midPix[0] > 200 and midPix[1] > 180 and midPix[2] > 150):
                stateRow.append(0)
            elif (midPix[0] > 160 and midPix[1] > 200 and midPix[2] > 70):
                stateRow.append(-1)
            elif (midPix[0] > 100 and midPix[1] > 150 and midPix[2] > 80):
                stateRow.append(2)
            elif (midPix[0] > 205 and midPix[1] > 45 and midPix[2] > 45):
                stateRow.append(3)
            else:
                stateRow.append(9)
                print(midPix)
                boxSpace = (pos[0]-boxWidth//2,pos[1]-boxWidth//2,pos[0]+boxWidth//2, pos[1]+boxWidth//2)
                boxPic = ImageGrab.grab(boxSpace)
                boxPic.save('%s,%s.png' % (pos[0],pos[1]))
                
                ''' 
            #click(pos[0],pos[1],0.2)
            #boxSpace = (pos[0]-boxWidth//2,pos[1]-boxWidth//2,pos[0]+boxWidth//2, pos[1]+boxWidth//2)
            #boxPic = ImageGrab.grab(boxSpace)
            #stateRow.append(0)
            #boxPic.save('%s,%s.png' % (pos[0],pos[1]))
        state.append(stateRow)
    return state


def play(difficulty, playBox):
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
    
    click(middleBox[0],middleBox[1],(playBox.left, playBox.top),0.2)
    
    #Needed for particles to fade
    time.sleep(animationDelay)
    
    state = getStateFromBoard(playBox, boxWidth)
    
    print(state)
    displayState(state)

def parse_file(file_name):
    difficulty = []
    # open tbe file
    with open(file_name) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            if cnt == 1:
                if line.strip() == "EASY":
                    print("EASY TEST FILE")
                    difficulty = difficultyNames[0]
                elif line.strip() == "MEDIUM":
                    print("Medium test file")
                    difficulty = difficultyNames[1]
                elif line.strip() == "HARD":
                    print("Hard test file")
                    difficulty = difficultyNames[2]
                else:
                    print("Difficulty in test file not recognized")
            else:
                # get the string vals from the file and turn them into ints
                vals = line.rstrip().split(", ")
                solutionPositions.append([int(i) for i in vals] )

            line = fp.readline()
            cnt += 1
        print(solutionPositions)

    return difficulty

if __name__ == "__main__":
    print("Initializing Minesweeper Program")

    # count the arguments
    arguments = len(sys.argv) - 1

    # if no input arg passed in, look for windows exe for minesweeper
    if arguments == 0:
        result = (3,None)
        while (result[0] == 3):
            result = getPlayBox()
        difficulty = result[0]
        playBox = result[1]
        
        if (playBox != None):
            print('Detected Difficulty:',difficultyNames[difficulty])
            play(difficulty, playBox)

        input("Press enter to exit.\n")
    
    # if one argument is passed in, open file and parse it
    elif arguments == 1:
        difficulty = parse_file(sys.argv[1])
        # call file parse function here

    # output usage statement to tell user how to run program if incorrect args passed
    else:
        print("ERROR - wrong number of input arguments entered.")
        print("Usage 1 (no input arguments): python minesweeperPro.py")
        print("Usage 2 (1 input arguement): python minesweeperPro.py testFile.txt")