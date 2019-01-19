import pygame
class Quadtree:
    WHITE=(255,255,255)
    def __init__(self,position,size,capacity=10,points=None,window=None,color=WHITE):
        self.position=position
        self.size=size
        self.capacity=capacity
        self.window=window
        self.color=color
        self.points=points
        self.check()
    def check(self):
        counter=0
        for point in self.points:
            if self.contains(point):
                counter+=1
        print("counter=",counter)
        if counter>self.capacity:
            self.divide()
            for square in self.squares:
                square.show()
                print(square.position)
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
        px,py=point.position
        #wsx,wsy=self.window.size
        #hx,hy=wsx//2,wsy//2
        #print(x,y)
        #print(sx,sy)
        #print(px,py)
        #print("")
        if x<=px<sx and y<=py<sy:
            return True
        else:
            return False
    def divide(self):
        sx,sy=self.size
        hx,hy=sx//2,sy//2
        capacity=self.capacity
        points=self.points
        window=self.window
        self.squares=  [Quadtree((0,0),(hx,hy),capacity,points,window),
                        Quadtree((hx,0),(hx,hy),capacity,points,window),
                        Quadtree((0,hy),(hx,hy),capacity,points,window),
                        Quadtree((hx,hy),(hx,hy),capacity,points,window)]



print("Quadtree imported")
