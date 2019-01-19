#-------#
#Credits#
#-------#

__author__="Marc Partensky"
__license__="Marc Partensky Company"
__title__="Ride"

"""This program needs pygame to be run."""

#------------#
#Dependencies#
#------------#

from mycolors import *
from mywindow import *
from mymoves import *
from mycontrols import *


import math
import random
import numpy as np
import noise

#-------#
#Classes#
#-------#

class Player:
    def __init__(self,name="Player"):
        self.name=name
        self.color=color
        self.radius=10
        self.view_field=100
    def start(self,game):
        self.position=[0,0]
        self.velocity=[0,0]
        self.acceleration=map.gravity
    def draw(self,game):
        x,y=self.position
        vfx,vfy=self.view_field

        raw_position=
        raw_radius=self.radius
        pygame.draw.circle(game.window.screen,self.color,raw_position,raw_radius,0)
    def move(self,game):
        x,y=self.position
        vx,vy=self.velocity
        ax,ay=self.acceleration
        vx+=ax
        vy+=ay
        x+=vx
        y+=vy
        self.position=x,y
        self.velocity=vx,vy
        self.acceleration=ax,ay
    def colisionChanges(self):
        pass

    def update(self,game):
        self.move()
        self.collisionChanges()


class Map:
    def __init__(self,size=1000):
        self.size=size
        self.grid=[noise.noise(i) in range(size)]
        self.gravity=[0,5]

class Rider:
    def __init__(self):
        self.name=__title__
        self.window=Window(self,__title__)
        self.map=Map()
        self.player=Player()
        self.session()
    def session(self):
        self.start()
        while self.window.open:
            self.window.check()
            self.update()
    def start(self):
        self.player.start()
    def update(self):
        self.player.update()


#-------#
#Actions#
#-------#

#functions=["math.sin(x)","math.cos(x)","math.exp(x)"]

#Grapher=Grapher(functions)
