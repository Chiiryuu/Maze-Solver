import time
import helperFunctions as funcs

difficultyNames = ['Easy','Medium','Hard']
difficulty = -1
                    #Width, height
difficultySizes = [(9,9),(16,16),(30,16)]
difficultyBoxSizes = [16,16,16]
difficultyBombs = [10,40,99]
boxPositions = []
solutionPositions = []

#State naming convention:  -2: Bomb, -1: unexplored, 0: empty, 1: 1, 2:2... etc
    
def displayPlayBox(board):
    """ This function is used to convert a board into a string representing the 
        current state of the board. Board is a list of lists that is accessed
        by col,row. Common use is in the checkSolved function to get the playBox
        and solutionPositions as a string to compare to eachother.
    """
    colSize = len(board)
    rowSize = len(board[0])
    rowStrings = ['']*colSize

    # go through rows and cols
    for i in range(rowSize):
        for j in range(colSize):
            # add value in playBox to rowstrings
            rowStrings[j] += str(board[i][j]) + ' '
    result = ''

    # concatanate all of the row strings with a newline
    for string in rowStrings:
        result += string + '\n'

    # replace number representations with easier to read characters 
    result = result.replace('-1','X').replace('-2','B').replace('0',' ').replace('9','?')

    return result

def parse_file(file_name):
    """ This function is used to parse an input file. It detects the difficulty based off 
        of the first line in the file, and then the solved minesweeper board is the 2nd
        line until the end and they are comma separated ints. The program accesses data
        by col,row so the solutionPositions is set up that way to avoid inconsistency. 
    """
    # open the file
    with open(file_name) as fp:
        # get the line and set our counters to their respective starting values
        line = fp.readline()
        cnt = 1
        rowCount = 0

        # go through all lines
        while line:
            # if we are on the first line, we need to find out difficulty level
            if cnt == 1: 
                if line.strip() == "EASY":
                    difficulty = 0
                elif line.strip() == "MEDIUM":
                    difficulty = 1
                elif line.strip() == "HARD":
                    difficulty = 2
                else:
                    print("Difficulty in test file not recognized")
                # create empty solution positions based on difficulty sizes
                solutionPositions = [[None for i in range(difficultySizes[difficulty][0])] for j in range(difficultySizes[difficulty][1])]
            else:
                # get the string vals from the file and turn them into ints
                vals = line.rstrip().split(", ")
                
                for i in range(0,len(vals)):
                    valInt = int(vals[i])
                    
                    # put value into solution positions as (col,row)
                    solutionPositions[i][rowCount-1] = valInt

            #increment line and other counters
            line = fp.readline()
            cnt += 1
            rowCount += 1

    return difficulty, solutionPositions

def get_empty_play_box(difficulty):
    """ This function is used to create an empty play box with the appropriate
        size for the difficulty. Difficulty is passed into the function and it
        is an integer representing the difficulty. 
    """
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

def revealZeros(col, row, difficulty, playBox, solutionPositions):
    """ This function is used to for when a empty box in minesweeper is "clicked".
        With the file input method, this doesn't happen automatically like it
        does with using the executable. There are 3 base cases for the recursion
        and if a zero is found, it recurses on all 8 neighbors as well. col and row 
        are passed in and are the col,row value to index into the playBox and 
        solutionPositions boards which are also passed in. Difficulty is passed in
        as an integer.
    """
    # If out of bounds - return
    if col < 0 or col > difficultySizes[difficulty][0]-1 or row < 0 or row > difficultySizes[difficulty][1]-1:
        return

    # if spot in playBox is already "revealed", return
    if playBox[col][row] != -1:
        return

    # if value in solutionPositions is not 0, return
    if solutionPositions[col][row] != 0:
        return

    # if we have not returned, we have valid bounds and an empty space so assign it to playBox
    playBox[col][row] = 0

    # recurse on all possible neighbors (8 options)
    revealZeros(col, row-1, difficulty, playBox, solutionPositions)
    revealZeros(col+1, row-1, difficulty, playBox, solutionPositions)
    revealZeros(col+1, row, difficulty, playBox, solutionPositions)
    revealZeros(col+1, row+1, difficulty, playBox, solutionPositions)
    revealZeros(col, row+1, difficulty, playBox, solutionPositions)
    revealZeros(col-1, row+1, difficulty, playBox, solutionPositions)
    revealZeros(col-1, row, difficulty, playBox, solutionPositions)
    revealZeros(col-1, row-1, difficulty, playBox, solutionPositions)

