import pygame

class Quadtree:
    WHITE=(255,255,255)
    def __init__(self,position,size,capacity=1,points=None,window=None,indent=0,max_indent=10,shown=False,color=WHITE):
        self.position=position
        self.size=size
        self.capacity=capacity
        self.window=window
        self.color=color
        self.points=points
        self.max_indent=max_indent
        self.indent=indent+1
        self.squares=self.points
        if indent<=max_indent:
            if shown:
                self.show()
            self.check()

    def check(self):
        counter=0
        for point in self.points:
            if self.contains(point):
                counter+=1
        if counter>self.capacity:
            self.divide()

    def show(self):
        x,y=self.position
        sx,sy=self.size
        pygame.draw.line(self.window.screen, self.color, (x,y), (x+sx,y), 1)
        pygame.draw.line(self.window.screen, self.color, (x+sx,y), (x+sx,y+sy), 1)
        pygame.draw.line(self.window.screen, self.color, (x+sx,y+sy), (x,y+sy), 1)
        pygame.draw.line(self.window.screen, self.color, (x,y+sy), (x,y), 1)

    def contains(self,point):
        x,y=self.position
        sx,sy=self.size
        px,py=point
        if x<=px<x+sx and y<=py<y+sy:
            return True
        else:
            return False

    def divide(self):
        x,y=self.position
        sx,sy=self.size
        hx,hy=sx//2,sy//2
        capacity=self.capacity
        points=self.points
        window=self.window
        self.squares=  [Quadtree((x,y),(hx,hy),capacity,points,window,self.indent).squares,
                        Quadtree((x+hx,y),(hx,hy),capacity,points,window,self.indent).squares,
                        Quadtree((x,y+hy),(hx,hy),capacity,points,window,self.indent).squares,
                        Quadtree((x+hx,y+hy),(hx,hy),capacity,points,window,self.indent).squares]



print("Quadtree imported")
