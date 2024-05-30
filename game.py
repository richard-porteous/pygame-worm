import random
import pygame
from pygame.locals import *
from keyinput import *

############################
#### Set Up the Display ####
############################

# Initialize the pygame code
pygame.init()

#colors
white = (255,255,255)
black = (0,0,0)

# Display
size = width, height = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.update()

#clear the display
screen.fill(white)
background = pygame.Surface.copy(screen)

#draw lines for the grid on the background
for y in range(0, height, 40):
    pygame.draw.line(background, black, (0,y), (width,y))
for x in range(0, width,  40):
    pygame.draw.line(background, black, (x,0), (x,height))

# place the background on the screen
screen.blit(background,(0,0))

# Max frame rate
clock = pygame.time.Clock()
FPS = 60

############################
###### Game Classes ########
############################

class GameObject():
    
    def __init__(self, img_name, initial_pos):
        self.img = pygame.image.load(img_name)
        self.img = pygame.transform.scale_by(self.img, 0.5 )
        self.rect = self.img.get_rect()
        self.set_pos(initial_pos)
    
    def set_pos(self, pos):
        self.rect.center = pos

    def draw(self):
        screen.blit(self.img, self.rect)


class KinematicObject(GameObject):
    last_dir = [0,0]

    def __init__(self, img_name, initial_pos):
        super().__init__(img_name, initial_pos)
    
    def calc_current_tile_axis_center(self, pos_axis):
        return int(pos_axis/40) * 40 + 20

    def set_next_move(self, velocity):
        # python scope - look it up!
        if velocity[1] != 0:
            d = velocity[1]
            p = self.rect.center[1]
        else:
            d = velocity[0]
            p = self.rect.center[0]

        t = self.calc_current_tile_axis_center(p)
        e = p + d
        o = e - t
        
        if d > 0 and p < t and t <= e:
            return [True, o]
        
        if d < 0 and p > t and t >= e:
            return [True, o]
        
        return [False, o]

    def move(self, dir_req, dt , speed):
        self.speed = speed
        dist = int(dt * speed)
        if self.last_dir[0] == 0 and self.last_dir[1] == 0:
            self.last_dir = dir_req
            dir = dir_req
        else:
            dir = self.last_dir

        velocity = (dir[0] * dist), (dir[1] * dist)
        passed_center, overshoot = self.set_next_move(velocity)

        if passed_center:
            self.rect.center = (self.calc_current_tile_axis_center(self.rect.center[0]), \
                    self.calc_current_tile_axis_center(self.rect.center[1]))
            self.last_dir = dir_req
            dir = dir_req
            velocity = (dir[0] * abs(overshoot), dir[1] * abs(overshoot))
        
        self.rect = self.rect.move(velocity)


class Player(KinematicObject):
    speed = 0.2
    tailpieces = []

    def __init__(self, initial_pos, speed):
        super().__init__("assets/player/blue_body_squircle.png",  initial_pos)
        self.speed = speed

    def move(self, dir, dt ):
        super().move(dir, dt, self.speed)

    def set_speed(self, speed):
        self.speed = speed

    def grow_tail(self, initial_pos):
        t = Tail(initial_pos, self.speed)
        self.tailpieces.append(t)
    
    def draw(self):
        super().draw()
        for t in self.tailpieces:
            t.draw()

class Tail(GameObject):
    speed = 0.2

    def __init__(self, initial_pos, speed):
        super().__init__("assets/player/blue_body_circle.png",  initial_pos)
        self.speed = speed


class Food(GameObject):
    def __init__(self):
        super().__init__("assets/food/tile_coin.png", (-1,-1))

    def get_random_pos(self) -> tuple[int, int]:
        x = random.randrange(0, int(width/40)) * 40 + 20
        y = random.randrange(0, int(height/40)) * 40 + 20
        return (x,y)
    
    def reposition(self):
        pos = self.get_random_pos()
        self.set_pos(pos)



############################
###### Get Game ready ######
############################

# control variable
game_running = True

held_keys = KeyInput()

#Get the player image and a rectangle for size/position
player = Player((width/2 - 20, height/2), 0.2)
food = Food()
food.reposition()

############################
######### GAME LOOP ########
############################

while game_running:
    # clock tick with a value will return the delta time
    # as well as prevent clock speed being higher than FPS
    dt = clock.tick(FPS)

    game_running = held_keys.getEvents()
    dir = held_keys.get_direction()

    player.move(dir, dt)
    if Rect.collidepoint(food.rect, player.rect.center):
        player.grow_tail(food.rect.center)
        food.reposition()


    screen.blit(background,(0,0))

    food.draw()
    player.draw()
    
    pygame.display.update()

############################
### quit window clean up ###
############################

pygame.quit()

