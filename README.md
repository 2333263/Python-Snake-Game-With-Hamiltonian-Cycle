# Python-Snake-Game-with-A-Star
The game snake made in python, it also includes an A* algorithm so if you dont want to play it you can have the game play itself


Made using pygame and numpy.
I do plan on adding a better AI that plays snake but the A* (that doesnt actually work too great right now) is good enough

I do want to just quickly talk about how the game actually functions.

The game runs on a grid system of 80x80 nodes, each node represents a 10x10 pixel square on the screen itself.
The snake itself is is made up of a linked list of body parts, each part keeps track of which part is in front of it in the snake itself.
In each iteration of the game, each part of the snake moves into the node position of its parent body part, only the head moves indepenedently of the rest of the snake, this way when the snake turns it creates an L shape instead of moving all the body parts in the new direction.
