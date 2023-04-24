#!/usr/bin/env python3
import pygame
from pygame.transform import *
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

# draw each layer in the map
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

# this function cannot be moved outside of main.py
def draw_map():
    for obj in sprite_group:
        x = zoomify(obj.rect.x - follower.x)
        y = zoomify(obj.rect.y - follower.y)
        # check if the blocks are visible
        if (x > -GRID_SIZE*ZOOM and x < textbox.x) and (y > -GRID_SIZE*ZOOM and y < HEIGHT):
            obj.surf = scale_by(obj.image, ZOOM)
            screen.blit(obj.surf, (x, y))

# this is a hack to allow rendering in the first frame
follower.x -= 0.2
# this is the main loop. the game happens in here
while running:
    needs_rerender = False;
    # event loop
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

        # TODO: this might be removed later
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

                            # FIXME: your player might refuse to move if there is a block
                            # in front of the block that you want to move to.
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
                            needs_rerender = True;
                                
                    print(lineData)
                    textbox.flush_text()
                    # because python is autistic for some reason,
                    # we can't include this line in the flust_text
                    # function
                    command_index = 0

                elif event.key in [K_UP, K_DOWN]:
                    # implements going back in command history
                    if event.key == K_UP and command_index >= -len(command_history) + 1:
                        command_index -= 1
                    if event.key == K_DOWN and command_index <= -1:
                        command_index += 1
                    print(command_index)
                    if command_index < 0:
                        textbox.text = command_history[command_index]
                    else:
                        textbox.text = ""
                else:
                    textbox.add_char(event.unicode)




    # smooth movement code
    diff_x = player.x - follower.x
    if diff_x != 0:
        follower.x += diff_x/MOVEMENT
    elif diff_x < 5:
        follower.x = player.x
        print(follower.x)


    diff_y = player.y - follower.y
    if diff_y != 0:
        follower.y += diff_y/MOVEMENT
    elif diff_y < 5:
        follower.y = player.y


    # draw stuff only if there is movement,
    # this if statement will have to change once there are other sprites and such
    if abs(diff_x) > CHANGE_THRESHOLD or abs(diff_y) > CHANGE_THRESHOLD:
        # make the screen white
        screen.fill(BG_GRAY)
        draw_map()

        # draw the cupboard
        screen.blit(scale_by(cupboard.image, ZOOM), (zoomify(cupboard.x - follower.x), zoomify(cupboard.y - follower.y)))

        # draw the follower (player)
        # position is fixed because the world moves around the player
        screen.blit(scale_by(player.image, ZOOM), (WIDTH/3, HEIGHT/2))

    # draw coin counter
    img = pygame.image.load("./sprites/coin.png")
    img = pygame.transform.scale(img,(GRID_SIZE*5,GRID_SIZE*5))

    screen.blit(img,(0,0))

    font = pygame.font.SysFont('Comic Sans MS', GRID_SIZE*2)
    text = font.render(" x"+str(coins), False, (0, 0, 0))
    screen.blit(text,(GRID_SIZE*0.8,GRID_SIZE))
    if textbox.active:
        # if needs_rerender:
        # draw the terminal
        pygame.draw.rect(screen, BLACK, textbox.rect)

        # render the text
        textbox.refresh_text()
        screen.blit(textbox.text_surface, (textbox.fontx, textbox.fonty))
    else:
        pygame.draw.rect(screen, TERM_GRAY, textbox.rect)

    # display contents
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
