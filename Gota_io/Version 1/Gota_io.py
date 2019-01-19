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

BLUE    = (  0,  0,255)
RED     = (255,  0,  0)
YELLOW  = (255,255,  0)
BLACK   = (  0,  0,  0)
GREY    = (127,127,127)
WHITE   = (255,255,255)

COLORS=[BLACK,WHITE,RED,YELLOW,BLUE]

#-------#
#Classes#
#-------#

class Window:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont(FONT, 65)
        info = pygame.display.Info()
        w=info.current_w
        h=info.current_h
        self.size=(w/2,h/2)
        self.screen=pygame.display.set_mode(self.size)
        pygame.display.set_caption(GAME_NAME)
        pygame.display.flip()
    def select(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    return (event.pos[0],event.pos[1])
    def point(self):
        for event in pygame.event.get():
            return (event.pos[0],event.pos[1])
    def display(self):
        pygame.display.flip()

class Map:
    def __init__(self,size=(100,100),colors=(BLACK,GREY,WHITE)):
        self.colors=(self.background_color,self.axes_color,self.borders_color)=colors
        self.size=size
        self.map=np.zeros(self.size)


class Player:
    def __init__(self,name=None,skin=None):
        self.name=name
        self.skin=skin
        self.color=random.choice(COLORS)
        self.speed_constant=10
    def spawn(self,map):
        self.alive=True
        self.map=map
        self.position=(random.choice(range(self.map.size[0])),random.choice(range(self.map.size[1])))
        self.cursor=(random.choice(range(self.map.size[0])),random.choice(range(self.map.size[1])))
        self.speed=self.speed_constant
        self.mass=100
        self.grow()
        self.latest_move_time=time.time()
    def grow(self):
        self.size=sqrt(self.mass/math.pi) #A=pi*r^2
        self.hitbox=self.size/2
        f=self.view_factor=self.size*10
        self.view_field=(-f,-f,2*f,2*f)
    def draw(self,window,position):
        if self.skin is not None:
            self.skin.draw(window,position)
        (_x,_y)=self.position
        (x,y)=(int(_x),int(_y))
        pygame.draw.circle(window.screen, self.color, (x,y), int(self.size))
    def closest(self,entities):
        entities.remove(self)
        r=9999
        for _entity in entities:
            (x,y)=_entity.position
            _r=sqrt(x**2+y**2)
            if _r<r:
                entity=_entity
                r=min(r,_r)
        return entity
    def getPolar(self,cartesian):
        (x,y)=cartesian
        p=sqrt(x**2+y**2)
        o=math.atan(y/x)
        polar=(p,o)
        return polar
    def getCartesian(self,polar):
        (p,o)=polar
        (x,y)=(p*math.cos(o),p*math.sin(o))
        cartesian=(x,y)
        return cartesian
    def move(self,window):
        wsx,wsy=window.size
        tx,ty=wsx//2,wsy//2
        (x,y)=self.position
        (cx,cy)=self.cursor=pygame.mouse.get_pos()
        self.direction=(cx-tx,cy-ty)
        (p,o)=self.getPolar(self.direction)
        new_move_time=time.time()
        delta_time=new_move_time-self.latest_move_time
        self.latest_move_time=new_move_time
        self.speed=(self.speed_constant*delta_time)/self.mass
        p*=self.speed
        (px,py)=self.getCartesian((p,o))
        (x,y)=(px+x,py+y)
        self.position=(x,y)
    def spectate():
        pass



class Human(Player):
    def __init__(self,name=None,skin=None):
        Player.__init__(self)
    def play(self,game):
        if self.alive:
            game.show(self)
            #self.cursor=game.window.point()
            self.move(game.window)
        else:
            self.spawn(game.map)


class Bot(Player):
    def __init__(self,name=None,skin=None):
        Player.__init__(self)

    def play(self,game):
        if self.alive:
            self.cursor=self.analyze(game.entities)
            self.move(game.window)
        else:
            self.spawn(game.map)

    def analyze(self,entities):
        return self.closest(entities).position






class Skin:
    def __init__(self):
        self.size=100

    def draw(self,window,position):
        pass

class Gota_io:
    def __init__(self,window,map,entities):
        self.window=window
        self.map=map
        self.entities=entities
        self.active=True

    def play(self):
        while self.active:
            for entity in self.entities:
                entity.play(self)

    def show(self,player):
        self.window.screen.fill(self.map.background_color)
        (x,y,sx,sy)=player.view_field
        px,py=player.position
        player.draw(self.window,(0,0))
        for entity in self.entities:
            (x,y)=entity.position
            if x<x<sx and y<y<sy:
                position=(x-px,y-py)
                entity.draw(self.window,position)
        self.window.display()

    def collision(self,player1,player2):
        pass


class Manager:
    def __init__(self):
        self.window=Window()

        self.play()

    def play(self):
        self.players=PLAYERS
        self.player=PLAYERS[0]
        self.map=Map()
        game=Gota_io(self.window,self.map,self.players)
        for player in self.players:
            player.spawn(game.map)
        game.play()

#-----------------#
#Default Variables#
#-----------------#

DISPLAY=True
FONT="monospace"
PLAYERS=[Human("Marc"),Bot(),Bot(),Bot()]
PLAYERS=[Human("Marc")]
DIRECTORY="/Users/olivierpartensky/Programs/Library/Puissance4/"
os.chdir(DIRECTORY)

#-------#
#Actions#
#-------#

if __name__ == "__main__":
    main=Manager()
