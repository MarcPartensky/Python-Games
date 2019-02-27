from myentity import Entity
from math import exp,sin

import time

moving1=lambda x:sin(x/100)/100
moving2=lambda x:sin(x/100)


class Camera(Entity):
    def __init__(self,position,size,borders):
        """Create camera object using position, size and borders."""
        Entity.__init__(self,position=position,size=size,borders=borders)
        self.moving_function=moving2
    def __call__(self,direction,window):
        """Return vision using direction."""
        dx,dy=direction
        x,y=self.position
        sx,sy=self.size
        #self.direction=[dx-(x+sx/2),dy-(y+sy/2)]
        self.position=[dx-sx/2,dy-sy/2]
        #self.direct(window)
        self.move()
        self.affectBorders()
        #print("self.borders:",self.borders)
        self.position,self.round(self.position)

        #self.update(window)
        vision=self.position+self.size
        return vision

    def round(self,position,precision=1):
        position[0]=round(position[0],precision)
        position[1]=round(position[1],precision)
        return position
