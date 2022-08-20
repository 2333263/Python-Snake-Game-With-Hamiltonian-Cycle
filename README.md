# Python-Snake-Game-with-A-Star
The game snake made in python, It also includes a Hamiltonian path that can be generated and followed by the snake


Made using pygame and numpy.

I do want to just quickly talk about how the game actually functions.

The game runs on a grid system of 40x40 nodes, each node represents a 20x20 pixel square on the screen itself.
The snake itself is is made up of a linked list of body parts, each part keeps track of which part is in front of it in the snake itself.
In each iteration of the game, each part of the snake moves into the node position of its parent body part, only the head moves indepenedently of the rest of the snake, this way when the snake turns it creates an L shape instead of moving all the body parts in the new direction.

How does the AI work:
At the beginning of the game, a Hamiltonian path is generated which the snake follows. This is done by doing the following:
  At each node, a list of all possible moves are creates (namely, up, down, left, right)
  An a modified A* search (modified so that it finds the longest path back to the original node instead of the shortest) is run from each of these possible positions to find which one will lead the snake down the furthest route but still return to its original node.
  The node that has the longest route is added to the path and the program moves onto the next node, using the new node as the new base node.
