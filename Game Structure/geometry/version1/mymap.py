from mywindow import Window
from myzone import Zone

import numpy as np
import os

class Component:
    def __init__(self,color=(0,255,0)):
        """Create a component."""
        self.color=color
    def show(self,window,position,size):
        """Show the component on the screen's using window, position and size."""
        window.draw.rect(window.screen,self.color,position+[size[0]+1,size[1]+1],0)
    def save(self,directory):
        """Save the component for later use."""
        pa

class Grass(Component):
    def __init__(self):
        self.grid=[[0,0,1,0,0,0,1,0,0,0]]
    def show(self,window,position,size):
        pass


class Map(Zone):
    def __init__(self,size=[20,20],theme={},view=None):
        """Create a map using size, theme, view, components"""
        Zone.__init__(self,size=size,theme=theme,view=view)
        self.size=size
        sx,sy=self.size

    def edit(self,window):
        pass
        self.grid=[[Component() for x in range(sx)] for y in range(sy)]

    def fill(self,position,value): #This method is totally useless
        """Fill the position with the given value."""
        x,y=position
        self.grid[y][x]=value

    def showPlane(self,window):
        """Show the map on the window."""
        self.showGrid(window)
        self.showCases(window)
        self.showBorders(window)

    def showCases(self,window):
        """Show all the components on screen."""
        sx,sy=self.size
        nx=sx//2
        ny=sy//2
        for y in range(sy):
            for x in range(sx):
                position=self.getToScreen([x-nx,y-ny+1],window)
                self.grid[y][x].show(window,position,self.units)



if __name__=="__main__":
    window=Window("Map")
    map=Map()
    print(map.grid)
    map(window)
