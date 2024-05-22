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


class GameObject():
    
    def __init__(self, img_name, initial_pos):
        self.img = pygame.image.load(img_name)
        self.rect = self.img.get_rect()
        self.rect.center = initial_pos

    def draw(self):
        screen.blit(self.img, self.rect)



# control variable
game_running = True

held_keys = KeyInput()

#define white
white = (255,255,255)
#clear the screen
screen.fill(white)

# Max frame rate
clock = pygame.time.Clock()
FPS = 60

#Get the player image and a rectangle for size/position
player = GameObject("assets/player/blue_body_squircle.png", (width/2, height/2))
speed = 0.4

# GAME LOOP
while game_running:
    # clock tick with a value will return the delta time
    # as well as prevent clock speed being higher than FPS
    dt = clock.tick(FPS)

    game_running = held_keys.getEvents()
    dir = held_keys.get_direction()

    velocity = (dir[0] * dt * speed, dir[1] * dt * speed)
    player.rect = player.rect.move(velocity)

    screen.fill(white)
    player.draw()
    pygame.display.update()


# quit the pygame window
pygame.quit()
