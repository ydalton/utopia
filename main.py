#!/usr/bin/env python3
import pygame
from identify import identify
from constants import *
from objects import *
from pygame.locals import (
    K_UP,
    K_DOWN
)
from pytmx.util_pygame import load_pygame

pygame.init()
pygame.display.set_caption(GAME_NAME)
screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()
tmx_data = load_pygame('./tiles/maze.tmx')
sprite_group = pygame.sprite.Group()

for layer in tmx_data.layers:
    if hasattr(layer,'data'):
        for x,y,surf in layer.tiles():
            pos =(x * GRID_SIZE,y * GRID_SIZE)
            Tile(pos = pos, surf = surf, groups = sprite_group)
    sprite_group.draw(screen)

running = True
# defining object
cupboard = Cupboard((47) * GRID_SIZE, (3) * GRID_SIZE, pygame.image.load("./tiles/cupboard_tile.png"))

player = Point((47) * GRID_SIZE, (5) * GRID_SIZE, 1, pygame.image.load("./sprites/hero.png"))
follower = Point((47) * GRID_SIZE, (5) * GRID_SIZE, 20, pygame.image.load("./sprites/hero.png"))

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

                            p_idx_x = int(player.x / GRID_SIZE)
                            p_idx_y = int(player.y / GRID_SIZE)

                            if lineData[1] not in [".left()",".right()",".up()",".down()",".interact(player.y, player.x)"]:
                                eval(lineData[0] + lineData[1])
                            elif lineData[1] == ".left()" and grid[p_idx_y][p_idx_x - 1] != 0: 
                                eval(lineData[0] + lineData[1])
                            elif lineData[1] == ".right()" and grid[p_idx_y][p_idx_x + 1] != 0:
                                eval(lineData[0] + lineData[1])
                            elif lineData[1] == ".up()" and grid[p_idx_y - 1][p_idx_x] != 0:
                                eval(lineData[0] + lineData[1])
                            elif lineData[1] == ".down()" and grid[p_idx_y + 1][p_idx_x] != 0:
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
                    if len(command_history) > 0:
                        # TODO command history is not completely working
                        if command_index > -1:
                            textbox.text = command_history[len(command_history) - command_index - 1]
                        else:
                            textbox.text = ""
                else:
                    textbox.add_char(event.unicode)

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
    screen.fill((20,20,18))

    # draw the rectangles
    sprite_group.draw(screen)

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
    img = pygame.transform.scale(img,(GRID_SIZE*5,GRID_SIZE*5))
    screen.blit(img,(0,0))
    font = pygame.font.SysFont('Comic Sans MS', GRID_SIZE*2)
    text = font.render(" x"+str(coins), False, (0, 0, 0))
    screen.blit(text,(GRID_SIZE*0.8,GRID_SIZE))

    # display contents
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
