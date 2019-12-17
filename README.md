# Minesweeper AI
A program that plays minesweeper, by weighing the probability of mines being on certain tiles. 
Created as a CS 440 project.
If you are reading this outside of Github, here is a link to our repository: https://github.com/Chiiryuu/Minesweeper-AI

### Requirements
For this program to work properly, several things are needed:
* Minesweeper Game
   * Works on the Windows XP Minesweeper (Available here)
   * http://www.minesweeper.info/downloads/WinmineXP.html
   * This is also bundled in the repository for ease of use.
* Linux application 'Scrot'
   * For this application to run on linux, you need the application Scrot for interfacing with pyautogui
* Pyhon packagage 'pyautogui'
   * Handles taking screenshots and clicking through Python
* Pyhon packagage 'PIL'
   * Handles image manipulation and conversion
   
### Current State of the Program
In its current state, the program can solve Minesweeper either by detecting Minesweeper XP on the screen or by opening a data file. Optionally, the program can be asked to run a number a times in data mode to collect date on win rate and other statistics.

### How to use
To run the program (after all requirements are satisfied), open the Windows XP Minesweeper application and run the python file 'minesweepPro.py' in a terminal that does not cover up the game. The program will automatically play the game. To cancel in mid-game, move the mouse to the Top-Left of the screen.

Optionally, run with the flag '-win' to repeat play until a win is achieved. Use this wisely, as it can be difficult to kill the program while it is playing.

The flag '-data' will send the program into data collection mode, where the program will run the currently selected difficulty in the Minesweeper XP application 100 times on each of the 4 guessing algorithms, collecting and exporting data to CSV files in the data folder. Some example data has been included in the repository.

If a file name is sent to the program, it will attempt to solve such a file. This can be used to find bugs in the application and visually see how randomness works in the program, based on its win rate with the exact same input file.

### AI Implementation
Minesweeper, despite being perfectly solvable in some instances, is a random game and therefore cannot be beaten every time it is played. This is due to ambiguity in the data given to the user. Because of this, the AI was implemented as follows:
* As new data comes with every click, this application is an online search.
* The image of the board is converted into a traditional state array.
* AC-3 is run repeatedly in order to find all unambiguous assignments.
* If AC-3 cannot get any closer to problem, all unknown spaces are weighted with a probability heuristic.
* A space with the lowest probability to be a bomb is chosen randomly from all spaces with the same probability.
* This repeats until either the game is solved or a mine is found.

### Control Flow of Program
* 1.) Locate game on screen
* 2.) Dicsern selected difficulty
* 3.) Begin game by clicking middle tile
  * Any tile with 8 neighbors is optimal.
* 4.) Convert board on screen into a state in memory
* 5.) Locate all definite bombs and unexplored safe squares
  * If > 0, click all relevant squares and return to 4.)
  * Otherwise, click a square that is least likely to be a bomb then return to 4.)
* 6.) Terminate after finding all bombs or losing
