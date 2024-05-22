# the pygame imports to make them usable in our game
import pygame
from pygame.locals import *
from keyinput import *

# Initialize the pygame code
pygame.init()


# set window size
size = width, height = (800, 600)
screen = pygame.display.set_mode(size)
# update the display to see what we set
pygame.display.update()

# control variable
game_running = True

held_keys = KeyInput()

#define white
white = (255,255,255)
#clear the screen
screen.fill(white)
#Get the player image and a rectangle for size/position
player = pygame.image.load("assets/player/blue_body_squircle.png")
player_rect = player.get_rect()
player_rect.center = width/2, height/2

# GAME LOOP
while game_running:
    game_running = held_keys.getEvents()
    screen.fill(white)
    screen.blit(player, player_rect)
    pygame.display.update()


# quit the pygame window
pygame.quit()
