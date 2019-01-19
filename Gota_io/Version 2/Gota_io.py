__author__="Marc Partensky"
__license__="Partensky Company"

#------------#
#Importations#
#------------#

import pygame
from pygame.locals import *
import numpy as np
import random
import os
import math
from math import *
import time

GAME_NAME="Gota.io"

DISPLAY=True
FONT="monospace"

BLUE    = (  0,  0,255)
RED     = (255,  0,  0)
YELLOW  = (255,255,  0)
BLACK   = (  0,  0,  0)
GREY    = (127,127,127)
WHITE   = (255,255,255)
COLORS=[BLACK,WHITE,RED,YELLOW,BLUE]

import Window
import Manager
import Map
import Game
import Player
import Bot
import Human

PLAYERS=[Human("Marc"),Bot(),Bot(),Bot()]
DIRECTORY="/Users/olivierpartensky/Programs/Library/Puissance4/"
os.chdir(DIRECTORY)

#-------#
#Actions#
#-------#

if __name__ == "__main__":
    main=Manager()
