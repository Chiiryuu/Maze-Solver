# Minesweeper AI
A program that plays minesweeper, by weighing the probability of mines being on certain tiles. 
Created as a CS 440 project using https://github.com/aimacode/aima-python

### Things we have to do to start
* Plan exactly what our goal is
* Decide on search method (or plan support multiple types of searches)
* Write up project proposal
* Make program click on a position on the board
* Convert image of a game to state after each click
  * To save time, only look at unopened positions next to opened ones (ones that have numbers by them)
* Calculate spot with the lowest probability to be a mine