def getStateFromBoard(playBox):
    """ This function needed to be a little different than the similar method
        for using the minesweeper windows executable. It gets the state values
        from the playBox rather than grabbing an image of the board and getting
        the values from the pixels there. State is a 2d array of state tuples.
        It is accessed by state[col][row] and value there will be a tuple that
        looks like (value, num bombs touching, list of neighbors)
    """
    stateVal = []

    # go through all (col,row) positions
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
                bombs = 0
                neighbors = funcs.getNeighbors(i, j, width, height)
                newState = (val, bombs, neighbors)
                stateRow.append(newState)
            state.append(stateRow)
            
    funcs.writeNeighbors(state)
        
    return state

def checkSolved(playBox, solutionPositions):
    """ This function is used to check if the playBox and solutionPosition boards
        are equal. If they are equal, return 1 to show that we have won the game.
        If they are not, function returns 0 to show that we are still alive (losing
        the game is handled in the play function).
    """
    # we won!
    if displayPlayBox(playBox) == displayPlayBox(solutionPositions):
        return 1
    # we are alive!
    else:
        return 0

def firstClick(playBox, solutionPositions, happyLevel, numBoxes, difficulty):
    """ This function is for handling the first click we make for the board.
        It finds the middle col,row for the board, and attempts to set that
        position. If it is a mine to begin with, we attempt to try to find 
        another position that is not a mine to start with. If for some reason
        we can't find a starting position (shouldn't happen), set happyLevel
        to -1 to represent that we lost.
    """
    # get position in middle of the board for first click
    middlePositionCol = numBoxes[0]//2
    middlePositionRow = numBoxes[1]//2

    # if "click" is on a empty square, call reveal zeros to reveal all empty squares connecting it
    if solutionPositions[middlePositionCol][middlePositionRow] == 0:
        revealZeros(middlePositionCol, middlePositionRow, difficulty, playBox, solutionPositions)

    # if middle position is a bomb, don't let us click and lose on first try (switch to click to position next to it)
    elif solutionPositions[middlePositionCol][middlePositionRow] == -2:
        breakCond = False
        while(solutionPositions[middlePositionCol][middlePositionRow] == -2 and breakCond == False):
            middlePositionCol += 1
            middlePositionRow += 1
            if middlePositionCol > difficultySizes[difficulty][0]-1 or middlePositionRow > difficultySizes[difficulty][1]-1:
                breakCond = True
        playBox[middlePositionCol][middlePositionRow] = solutionPositions[middlePositionCol][middlePositionRow]

    # if we couldn't try to click another bomb to begin with, set happyLevel to -1 (we lost)
    else:
        playBox[middlePositionCol][middlePositionRow] = solutionPositions[middlePositionCol][middlePositionRow]
        if playBox[middlePositionCol][middlePositionRow] == -2:
            happyLevel = -1

