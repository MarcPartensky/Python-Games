from myentity import Entity
from mywindow import Window
from mycolors import *

from random import randint as rdt
from math import cos,sin,sqrt,atan,pi,exp
from cmath import phase

import pygame

sigmoid=lambda x:1/(1+exp(-5*(2*x-1.5)))
sigmoid=lambda x:-cos(3*x)/2+1/2
sigmoid=lambda x:x**2


class Rectangle(Entity):
    def __init__(self,position,size,borders,friction,controllable,color=WHITE):
        Entity.__init__(self,position=position,size=size,borders=borders,friction=friction,controllable=controllable)
        self.borders=borders
        self.color=color
        self.rectangles=[]
        self.moving_function=lambda x:100*sin(x/10)
        
    def old_update(self,input):
        cursor,keys=input
        self.direct(cursor)
        self.follow()
        self.affectFriction()
        self.move()
        self.affectBorders()
        #print(self.velocity,self.acceleration)
        for rectangle in self.rectangles:
            #print(rectangle.borders)
            rectangle.borders[:2]=self.position
            rectangle.update(input)
        #print(self.position)

    def duplicate(self,number):
        if number>0:
            #print(self.size)
            borders=self.position+self.size
            sx,sy=self.size
            position=[rdt(0,sx//2),rdt(0,sy//2)]
            size=[sx//2,sy//2]
            #print(size)
            friction=self.friction
            entity=Rectangle(position=position,size=size,borders=borders,friction=friction,controllable=self.controllable)
            entity.duplicate(number-1)
            self.rectangles.append(entity)

    def old_direct(self,cursor):
        bx,by,bsx,bsy=self.borders
        cx,cy=cursor
        px,py=self.position
        #print("e:",cx,bx,bsx,px)
        dx,dy=[(cx-bx)-(bsx//4+px),(cy-by)-(bsy//4+py)]
        #dx,dy=[(cx-whx)-(px-hx),(cy-why)-(py-hy)]
        #print("s:",dx,dy)
        a=phase(complex(dx,dy))
        n=sqrt(dx**2+dy**2)
        n_max=sqrt((bsx//2)**2+(bsy//2)**2)
        #if n<1: print(dx,dy)
        n=sigmoid(n/n_max)*5
        #print(n)
        self.direction=[a,n]

    def show(self,window):
        for rectangle in self.rectangles:
            rectangle.show(window)
        #self.borders[i]
        raw_position=[self.position[i]+self.borders[i] for i in range(self.dimensions)]
        raw_coordonnates=raw_position+self.size
        pygame.draw.rect(window.screen,self.color,raw_coordonnates,1)
        window.print(str(raw_position),position=raw_position)
