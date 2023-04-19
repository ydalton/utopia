from objects import *
from constants import *
import pygame

cupboard = Cupboard(1,1,pygame.image.load("./tiles/cupboard_tile.png"))


print(coins)

coins += cupboard.interact(1,1)

print(coins)

cupboard.coins += 1 #reset

add = "coins += cupboard.interact(1,1)"
exec(add)

print(coins)