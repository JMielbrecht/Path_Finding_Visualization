import math
import sys
import pygame
from pygame.locals import *

pygame.init()

boardSize = (500, 500)
# SCREEN
screen = pygame.display.set_mode(boardSize)
clock = pygame.time.Clock()

''' GUI FUNCTIONALITY '''

# Booleans to keep track of "mode"
walls_btn_pressed = False
start_btn_pressed = False
end_btn_pressed = False
clear_btn_pressed = False

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.Gcost = 0  # distance from starting Node
        self.Hcost = 0  # distance from end node
        self.Fcost = 0  # Fcost = Gcost + Hcost
        self.parentNode = None  # Points to previous node in path
        self.neighbour = []  # Array of self's neighboring nodes
        self.open = False
        self.closed = False
        self.wall = False

    def addNeighbor(self, grid):
        x = self.x
        y = self.y

        if x < COLS - 1 and self.wall == False: # if it is a wall do not include
            if y > 0:
                if grid[x + 1][y].wall == False and grid[x][y - 1].wall == False: #-----------------------------
                    self.neighbour.append(grid[x + 1][y - 1])
            self.neighbour.append(grid[x + 1][y])                               # adds neighbours to the right only if it is a node not along the right wall of the grid
            if y < ROWS - 1:
                if grid[x + 1][y].wall == False and grid[x][y + 1].wall == False:
                    self.neighbour.append(grid[x + 1][y + 1])                   #-----------------------------
        if x > 0 and self.wall == False:
            if y > 0:
                if grid[x - 1][y].wall == False and grid[x][y - 1].wall == False:
                    self.neighbour.append(grid[x - 1][y - 1])   # -----------------------------
            self.neighbour.append(grid[x - 1][y])               # adds neighbours to the left only if it is a node not along the left wall of the grid
            if y < ROWS - 1:
                if grid[x - 1][y].wall == False and grid[x][y - 1].wall == False:
                    self.neighbour.append(grid[x - 1][y + 1])   # -----------------------------
        if y > 0 and self.wall == False:
            self.neighbour.append(grid[x][y - 1])           # adds neighbours directly above only if it is a node not along the top of the grid
        if y < ROWS - 1 and self.wall == False:
            self.neighbour.append(grid[x][y + 1])           # adds neighbours directly below only if it is a node not along the bottom of the grid

    def clear_node(self): #Resets node to default vals
        self.x = -1
        self.y = -1
        self.Gcost = 0
        self.Hcost = 0
        self.parentNode = None
        self.neighbour = []
        self.open = False
        self.closed = False
        self.wall = False


''' GLOBAL VARS '''

# sets the size of the grid
ROWS = 50
COLS = 50

#for pygame and display
WIDTH = boardSize[0]/COLS
HEIGHT = boardSize[1]/ROWS
DARK_GREEN = (12, 64, 0)
RED = (100, 0, 0)
LIGHT_RED = (220, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 50, 255)
GREY = (215, 215, 215)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Color palette for buttons in GUI
WALL_DRAWN = (0, 0, 0)
START_BTN = (0, 200, 0)
END_BTN = (230, 0, 0)
CLR_BTN = (255, 51, 0)

# Keeps track of current start and end points
curr_start = None
curr_end = None


'''FUNCTONS'''


#calculates Hcost
def calcDistance(currentNode, endNode):
    return math.sqrt(pow(currentNode.x - endNode.x, 2) + pow(currentNode.y - endNode.y, 2)) #Hcost of the current node

# Resets the program
def clear_screen():
    global start
    global end
    global running
    global grid

    # Resetting variables
    start = None
    end = None
    running = True

    # Reset GUI to default
    screen.fill(WHITE)
    for y in range(COLS):
        for x in range(ROWS):
            # rect = pygame.Rect(x * (height + 1), y * (width + 1), height, width)
            pygame.draw.rect(
                screen, GREY, [int(WIDTH * x), int(HEIGHT * y), int(WIDTH), int(HEIGHT)], 1)
            pygame.display.update()
            grid[x][y].clear_node()  # Reset each node to default

    # Toolbar background
    pygame.draw.rect(screen, GREY, (0, 0, boardSize[0], 40))


