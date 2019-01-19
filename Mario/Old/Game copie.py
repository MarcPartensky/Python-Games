import pygame
import random
import time
import numpy as np
import noise

from mycolors import *
from mywindow import *
from mymoves import *
from mycontrols import *

class Block:
    def __init__(self):
        self.grid=grid

class Map:
    def __init__(self):
        self.size=[500,20]
        self.grid=np.zeros(self.size)
        self.view=[0,20]

    def generate(self):
        hights=np.zeros(self.size[0])
        self.

    def show(self):


class Player:
    def __init__(self,spawn_position):
        self.spawn_position=spawn_position

    def spawn(self):
        self.position=self.spaw_position
        self.velocity=[0,0]
        self.acceleration=[0,5]

    def update(self,game):
        self.move

    def move(self):
        x,y=self.position
        vx,vy=self.velocity
        ax,ay=self.acceleration
        vx+=ax
        vy+=ay
        x+=vx
        y+=vy
        self.position=[x,y]
        self.velocity=[vx,vy]

    def show(self,window):
        pygame.draw.rect(window.screen,self.color)

class Game:
    def __init__(self):
        self.map=Map()
        self.player=Player()
        self.window=Window()
        self.entities=[self.map,self.player]
        self.delta=0.0001

    def session(self):
        self.play()

    def show(self):
        self.window.screen.fill(BLACK)
        for entity in self.entities:
            entity.show(self.window)
        self.window.flip()

    def update(self):
        for entity in self.entities:
            entity.update(self)

    def play(self):
        self.show()
        while self.window.open:
            self.window.check()
            self.update()
            self.show()
            time.sleep(self.delta)
