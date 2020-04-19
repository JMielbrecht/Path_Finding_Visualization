import pygame, random, numpy as np, matplotlib.pyplot as plt

screen = pygame.display.set_mode((600,400), 0, 8)
BKG = (0, 0, 0)
screen.fill(BKG)  # white screen
draw_on = False
last_pos = (0, 0)
color = (255, 255, 255)
radius = 2

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

# MAP OUTPUT
fig, ax = plt.subplots(figsize=(12,12))

ax.imshow(mapArr, cmap=plt.cm.tab20b)

ax.scatter(start[1],start[0], marker = "*", color = "yellow", s = 200)

ax.scatter(goal[1],goal[0], marker = "*", color = "red", s = 200)

plt.show()
pygame.quit()