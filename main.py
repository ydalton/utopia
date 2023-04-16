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


class TextBox:
    def __init__(self):
        self.x = WIDTH//2
        self.y = HEIGHT
        self.rect = pygame.Rect(WIDTH//2, 0, self.x, self.y)
        self.text = "lolzers"
        self.__font = pygame.font.Font(None, 16)
        self.__offset = 5
        self.fontx = self.x + self.__offset
        self.fonty = self.__offset
        self.text_surface = self.__font.render(self.text, True, WHITE)
        self.active = False
    def add_char(self, _char):
        if _char == '\n':
            self.text += '\n'
        else:
            self.text += _char
    def del_char(self):
        if len(self.text) > 0:
            self.text = self.text[:-1]
    def refresh_text(self):
        self.text_surface = self.__font.render(self.text, True, WHITE)


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
textbox = TextBox()
while running:
    # event loop
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False;
        if event.type == pygame.MOUSEBUTTONDOWN:
            if textbox.rect.collidepoint(event.pos):
                textbox.active = not textbox.active
            else:
                textbox.active = False
        if event.type == pygame.KEYDOWN:
            if textbox.active:
                if event.key == pygame.K_BACKSPACE:
                    textbox.del_char()
                elif event.key == pygame.K_RETURN:
                    textbox.add_char('\n')
                else:
                    textbox.add_char(event.unicode)
                    print(textbox.text)
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
    # draw the follower
    pygame.draw.rect(screen, RED, pygame.Rect(follower.x - middle, follower.y - middle, follower.size, follower.size))
    # draw the point
    pygame.draw.rect(screen, RED, pygame.Rect(point.x, point.y, point.size, point.size))
    # draw the terminal
    pygame.draw.rect(screen, BLACK, textbox.rect)
    # render the text
    textbox.refresh_text()
    screen.blit(textbox.text_surface, (textbox.fontx, textbox.fonty))
    # display contents
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