# Creates user-specified button
def make_button(surface, color, coords, text, font_size=11):
    pygame.draw.rect(surface, color, coords)
    btn_text = pygame.font.Font("freesansbold.ttf", font_size)
    text_surface, text_rect = text_objects(text, btn_text)
    text_rect.center = ((coords[0] + (coords[2]/2)),
                       (coords[1] + (coords[3]/2)))
    screen.blit(text_surface, text_rect)


# HELPER FUNCTION FOR makeButton()
def text_objects(text, font, font_color=BLACK):  
    text_surface = font.render(text, True, font_color)
    return text_surface, text_surface.get_rect()

# Highlights buttons, checks functionality
def check_buttons():

    mouse = pygame.mouse.get_pos()
    draw_walls_highlighted = (250, 250, 250)
    start_point_highlighted = (0, 255, 0)
    end_point_highlighted = (255, 0, 0)
    clear_btn = (255, 51, 0)
    clear_btn_highlighted = (255, 77, 33)

    # Referencing global button-activation vars locally
    global walls_btn_pressed
    global start_btn_pressed
    global end_btn_pressed
    global clear_btn_pressed

    # Check 'DRAW WALLS' button
    if 5+90 > mouse[0] > 5 and 5+30 > mouse[1] > 5:
        make_button(screen, draw_walls_highlighted, (5, 5, 90, 30), "DRAW WALLS")
    elif walls_btn_pressed:
        make_button(screen, draw_walls_highlighted, (5, 5, 90, 30), "DRAW WALLS")
    else:
        make_button(screen, WHITE, (5, 5, 90, 30), "DRAW WALLS")

    # Check 'START POINT' button
    if 110+80 > mouse[0] > 110 and 5 < mouse[1] < 5+30:
        make_button(screen, start_point_highlighted,
                   (110, 5, 80, 30), "START POINT")
    elif start_btn_pressed:
        make_button(screen, start_point_highlighted,
                   (110, 5, 80, 30), "START POINT")
    else:
        make_button(screen, START_BTN, (110, 5, 80, 30), "START POINT")

    # Check 'END POINT' button
    if 200+80 > mouse[0] > 200 and 5 < mouse[1] < 5+30:
        make_button(screen, end_point_highlighted, (200, 5, 80, 30), "END POINT")
    elif end_btn_pressed:
        make_button(screen, end_point_highlighted, (200, 5, 80, 30), "END POINT")
    else:
        make_button(screen, END_BTN, (200, 5, 80, 30), "END POINT")

    # Check 'CLEAR' button
    if 450+45 > mouse[0] > 450 and 5 < mouse[1] < 5+30:
        make_button(screen, clear_btn_highlighted, (450, 5, 45, 30), "CLEAR")
    elif clear_btn_pressed:
        make_button(screen, clear_btn_highlighted, (450, 5, 45, 30), "CLEAR")
    else:
        make_button(screen, clear_btn, (450, 5, 45, 30), "CLEAR")

    ''' BUTTON ACTIVATION '''
    if (5+90 > mouse[0] > 5 and 5+30 > mouse[1] > 5):  # Draw Walls
        if pygame.mouse.get_pressed()[0]:
            print("Draw Walls pressed")
            walls_btn_pressed = True
            start_btn_pressed = False
            end_btn_pressed = False
            clear_btn_pressed = False
    elif (110+80 > mouse[0] > 110 and 5 < mouse[1] < 5+30):  # Start Point
        if pygame.mouse.get_pressed()[0]:
            make_button(screen, start_point_highlighted,
                       (110, 5, 80, 30), "START POINT")
            print("Start Point Button pressed")
            walls_btn_pressed = False
            start_btn_pressed = True
            end_btn_pressed = False
            clear_btn_pressed = False
    elif (200+80 > mouse[0] > 200 and 5 < mouse[1] < 5+30):  # End Point
        if pygame.mouse.get_pressed()[0]:
            make_button(screen, end_point_highlighted,
                       (200, 5, 80, 30), "END POINT")
            print("End Point Button pressed")
            walls_btn_pressed = False
            start_btn_pressed = False
            end_btn_pressed = True
            clear_btn_pressed = False
    elif (450+45 > mouse[0] > 450 and 5 < mouse[1] < 5+30):  # Clear
        if pygame.mouse.get_pressed()[0]:
            print("Clear Button pressed")
            walls_btn_pressed = False
            start_btn_pressed = False
            end_btn_pressed = False
            clear_btn_pressed = True

