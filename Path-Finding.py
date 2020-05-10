
import pygame
import math
import heapq
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


pygame.init()
############# INTERACTIVE MAP MAKING #############
screen = pygame.display.set_mode((200,200), 0, 8)
BKG = (0, 0, 0)
screen.fill(BKG)  # white screen
draw_on = False
last_pos = (0, 0)
color = (255, 255, 255)
radius = 1

def roundline(srf, color, start, end, radius=1):
    dx = end[0]-start[0]
    dy = end[1]-start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int( start[0]+float(i)/distance*dx)
        y = int( start[1]+float(i)/distance*dy)
        pygame.draw.circle(srf, color, (x, y), radius)

try:
    while True:
        e = pygame.event.wait()
        if e.type == pygame.QUIT:
            raise StopIteration
        if e.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.circle(screen, color, e.pos, radius)
            draw_on = True
        if e.type == pygame.MOUSEBUTTONUP:
            draw_on = False
        if e.type == pygame.MOUSEMOTION:
            if draw_on:
                pygame.draw.circle(screen, color, e.pos, radius)
                roundline(screen, color, e.pos, last_pos,  radius)
            last_pos = e.pos
        pygame.display.flip()

except StopIteration:
    pass

mapArr = pygame.surfarray.pixels2d(screen) / 255
print(mapArr)
print(mapArr[0].size)

# START AND GOAL:
start = (0, 0)
goal = (0, 0)

# CUSTOMIZE START/GOAL
pos_arr = [start, goal]
color_arr = [(255,255,0), (255,0,0)]
i = 0
try:
    while True:
        while i < len(pos_arr):
            e = pygame.event.wait()
            if e.type == pygame.QUIT or i >= len(pos_arr):
                raise StopIteration
            if e.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                pos_arr[i] = (x, y)
                if mapArr[x][y] == 1.:
                    print("Invalid point chosen.")
                    pass
                else:
                    pygame.draw.circle(screen, color_arr[i], pos_arr[i], 2)
                    print("Valid point chosen.")
                    i += 1
                    if i >= len(pos_arr):
                        raise StopIteration
            if e.type == pygame.MOUSEMOTION:
                pass
            pygame.display.flip()

except StopIteration:
    pass
############################################

'''
# MAP OUTPUT
fig, ax = plt.subplots(figsize=(12,12))
ax.imshow(mapArr, cmap=plt.cm.tab20b)
ax.scatter(pos_arr[0][1], pos_arr[0][0], marker = "*", color = "yellow", s = 200)
ax.scatter(pos_arr[1][1], pos_arr[1][0], marker = "*", color = "red", s = 200)
plt.show()
'''


pygame.quit()

rows = len(mapArr)
print(rows)
columns = len(mapArr[0])
print(columns)

class Node:
    def __init__(self, x, y, map):
        self.x = x
        self.y = y
        self.Gcost = 0  # distance from starting Node
        self.Hcost = 0  # distance from end node
        self.Fcost = 0  # Fcost = Gcost + Hcost
        self.parentNode = None
        self.neighbour = []

        if map[x][y] == 1:
            self.wall = True
        else:
            self.wall = False

        self.open = False
        self.closed = False


    def addNeighbor(self, grid):
        x = self.x
        y = self.y

        if x < columns - 1 and self.wall == False: # if it is a wall do not include
            if y > 0:
                self.neighbour.append(grid[x + 1][y - 1])   #-----------------------------
            self.neighbour.append(grid[x + 1][y])           # adds neighbours to the right only if it is a node not along the right wall of the grid
            if y < rows - 1:
                self.neighbour.append(grid[x + 1][y + 1])   #-----------------------------
        if x > 0 and self.wall == False:
            if y > 0:
                self.neighbour.append(grid[x - 1][y - 1])   # -----------------------------
            self.neighbour.append(grid[x - 1][y])           # adds neighbours to the left only if it is a node not along the left wall of the grid
            if y < rows - 1:
                self.neighbour.append(grid[x - 1][y + 1])   # -----------------------------
        if y > 0 and self.wall == False:
            self.neighbour.append(grid[x][y - 1])           # adds neighbours directly above only if it is a node not along the top of the grid
        if y < rows - 1 and self.wall == False:
            self.neighbour.append(grid[x][y + 1])           # adds neighbours directly below only if it is a node not along the bottom of the grid

#GRAPH FUNCTIONS
#calculates Hcost
def calcDistance(currentNode, endNode):
    return math.sqrt(pow(currentNode.x - endNode.x, 2) + pow(currentNode.y - endNode.y, 2)) #Hcost of the current node

# ====================

# CREATE INT MAP ARRAY from FLOAT MAP ARRAY
drawn_map = [[0 for j in range(columns)] for k in range(rows)]

# convert each element in grid float -> int
for i in range(columns):
    for j in range(rows):
        drawn_map[i][j] = int(mapArr[i][j])

# creates 2d array which is going to be used for the graph
grid = [[None for x in range(rows)] for y in range(columns)]

# makes each element of the area equal to box
for i in range(len(grid[0])):
    for j in range(len(grid[0])):
        grid[i][j] = Node(i, j, drawn_map)

def reconstruct_path(cameFrom, current):
    total_path = {current}
    while current in cameFrom.Keys:
        current = cameFrom[current]
        total_path.prepend(current)
    return total_path

'''
# TEST CASE
path_map = np.array([   [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
'''

# adds the neighbours list to each node
for i in range(len(grid)):
    for j in range(len(grid[0])):
        grid[i][j].addNeighbor(grid)

start = grid[pos_arr[0][0]][pos_arr[0][1]] #start node
print(pos_arr[1][0])
print(pos_arr[1][1])
end = grid[pos_arr[1][0]][pos_arr[1][1]] #end node

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
    openList.pop(small)

    closedList.append(currentNode)
    currentNode.closed = True

    if currentNode == end:  #we found the path to the end node
        return True

    for i in range(len(currentNode.neighbour)):
        temp_gcost = currentNode.Gcost + calcDistance(currentNode, currentNode.neighbour[i])
        if currentNode.neighbour[i].wall == True or currentNode.neighbour[i].closed == True: #if neighbour is a wall or if it is in the closed list skip the node
            pass
        elif currentNode.neighbour[i].open == False or currentNode.neighbour[i].Gcost > temp_gcost:
            currentNode.neighbour[i].Hcost = calcDistance(currentNode.neighbour[i], end)
            currentNode.neighbour[i].Gcost = temp_gcost
            currentNode.neighbour[i].Fcost = currentNode.neighbour[i].Hcost + temp_gcost
            currentNode.neighbour[i].parentNode = currentNode

            if currentNode.neighbour[i] not in openList:
                openList.append(currentNode.neighbour[i])
                currentNode.neighbour[i].open = True

    return False


#adds start node to openList
openList.append(start)
start.open = True
#openListFcost.append(start.Fcost) heap of f cost
#heapq.heapify(openListFcost)

foundEnd = False

while foundEnd == False:
    foundEnd = AstarAlgorithm()

# backtracks the shortest path from end to start
temp = end
while temp != start:
    temp = temp.parentNode
    if temp != start:
        shortestPath.append(temp)
# reverses the list so the order of the list is start to end
shortestPath.reverse()

print(shortestPath)




