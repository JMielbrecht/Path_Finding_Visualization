import math

import pygame
from pygame.locals import *

pygame.init()

boardSize = (500, 500)

screen = pygame.display.set_mode(boardSize)
clock = pygame.time.Clock()


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.Gcost = 0  # distance from starting Node
        self.Hcost = 0  # distance from end node
        self.Fcost = 0  # Fcost = Gcost + Hcost
        self.parentNode = None
        self.neighbour = []
        self.open = False
        self.closed = False
        self.wall = False

    def addNeighbor(self, grid):
        x = self.x
        y = self.y

        if x < columns - 1 and self.wall == False: # if it is a wall do not include
            if y > 0:
                if grid[x + 1][y].wall == False and grid[x][y - 1].wall == False: #-----------------------------
                    self.neighbour.append(grid[x + 1][y - 1])
            self.neighbour.append(grid[x + 1][y])                               # adds neighbours to the right only if it is a node not along the right wall of the grid
            if y < rows - 1:
                if grid[x + 1][y].wall == False and grid[x][y + 1].wall == False:
                    self.neighbour.append(grid[x + 1][y + 1])                   #-----------------------------
        if x > 0 and self.wall == False:
            if y > 0:
                if grid[x - 1][y].wall == False and grid[x][y - 1].wall == False:
                    self.neighbour.append(grid[x - 1][y - 1])   # -----------------------------
            self.neighbour.append(grid[x - 1][y])               # adds neighbours to the left only if it is a node not along the left wall of the grid
            if y < rows - 1:
                if grid[x - 1][y].wall == False and grid[x][y - 1].wall == False:
                    self.neighbour.append(grid[x - 1][y + 1])   # -----------------------------
        if y > 0 and self.wall == False:
            self.neighbour.append(grid[x][y - 1])           # adds neighbours directly above only if it is a node not along the top of the grid
        if y < rows - 1 and self.wall == False:
            self.neighbour.append(grid[x][y + 1])           # adds neighbours directly below only if it is a node not along the bottom of the grid



#FUNCTONS

#calculates Hcost
def calcDistance(currentNode, endNode):
    return math.sqrt(pow(currentNode.x - endNode.x, 2) + pow(currentNode.y - endNode.y, 2)) #Hcost of the current node


# sets the size of the grid
rows = 50
columns = 50

#for pygame and display
width = boardSize[0]/columns
height = boardSize[1]/rows
darkGreen = (12, 64, 0)
red = (100, 0, 0)
lightRed = (220, 0, 0)
green = (0, 255, 0)
blue = (0, 50, 255)
grey = (215, 215, 215)
white = (255, 255, 255)
black = (0, 0, 0)


# creates 2d array which is going to be used for the grid
grid = [[0 for i in range(columns)] for j in range(rows)]

# makes each element of the area equal to box
for i in range(columns):
    for j in range(rows):
        grid[i][j] = Node(i, j)




start = None #start node
end = None #end node

screen.fill(white)
for y in range(columns):
    for x in range(rows):
        # rect = pygame.Rect(x * (height + 1), y * (width + 1), height, width)
        pygame.draw.rect(screen, grey, [(width) * x, (height) * y, width, height], 1)
        pygame.display.update()
running = True
while running:

    for event in pygame.event.get():

        if pygame.mouse.get_pressed()[0]:
            position = pygame.mouse.get_pos()
            p1 = position[0] // (boardSize[0] // columns)
            p2 = position[1] // (boardSize[1] // rows)
            box = grid[p1][p2]
            if box != start and box != end and box.wall == False:
                box.wall = True
                pygame.draw.rect(screen, black, (p1 * width, p2 * height, width, height), 0)
        elif pygame.mouse.get_pressed()[2]:
            position = pygame.mouse.get_pos()
            p1 = position[0] // (boardSize[0] // columns)
            p2 = position[1] // (boardSize[1] // rows)
            box = grid[p1][p2]
            if box != start and box != end and box.wall == False:
                if start == None:
                    start = box
                    pygame.draw.rect(screen, darkGreen, (p1 * width, p2 * height, width, height), 0)
                elif end == None:
                    end = box
                    pygame.draw.rect(screen, red, (p1 * width, p2 * height, width, height), 0)

        elif event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
            if event.key == K_RETURN:
                running = False
        pygame.display.update()
    pygame.display.update()


# adds the neighbours list to each node
for i in range(columns):
    for j in range(rows):
        grid[i][j].addNeighbor(grid)


openList = []
openListFcost = [] #for heap might implement
closedList = []
wallList = []
shortestPath = []
pathLength = 0


def AstarAlgorithm():
    #currentNode becomes lowest Fcost Node from OpenList

    small = 0
    for i in range((len(openList))):
        if openList[i].Fcost < openList[small].Fcost:
            small = i
    currentNode = openList[small]
    currentNode.open = False
    #pygame.draw.rect(screen, green, (currentNode.x * width, currentNode.y * height, width, height), 0)
    openList.pop(small)

    closedList.append(currentNode)
    currentNode.closed = True
    if not (currentNode == start or currentNode == end):
        pygame.draw.rect(screen, lightRed, (currentNode.x * width, currentNode.y * height, width, height), 0)
        pygame.display.update()

    if currentNode == end:  #we found the path to the end node
        return True

    for i in range(len(currentNode.neighbour)):
        temp_gcost = currentNode.Gcost + calcDistance(currentNode, currentNode.neighbour[i])
        if currentNode.neighbour[i].wall == True or currentNode.neighbour[i].closed == True or currentNode.neighbour[i] == start: #if neighbour is a wall or if it is in the closed list skip the node
            pass
        elif currentNode.neighbour[i].open == False or currentNode.neighbour[i].Gcost > temp_gcost:
            currentNode.neighbour[i].Hcost = calcDistance(currentNode.neighbour[i], end)
            currentNode.neighbour[i].Gcost = temp_gcost
            currentNode.neighbour[i].Fcost = currentNode.neighbour[i].Hcost + temp_gcost
            currentNode.neighbour[i].parentNode = currentNode

            if currentNode.neighbour[i] not in openList:
                openList.append(currentNode.neighbour[i])
                currentNode.neighbour[i].open = True
                if not currentNode.neighbour[i] == end:
                    pygame.draw.rect(screen, green, (currentNode.neighbour[i].x * width, currentNode.neighbour[i].y * height, width, height), 0)
                    pygame.display.update()

    return False


#adds start node to openList
openList.append(start)
start.open = True
#openListFcost.append(start.Fcost) heap of f cost
#heapq.heapify(openListFcost)

foundEnd = False

while foundEnd == False:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        pygame.quit()
    foundEnd = AstarAlgorithm()
    pygame.display.update()
    #clock.tick(10)



# backtracks the shortest path from end to start
temp = end
while temp != start:
    temp = temp.parentNode
    if temp != start:
        shortestPath.append(temp)
# reverses the list so the order of the list is start to end
shortestPath.reverse()

count = 0
display = True

while display == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            display = False
    pygame.draw.rect(screen, blue, (shortestPath[count].x * width, shortestPath[count].y * height, width, height), 0)
    pygame.display.update()
    #clock.tick(30)
    if count < len(shortestPath) - 1:
        count += 1
print(shortestPath)