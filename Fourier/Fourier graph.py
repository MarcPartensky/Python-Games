from mywindow import Window
from mycolors import *

from time import time

from random import randint as rd
from math import sin,cos,sqrt
import pygame

class Graph:
    def __init__(self,window,precision=20,speed=0.01,factor=10):
        self.window=window
        #self.window.background_color=WHITE
        self.speed=speed

        #self.coefficients=[[1,1,1] for i in range(self.precision)]
        #self.coefficients=[[10,1,0],[4,5,0],[0.8,29,0]]
        #self.coefficients=[[[rd(1,5)/(i+1),rd(1,5)*(i+1)] for j in range(2)] for i in range(precision)]
        #self.coefficients=[[[-60,1],[50,1]],[[30,1],[18,2]],[[-8,2],[-12,3]],[[10,3],[14,5]]]
        #self.coefficients=[[-60,30,-8,10],[50,18,-12,14]]
        self.coefficients=[(rd(10,20)/(i+1),rd(10,20)/(i+1)) for i in range(precision)]
        self.factor=factor
        self.precision=min(precision,len(self.coefficients))
        self.points=[(0,0) for i in range(self.precision)]
        self.color=self.window.reverseColor(self.window.background_color)
        #print(self.coefficients)
        self.graph=[]
        self.time=0
        self.centerGraph()


    def centerGraph(self):
        x,y=self.window.size
        self.center=x//2,y//2

    def updatePoint(self,precision):
        x,y=(0,0)
        t=self.time
        for i in range(precision):
            X,Y=self.coefficients[i]
            ax,wx=X
            ay,wy=Y
            x+=ax*cos(wx*t)
            y+=ax*sin(wx*t)
        return (x,y)


    def old_update(self):
        #self.time=time()
        self.time+=self.speed
        l=len(self.coefficients)
        for i in range(l):
            self.points[i]=self.updatePoint(i+1)
        self.graph.append(self.points[-1])

    def update(self):
        #self.time=time()
        self.time+=self.speed
        t=self.time
        l=len(self.coefficients)
        x,y=self.points[0]
        for i in range(1,l):
            a,w=self.coefficients[i]
            x+=a*cos(w*t)
            y+=a*sin(w*t)
            self.points[i]=(x,y)
        self.graph.append(self.points[-1])
        #print(self.points[-1],self.graph)

    def __call__(self):
        while self.window.open:
            self.window.check()
            self.update()
            self.show()

    def show(self):
        self.window.clear()
        self.center=self.window.point()
        self.showPoints()
        self.showCircles()
        self.showGraph()
        self.window.flip()

    def adjust(self,point):
        return (int(self.factor*point[0])+self.center[0],int(self.factor*point[1])+self.center[1])

    def showGraph(self):
        graph=[self.adjust(point) for point in self.graph]
        #print(self.graph)
        #print(graph)
        #print(graph)
        if len(graph)>1:
            pygame.draw.lines(self.window.screen,self.color,False,graph,1)


    def showPoints(self,color=GREEN):
        points=[self.adjust(point) for point in self.points]
        radius=2
        for point in points:
            pygame.draw.circle(self.window.screen,color,point,radius,1)

    def showCircles(self,color=RED):
        l=self.precision
        f=self.factor
        temp=(0,0)
        for i in range(0,l-1):
            #px,py=point
            #px,py=temp
            #temp=self.points[i]
            #point=self.points[i]
            #radius=int(f*sqrt((px-x)**2+(py-y)**2))
            #a,b=self.coefficients[i][0][0],self.coefficients[i][1][0]
            #radius=int(f*sqrt(a**2+b**2))
            radius=int(f*self.coefficients[i+1][0])
            #print(radius)
            point=self.adjust(self.points[i])
            #print((x,px),(y,py),radius)
            pygame.draw.circle(self.window.screen,color,point,radius,1)
            #pygame.draw.circle(self.window.screen,self.color,point,1,1)
            #pygame.draw.circle(self.window.screen,color,point,radius,0)



if __name__=="__main__":
    window=Window("Fourier Graph",size=[1400,900],fullscreen=True)
    graph=Graph(window)
    graph()
