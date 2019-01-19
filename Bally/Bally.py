GAME_NAME="Bally"
DIRECTORY="/Users/olivierpartensky/Programs/Library/Bally/"

DISPLAY=True
FONT="monospace"

BLUE    = (  0,  0,255)
RED     = (255,  0,  0)
YELLOW  = (255,255,  0)
BLACK   = (  0,  0,  0)
GREY    = (127,127,127)
WHITE   = (255,255,255)
COLORS=[BLACK,WHITE,RED,YELLOW,BLUE]

import random
import numpy as np
import pygame
import time
from pygame.locals import *

class Window:
    made=0
    def __init__(self,size=None,title=GAME_NAME,font=FONT):
        Window.made+=1
        self.number=Window.made
        self.title=title
        self.font=font
        pygame.init()
        self.font = pygame.font.SysFont(self.font, 65)
        info = pygame.display.Info()
        if size is None:
            self.size=(info.current_w/2,info.current_h/2)
        else:
            self.size=size
        self.screen=pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.title)
        pygame.display.flip()
    def adapt(self,picture,size):
        return pygame.transform.scale(picture,size)

    def closed(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
    def select(self):
        done=False
        while self.closed():
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    return (event.pos[0],event.pos[1])
    def point(self):
        for event in pygame.event.get():
            return (event.pos[0],event.pos[1])
    def flip(self):
        pygame.display.flip()
    def draw(self,picture,position):
        self.screen.blit(picture, position)
    def drawAll(self,map):
        self.draw(self.background,(0,0))
        for entity in map.entities:
            self.draw(entity.picture,entity.position)


class Character:
    made=0
    def __init__(self,name,picture_directory,size=None):
        self.number=Character.made
        Character.made+=1
        self.name=name
        self.picture_directory=DIRECTORY+picture_directory
        self.size=size
        self.picture=pygame.image.load(self.picture_directory).convert()

class Entity:
    made=0
    def __init__(self,character,size,mass,max_life,spawner):
        self.number=Entity.made
        Entity.made+=1
        self.character=character
        self.size=size
        self.mass=mass
        self.spawner=spawner
        self.position=self.spawner.position
        self.speed=[0,0]
        self.acceleration=[0,0]
        self.picture=pygame.transform.scale(self.character.picture,self.size)
        self.max_life=
        self.life=0
        self.alive=False
    def move(self):
        x,y=self.position
        sx,sy=self.speed
        ax,ay=self.acceleration
        sx+=ax
        sy+=ay
        self.speed=[sx,sy]
        x+=sx
        y+=sy
        self.position=[x,y]
    def bounce(self,sense):
        self.speed=self.direction

class Map:
    made=0
    def __init__(self,name,background_directory,gravity=False):
        Map.made+=1
        self.name=name
        self.number=Map.made
        self.entities=[]
        self.background_directory=DIRECTORY+background_directory
        self.background=pygame.image.load(self.background_directory)
        self.size=[100,100]
        self.entity_size=[50,50]
        self.gravity=gravity
        self.gravitational_constant=9.81
        self.tick=10

    def spawnAll(self):
        for entity in self.entities:
            self.spawn(entity)
    def spawn(self,entity):
        position=entity.spawner
        entity.alive=True
    def affectGravity(self,entity):
        g=self.gravitational_constant
        entity.acceleration=[0,-g]
    def add(self,entity):
        entity=Entity(character,position)
        if gravity:
            self.affectGravity(entity)
        self.entities.append(entity)
        self.entities.append(entity)
    def delete(self,entity):
        self.entities.remove(entity)
    def update(self):
        ticks=int(time.time()*1000)
        dt=self.tick
        if ticks%dt==0:
            for entity in self.entities:
                entity.move()
    def generate(self,window):
        msx,msy=self.size
        wsx,wsy=window.size
        case_size=(wsx/msx,wsy/msy)
        window.background=window.adapt(self.background,(0,0))
        self.spawnAll()
        window.drawAll(self)
        while not window.closed():
            self.update()
            window.drawAll(self)
            window.flip()

class Ball(Entity):
    def __init__(self,radius=100,color=None):
        Entity.__init__(self,name="Ball")
        self.color=color
        self.radius=radius
        self.size=[self.radius*2]*2



class Manager:
    def __init__(self):
        self.window=Window(size=(1000,600))
        self.map=Map(name="Jupiter",background_directory="Pictures/jupiter.jpg")
        Kirby=Character(name="Kirby",picture_directory="Pictures/kirby.png")
        self.characters=[Kirby]
        for entity in self.entities:
            self.map.add(entity)
        #self.ball=Ball()
    def action1(self):
        #self.map.add(self.ball)
        self.map.generate(self.window)


main=Manager()
main.action1()
