# Minesweeper AI
A program that plays minesweeper, by weighing the probability of mines being on certain tiles. 
Created as a CS 440 project using https://github.com/aimacode/aima-python

### Requirements
For this program to work properly, several things are needed:
* Minesweeper Game
   * Works on the Windows XP Minesweeper (Available here)
   * http://www.minesweeper.info/downloads/WinmineXP.html
* Linux application 'Scrot'
   * For this application to run on linux, you need the application Scrot for interfacing with pyautogui
* Pyhon packagage 'pyautogui'
   * Handles taking screenshots and clicking through Python
   
### Current State of the Program
In its current state, the program will locate the minesweeper application on screen and simply click each space in the game, column by column.

### How to use
Before running the program, take the 3 images out of the folder corresponding to your operating system and place them in the same directory is 'minesweeperPro.py'. This must be done because Google chose to use different color palettes on different operating systems.

To run the program (after all requirements are satisfied), open the Google minesweeper application and run the python file 'minesweepPro.py' in a terminal that does not cover up the game. The program will automatically play the game. To cancel in mid-game, move the mouse to the Top-Left of the screen.

### Things we have to do to start
* Plan exactly what our goal is
* Decide on search method (or plan support multiple types of searches)
* Write up project proposal
* Start working with beginner difficulty
* Make program click on a position on the board
* Convert image of a game to state after each click
  * To save time, only look at unopened positions next to opened ones (ones that have numbers by them)
* Calculate spot with the lowest probability to be a mine
* Later support harder difficulties (if we have time)
