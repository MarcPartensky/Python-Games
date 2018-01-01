
from myplane import Plane
from mywindow import Window
from mycolors import *

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
    def __init__(self,plane=Plane(),window=Window()):
        self.plane=plane
        self.window=window


    def rect(self,screen,color,position,size,filled=False):
        position=self.plane.getToScreen(position,self.window)
        size=self.plane.getToScreen(size,self.window)
        self.window.draw.rect(screen,color,position+size,not filled)

    def circle(self,screen,color,position,radius,filled=False):
        position=self.plane.getToScreen(position,self.window)
        #Need to implement ellipses

    def square(self,screen,color,position,side_size,filled=False):
        position=self.plane.getToScreen(position,self.window)
        size=self.plane.getToScreen([side_size,side_size],self.window)
        self.window.draw.rect(screen,color,position+size,not filled)

    def polygon(self,color,positions,filled=False): #No clue of what i'm doing to do here.
        pass

    def line(self,screen,color,start_position,end_position,width=1):
        start_position=self.plane.getToScreen(start_position,self.window)
        end_position=self.plane.getToScreen(end_position,self.window)
        self.window.draw.line(screen,color,start_position,end_position,width)

    def lines(self,color,positions,connected=True,width=1):
        new_positions=self.plane.getAllToScreen(positions,self.window)
        self.window.draw.lines(screen,color,connected,positions,width)

    def show(self):
        self.plane.showGrid(self.window)
        self.window.flip()

    def clear(self):
        self.plane.clear(self.window)

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