def play(difficulty, playBox, solutionPositions):
    """ This function is used to play and solve minesweeper with file input. It first 
        finds the middle position in the board and checks if it is a bomb in the solution.
        If it is a bomb, it will loop until it finds one that is not so that we don't lose 
        right away. If not a bomb, it assigns the value to playBox. Everytime a value is 
        assigned to playbox, we call revealZeros if it was a zero. It then loops until 
        a terminating condition is met, and calls various methods to find bombs, safe 
        locations and guesses to keep playing the game.
    """
    # set initial starting values 
    boxPositions.clear()
    startTime = time.time()
    guesses = 0
    happyLevel = 0
    
    # get the number of boxes based on the difficulty level of the minesweeper
    numBoxes = difficultySizes[difficulty]

    # set up box positions
    for i in range(numBoxes[0]):
        col = []
        for j in range(numBoxes[1]):
            col.append((i,j))
        boxPositions.append(col)
    
    # call function to handle first "click"
    firstClick(playBox, solutionPositions, happyLevel, numBoxes, difficulty)

    # get the current state from playBox
    state = getStateFromBoard(playBox)
        
    # set inital loop condition values
    changed = True   
    count = 0 
    numBombs = difficultyBombs[difficulty]

    while (changed == True and happyLevel != -1 and numBombs > 0):
        changed = False

        # find bombs and safe locations
        bombs = funcs.findBombs(state)
        safes = funcs.findSafes(state)

        # loop through bomb locations
        for bomb in bombs:
            # one less bomb that is unknown
            numBombs = numBombs - 1

            # get the actual location (col,row) of the bomb
            bombPos = funcs.indexToColRow(bomb, len(state[0])) 
            bombLocation = boxPositions[bombPos[0]][bombPos[1]]
        
            # flag as bomb: set position to -2 but since we know it is a bomb we don't lose
            playBox[bombLocation[0]][bombLocation[1]] = -2
            
            # if there are no more unknown bombs
            if (numBombs == 0):
                print("All bombs successfully flagged!")

                # call getUnknowns to get next safe moves
                safes = funcs.getUnknowns(state)
                # if there are no more, we have won
                if safes == []:
                        changed = True
        
        # go through safe locations 
        for safe in safes:
            changed = True
            safePos = funcs.indexToColRow(safe, len(state[0]) ) 
            safeLocation = boxPositions[safePos[0]][safePos[1]]
            
            # if the safe location is a 0, call reveal zeros
            if solutionPositions[safeLocation[0]][safeLocation[1]] == 0:
                revealZeros(safeLocation[0], safeLocation[1], difficulty, playBox, solutionPositions)
            # otherwise just set the playBox to have the new position (double check in case we clicked a bomb and lost)
            else:
                playBox[safeLocation[0]][safeLocation[1]] = solutionPositions[safeLocation[0]][safeLocation[1]]

                # clicked a bomb, lost 
                if playBox[safeLocation[0]][safeLocation[1]] == -2:
                    happyLevel = -1

        # if we have made changes
        if (changed == True):
            # make sure we haven't lost, and if we haven't check if we have won
            if happyLevel != -1:
                happyLevel = checkSolved(playBox, solutionPositions)

            # if we have won, change changed to be false so we exit loop
            if (happyLevel == 1):
                changed = False
            # otherwise we are still alive so get the new state from playBox
            else:
                state = getStateFromBoard(playBox)

        # if we haven't made changes, we need guesses
        else:
            if (guesses == 0):
                print("Guesses are required for this board.")
            guesses += 1

            # call the chooseBestGuess function
            guess = funcs.chooseBestGuessV2(state, numBombs)
            choice = guess[0]
            ratio = guess[1]

            # get the guess location
            choicePos = funcs.indexToColRow(choice, len(state[0]) ) 
            choiceLocation = boxPositions[choicePos[0]][choicePos[1]]

            # if we reveal a zero, call the reveal zeros function and set changed to be true
            if solutionPositions[choiceLocation[0]][choiceLocation[1]] == 0:
                revealZeros(choiceLocation[0], choiceLocation[1], difficulty, playBox, solutionPositions)
                changed = True
            # otherwise assign the value
            else:
                playBox[choiceLocation[0]][choiceLocation[1]] = solutionPositions[choiceLocation[0]][choiceLocation[1]]

                # check if we clicked a bomb and lost - if so, assign happy level to -1
                if playBox[choiceLocation[0]][choiceLocation[1]] == -2:
                    happyLevel = -1
                # if we didn't lose, check if it is solved
                else:
                    happyLevel = checkSolved(playBox, solutionPositions)
                    if (happyLevel == 0):
                        changed = True
                    if (happyLevel == -1):
                        break
            state = getStateFromBoard(playBox)

    # display final state
    funcs.displayState(state)

    # print out if we lost or won 
    if (happyLevel == -1):
        print("I lost... \nTotal number of guesses made: ",guesses,'\nRuntime: ',(time.time() - startTime)," seconds.\n")
        return -1
    elif happyLevel == 1:
        print("I won! :D\nTotal number of guesses made: ",guesses,"\nTime to complete: ",(time.time() - startTime)," seconds.\n")
        return 0
