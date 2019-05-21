from myabstract import Form,Point

from mypixel import Pixel

from pygame.locals import *


import time
import mycolors

class Case(Pixel):
    def __init__(self,position,size=(1,1),color=mycolors.WHITE,fill=True):
        """Create a pixel."""
        self.position=position
        self.size=size
        self.color=color
        self.fill=fill

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

    def getForm(self,fill=None,area_color=None,side_color=None):
        """Return the abstract form associated with the case."""
        if not fill: fill=self.fill
        if not area_color: area_color=self.color
        if not side_color: side_color=mycolors.WHITE
        xmin,ymin,xmax,ymax=self.getCorners()
        p1=Point(xmin,ymin)
        p2=Point(xmax,ymin)
        p3=Point(xmax,ymax)
        p4=Point(xmin,ymax)
        points=[p1,p2,p3,p4]
        return Form(points,fill=fill,side_color=side_color,area_color=area_color,point_show=False)

    form=getForm

    def center(self):
        """Return the center of the case."""
        xmin,ymin,xmax,ymax=self.getCorners()
        x=(xmin+xmax)/2
        y=(ymin+ymax)/2
        return Point(x,y)

    def show(self,surface,**kwargs):
        """Show the case. By default it only show the associated form."""
        self.showForm(surface,**kwargs)

    def showText(self,surface,text):
        """Show the text on the surface."""
        point=self.center()
        point.showText(surface,text)

    def showForm(self,surface,fill=None,area_color=None,side_color=None):
        """Show the pixel on screen."""
        f=self.getForm(fill,area_color,side_color)
        f.show(surface)

    __getitem__=lambda self,i:self.position[i]

    #def __getitem__(self,index):

    def __str__(self):
        """Return the string representation of the object."""
        return "case("+str(self.position[0])+","+str(self.position[1])+")"

    def getCorners(self):
        """Return the corners of the case."""
        px,py=self.position
        sx,sy=self.size
        return (px,py,px+sx,py+sy)

    def __contains__(self,position):
        """Determine if the point is in the paint."""
        x,y=position
        xmin,ymin,xmax,ymax=self.getCorners()
        return (xmin<=x<=xmax) and (ymin<=y<=ymax)


    __repr__=__str__

if __name__=="__main__":
    from mysurface import Surface
    from myzone import Zone
    surface=Surface(plane=Zone(size=[20,20]))
    cases=[Case([x,y],color=mycolors.random(),fill=True) for x in range(-5,5) for y in range(-5,5)]
    while surface.open:
        surface.check()
        surface.control()
        surface.clear()
        surface.show()
        for case in cases:
            case.show(surface)
        surface.flip()
