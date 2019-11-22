import pyautogui
import time
from PIL import Image, ImageGrab

#Close program if you go to (0,0)
#  https://pyautogui.readthedocs.io/en/latest/cheatsheet.html
#image = cv2.cvtColor(np.array(pyautogui.screenshot(region=(0, 0, 1300, 750))), cv2.COLOR_BGR2GRAY)


pyautogui.FAILSAFE = True
difficultyNames = ['Easy','Medium','Hard']
difficultyPics = ['easy.png', 'medium.png', 'hard.png']
difficulty = -1
difficultySizes = [(10,8),(18,14),(24,20)]
difficultyBoxSizes = [45,30,25]
difficultyBombs = [10,40,99]
boxPositions = []
uiHeight=60

#State naming convention: -2: Bomb, -1: unexplored, 0: empty, 1: 1, 2:2... etc

animationDelay=0.85

def click(x,y,origin, delay=0):
    try:
        if (delay > 0):
            pyautogui.moveTo(x, y, duration=delay)
        pyautogui.click(x,y) #button='right'
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

if __name__ == "__main__":
    print("Initializing Minesweeper Program")
    result = getPlayBox()
    difficulty = result[0]
    playBox = result[1]
    if (playBox != None):
        print('Detected Difficulty:',difficultyNames[difficulty])
        play(difficulty, playBox)
    
    #center = (playBox.left + (playBox.width // 2), playBox.top + (playBox.height // 2) )
    #click(center[0], center[1])
   


#screenshot = pyautogui.screenshot()
