from mywindow import Window
from myplane import Plane
from mycolors import *

from math import cos,sin,exp

import random

sigmoid=lambda x:1/(1+exp(-x))
alea=   lambda x:sin(x)*random.random()

class Grapher(Plane):
    """The grapher is a tool using the Plane class made in order to show functions taking one input.
       The methods proper to the plane allows the user to move in space to see the function from every perspective."""
    def __init__(self,functions):
        """Create a grapher and stores its functions with its predefined colors."""
        Plane.__init__(self)
        self.functions=functions
        self.colors=([RED,BLUE,GREEN,YELLOW]+[window.randomColor() for i in range(len(functions)-4)])[:len(functions)]

    def show(self,window):
        """Show the elements on screen using the window."""
        self.showGrid(window)
        self.showFunctions(window)


    def showFunctions(self,window):
        """Overload of the update method of plane for the Grapher class in order to print the functions,
        takes window in parameter."""
        wsx,wsy=window.size
        for i,function in enumerate(self.functions):
            self.showGraph(function,window,self.colors[i])
            window.print(str(function),[wsx-wsx/5,wsy-wsy/20*(i+2)],color=self.colors[i],size=25)

    def showGraph(self,function,window,color=None):
        """Show the graph of a function on screen using the function, the window and an optional color."""
        if not color: color=window.randomColor()
        wsx,wsy=window.size
        points=[]
        for X in range(0,wsx):
            x,y=self.getFromScreen([X,0],window)
            X,Y=self.getToScreen([x,function(x)],window)
            points.append((X,Y))
        window.draw.lines(window.screen,color,False,points,1)


if __name__=="__main__":
    window=Window(size=[1440,900],fullscreen=True)
    grapher=Grapher([sin,cos,sigmoid,alea])
    grapher(window)
