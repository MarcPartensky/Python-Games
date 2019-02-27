from mywindow import Window
from mycolors import BLACK,WHITE,RED

from map import Map
from player import Player

import random

import pygame
from pygame.locals import *

class Game:
    def __init__(self):
        self.name="Test"
        self.map_size=[60,40]
        self.map=Map(self.map_size)
        self.window_size=[1400,800]
        self.fullscreen=False
        self.window=Window(self.name,self.window_size,self.fullscreen,text_color=RED)
        self.player=Player(borders=[0,0]+self.map.size)
        #print(self.map.grid)

    def __call__(self):
        self.show()
        while self.window.open:
            self.window.check()
            #self.getInput()
            self.update()
            self.show()

    def update(self):
        self.map.update()
        self.player.update(self.map,self.window)
        keys=self.window.press()
        if keys[K_RSHIFT]:
            self.map.camera.size[0]+=1
            self.map.camera.size[1]+=1
        if keys[K_LSHIFT]:
            self.map.camera.size[0]-=1
            self.map.camera.size[1]-=1

    def show(self):
        self.window.clear()
        #print("self.player.position:",self.player.position)
        self.map.show(self.player.position,self.player.size,self.window)
        self.window.print(text="Player's position: "+str(self.player.position),position=[10,10])
        self.window.flip()


if __name__=="__main__":
    game=Game()
    game()
