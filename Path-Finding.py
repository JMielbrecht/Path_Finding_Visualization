
import pygame
import math
import heapq
pygame.init()


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



#FUNCTONS

#calculates Hcost
def calcDistance(currentNode, endNode):
    return math.sqrt(pow(currentNode.x - endNode.x, 2) + pow(currentNode.y - endNode.y, 2)) #Hcost of the current node


# sets the size of the grid
rows = 25
columns = 25

# creates 2d array which is going to be used for the grid
grid = [[0 for i in range(columns)] for j in range(rows)]

# makes each element of the area equal to box
for i in range(columns):
    for j in range(rows):
        grid[i][j] = Node(i, j)

# adds the neighbours list to each node
for i in range(columns):
    for j in range(rows):
        grid[i][j].addNeighbor(grid)

start = grid[0][0] #start node
end = grid[20][20] #end node

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



