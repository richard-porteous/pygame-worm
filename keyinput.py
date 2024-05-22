# the pygame imports to make them usable in our game
import pygame
from pygame.locals import *

class KeyInput():

    def __init__(self) -> None:
        self.key_queue = []
        self.last_key_pressed = "none"

    def getEvents(self):
       
        for event in pygame.event.get():
            if event.type == QUIT or (event.type==pygame.KEYDOWN and event.key in [K_ESCAPE]):
                self.key_queue.clear()
                return False
            
            if event.type==pygame.KEYDOWN:
                if event.key in [K_DOWN]:
                    self.last_key_pressed = "D"
                    self.key_queue.append("D")
                if event.key in [K_UP]:
                    self.last_key_pressed = "U"
                    self.key_queue.append("U")
                if event.key in [K_RIGHT]:
                    self.last_key_pressed = "R"
                    self.key_queue.append("R")
                if event.key in [K_LEFT]:
                    self.last_key_pressed = "L"
                    self.key_queue.append("L")

            if event.type==pygame.KEYUP:
                if event.key in [K_DOWN]:
                    self.key_queue.remove("D")
                if event.key in [K_UP]:
                    self.key_queue.remove("U")
                if event.key in [K_RIGHT]:
                    self.key_queue.remove("R")
                if event.key in [K_LEFT]:
                    self.key_queue.remove("L")
        
        return True

    def get_direction(self):
        if len(self.key_queue) > 0:
            return self.get_direction_vector(self.key_queue[0])
        else:
            return self.get_direction_vector(self.last_key_pressed)

    def get_direction_vector(self, key_eval):
        match (key_eval):
            case "U":
                return [0,-1]
            case "D":
                return [0,1]
            case "L":
                return [-1,0]
            case "R":
                return [1,0]
        return [0,0]



