# Minesweeper AI
A program that plays minesweeper, by weighing the probability of mines being on certain tiles. 
Created as a CS 440 project using https://github.com/aimacode/aima-python

### Requirements
For this program to work properly, several things are needed:
* Minesweeper Game
   * Works on Google's Minesweeper (Simply search google for 'minesweeper' and click play)
* Linux application 'Scrot'
   * For this application to run on linux, you need the application Scrot for interfacing with pyautogui
* Pyhon packagage 'pyautogui'
   * Handles taking screenshots and clicking through Python
   
### Current State of the Program
In its current state, the program will locate the minesweeper application on screen and simply click each space in the game, column by column.

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
