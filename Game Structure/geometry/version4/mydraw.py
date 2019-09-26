
from myplane import Plane
from mywindow import Window
from mycolors import *
from math import sqrt

"""
Structure:

Plane:
- init(name,size,fullscreen,theme,view)
- show(view) ?
- getFromScreen(position)
- getToScreen(position)



Draw:
-draw.circle(color,position,radius,filled)
-draw.rect(color,position,size,filled)
-draw.line(color,start_position,end_position,width)
-draw.lines(color,connected,positions,width)


Client:
-map.draw.rect(color,position,filled)
-map.draw.line(color,start_position)
"""



class Draw:
    def __init__(self,plane=Plane(),window=None,**kwargs):
        if window: self.window=window
        else: window=Window(**kwargs)
        self.plane=plane
        self.window=window
        self.window.text_size=30


    def rect(self,screen,color,rect,filled=False,conversion=True):
        if conversion:
            position=rect[:2]
            size=rect[2:]
            sx,sy=size
            position=self.plane.getToScreen(position,self.window)
            ux,uy=self.plane.units
            size=[sx*ux+1,sy*uy+1]
            rect=position+size
        self.window.draw.rect(screen,color,rect,not(filled))

    def ellipse(self,screen,color,rect,filled=False):
        coordonnates=Plane.getCoordonnatesFromRect(rect)
        x,y,sx,sy=coordonnates
        py,px=self.plane.getToScreen((x,y),self.window)
        psx,psy=self.plane.getToScreen((sx,sy),self.window)
        pmx,pmy,pMx,pMy=Plane.getRectFromCoordonnates([px,py,psx,psy])
        rect=[pmx,pmy,pMx,pMy]
        self.window.draw.ellipse(screen,color,rect,filled)

    def circle(self,screen,color,position,radius,filled=False,conversion=True):
        #self.ellipse(screen,color,position+[radius,radius],filled)

        #rx,ry=self.plane.getToScreen([radius,radius],self.window)
        #rect=self.plane.getRectFromScreen(position+[radius,radius])
        #self.window.draw.ellipse(screen,color,rect,width)
        #Need to implement ellipses
        #r=int(radius/self.plane.units[0])
        #r,ry=self.plane.getToScreen([radius,radius],self.window)
        position=self.plane.getToScreen(position,self.window)
        x,y=position
        if conversion:
            rx,ry=[radius*self.plane.units[i] for i in range(2)]
            radius=int((rx+ry)/2)
        if radius<1: radius=1
        #r=0.1
        self.window.draw.circle(screen,color,position,radius,not(filled))

    def square(self,screen,color,position,side_size,filled=False):
        position=self.plane.getToScreen(position,self.window)
        size=self.plane.getToScreen([side_size,side_size],self.window)
        self.window.draw.rect(screen,color,position+size,not filled)

    def polygon(self,screen,color,positions,filled=False): #No clue of what i'm doing to do here.
        screen_positions=self.plane.getAllToScreen(positions,self.window)
        self.window.draw.polygon(screen,color,screen_positions,filled)

    def line(self,screen,color,start_position,end_position,width=1,conversion=True):
        if conversion:
            start_position=self.plane.getToScreen(start_position,self.window)
            end_position=self.plane.getToScreen(end_position,self.window)
        self.window.draw.line(screen,color,start_position,end_position,width)

    def lines(self,screen,color,positions,connected=True,width=1,conversion=True):
        if conversion: positions=self.plane.getAllToScreen(positions,self.window)
        self.window.draw.lines(screen,color,connected,positions,width)

    def arc(self,screen,color,rect,start_angle,stop_angle,width=1):
        position=rect[:2]
        size=rect[2:]
        position=self.plane.getToScreen(position,self.window)
        size=self.plane.getToScreen(size,self.window)
        self.window.draw.arcarc(screen,color,rect,start_angle,stop_angle,width)



    def show(self):
        self.plane.showGrid(self.window)
        self.window.flip()

    def clear(self,**kwargs):
        self.plane.clear(self.window,**kwargs)

    def check(self):
        self.window.check()

    def control(self):
        self.plane.control(self.window)



if __name__=="__main__":
    window=Window("mydraw")
    plane=Plane()
    draw=Draw(plane,window)
    while draw.window.open:
        draw.check()
        draw.control()
        draw.clear()
        draw.line(WHITE,(3,-5),(-2,6))
        draw.show()
