
import pygame
pygame.init()


class box:
    def __init__(self):

rows, columns = (25, 25) # sets the size of the grid

# creates 2d array which is going to be used for the grid
grid = [[0 for i in range(columns)] for j in range(rows)]

# makes each element of the area equal to box
for i in range(columns):
    for j in range(rows):
        grid[i][j] = box