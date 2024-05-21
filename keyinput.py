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
        return True
            