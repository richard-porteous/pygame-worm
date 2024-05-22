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
        self.img = pygame.transform.scale_by(self.img, 0.5 )
        self.rect = self.img.get_rect()
        self.rect.center = initial_pos

    def draw(self):
        screen.blit(self.img, self.rect)



# control variable
game_running = True

held_keys = KeyInput()

#colors
white = (255,255,255)
black = (0,0,0)

#clear the display
screen.fill(white)

#background - copy screen surface area
background = pygame.Surface.copy(screen)

#draw lines for the grid on the background
for y in range(0, height, 40):
    pygame.draw.line(background, black, (0,y), (width,y))
for x in range(0, width,  40):
    pygame.draw.line(background, black, (x,0), (x,height))

# blit the background to screen
screen.blit(background,(0,0))

# Max frame rate
clock = pygame.time.Clock()
FPS = 60

#Get the player image and a rectangle for size/position
player = GameObject("assets/player/blue_body_squircle.png", (width/2 - 20, height/2))
speed = 0.2

# GAME LOOP
while game_running:
    # clock tick with a value will return the delta time
    # as well as prevent clock speed being higher than FPS
    dt = clock.tick(FPS)

    game_running = held_keys.getEvents()
    dir = held_keys.get_direction()

    velocity = (dir[0] * dt * speed, dir[1] * dt * speed)
    player.rect = player.rect.move(velocity)

    screen.blit(background,(0,0))
    player.draw()
    pygame.display.update()


# quit the pygame window
pygame.quit()
