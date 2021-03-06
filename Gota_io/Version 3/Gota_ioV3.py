#-------#
#Credits#
#-------#

__author__=   "Marc Partensky"
__license__=  "Partensky Company"
__game__=     "Gota.io"

#------------#
#Importations#
#------------#

from mywindow import *
from mycolors import *
from Quadtree import *

import pygame
from pygame.locals import *
import numpy as np
import random
import os
import math
import copy
from math import *
import time

#-------------#
#Complementary#
#-------------#

def modified_sigmoid(x):
  return 2/(1+math.exp(-5*x))-1

#-------#
#Classes#
#-------#

class Map:
    def __init__(self,size=(100,100),colors=(BLACK,GREY,WHITE)):
        self.colors=(self.background_color,self.grid_color,self.borders_color)=colors
        self.size=size

class Food:
    def __init__(self,game):
        self.color=random.choice(COLORS)
        self.automatic_respawn=True
        self.radius_constant=5
    def spawn(self,game):
        map=game.map
        self.position=(random.choice(range(map.size[0])),random.choice(range(map.size[1])))
        self.mass=random.randint(5,10)
        self.grow()
    def grow(self):
        self.radius=int(sqrt(self.mass/math.pi))*self.radius_constant #A=pi*r^2
        self.hitbox=self.radius/2

class Player:
    def __init__(self,game,name=None,skin=None):
        self.name=name
        self.skin=skin
        self.active=True
        self.color=WHITE
        self.action=50
        self.radius_constant=5
        self.automatic_respawn=True
        self.reach=1./4.
        self.velocity_constant=10.
    def spawn(self,game):
        map=game.map
        self.alive=True
        self.position=(random.choice(range(map.size[0])),random.choice(range(map.size[1])))
        self.cursor=[0,0]
        self.velocity=[0,0]
        self.mass=random.randint(50,100)
        self.grow()
    def grow(self):
        self.radius=int(sqrt(self.mass/math.pi))*self.radius_constant #A=pi*r^2
        self.hitbox=self.radius/2
        f=self.view_factor=self.radius*10
        self.view_field=(-f,-f,2*f,2*f)
        self.max_velocity=self.velocity_constant/self.radius
    def closeCheck(self,game):
        (x,y)=self.position
        players=game.players[:]
        #print
        players.remove(self)
        #print(game.players,players)
        d=9999
        for i,player in enumerate(players):
            (px,py)=player.position
            nd=sqrt((px-x)**2+(py-y)**2)
            #print(i,nd,player.position)
            if nd<d:
                closest=player
                d=min(d,nd)
        self.closest=closest
        #print(i,"self.closest=",self.closest)
        #time.sleep(0.1)
    def move(self,game):
        wsx,wsy=self.window.size
        x,y=self.position
        cx,cy=self.cursor
        mx,my=game.map.size
        mv=self.max_velocity
        r=self.reach
        a=self.action
        wsm=min(wsx,wsy)
        #print("self.cursor=",self.cursor)
        #print(modified_sigmoid(cx/(r*wsm)))
        vx,vy=(mv*modified_sigmoid(cx/(r*wsm)),mv*modified_sigmoid(cy/(r*wsm)))
        self.velocity=vx,vy
        x+=vx
        y+=vy
        self.position=x,y
        #print("self.velocity=",self.velocity)
        #print("self.position=",self.position)
    def spectate():
        pass
    def show(self,game):
        if self.window.open:
            self.window.check()
            self.window.screen.fill(game.map.background_color)
            self.draw(game)
            self.window.flip()
        else:
            self.active=False
    def eatCheck(self,game):
        mass=self.mass
        entities=game.entities[:]
        for entity in entities:
            pass

    def draw(self,game):
        x,y=self.position
        mx,my=game.map.size
        wsx,wsy=self.window.size
        tx,ty=(wsx//2,wsy//2)
        entities=game.entities[:]
        _list=[(entities[i],entities[i].mass) for i in range(len(entities))]
        sorted_list=sorted(_list,key=lambda _list:_list[1])
        #print(sorted_list)
        entities=[sorted_list[i][0] for i in range(len(entities))]
        #print(entities)
        #print(sorted_list)
        #time.sleep(5)
        #print("in draw","entities=",game.entities)
        #Quadtree((0,0),(wsx,wsy),1,entities,self.window)
        for entity in entities:
            #print("entity=",entity)
            ex,ey=entity.position
            r=self.radius
            h=r//2
            raw_position=(int(((ex-x)*wsx)/mx)+tx+h,int(((ey-y)*wsy)/my)+ty+h)
            #print(entity,": position=",raw_position)
            if self.skin is not None:
                self.skin.draw(game.window,raw_position)
            else:
                pygame.draw.circle(self.window.screen, entity.color, raw_position, entity.radius, 0)




class Human(Player):
    def __init__(self,game,name="No name",skin=None):
        Player.__init__(self,game,name)
        self.window=Window(game,size=[1200,800])
        self.color=BLUE
    def update(self,game):
        wsx,wsy=self.window.size
        tx,ty=wsx//2,wsy//2
        if self.alive:
            px,py=pygame.mouse.get_pos()
            self.cursor=px-tx,py-ty
            #print(self.cursor)
            self.move(game)
        if not self.alive and self.automatic_respawn:
            self.spawn(game)



class Bot(Player):
    def __init__(self,game,name="No name",skin=None):
        Player.__init__(self,game,name)
        self.window=Window(game,size=[1200,800],set=False)
        self.color=RED

    def update(self,game):
        if self.alive:
            self.lead(game)
            self.move(game)
        if not self.alive and self.automatic_respawn:
            self.spawn(game)

    def lead(self,game):
        self.closeCheck(game)
        px,py=self.position
        cpx,cpy=self.closest.position
        self.cursor=(cpx-px+10,cpy-py+10)






class Skin:
    def __init__(self):
        self.radius=100

    def draw(self,window,position):
        pass

class Game:
    def __init__(self):
        self.name=__game__
        self.map=Map()
        self.objects=[]
        self.solo=True
        self.solo_player=Human(self,"Marc")
        self.players=[self.solo_player]+[Bot(self) for i in range(5)]
        self.objects=[Food(self) for i in range(100)]
        self.entities=self.players+self.objects
        self.gametick=0.1
        self.active=False
        #self.soloSession()
        self.session()

    def soloSession(self):
        self.active=True
        self.start()

    def session(self):
        self.active=True
        self.start()
        while self.active:
            self.update()
            self.show()
            self.activeCheck()
            #time.sleep(self.gametick)
        self.active=False

    def start(self):
        for object in self.objects:
            object.spawn(self)
        for player in self.players:
            player.spawn(self)
        self.activeCheck()

    def update(self):
        for player in self.players:
            player.update(self)

    def activeCheck(self):
        if self.solo:
            self.soloActiveCheck()
        else:
            self.multiActiveCheck()

    def soloActiveCheck(self):
        self.active=self.solo_player.active
        if not self.active:
            quit()

    def multiActiveCheck(self):
        active=False
        for player in self.players:
            if not player.active:
                self.players.remove(player)
            if isinstance(player,Human):
                active=True
        self.active=active

    def show(self):
        for player in self.players:
            if player.window.open:
                player.show(self)

#-------#
#Default#
#-------#

#DIRECTORY="/Users/olivierpartensky/Programs/Library/Gota.io/"
#os.chdir(DIRECTORY)

#-------#
#Actions#
#-------#

if __name__ == "__main__":
    main=Game()
