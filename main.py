#!/usr/bin/env python3
import pygame
from identify import identify
from constants import *
from objects import *
from pygame.locals import (
    K_UP,
    K_DOWN
)

# draw grid
def drawGrid():
    for y,x_axis in enumerate(grid):
        for x,base in enumerate(x_axis):
            if base == "c":
                tile = pygame.image.load("./tiles/center_tile.png")

            elif base == "l":
                tile = pygame.image.load("./tiles/l_tile.png")
            elif base == "r":
                tile = pygame.image.load("./tiles/r_tile.png")
            elif base == "t":
                tile = pygame.image.load("./tiles/t_tile.png")
            elif base == "d":
                tile = pygame.image.load("./tiles/d_tile.png")

            elif base == "tl":
                tile = pygame.image.load("./tiles/tl_tile.png")
            elif base == "tr":
                tile = pygame.image.load("./tiles/tr_tile.png")
            elif base == "dl":
                tile = pygame.image.load("./tiles/dl_tile.png")
            elif base == "dr":
                tile = pygame.image.load("./tiles/dr_tile.png")

            else:    
                tile = pygame.image.load("./tiles/base_tile.png")
                
            tile = pygame.transform.scale(tile,(GRID_SIZE, GRID_SIZE))
            screen.blit(tile, (x*GRID_SIZE, y*GRID_SIZE))


pygame.init()
pygame.display.set_caption(GAME_NAME)
screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()

running = True
# defining object
cupboard = Cupboard((6) * GRID_SIZE, (5) * GRID_SIZE, pygame.image.load("./tiles/cupboard_tile.png"))

player = Point((len(grid[0])//2) * GRID_SIZE, (len(grid)//2) * GRID_SIZE, 1, pygame.image.load("./sprites/player.png"))
follower = Point((len(grid[0])//2) * GRID_SIZE, (len(grid)//2) * GRID_SIZE, 20, pygame.image.load("./sprites/player.png"))

textbox = TextBox()


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

                            if lineData[1] not in [".left()",".right()",".up()",".down()",".interact(player.y, player.x)"]:
                                eval(lineData[0] + lineData[1])
                            elif lineData[1] == ".left()" and player.x - GRID_SIZE >= 0:
                                eval(lineData[0] + lineData[1])
                            elif lineData[1] == ".right()" and player.x + 2*GRID_SIZE <= GRID_WIDTH:
                                eval(lineData[0] + lineData[1])
                            elif lineData[1] == ".up()" and player.y - GRID_SIZE >= 0:
                                eval(lineData[0] + lineData[1])
                            elif lineData[1] == ".down()" and player.y + 2*GRID_SIZE <= GRID_HEIGHT:
                                eval(lineData[0] + lineData[1])
                            elif lineData[1] == ".interact(player.y, player.x)":
                                add = "coins += "
                                exec(add + lineData[0] + lineData[1])
                                print(coins)
                                
                    print(lineData)
                    textbox.flush_text()

                elif event.key in [K_UP, K_DOWN]:
                    # implements going back in command history
                    if event.key == K_UP and command_index + 1 < len(command_history)-1:
                        command_index += 1
                    if event.key == K_DOWN and command_index - 1 >= -1:
                        command_index -= 1
                    print(command_index)
                    if len(command_history) > 0:
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

     # draw the cupboard
    screen.blit(cupboard.image, (cupboard.x, cupboard.y))

    # draw the follower (player)
    screen.blit(player.image, (follower.x, follower.y))

    # draw the terminal
    pygame.draw.rect(screen, BLACK, textbox.rect)

    # render the text
    textbox.refresh_text()
    screen.blit(textbox.text_surface, (textbox.fontx, textbox.fonty))

    # draw coin counter
    img = pygame.image.load("./sprites/coin.png")
    screen.blit(img,(0,0))
    font = pygame.font.SysFont('Comic Sans MS', 10)
    text = font.render(" x"+str(coins), False, (0, 0, 0))
    screen.blit(text,(7,7))

    # display contents
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
