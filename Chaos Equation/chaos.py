from mywindow import Window
from mycolors import *
from math import sqrt
from random import randint
import pygame

class Chaos:
    def __init__(self,window,equations,number=255,radius=1,start=0,delta=0.000001):
        fx,fy=equations
        self.start=start
        self.window=window
        self.window.name="Chaos"
        self.window.size=[1440,900]
        self.window.fullscreen=True
        self.window.build()
        self.fx=fx
        self.fy=fy
        self.number=number
        #self.colors=[self.window.randomColor() for i in range(number)]
        self.colors=[(i,0,0) for i in range(number)]
        self.radius=radius
        wsx,wsy=window.size
        self.positions=[[wsx//2,wsy//2] for i in range(number)]
        #self.points=self.generate(number,window.size)
        self.delta=delta

    def old_generate(self,number,size):
        sx,sy=size
        #return [[randint(0,sx-1),randint(0,sy-1),self.window.randomColor()] for i in range(number)]
        return [[0,0,self.window.randomColor()] for i in range(number)]

    def old1_generate(self,position,t,number):
        x,y=position
        points=[]
        for i in range(number):
            points.append([x,y])
            nx=fx(x,y,t)
            ny=fy(x,y,t)
            x,y=nx,ny
        return points



    def __call__(self):
        self.time=self.start
        while self.window.open:
            self.window.check()
            #self.update()
            self.show()
            self.time+=self.delta

    def update(self,t=1):
        for i,point in enumerate(self.points):
            x,y=point
            nx=self.fx(x,y,t)
            ny=self.fy(x,y,t)
            self.points[i]=[nx,ny]
            print([nx,ny])

    def show(self):
        t=self.time
        #print(t)
        wsx,wsy=window.size
        self.window.clear()
        positions=[]
        x,y=t,t

        for i in range(self.number):
            nx=self.fx(x,y,t)
            ny=self.fy(x,y,t)
            x,y=nx,ny
            #print([x,y])
            if not (-1<x<1 and -1<y<1):
                break
            px=convert(x,[-1,1],[0,wsx])
            py=convert(y,[-1,1],[0,wsy])
            position=[px,py]
            position=self.integer(position)
            positions.append(position)

        md=1
        for i in range(min(len(positions),len(self.positions))):
            #print(positions[i],self.positions[i])
            x1,y1=positions[i]
            x2,y2=self.positions[i]
            d=distance(x2-x1,y2-y1)
            md=max(d,md)
        print(md)

            #pygame.draw.circle(self.window.screen,c,positions[i],self.radius,0)
        for i in range(min(len(positions),len(self.positions))):
            c=self.window.wavelengthToRGB(convert(d,[md,0],[380,780]))
            pygame.draw.line(self.window.screen,c,self.positions[i],positions[i],1)

        self.delta=0.001/md**10

        self.positions=positions[:]

        #pygame.draw.lines(self.window.screen,WHITE,0,positions,1)

        self.window.flip()

    def integer(self,position):
        return [int(x) for x in position]

def distance(x,y):
    return sqrt(x**2+y**2)





def convert(number,interval1,interval2):
    im1,iM1=interval1
    im2,iM2=interval2
    s=(iM2-im2)/(iM1-im1) #scaling
    return (number-im1)*s+im2

if __name__=="__main__":
    window=Window()
    print(window.inWindow([2,4]))
    fx=lambda x,y,t:-x**2+x*t+y
    fy=lambda x,y,t:x**2-y**2-t**2-x*y+y*t-x+y
    equations=[fx,fy]
    chaos=Chaos(window,equations)
    chaos()
