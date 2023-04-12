#!/usr/bin/env python3
import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)

GRID_SIZE = 100
# to represent an object's
class Point:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
    def left(self):
        self.x -= GRID_SIZE
    def right(self):
        self.x += GRID_SIZE
    def up(self):
        self.y -= GRID_SIZE
    def down(self):
        self.y += GRID_SIZE



# draw grid
def drawGrid():
    for y in range(0, HEIGHT, GRID_SIZE):
        for x in range(0, WIDTH, GRID_SIZE):
            rect = pygame.Rect(x+1, y+1, GRID_SIZE - 1, GRID_SIZE - 1)
            pygame.draw.rect(screen, WHITE, rect, 0)


# return the sign of a number
def sign(number):
    if number > 1:
        return 1
    elif number == 0:
        return 0
    else:
        return -1

# window width and height
WIDTH = 800
HEIGHT = 600

pygame.init()
pygame.display.set_caption("Utopia")
screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

MOVEMENT = 8

running = True
point = Point(WIDTH/2, HEIGHT/2, 1)
follower = Point(WIDTH/2, HEIGHT/2, 20)
while running:
    # event loop
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False;
        if event.type == pygame.KEYDOWN:
            if event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                print(f"Point: {point.x} {point.y}\tFollower: {follower.x} {follower.y}")
                if event.key == K_UP and point.y - GRID_SIZE >= 0:
                    point.up()
                if event.key == K_DOWN and point.y + GRID_SIZE <= HEIGHT:
                    point.down()
                if event.key == K_LEFT and point.x - GRID_SIZE >= 0:
                    point.left()
                if event.key == K_RIGHT and point.x + GRID_SIZE <= WIDTH:
                    point.right()

    # smooth movement code
    diff = point.x - follower.x
    if diff != 0:
        follower.x += diff/MOVEMENT
    elif diff < 5:
        follower.x = point.x

    diff = point.y - follower.y
    if diff != 0:
        follower.y += diff/MOVEMENT
    elif diff < 5:
        follower.y = point.y

    # make the screen white
    screen.fill(BLACK)
    # draw the rectangles
    drawGrid()
    middle = follower.size/2
    pygame.draw.rect(screen, RED, pygame.Rect(follower.x - middle, follower.y - middle, follower.size, follower.size))
    pygame.draw.rect(screen, RED, pygame.Rect(point.x, point.y, point.size, point.size))
    # display contents
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
10
