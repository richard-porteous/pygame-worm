# the pygame imports to make them usable in our game
import pygame
from pygame.locals import *


# Initialize the pygame code
pygame.init()


# set window size
size = width, height = (800, 600)
screen = pygame.display.set_mode(size)
# update the display to see what we set
pygame.display.update()

# control variable
game_running = True


# GAME LOOP
while game_running:
    # event listeners 
    # i.e. listen to key-presses or windows closing etc.
    for event in pygame.event.get():
        if event.type == QUIT:
            # collapse the app
            game_running = False


    pygame.display.update()


# quit the pygame window
pygame.quit()
