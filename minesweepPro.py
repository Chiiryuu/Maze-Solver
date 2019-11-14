import pyautogui

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

def click(x,y, delay=0):
    try:
        if (delay > 0):
            pyautogui.moveTo(x, y, duration=delay)
        pyautogui.click(x,y)
    except:
        print('Triggered Failsafe')

def getPlayBox():
    for i in range(len(difficultyPics)):
        print('Searching for',difficultyNames[i])
        playBox = pyautogui.locateOnScreen(difficultyPics[i])
        print(playBox)
        if (playBox != None):
            return (i,playBox)
    print("ERROR: Could not find playing field!")
    return (3,None)

def play(difficulty, playBox):
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
    print(boxPositions)
    for row in boxPositions:
        for pos in row:
            click(pos[0],pos[1],0.2)

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