# Clear "active" button state
def clear_button_state():
    global walls_btn_pressed
    global start_btn_pressed
    global end_btn_pressed
    global clear_btn_pressed

    walls_btn_pressed = False
    start_btn_pressed = False
    end_btn_pressed = False
    clear_btn_pressed = False

# Clears start point / end point, returns color of square to gray
def reset_start(x, y, node):
    curr_start

# THE ALGORITHM
def AstarAlgorithm():

    # global variables
    global openList
    global closedList
    global currentNode
    

    #currentNode becomes lowest Fcost Node from OpenList

    small = 0
    for i in range((len(openList))):
        if openList[i].Fcost < openList[small].Fcost:
            small = i
    try:
        currentNode = openList[small]
    except(IndexError):
        print("No shortest path found.")
        # If no path is found between the nodes, the program ends as if it had found it.
        return True

    currentNode.open = False
    #pygame.draw.rect(screen, green, (currentNode.x * width, currentNode.y * height, width, height), 0)
    openList.pop(small)

    closedList.append(currentNode)
    currentNode.closed = True
    if not (currentNode == start or currentNode == end):
        pygame.draw.rect(screen, LIGHT_RED, (int(currentNode.x * WIDTH),
                                             int(currentNode.y * HEIGHT), int(WIDTH), int(HEIGHT)), 0)
        pygame.display.update()

    if currentNode == end:  # we found the path to the end node
        return True

    for i in range(len(currentNode.neighbour)):
        temp_gcost = currentNode.Gcost + \
            calcDistance(currentNode, currentNode.neighbour[i])
        # if neighbour is a wall or if it is in the closed list skip the node
        if currentNode.neighbour[i].wall == True or currentNode.neighbour[i].closed == True or currentNode.neighbour[i] == start:
            pass
        elif currentNode.neighbour[i].open == False or currentNode.neighbour[i].Gcost > temp_gcost:
            currentNode.neighbour[i].Hcost = calcDistance(
                currentNode.neighbour[i], end)
            currentNode.neighbour[i].Gcost = temp_gcost
            currentNode.neighbour[i].Fcost = currentNode.neighbour[i].Hcost + temp_gcost
            currentNode.neighbour[i].parentNode = currentNode

            if currentNode.neighbour[i] not in openList:
                openList.append(currentNode.neighbour[i])
                currentNode.neighbour[i].open = True
                if not currentNode.neighbour[i] == end:
                    pygame.draw.rect(screen, GREEN, (int(currentNode.neighbour[i].x * WIDTH), int(
                        currentNode.neighbour[i].y * HEIGHT), int(WIDTH), int(HEIGHT)), 0)
                    pygame.display.update()

    return False


