#-------#
#Credits#
#-------#

__author__="Marc Partensky"
__license__="Marc Partensky Company"
__game__="Ball Control"

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
    DIRECTORY="/Users/olivierpartensky/Programs/Python/Games/Ball Control/"
    os.chdir(DIRECTORY)
finally:
    pass

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



def Entity:
    def __init__(self,name):
        self.name=name
        self.alive=False
        self.gravity=[0,9.81]
    def spawn(self,map,position,force=self.gravity):
        self.alive=True
        self.position=[0,0]
        self.velocity=[0,0]
        self.acceleration=force
    def move(self):
        x,y=self.position
        sx,sy=self.speed
        ax,ay=self.acceleration
        sx+=ax
        sy+=ay
        self.speed=sx,sy
        x+=sx
        y+=sy
        self.position=x,y
    def affectBorder(self,map):
        map.size


    def show(self,window):
        window.draw(self.color,self.position,self.size)
    def kill(self):
        self.alive=False

class Paddle:
    def __init__(self,window):
        self.color=BLUE
        wx,wy=window.size
        self.entry=wy/10
        y1=random.choice([0,wy])
        y2=random.randint(0,wy)
        ym=min(y1,y2)
        yM=max(y1,y2)
        self.size=[wx/5,yM-ym]
        self.position=[wx-self.size[0],ym]
        self.speed=[-7,0]
        self.acceleration=[0,0]

    def checkCollision(self,entity):
        x,y=self.position
        xs,ys=self.size
        sx,sy=self.speed
        ex,ey=entity.position
        esx,esy=entity.speed
        if y<ey<y+ys and x<ex<x+xs:
            entity.speed=[sx,sy]
    def show(self,window):
        window.draw(self.color,self.position,self.size)

class Ball:
    def __init__(self,window,color,radius):
        self.color=color
        self.radius=radius
        self.action=10
        self.gravity_constant=9.81
        self.air_friction=[0.01,0.01]
        self.border_friction=[0.05,0.05]

    def spawn(self,window):
        wx,wy=window.size
        self.position=[random.randint(0,wx),random.randint(0,wy)]
        self.speed=[0,0]
        self.acceleration=[0,self.gravity_constant]

    def move(self,time):
        ax,ay=self.acceleration
        vx,vy=self.speed
        x,y=self.position
        vx+=ax*time
        vy+=ay*time
        self.speed=vx,vy
        x+=vx*time
        y+=vy*time
        self.position=int(x),int(y)

    def borderChanges(self,window):
        x,y=self.position
        vx,vy=self.speed
        wx,wy=window.size
        if x<0:
            x=0
            vx=-vx
        if x>wx:
            x=wx
            vx=-vx
        if y<0:
            y=0
            vy=-vy
        if y>wy:
            y=wy
            vy=-vy
        fx,fy=self.border_friction
        vx*=1-fx
        vy*=1-fy
        self.position=x,y
        self.speed=vx,vy

    def lead(self,window):
        vx,vy=self.speed
        a=self.action
        keys=pygame.key.get_pressed()
        if keys[K_LEFT]:
            vx-=a
        if keys[K_RIGHT]:
            vx+=a
        if keys[K_UP]:
            vy-=a
        if keys[K_DOWN]:
            vy+=a
        self.speed=vx,vy

    def frictionChanges(self):
        vx,vy=self.speed
        fx,fy=self.air_friction
        vx*=(1-fx)
        vy*=(1-fy)
        self.speed=vx,vy


    def play(self,time,window):
        self.move(time)
        self.borderChanges(window)
        self.frictionChanges()

    def show(self,window):
        window.screen.fill(window.color)
        pygame.draw.circle(window.screen, self.color, self.position, self.radius, 0)

#Main#

class Game:
    def __init__(self):
        self.name="Ball Control"
        self.window_color=BLACK
        self.ball_color=GREEN
        self.ball_radius=20
        self.time=1

        self.window=Window(self.name,self.window_color)
        self.window.flip()
        self.ball=Ball(self.window,self.ball_color,self.ball_radius)

        self.play()

    def show(self):
        self.ball.show(self.window)
        self.paddle.show(self.window)
        self.window.flip()

    def play(self):
        sent=0
        self.paddle=Paddle(self.window)
        instant=int(time.time())
        self.ball.spawn(self.window)
        while self.window.opened:
            if int(time.time())-instant>1:
                print(sent)
                instant=int(time.time())
                sent+=1
                self.paddle=Paddle(self.window)
            self.window.check()
            self.ball.lead(self.window)
            self.paddle.move()
            self.paddle.checkCollision(self.ball)
            self.ball.play(self.time,self.window)
            self.show()


#-------#
#Actions#
#-------#

game=Game()
