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
from scipy.misc import toimage

class Map:
    def __init__(self,size=[20,20]):
        self.size=size
        self.generate()

    def generate(self):
        self.dimensions=3
        self.grid=np.zeros(self.size+[self.dimensions])
        self.terrain=np.zeros(self.size+[self.dimensions])
        sx,sy=self.size
        hx,hy=sx//2,sy//2
        noise=self.getNoise()

        for y in range(sy):
            for x in range(sx):
                self.grid[y][x]=[-hx+x,0,-hy+y]
                self.terrain[y][x]=[-hx+x,50*noise[y][x],-hy+y]

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


    def create(self):
        glBegin(GL_LINES)
        sx,sy=self.size
        """
        for y in range(sy-1):
            for x in range(sx-1):
                glVertex3fv(self.grid[y][x])
                glVertex3fv(self.grid[y+1][x])
                glVertex3fv(self.grid[y][x])
                glVertex3fv(self.grid[y][x+1])
                glVertex3fv(self.grid[y+1][x+1])
                glVertex3fv(self.grid[y][x+1])
                glVertex3fv(self.grid[y+1][x+1])
                glVertex3fv(self.grid[y+1][x])
        """
        for y in range(sy-1):
            for x in range(sx-1):
                glVertex3fv(self.terrain[y][x])
                glVertex3fv(self.terrain[y][x+1])
                glVertex3fv(self.terrain[y][x])
                glVertex3fv(self.terrain[y+1][x])
                glVertex3fv(self.terrain[y+1][x])
                glVertex3fv(self.terrain[y][x+1])
        glEnd()


class main:
    def __init__(self):
        pygame.init()
        display = (800,600)
        pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

        self.angles=[0,1,0,0]

        gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
        glTranslatef(0.0,0.0, -30)

        self.map=Map()
        self.run()

    def checkEvents(self):
        a,ax,ay,az=self.angles

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.open=False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.open=False

            if event.type == KEYDOWN:
                if event.key == pygame.K_a:
                    a+=1
                if event.key == pygame.K_x:
                    ax+=1
                if event.key == pygame.K_y:
                    ay+=1
                if event.key == pygame.K_z:
                    az+=1

        self.angles=a,ax,ay,az


    def run(self):
        self.open=True
        while self.open:
            self.checkEvents()
            self.update()
        pygame.quit()


    def update(self):
        a,ax,ay,az=self.angles
        glRotatef(a, ax, ay, az)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        self.map.create()
        pygame.display.flip()
        pygame.time.wait(10)



main()
