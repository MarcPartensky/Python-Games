from window import *
from colors import *

print("imported")

def square(x):
    return x**2-10

class Graph:
    def __init__(self,function,color=RED):
        self.function=function
        self.color=color
        self.dots=[]

    def place(self,size):
        self.dots=[]
        sx,sy=size
        for i in range(sx):
            x=(i-sx/2)
            y=self.function(x)
            print(x,y)
            self.dots.append((x,y))

    def draw(self,plan,translation,units,middle):
        self.place(plan.size)
        tx,ty=translation
        ux,uy=units
        mx,my=middle
        dots=[]
        for i in range(len(self.dots)):
            dx,dy=self.dots[i]
            position=((dx*ux+tx+mx,dy*uy+ty+my))
            dots.append(position)
        return dots


class Plan:
    def __init__(self,size=[100,100],background=WHITE,axis_color=BLACK):
        self.size=size
        sx,sy=size
        self.grid=[[background for x in range(sx)] for y in range(sy)]
        self.background=background
        self.axis_color=axis_color
        self.graphs=[]
        self.middle=[0,0]
        self.units=[2,2]
        self.translation=[sx//2,sy//2]
    def addGraph(self,graph):
        self.graphs.append(graph)
    def draw(self,window):
        wsx,wsy=window.size
        sx,sy=self.size
        mx,my=self.middle
        self.showAxis(window)
        for graph in self.graphs:
            curve=graph.draw(window,self.translation,self.units,self.middle)
            for dot in curve:
                x,y=dot
                if 0<=x<sx and 0<=y<sy:
                    self.grid[y][x]=graph.color

    def showAxis(self,window):
        sx,sy=self.size
        tx,ty=self.translation
        ux,uy=self.units
        for y in range(0,sx):
            self.grid[y][tx]=self.axis_color
            if y%uy==0:
                self.grid[y][tx+1]=self.axis_color
                self.grid[y][tx-1]=self.axis_color

        for x in range(0,sy):
            self.grid[ty][x]=self.axis_color
            if x%ux==0:
                self.grid[ty+1][x]=self.axis_color
                self.grid[ty-1][x]=self.axis_color



    def show(self,window):
        window.screen.fill(self.background)
        sx,sy=self.size
        wsx,wsy=window.size
        cx,cy=wsx/sx,wsy/sy
        for y in range(sx):
            for x in range(sy):
                color=self.grid[y][x]
                position=(x*cx,wsy-y*cy,cx,cy)
                pygame.draw.rect(window.screen, color, position, 0)


class Main:
    def __init__(self):
        self.name="Graph Printer"
        self.window=Window(self,size=[1000,700])
        self.plan=Plan([100,100],BLACK,WHITE)
        self.graph=Graph(square)
        self.plan.addGraph(self.graph)
        self.plan.draw(self.window)
        self.session()

    def session(self):
        while self.window.open:
            self.window.check()
            #self.plan.control()
            self.show()

    def show(self):

        self.plan.show(self.window)
        self.window.flip()



#-------#
#Actions#
#-------#

Main=Main()
