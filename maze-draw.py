import pygame, numpy as np, matplotlib.pyplot as plt

screen = pygame.display.set_mode((100,100), 0, 8)
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
                    print("Valid point chosen.")
                    i += 1
                    if i >= len(pos_arr):
                        raise StopIteration
            if e.type == pygame.MOUSEMOTION:
                pass
            pygame.display.flip()

except StopIteration:
    pass

# MAP OUTPUT
fig, ax = plt.subplots(figsize=(12,12))
ax.imshow(mapArr, cmap=plt.cm.tab20b)
ax.scatter(pos_arr[0][1], pos_arr[0][0], marker = "*", color = "yellow", s = 200)
ax.scatter(pos_arr[1][1], pos_arr[1][0], marker = "*", color = "red", s = 200)
plt.show()

pygame.quit()