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
        wsx,wsy=game.window.size
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

    def eatCheck(self,game):
        mass=self.mass
        entities=game.entities[:]
        for entity in entities:
            pass

    def show(self,game):
        x,y=self.position
        mx,my=game.map.size
        wsx,wsy=game.window.size
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
        raw_positions=[]
        for entity in entities:
            ex,ey=entity.position
            raw_positions.append((int(((ex-x)*wsx)/mx)+tx,int(((ey-y)*wsy)/my)+ty))
        for i,entity in enumerate(entities):
            #print("entity=",entity)
            r=self.radius
            h=r//2
            raw_position=raw_positions[i]
            #print(entity,": position=",raw_position)
            if self.skin is not None:
                self.skin.draw(game.window,raw_position)
            else:
                pygame.draw.circle(game.window.screen, entity.color, raw_position, entity.radius, 0)




class Human(Player):
    def __init__(self,game,name="No name",skin=None):
        Player.__init__(self,game,name)
        self.color=BLUE
    def update(self,game):
        wsx,wsy=game.window.size
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
        far=10
        self.cursor=(far*(cpx-px),far*(cpy-py))






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
        self.window=Window(self,size=[1400,800])
        self.player=Human(self,"Marc")
        self.players=[self.player]+[Bot(self) for i in range(5)]
        self.objects=[Food(self) for i in range(100)]
        self.entities=self.players+self.objects
        self.gametick=0.1
        self.collision_counter=[0,0] #temporary

    def play(self):
        self.start()
        self.loop()
        self.end()

    def start(self):
        for object in self.objects:
            object.spawn(self)
        for player in self.players:
            player.spawn(self)

    def loop(self):
        while self.window.open:
            self.window.check()
            self.update()
            quadtree=self.getQuadtree()
            #print(quadtree)
            #self.allCollision()
            self.show()
            #time.sleep(self.gametick)

    def end(self):
        self.window.kill()
        #print(self.collision_counter)

    def getQuadtree(self):
        raw_positions=[]
        for entity in self.entities:
            raw_positions.append(entity.position)
        return Quadtree((0,0), self.map.size ,1,raw_positions,self.window).squares


    def update(self):
        for player in self.players:
            player.update(self)

    def show(self):
        self.window.screen.fill(self.map.background_color)
        self.player.show(self)
        self.window.flip()

    def allCollision(self):
        l=len(self.entities)
        for a in range(l):
            entity1=self.entities[a]
            for b in range(a):
                entity2=self.entities[b]
                collided=self.twosCollision(entity1,entity2)
                print(collided)
                c=int(collided)
                self.collision_counter[c]+=1

    def twosCollision(self,entity1,entity2):
        x1,y1=entity1.position
        r1=entity1.radius
        x2,y2=entity2.position
        r2=entity2.radius
        if abs(x1-x2)<r1+r2 or abs(x1-x2)<r1+r2:
            return True
        else:
            return False






#-------#
#Default#
#-------#

#DIRECTORY="/Users/olivierpartensky/Programs/Library/Gota.io/"
#os.chdir(DIRECTORY)

#-------#
#Actions#
#-------#

if __name__ == "__main__":
    Game().play()
