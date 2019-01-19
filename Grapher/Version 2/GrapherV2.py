#-------#
#Credits#
#-------#

__author__="Marc Partensky"
__license__="Marc Partensky Company"
__title__="Grapher"

"""This program needs pygame to be run."""

#------------#
#Dependencies#
#------------#

from mycolors import *
from mywindow import *
from mymoves import *
from mycontrols import *


import math
import random
import numpy as np

#-------#
#Classes#
#-------#

class Graph:
    def __init__(self,function,color=RED):
        self.function=function
        self.color=color
        self.dots=[]

    def trace(self,plan,window):
        self.dots=[]
        ux,uy=plan.units
        mx,my=plan.middle
        px,py=plan.point
        wsx,wsy=window.size
        tx,ty=(wsx//2,wsy//2)
        for i in range(-tx+mx,tx+mx):
            x=float(i)/ux
            y=eval(self.function)
            X=x*ux+tx-mx
            Y=-y*uy+ty-my
            #print((x,y),(X,Y))
            if 0<=X<wsx and 0<=Y<wsy:
                self.dots.append((X,Y))

    def draw(self,plan,window):
        self.trace(plan,window)
        for i in range(len(self.dots)-1):
            start=self.dots[i]
            end=self.dots[i+1]
            pygame.draw.line(window.screen, self.color, start, end, 1)


class Plan:
    def __init__(self,background=WHITE,axis_color=BLACK,grid_color=DARKGREY):
        self.background=background
        self.axis_color=axis_color
        self.grid_color=grid_color
        self.graphs=[]
        self.default_middle=self.middle=[0,0]
        self.default_point=self.point=[0,0]
        self.default_units=self.units=[50,50]

    def addGraph(self,graph):
        self.graphs.append(graph)

    def draw(self,window):
        window.screen.fill(self.background)
        wsx,wsy=window.size
        translation=[wsx//2,wsy//2]
        self.drawAxis(window)
        for i,graph in enumerate(self.graphs):
            graph.draw(self,window)
            position=[wsx-200,wsy-(2+i)*30]
            window.showText(graph.function,position,graph.color,"monospace",20)

    def drawAxis(self,window):
        wsx,wsy=window.size
        ux,uy=self.units
        mx,my=self.middle
        tx,ty=(wsx//2,wsy//2)
        for x in range(0,wsx):
            if (x-tx+mx)%int(ux)==0:
                pygame.draw.line(window.screen, self.grid_color, (x,0),(x,wsy),1)
        for y in range(0,wsy):
            if (y-ty+my)%int(uy)==0:
                pygame.draw.line(window.screen, self.grid_color, (0,y),(wsx,y),1)
        pygame.draw.line(window.screen, self.axis_color, (tx-mx,0),(tx-mx,wsy),1)
        pygame.draw.line(window.screen, self.axis_color, (0,ty-my),(wsx,ty-my),1)


    def move(self,window,controller):
        wsx,wsy=window.size
        tx,ty=wsx//2,wsy//2
        mx,my=self.middle
        ux,uy=self.units
        middle_step=10
        zoom_step=0.1
        key=controller.pressed()
        if key[K_LEFT]:
            mx-=middle_step
        if key[K_RIGHT]:
            mx+=middle_step
        if key[K_DOWN]:
            my+=middle_step
        if key[K_UP]:
            my-=middle_step
        if key[K_RSHIFT]:
            #print(ux,uy)
            ux*=(1.+zoom_step)
            uy*=(1.+zoom_step)
        if key[K_LSHIFT]:
            if ux>2.:
                ux/=(1.+zoom_step)
            if uy>2.:
                uy/=(1.+zoom_step)
        if key[K_RETURN]:
            px,py=self.default_point
            mx,my=self.default_middle
            ux,uy=self.default_units

        px,py=pygame.mouse.get_pos()
        px=px+tx
        py=py+ty
        self.middle=mx,my
        self.units=ux,uy
        self.point=px,py


class Grapher:
    def __init__(self,functions,settings=None):
        if settings is None:
            self.setDefaultSettings()
        else:
            self.setNewSettings(settings)

        self.name="Grapher"
        self.controller=Controller()
        self.window=Window(self,self.window_size)
        self.plan=Plan(BLACK,WHITE)
        for function,color in zip(functions,self.graph_colors):
            self.graph=Graph(function,color)
            self.plan.addGraph(self.graph)
        self.plan.draw(self.window)
        self.session()

    def session(self):
        while self.window.open:
            self.window.check()
            #self.plan.control()
            self.show()
        self.window.kill()

    def show(self):
        self.plan.move(self.window,self.controller)
        self.plan.draw(self.window)
        self.window.flip()

    def setNewSettings(self,settings):
        self.window_size=settings[0]
        self.plan_units=settings[1]
        self.graph_colors=settings[2]
        self.settings=settings

    def setDefaultSettings(self):
        self.window_size=(1000,700)
        self.plan_units=[10,10]
        self.graph_colors=[RED,BLUE,GREEN,YELLOW,WHITE,PURPLE,GREY,DARKBLUE,DARKRED,DARKGREEN]
        self.settings=self.window_size,self.plan_units,self.graph_colors

#-------#
#Actions#
#-------#

functions=["random.uniform(0,1)","math.cos(x)","math.exp(x)"]

Grapher=Grapher(functions)
