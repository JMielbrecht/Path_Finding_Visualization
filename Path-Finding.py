
import pygame
pygame.init()


class Node:
    def __init__(self):
        self.Gcost = 0  # distance from starting Node
        self.Hcost = 0  # distance from end node
        self.Fcost = 0  # Fcost = Gcost + Hcost
        self.parentNode = None
        self.neighbour = []
        self.open = False
        self.closed = False

rows, columns = (25, 25) # sets the size of the grid

# creates 2d array which is going to be used for the grid
grid = [[0 for i in range(columns)] for j in range(rows)]

# makes each element of the area equal to box
for i in range(columns):
    for j in range(rows):
        grid[i][j] = Node