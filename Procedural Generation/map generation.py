import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np
import random

from itertools import product
import math
import random

import noise
import scipy
from scipy.misc import toimage



BLUE=   (  0,  0,255)
YELLOW= (255,255,100)
GREEN=  (  0,150,  0)
GREY=   (100,100,100)
WHITE=  (255,255,255)

class Window:
    made=0
    def __init__(self,game=None,title="Game",size=None,font="monospace",set=True):
        Window.made+=1
        self.number=Window.made
        self.title=title
        self.font=font
        self.open=True
        self.size=size
        if set:
            self.set()

    def set(self):
        pygame.init()
        self.setSize()
        self.font = pygame.font.SysFont(self.font, 65)
        self.screen=pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.title)

    def setSize(self):
        if self.size is None:
            info = pygame.display.Info()
            self.size=(info.current_w*2/3,info.current_h*2/3)
        else:
            self.size=size

    def pop_up(self,message):
        pass

    def scale(self,picture,size):
        return pygame.transform.scale(picture,size)

    def check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.open=False

    def select(self):
        while self.open:
            self.check()
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    return (event.pos[0],event.pos[1])

    def point(self):
        for event in pygame.event.get():
            return (event.pos[0],event.pos[1])

    def flip(self):
        pygame.display.flip()

    def drawPicture(self,picture,position):
        self.screen.blit(picture, position)

    def display(page):
        pass


class Map:
    def __init__(self,size=[500,500]):
        self.size=size
        self.generate()

    def generate(self):
        self.dimensions=3
        self.terrain=np.zeros(self.size+[self.dimensions])
        sx,sy=self.size
        hx,hy=sx//2,sy//2
        noise=self.getNoise()

        for y in range(sy):
            for x in range(sx):
                n=noise[y][x]
                n=(3*n+1)/2
                #print(n)
                if n<0.4:
                    color=BLUE
                    #(0,0,(255.0/0.2)*n)
                elif n<0.45:
                    color=YELLOW
                elif n<0.9:
                    color=GREEN
                elif n<1.0:
                    color=GREY
                else:
                    color=WHITE
                self.terrain[y][x]=color

    def getNoise(self):
        shape = (1024,1024)
        scale = 100.0
        octaves = 6
        persistence = 0.5
        lacunarity = 2.0

        world = np.zeros(shape)
        for i in range(shape[0]):
            for j in range(shape[1]):
                world[i][j] = noise.pnoise2(i/scale,
                                            j/scale,
                                            octaves=octaves,
                                            persistence=persistence,
                                            lacunarity=lacunarity,
                                            repeatx=1024,
                                            repeaty=1024,
                                            base=0)
        return world

    def show(self,window):
        sx,sy=self.size
        wsx,wsy=window.size
        cx,cy=(float(wsx)/float(sx),float(wsy)/float(sy))
        print(cx,cy)
        for y in range(sy):
            for x in range(sx):
                color=self.terrain[y][x]
                pygame.draw.rect(window.screen, color, (x*cx,y*cy,cx+1,cy+1), 0)

    def plot(self):
        scipy.misc.toimage(self.terrain)

class Main:

    def __init__(self):
        self.map=Map()
        self.window=Window()
        self.play()

    def play(self):
        self.map.plot()
        self.map.show(self.window)
        self.window.flip()
        while self.window.open:
            self.window.check()

main=Main()
