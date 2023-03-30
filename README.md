# Stone Automata Maze Challenge
https://sigmageek.com/solution/stone-automata-maze-challenge

## Challenge
Walk through an automaton whose matrix has 65 rows and 85 columns defined by
the rules presented on the site

## Algorithm
The selected algorithm to implement the solution was the A*, creating nodes that are neighbors to the current node being evaluated.
For the G Cost of the algorithm it was used the time frame divide by a constant value. A constant value of 1 will make the algorithm take longer to determine the shortest path, and with values bigger than 1, could find the result faster, but could not be the shortest path.  
The H Cost used the Euclidean distance from the node to the target node, and the F Cost is the sum of G cost and H Cost  

references to the algorithm:  
* https://plainenglish.io/blog/a-algorithm-in-python
* https://www.youtube.com/watch?v=-L-WgKMFuhE&list=PLFt_AvWsXl0cq5Umv3pMC9SPnKjfp9eGW&index=1

## Solution
The solution is formatted using the specifications:  
Each movement must be separated by a blank space. Each letter represents a move of the particle, and consequently an update of the board.

* **U** - movement up
* **D** - movement down
* **R** - movement to the right
* **L** - movement to the left

and is saved in a file named Solution_*Date*_*Hour*.txt

## Presentation
After the solution is calculated, the user can step using **'Space'** for generating the nexts steps for the automaton and the solution particle. The **'A'** when hold performs a continous move for the particle.