# Runs the pathfinder visualization on-screen; should be called only once during game loop unless application is reset
def run_visualization():

    count = 0
    display = True

    while display == True and shortestPath[count] != None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display = False
        pygame.draw.rect(screen, BLUE, (int(shortestPath[count].x * WIDTH), int(
            shortestPath[count].y * HEIGHT), int(WIDTH), int(HEIGHT)), 0)
        pygame.display.update()
        if count < len(shortestPath) - 1:
            count += 1
    if shortestPath[count] != None:
        print("The shortest path is: " + shortestPath + " units long.")
    else:
        print("Program Finished: No path found.")


# creates 2d array used for application -- middleman between GUI and back-end
grid = [[0 for i in range(COLS)] for j in range(ROWS)]

# makes each element of the area equal to box
for i in range(COLS):
    for j in range(ROWS):
        grid[i][j] = Node(i, j)

start = None #start node
end = None #end node

# Initialize GUI
screen.fill(WHITE)
for y in range(COLS):
    for x in range(ROWS):
        # rect = pygame.Rect(x * (height + 1), y * (width + 1), height, width)
        pygame.draw.rect(screen, GREY, [int(WIDTH * x), int(HEIGHT * y), int(WIDTH), int(HEIGHT)], 1)
        pygame.display.update()
running = True


# Drawing GUI toolbar
pygame.draw.rect(screen, GREY, (0, 0, boardSize[0], 40))  # Toolbar background
make_button(screen, WHITE, (5, 5, 90, 30), "DRAW WALLS")  # 'DRAW WALLS'
make_button(screen, GREEN, (110, 5, 80, 30), "START POINT")  # 'START POINT'
make_button(screen, END_BTN, (200, 5, 80, 30), "END POINT")  # 'END POINT'
make_button(screen, CLR_BTN, (450, 5, 45, 30), "CLEAR")  # 'CLEAR'

# Game loop
while running:

    for event in pygame.event.get():
        check_buttons()  # Checks button highlighting and activation

        position = pygame.mouse.get_pos()
        p1 = position[0] // (boardSize[0] // COLS)
        p2 = position[1] // (boardSize[1] // ROWS)
        print("p1 = " + str(p1) + "  " + "p2 = " + str(p2))
        box = grid[p1][p2]

        if walls_btn_pressed:
            if pygame.mouse.get_pressed()[0]:
                if box != start and box != end and box.wall == False and p2 > 4:
                    box.wall = True
                    pygame.draw.rect(screen, BLACK, (int(p1 * WIDTH), int(p2 * HEIGHT), int(WIDTH), int(HEIGHT)), 0)
        elif start_btn_pressed:
            if pygame.mouse.get_pressed()[0]:
                if box != start and box != end and box.wall == False and p2 > 4:
                    start = box
                    pygame.draw.rect(screen, DARK_GREEN, (int(p1 * WIDTH), int(p2 * HEIGHT), int(WIDTH), int(HEIGHT)), 0)
            start_btn_pressed = False
        elif end_btn_pressed:
            if pygame.mouse.get_pressed()[0]:
                if box != start and box != end and box.wall == False and p2 > 4:
                    end = box
                    pygame.draw.rect(screen, RED, (int(p1 * WIDTH), int(p2 * HEIGHT), int(WIDTH), int(HEIGHT)), 0)
            end_btn_pressed = False
        elif clear_btn_pressed:
            clear_screen()
            clear_button_state()
        elif event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit(1)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)
            if event.key == pygame.K_RETURN:
                print("Enter button pressed")
                running = False

        pygame.display.update()
    pygame.display.update()

# adds the neighbours list to each node
for i in range(COLS):
    for j in range(ROWS):
        grid[i][j].addNeighbor(grid)

# Initializing data structures used in A* algorithm
openList = []
closedList = []
wallList = []
shortestPath = []
pathLength = 0

#adds start node to openList
openList.append(start)
start.open = True
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
    try:
        temp = temp.parentNode
    except AttributeError:
        print("Node is null. No path has been found.")
        break
    if temp != start:
        shortestPath.append(temp)
# reverses the list so the order of the list is start to end
shortestPath.reverse()


run_visualization()
