import pygame
import random
import time
import numpy as np
import noise

from map import *
from player import *
from block import *
#from blocks_loader import *

from mycolors import *
from mywindow import *
from mymoves import *
from mycontrols import *


class Game:
    def __init__(self):
        self.name="Mario"
        self.loadTextures()

        self.player=Player(self.player_texture,[10,10])
        self.map=Map(self.blocks)

        self.entities=[self.map,self.player]
        self.delta=0.0001
        self.session()

    def loadTextures(self):
        dirt=Block(os.path.abspath("dirt2.jpg"))
        water=Block(os.path.abspath("water.jpg"))
        self.blocks={   "dirt":     dirt,
                        "water":    water}
        self.player_texture=os.path.abspath("character blue.png")

    def session(self):
        self.window=Window(self,(700,600))
        self.play()
        self.window.kill()

    def show(self):
        self.window.screen.fill(BLUE)
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

game=Game()
