from mywindow import Window
from mylab import Lab
from mycolors import *
from mygeometry import Form,Point
import random

class Room(Lab):
    def __init__(self,name,entities):
        Lab.__init__(self,name,entities)
    def update(self):
        for entity in self.entities:
            entity.update(self.window)
        if self.window.focus:
            x,y=self.window.point()
            self.window.focus.x=x
            self.window.focus.y=y
        if self.window.onclick():
            print("onClick")
            self.onclick()
        wx,wy=self.window.point()
        c=self.entities[0].center()
        c.color=GREEN
        c.show(self.window)
        x,y=c[0],c[1]
        self.entities[0].move(wx-x,wy-y)
        self.entities[0].rotate(0.01)
        self.collide()
    def collide(self):
        for i in range(len(self.entities)):
            self.entities[i].color=WHITE
        for i in range(len(self.entities)):
            for j in range(i+1,len(self.entities)):
                if self.entities[i]|self.entities[j]:
                    self.entities[i].color=RED
                    self.entities[j].color=RED
    def onclick(self):
        print("clicked")
        if self.window.focus is not None:
            self.window.focus=None
        else:
            for form in self.entities:
                for point in form.points:
                    if self.window.point() in point:
                        self.window.focus=point

if __name__=="__main__":
    entities=[Form([Point(random.random()*900,random.random()*400) for i in range(3)]) for i in range(3)]
    r=Room(name="Geometry",entities=entities)
    r()
