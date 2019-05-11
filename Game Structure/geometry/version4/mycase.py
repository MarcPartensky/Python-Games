from myabstract import Form,Point

from mypixel import Pixel

from pygame.locals import *


import time
import mycolors

class Case(Pixel):
    def __init__(self,position,size=(1,1),color=mycolors.WHITE):
        """Create a pixel."""
        self.position=position
        self.size=size
        self.color=color

    def __eq__(self,other):
        """Determine if two cases are the same by comparing its x and y components."""
        return self.position==other.position

    def __iter__(self):
        """Iterate the points of the form."""
        self.iterator=0
        return self

    def __next__(self):
        """Return the next point threw an iteration."""
        if self.iterator<2:
            value=self.position[self.iterator]
            self.iterator+=1
            return value
        else:
            raise StopIteration

    def show(self,surface):
        """Show the pixel on screen."""
        x,y=self.position
        sx,sy=self.size
        p1=Point(x,y)
        p2=Point(x+sx,y)
        p3=Point(x+sx,y+sy)
        p4=Point(x,y+sy)
        points=[p1,p2,p3,p4]
        form=Form(points,fill=True,area_color=self.color,point_show=False)
        form.show(surface)

    __getitem__=lambda self,i:self.position[i]

    #def __getitem__(self,index):

    def __str__(self):
        """Return the string representation of the object."""
        return "("+str(self.position[0])+","+str(self.position[1])+")"

    __repr__=__str__
