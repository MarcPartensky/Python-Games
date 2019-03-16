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
import noise


BLUE      = (  0,  0,255)
RED       = (255,  0,  0)
GREEN     = (  0,255,  0)
YELLOW    = (255,255,  0)
BLACK     = (  0,  0,  0)
WHITE     = (255,255,255)
GREY      = (100,100,100)
PURPLE    = (100,  0,100)
DARKGREY  = ( 20, 20, 20)
DARKRED   = ( 10, 10, 10)
DARKGREEN = ( 10, 10, 10)
DARKBLUE  = ( 10, 10, 10)


#-------#
#Classes#
#-------#

class Graph:
    def __init__(self,function,color=RED):
        self.function=function
        self.color=color
        self.dots=[]
        self.precision=1

    def trace(self,plan,window):
        self.dots=[]
        zx,zy=plan.zoom
        ux,uy=plan.units
        mx,my=plan.middle
        px,py=plan.point
        wsx,wsy=window.size
        tx,ty=(wsx//2,wsy//2)
        for X in range(0,wsx,self.precision):
            x=((X-tx)/zx+mx)/ux
            #y=eval(self.function)
            y=self.function(x)
            Y=(ty-(y*uy+my)*zy)
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
        self.velocity=[1,1]
        self.acceleration=[0,0]
        self.action=[10,10]
        self.friction=[2,2]
        self.zoom=[1.,1.]

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
            window.showText(str(graph.function),position,graph.color,"monospace",20)

    def drawAxis(self,window):
        wsx,wsy=window.size
        ux,uy=self.units
        mx,my=self.middle
        zx,zy=self.zoom
        tx,ty=(wsx//2,wsy//2)
        for x in range(0,int(ux/zx)):
            X=ux*x*zx
            P=tx-mx*zx
            pygame.draw.line(window.screen, self.grid_color, (P-X,0),(P-X,wsy),1)
            pygame.draw.line(window.screen, self.grid_color, (P+X,0),(P+X,wsy),1)
        #for y in range(-ty,ty,int(float(uy)*zy)):
        #Y=y-my*zy+ty
        for y in range(0,int(uy/zy)):
            Y=uy*y*zy
            P=ty-my*zy
            pygame.draw.line(window.screen, self.grid_color, (0,P-Y),(wsx,P-Y),1)
            pygame.draw.line(window.screen, self.grid_color, (0,P+Y),(wsx,P+Y),1)
        X,Y=(tx-mx*zx,ty-my*zy)
        pygame.draw.line(window.screen, self.axis_color, (X,0),(X,wsy),1)
        pygame.draw.line(window.screen, self.axis_color, (0,Y),(wsx,Y),1)


    def move(self,window,controller):
        wsx,wsy=window.size
        tx,ty=wsx//2,wsy//2
        mx,my=self.middle
        ux,uy=self.units
        zx,zy=self.zoom
        vx,vy=self.velocity
        ax,ay=self.acceleration
        acx,acy=self.action
        fx,fy=self.friction
        middle_step=min(ux,uy)
        zoom_step=0.1
        pressed=False
        key=controller.pressed()
        if key[K_LEFT]:
            ax=-acx/zx
        if key[K_RIGHT]:
            ax=acx/zx
        if key[K_DOWN]:
            ay=acy/zy
        if key[K_UP]:
            ay=-acy/zy
        vx+=ax
        vy+=ay
        mx+=vx
        my+=vy
        vx/=fx
        vy/=fy
        ax,ay=[0,0]
        if key[K_RSHIFT]:
            zx*=(1.+zoom_step)
            zy*=(1.+zoom_step)
        if key[K_LSHIFT]:
            if zx>0.1:
                zx/=(1.+zoom_step)
            if zy>0.1:
                zy/=(1.+zoom_step)
        if key[K_RETURN]:
            px,py=self.default_point
            mx,my=self.default_middle
            ux,uy=self.default_units
        if pygame.mouse.get_pressed()[0]:
            pressed=bool(pygame.mouse.get_pressed()[0])
            ax,ay=pygame.mouse.get_pos()
            mx+=int(float(ax-tx)*0.1)
            my+=int(float(ay-ty)*0.1)
        self.acceleration=ax,ay
        self.velocity=vx,vy
        self.middle=mx,my
        self.units=ux,uy
        self.zoom=zx,zy


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

if __name__=="__main__":
    functions=[math.sin,math.cos,math.exp,lambda x:x**3-2*x+1]
    Grapher=Grapher(functions)
