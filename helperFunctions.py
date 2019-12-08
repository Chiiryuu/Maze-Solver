import pyautogui
import time
import random
import sys
from PIL import Image, ImageGrab
import fileInput as fileHelper

def colRowToIndex(col, row, height):
    if (col < 0 or row < 0 or row >= height):
        return -1
    return col*height + row
    
def indexToColRow(index, height):
    col = index // height
    row = index % height
    return (col, row)
    
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
    print("neighbors: ", neighbors)
    return neighbors
    
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
        
    result = result.replace('-1','X').replace('-2','B').replace('0',' ').replace('9','?').replace('-3', 'F')
    print(result)
    return result

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
   # print(guessList)
    #This is done because completely unknown squares are assigned a strange weight
    return random.choice(guessList)

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
    return
    
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
    state = writeNeighbors(state)
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
    state = writeNeighbors(state)
    return safes