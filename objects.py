import pygame
from constants import *
from menus import *

#player class (also for the follower)
class Point:
    def __init__(self, x, y, size, image):
        self.x = x
        self.y = y
        self.size = size
        self.image = pygame.transform.scale(image,(GRID_SIZE, GRID_SIZE))
        self.facing = "right"
    def left(self):
        if self.facing == "right":
            self.facing = "left"
            self.image = pygame.transform.flip(self.image, True, False)
        self.x -= GRID_SIZE
    def right(self):
        if self.facing == "left":
            self.facing = "right"
            self.image = pygame.transform.flip(self.image, True, False)
        self.x += GRID_SIZE
    def up(self):
        self.y -= GRID_SIZE
    def down(self):
        self.y += GRID_SIZE
    
class Chest:
    def __init__(self, x, y, image,top):
        self.x = x
        self.y = y
        self.top = pygame.transform.scale(top,(GRID_SIZE, GRID_SIZE))
        self.image = pygame.transform.scale(image,(GRID_SIZE, GRID_SIZE))
        self.coins = 1
    def interact(self, player_y, player_x):
        if self.y == player_y and self.x == player_x:
            top = pygame.image.load("./tiles/chests/chest_open_t.png")
            image = pygame.image.load("./tiles/chests/chest_open_b.png")
            self.image = pygame.transform.scale(image,(GRID_SIZE, GRID_SIZE))
            self.top = pygame.transform.scale(top,(GRID_SIZE, GRID_SIZE))
            add_coins = self.coins
            self.coins = 0
            return add_coins

#exiting door class
class Door:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def interact(self, player_y, player_x):
        if self.y == player_y and self.x == player_x:
            #end the game
            print("End")

#terminal class
class TextBox:
    def __init__(self):
        self.x = WIDTH//1.5
        self.y = HEIGHT
        self.rect = pygame.Rect(WIDTH//1.5, 0, self.x, self.y)
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
        self.text_surface = self.__font.render(">>> " + self.text + "|", True, WHITE)
    def flush_text(self):
        if self.text != command_history[-1]:
            command_history.append(self.text)
        self.text = ""

# The Sprite class Tile is used to draw the image attached to a certain position(pos) and scale it to the grid size.
class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image = pygame.transform.scale(surf,(GRID_SIZE,GRID_SIZE))
        self.rect = self.image.get_rect(topleft = pos)

#info button class
class Button:
    def __init__(self, height, width, image, position):
        self.height = height
        self.width = width
        self.image = image
        self.rect = image.get_rect(topleft=position)
        self.menu = pygame.Surface((self.width, self.height))
    #button game loop
    def pMenu(self,screen):
        state = True
        cnt = 1
        while state:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    state = False
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        state = False
                        return False
                    elif event.key == pygame.K_ESCAPE:
                        state = False
                        return True
            if cnt == 1:
                #fade in
                self.menu.fill((0, 0, 0))
                for j in range(0, 20):
                    self.menu.set_alpha(j)
                    screen.blit(self.menu, (0, 0))
                    pygame.display.update()
                    pygame.time.delay(15)
                cnt = 0

                #info block
                info = pygame.transform.scale(pygame.image.load("./sprites/info_menu.png"),(int(self.height/2),int(self.width/2)))
                screen.blit(info, (int(self.height/4),int(self.width/4)))
                pygame.display.update()
    #button interaction
    def on_click(self, screen, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return Button.pMenu(self,screen)
        elif event.button == 1:
            if self.rect.collidepoint(event.pos):
                return Button.pMenu(self,screen)
        return True
