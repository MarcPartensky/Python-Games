#-------#
#Credits#
#-------#

__author__="Marc Partensky"
__license__="Marc Partensky Company"
__game__="Agar.io"

"""This game is available on every computer device that has Python installed."""

#------------#
#Dependencies#
#------------#

import os
os.system("pip2.7 install pygame")
import pygame
from pygame.locals import *
import math
import random
import numpy as np
import time

try:
    DIRECTORY="/Users/olivierpartensky/Programs/Python/Games/Agario/"
    os.chdir(DIRECTORY)
finally:
    pass

from Window import *

#---------#
#Variables#
#---------#

BLUE   = (  0,  0,255)
RED    = (255,  0,  0)
GREEN  = (  0,255,  0)
YELLOW = (255,255,  0)
BLACK  = (  0,  0,  0)
WHITE  = (255,255,255)

RIGHT = 0
UP    = 1
LEFT  = 2
DOWN  = 3

#-------#
#Classes#
#-------#

class Map:
    def __init__(self,size):
        self.size=size

class Game:
    def __init__(self):
        self.name=__game__
        self.window=Window(self)
        self.map=Map([10,10])
        self.objects=[]
        self.play()

    def play(self):
        self.start()
        while self.window.open:
            self.update()
            self.show()

    def start(self):
        self.window.drawBackground(BLACK)


    def update(self):
        for object in self.objects:
            object.update(self.map)


    def show(self):
        for object in self.objects:
            object.show(self.window)
        self.window.flip()






#-------#
#Actions#
#-------#

game=Game()
