#!/usr/bin/env python3
import pygame
from identify import identify
from constants import *
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT
)

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
        self.text = ""
        self.__font = pygame.font.Font(None, 32)
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
        self.text_surface = self.__font.render(">>> " + self.text, True, WHITE)
    def flush_text(self):
        command_history.append(self.text)
        self.text = ""
        command_index = 0


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

pygame.init()
pygame.display.set_caption(GAME_NAME)
screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()
# colors

running = True
player = Point(WIDTH/2, HEIGHT/2, 1)
follower = Point(WIDTH/2, HEIGHT/2, 20)
textbox = TextBox()
command_history = []
command_index = 0

while running:
    # event loop
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

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
                    inLine = textbox.text   #point.moveX(-3)
                    lineData = identify(inLine)
                    if lineData[3] == False:
                        for rep in range(abs(int(lineData[2]))):
                            print(f"Point: {player.x} {player.y}\tFollower: {follower.x} {follower.y}")
                            if player.y - GRID_SIZE >= 0 and player.y + GRID_SIZE <= HEIGHT and player.x - GRID_SIZE >= 0 and player.x + GRID_SIZE <= WIDTH:
                                try:
                                    eval(lineData[0] + lineData[1])
                                except:
                                    print("Does not work!")
                    print(lineData)

                    textbox.flush_text()
                elif event.key in [K_UP, K_DOWN]:
                    # implements going back in command history
                    if event.key == K_UP and command_index + 1 < len(command_history)-1:
                        command_index += 1
                    if event.key == K_DOWN and command_index - 1 >= -1:
                        command_index -= 1
                    print(command_index)
                    if command_index > -1:
                        textbox.text = command_history[len(command_history) - command_index - 1]
                    else:
                        textbox.text = ""
                else:
                    textbox.add_char(event.unicode)
                    print(textbox.text) 

    # smooth movement code
    diff = player.x - follower.x
    if diff != 0:
        follower.x += diff/MOVEMENT
    elif diff < 5:
        follower.x = player.x

    diff = player.y - follower.y
    if diff != 0:
        follower.y += diff/MOVEMENT
    elif diff < 5:
        follower.y = player.y

    # make the screen white
    screen.fill(BLACK)
    # draw the rectangles
    drawGrid()
    middle = follower.size/2
    # draw the follower
    pygame.draw.rect(screen, RED, pygame.Rect(follower.x - middle, follower.y - middle, follower.size, follower.size))
    # draw the point
    pygame.draw.rect(screen, RED, pygame.Rect(player.x, player.y, player.size, player.size))
    # draw the terminal
    pygame.draw.rect(screen, BLACK, textbox.rect)
    # render the text
    textbox.refresh_text()
    screen.blit(textbox.text_surface, (textbox.fontx, textbox.fonty))
    # display contents
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
