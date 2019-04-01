
from myplane import Plane
from mywindow import Window

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
    def __init__(self,plane,window):
        self.plane=plane
        self.window=window

    def rect(self,color,position,size,filled=False):
        position=self.plane.getToScreen(position,self.window)
        size=self.plane.getToScreen(size,self.window)
        self.window.draw.rect(self.window.screen,color,position+size,not filled)

    def circle(self,color,position,radius,filled=False):
        position=self.plane.getToScreen(position,self.window)
        #Need to implement ellipses

    def square(self,color,position,side_size,filled=False):
        position=self.plane.getToScreen(position,self.window)
        size=self.plane.getToScreen([side_size,side_size],self.window)
        self.window.draw.rect(self.window.screen,color,position+size,not filled)

    def polygon(self,color,positions,filled=False):
        pass

    def line(self,color,start_position,end_position,width=0):
        start_position=self.plane.getToScreen(start_position,self.window)
        end_position=self.plane.getToScreen(end_position,self.window)
        slef.widnow.draw.line(self.window.screen,color,start_position,end_position,width)

    def lines(self,color,positions,width=0):
        new_positions=



if __name__=="__main__":
    window=Window()
    plane=Plane()
    draw=Draw(plane,window)
