#!/usr/bin/env python3
import pygame
from identify import identify
from pygame.locals import (
    K_UP,
    K_DOWN
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
    for y,x_axis in enumerate(grid):
        for x,base in enumerate(x_axis):
            if base == "c":
                tile = pygame.image.load("tiles\\center_tile.png")

            elif base == "l":
                tile = pygame.image.load("tiles\\l_tile.png")
            elif base == "r":
                tile = pygame.image.load("tiles\\r_tile.png")
            elif base == "t":
                tile = pygame.image.load("tiles\\t_tile.png")
            elif base == "d":
                tile = pygame.image.load("tiles\\d_tile.png")

            elif base == "tl":
                tile = pygame.image.load("tiles\\tl_tile.png")
            elif base == "tr":
                tile = pygame.image.load("tiles\\tr_tile.png")
            elif base == "dl":
                tile = pygame.image.load("tiles\\dl_tile.png")
            elif base == "dr":
                tile = pygame.image.load("tiles\\dr_tile.png")

            elif base == "_cupboard":
                tile = pygame.image.load("tiles\\cupboard_tile.png")

            else:    
                tile = pygame.image.load("tiles\\base_tile.png")
                
            tile = pygame.transform.scale(tile,(GRID_SIZE, GRID_SIZE))
            screen.blit(tile, (x*GRID_SIZE, y*GRID_SIZE))

#grid creation (not auto generated)
grid = [
    ["tl","t","t","t","tr"],
    ["l","c","c","c","r"],
    ["l","c","cupboard","c","r"],
    ["l","c","c","c","r"],
    ["dl","d","d","d","dr"]
]

GRID_WIDTH = len(grid[0]) * GRID_SIZE
GRID_HEIGHT = len(grid) * GRID_SIZE

# window width and height
WIDTH = (len(grid[0]) * 2) * GRID_SIZE
HEIGHT = (len(grid)) * GRID_SIZE

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
player = Point((len(grid[0])//2) * GRID_SIZE, (len(grid)//2) * GRID_SIZE, 1)
follower = Point((len(grid[0])//2) * GRID_SIZE, (len(grid)//2) * GRID_SIZE, 20)
player_image = pygame.image.load("tiles\\base_tile.png")     
player_image = pygame.transform.scale(player_image,(GRID_SIZE, GRID_SIZE))

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

                            if lineData[1] == ".left()" and player.x - GRID_SIZE >= 0:
                                eval(lineData[0] + lineData[1])
                            elif lineData[1] == ".right()" and player.x + GRID_SIZE <= GRID_WIDTH:
                                eval(lineData[0] + lineData[1])
                            elif lineData[1] == ".up()" and player.y - GRID_SIZE >= 0:
                                eval(lineData[0] + lineData[1])
                            elif lineData[1] == ".down()" and player.y + GRID_SIZE <= GRID_HEIGHT:
                                eval(lineData[0] + lineData[1])
                                
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

    # draw the follower (player)
    screen.blit(player_image, (follower.x - middle, follower.y - middle))
    
    # draw the terminal
    pygame.draw.rect(screen, BLACK, textbox.rect)

    # render the text
    textbox.refresh_text()
    screen.blit(textbox.text_surface, (textbox.fontx, textbox.fonty))

    # display contents
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
