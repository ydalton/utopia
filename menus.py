import pygame
from constants import *

def startMenu(screen):
    state = True
    clock = pygame.time.Clock()
    button = pygame.Rect(WIDTH / 2.6, HEIGHT / 1.5, WIDTH / 2.6, HEIGHT / 6)

    while state:
        background = pygame.transform.scale(pygame.image.load("./tiles/start_background.png"),(WIDTH, HEIGHT))
        screen.blit(background,(0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                
        pygame.draw.rect(screen, (255, 255, 255), button)
        img = pygame.transform.scale(pygame.image.load("./sprites/start.png"),(WIDTH / 2.6, HEIGHT / 6))
        screen.blit(img,(WIDTH / 2.6, HEIGHT / 1.5))
        pygame.display.flip()
        clock.tick(60)

def endMenu(screen, endCoins):
    menu = pygame.Surface((WIDTH, HEIGHT))
    cnt = 1
    state = True
    clock = pygame.time.Clock()
    while state:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = False
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = False
                    return False
                elif event.key == pygame.K_RETURN:
                    state = False
                    return False

        if cnt == 1:
            menu.fill('grey')
            font = pygame.font.SysFont('Comic Sans MS', GRID_SIZE*2)
            text = font.render("You collected x" + str(endCoins) + " coins", False, (0, 0, 0))
            text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
            menu.blit(text, text_rect)

            message = "To end the game press ESCAPE or ENTER"
            text = font.render(message, False, (0, 0, 0))
            text_rect = text.get_rect(center=(WIDTH/2, (HEIGHT/2)+(GRID_SIZE*3)))
            menu.blit(text, text_rect)
            
            for j in range(0, 255):
                menu.set_alpha(j)
                screen.blit(menu, (0, 0))
                pygame.display.update()
                pygame.time.delay(10)
            
            menu.set_alpha()
            screen.blit(menu, (0, 0))
            cnt = 0
        
        pygame.display.update()
        clock.tick(60)
