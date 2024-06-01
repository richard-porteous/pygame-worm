import math
import random
import pygame
from pygame.locals import *
from keyinput import *

############################
#### Set Up the Display ####
############################

# Initialize the pygame code
pygame.init()

#some game constants
TILESQRT = 40
TILESIZE = (TILESQRT, TILESQRT)

#colors
white = (255,255,255)
black = (0,0,0)

# Display
size = width, height = (TILESQRT*20, TILESQRT*16)
screen = pygame.display.set_mode(size)
pygame.display.update()

#clear the display
screen.fill(white)
background = pygame.Surface.copy(screen)

#draw lines for the grid on the background
for y in range(0, height, TILESIZE[1]):
    pygame.draw.line(background, black, (0,y), (width,y))
for x in range(0, width,  TILESIZE[0]):
    pygame.draw.line(background, black, (x,0), (x,height))

# place the background on the screen
screen.blit(background,(0,0))

# Max frame rate
clock = pygame.time.Clock()
FPS = 60

############################
##### Helper Functions #####
############################

def get_tpos_from_pos(pos):
    axs = int(math.copysign(1,pos[0]))
    ays = int(math.copysign(1,pos[1]))
    return axs * int(abs(pos[0])/TILESIZE[0]), ays * int(abs(pos[1])/TILESIZE[1])

def get_pos_from_tpos(tpos):
    axs = int(math.copysign(1,tpos[0]))
    ays = int(math.copysign(1,tpos[1]))
    return axs * (abs(tpos[0]) * TILESIZE[0] + int(TILESIZE[0]/2)), ays * (abs(tpos[1]) * TILESIZE[1] + int(TILESIZE[1]/2))

def calc_current_tile_axis_center_pos(pos_axis):
    axs = int(math.copysign(1,pos_axis))
    return axs * int(abs(pos_axis)/TILESQRT) * TILESQRT + int(TILESQRT/2)

def get_direction_from_position_diff(end_pos, start_pos):
    dirx = 0
    diry = 0
    if end_pos[0] - start_pos[0] != 0:
        dirx = int(math.copysign(1,end_pos[0] - start_pos[0]))
    if end_pos[1] - start_pos[1] != 0:
        diry = int(math.copysign(1,end_pos[1] - start_pos[1]))
    
    return [dirx,diry]


def detect_edges(dir, pos):
    boundry = "none"
    right_pos = calc_current_tile_axis_center_pos(width-1)
    #print(right_pos)
    bottom_pos = calc_current_tile_axis_center_pos(height-1)
    #print(bottom_pos)


    if pos[0] <= TILESIZE[0]/2 and dir[0] < 0:
        boundry = "left"
        end_move_pos = right_pos + TILESIZE[0], pos[1]
        #print(boundry, dir, pos, end_move_pos)
        
    elif pos[0] >= right_pos and dir[0] > 0:
        boundry = "right"
        end_move_pos = (-TILESIZE[0]/2, pos[1])
        #print(boundry, dir, pos, end_move_pos)

    elif pos[1] <= TILESIZE[1]/2 and dir[1] < 0:
        boundry = "top"
        end_move_pos = pos[0], bottom_pos + TILESIZE[0]
        #print(boundry, dir, pos, end_move_pos)

    elif  pos[1] >= bottom_pos and dir[1] > 0:
        boundry = "bottom"
        end_move_pos = (pos[0], -TILESIZE[1]/2)
        #print(boundry, dir, pos, end_move_pos)

    if boundry in ["left","right","top","bottom"]:
        #print (True, dir, end_move_pos)
        return (True, dir, end_move_pos)

    return (False, dir, pos)


############################
###### Game Classes ########
############################

class GameObject():
    
    def __init__(self, img_name, initial_t_pos):
        self.img = pygame.image.load(img_name)
        self.img = pygame.transform.scale_by(self.img, 0.5 )
        self.rect = self.img.get_rect()
        initial_pos = get_pos_from_tpos(initial_t_pos)
        self.set_pos(initial_pos)
    
    def set_pos(self, pos):
        self.rect.center = pos

    def draw(self):
        screen.blit(self.img, self.rect)


class KinematicObject(GameObject):
    last_dir = [0,0]
    last_center = (0,0)

    def __init__(self, img_name, initial_t_pos):
        super().__init__(img_name, initial_t_pos)
    
    def set_next_move(self, velocity):
        # python scope - look it up!
        if velocity[1] != 0:
            d = velocity[1]
            p = self.rect.center[1]
        else:
            d = velocity[0]
            p = self.rect.center[0]

        t = calc_current_tile_axis_center_pos(p)
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
        final_dist = dist
        if self.last_dir[0] == 0 and self.last_dir[1] == 0:
            self.last_dir = dir_req
            dir = dir_req
        else:
            dir = self.last_dir

        velocity = (dir[0] * dist), (dir[1] * dist)
        passed_center, overshoot = self.set_next_move(velocity)

        if passed_center:
            x = calc_current_tile_axis_center_pos(self.rect.center[0])
            y = calc_current_tile_axis_center_pos(self.rect.center[1])
            self.rect.center = (x, y)
            self.last_center = (x, y)
            self.last_dir = dir_req
            dir = dir_req
            final_dist = abs(overshoot)
            velocity = (dir[0] * final_dist, dir[1] * final_dist)

        detected, dir_d, pos_d = detect_edges(dir,self.rect.center)
        if detected:
            self.rect.center = pos_d

        self.rect = self.rect.move(velocity)
        return final_dist


class Player(KinematicObject):
    speed = 0.2
    tailpieces = []

    def __init__(self, initial_pos, speed):
        super().__init__("assets/player/blue_body_squircle.png",  initial_pos)
        self.speed = speed

    def move(self, dir, dt ):
        super().move(dir, dt, self.speed)

    def grow_tail(self, initial_t_pos):
        t = Tail(initial_t_pos, self.speed)
        self.tailpieces.append(t)
    
    def draw(self):
        super().draw()
        for t in self.tailpieces:
            t.draw()

class Tail(GameObject):
    speed = 0.2

    def __init__(self, initial_t_pos, speed):
        super().__init__("assets/player/blue_body_circle.png",  initial_t_pos)
        self.speed = speed


class Food(GameObject):
    def __init__(self):
        super().__init__("assets/food/tile_coin.png", (-1,-1))

    def get_random_pos(self) -> tuple[int, int]:
        x = random.randrange(0, int(width/TILESQRT)) * TILESQRT + int(TILESQRT/2)
        y = random.randrange(0, int(height/TILESQRT)) * TILESQRT + int(TILESQRT/2)
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
player = Player((10, 8), 0.2)
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
        player.grow_tail(get_tpos_from_pos(food.rect.center))
        food.reposition()


    screen.blit(background,(0,0))

    food.draw()
    player.draw()
    
    pygame.display.update()

############################
### quit window clean up ###
############################

pygame.quit()

