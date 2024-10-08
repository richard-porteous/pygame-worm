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

def detect_center_reached(pos, velocity):
    """
    All values are single axis. 
    Returns: tile_center_reached, overshoot_amount
    """

    if velocity[1] == 0:
        dist = velocity[0]
        obj_center = pos[0]
    else:
        dist = velocity[1]
        obj_center = pos[1]

    tile_center = calc_current_tile_axis_center_pos(obj_center)
    full_move_pos = obj_center + dist
    overshoot = full_move_pos - tile_center
    
    if dist > 0 and obj_center < tile_center and tile_center <= full_move_pos:
        return [True, overshoot]
    
    if dist < 0 and obj_center > tile_center and tile_center >= full_move_pos:
        return [True, overshoot]

    return [False, overshoot]

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
    speed = 0.2
    last_dir_moved = [0,0]
    last_center_reached = (0,0)
    ## this is pass back info
    prev_dir_moved = [0,0]
    prev_center_reached = (0,0)
    dist = 0
    final_dist = 0
    ##
    

    def __init__(self, img_name, initial_t_pos):
        super().__init__(img_name, initial_t_pos)
    
    def move(self, dir_req, dt , speed):
        self.speed = speed
        dist = int(dt * speed)
        final_dist = 0
        if self.last_dir_moved[0] == 0 and self.last_dir_moved[1] == 0:
            self.last_dir_moved = dir_req
            dir = dir_req
        else:
            dir = self.last_dir_moved

        velocity = (dir[0] * dist), (dir[1] * dist)

        passed_center, overshoot = detect_center_reached(self.rect.center, velocity)
        if passed_center:
            self.prev_dir_moved = self.last_dir_moved
            self.prev_center_reached = self.last_center_reached

            x = calc_current_tile_axis_center_pos(self.rect.center[0])
            y = calc_current_tile_axis_center_pos(self.rect.center[1])
            self.rect.center = (x, y)
            self.last_center_reached = (x, y)
            self.last_dir_moved = dir_req
            dir = dir_req
            final_dist = abs(overshoot)
            velocity = (dir[0] * final_dist, dir[1] * final_dist)

        detected, dir_d, pos_d = detect_edges(dir,self.rect.center)
        if detected:
            self.rect.center = pos_d

        self.rect = self.rect.move(velocity)

        self.dist = dist
        self.final_dist = final_dist
        return passed_center


class Player(KinematicObject):
    tailpieces = []

    def __init__(self, initial_pos, speed):
        super().__init__("assets/player/blue_body_squircle.png",  initial_pos)
        self.speed = speed

    def move(self, dir, dt ):
        #print("NEW MOVE")
        passed_center = super().move(dir, dt, self.speed)
        object_to_follow = self
        for t in self.tailpieces:
            t.follow(object_to_follow, passed_center)
            object_to_follow = t

    def grow_tail(self, initial_t_pos):
        l = len(self.tailpieces)
        t = Tail(initial_t_pos, self.speed, str(l))
        self.tailpieces.append(t)
    
    def draw(self):
        super().draw()
        for t in self.tailpieces:
            t.draw()

class Tail(GameObject):
    name = "tp"
    speed = 0.2
    last_dir_moved = [0,0]
    last_center_reached = (0,0)
    ## this is pass back info
    prev_dir_moved = [0,0]
    prev_center_reached = (0,0)
    dist = 0
    final_dist = 0
    ##

    def __init__(self, initial_t_pos, speed, name):
        super().__init__("assets/player/blue_body_circle.png",  initial_t_pos)
        self.speed = speed
        self.name += name

    def follow(self, object_to_follow, passed_center):
        self.dist = object_to_follow.dist
        self.final_dist = object_to_follow.final_dist
        if passed_center:
            self.prev_dir_moved = self.last_dir_moved
            self.prev_center_reached = self.last_center_reached
            self.last_center_reached = object_to_follow.prev_center_reached
            self.last_dir_moved = object_to_follow.prev_dir_moved
            self.rect.center = self.last_center_reached
            velocity = (self.last_dir_moved[0] * self.final_dist, self.last_dir_moved[1] * self.final_dist)
            #print("pc_follow", self.name, velocity)
        else:
            velocity = (self.last_dir_moved[0] * self.dist), (self.last_dir_moved[1] * self.dist)
            #print("follow", self.name, velocity)

        self.rect = self.rect.move(velocity)


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

