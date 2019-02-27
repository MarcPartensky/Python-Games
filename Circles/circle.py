from mycolors import *
import pygame

class Circle:
    def __init__(self,position,velocity=[0,0],acceleration=[0,0],borders=None,radius=50,color=WHITE,mass=1):
        self.position=position
        self.velocity=velocity
        self.acceleration=acceleration
        self.borders=borders
        self.radius=radius
        self.color=color
        self.mass=mass
        self.alive=False

    def spawn(self):
        self.alive=True

    def update(self):
        self.move()
        if self.borders is not None:
            self.affectBorder()


    def affectBorder(self):
        x,y=self.position
        vx,vy=self.velocity
        X,Y=self.borders
        if not (X[0]<=x<X[1]):
            vx*=-1
            if x<X[0]:
                x=0
            if x>=X[1]:
                x=X[1]-1
        if not (Y[0]<=y<Y[1]):
            vy*=-1
            if y<Y[0]:
                y=0
            if y>=Y[1]:
                y=Y[1]-1
        self.velocity=[vx,vy]
        self.position=[x,y]


    def move(self):
        for i in range(2):
            self.velocity[i]+=self.acceleration[i]
            self.position[i]+=self.velocity[i]

    def show(self,window):
        wsx,wsy=window.size
        raw_position=[int(self.position[i]) for i in range(2)]
        pygame.draw.circle(window.screen,self.color,raw_position,self.radius,1)
        #window.print(str(self.position),self.position)
