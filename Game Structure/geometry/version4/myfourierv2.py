from myabstract import Point
from myinterpolation import PolynomialInterpolation
from mycurves import Trajectory
from pygame.locals import *

import mycolors
import pygame
import numpy as np
import math
import cmath


class Fourier:
    def __init__(self,context):
        """Initialization."""
        self.context=context
        #Graphs
        self.graph_drawing=[]
        self.graph_construction=[]
        self.graph_display=[]
        #Mode
        self.mode=0
        self.step=0
        self.max_step=1000
        self.messages=['drawing', 'construction', 'display']
        self.coefficients=[]
        self.interval=list(range(-10,10+1))
        self.integral_precision=100


    def __call__(self):
        """Main loop."""
        self.setMode(self.mode)
        while self.context.open:
            self.events()
            self.main()
            self.show()

    def events(self):
        """Deal with all the events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.context.open=False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.context.open=False
                if event.key == K_SPACE:
                    self.setMode((self.mode+1)%3)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: self.place()
                if event.button == 4: self.context.draw.plane.zoom([1.1,1.1])
                if event.button == 5: self.context.draw.plane.zoom([0.9,0.9])


    def main(self):
        """Code inside the loop."""
        if self.mode==0: #drawing
            pass
        elif self.mode==1: #construction
            self.step+=1
            if self.step>self.max_step:
                self.mode=2
            else:
                self.build()
        elif self.mode==2: #display
            pass

    def show(self):
        """Show the graph."""
        self.context.control()
        self.context.clear()
        self.context.show()
        if self.mode==0:
            self.showModeDrawing()
        elif self.mode==1:
            self.showModeConstruction()
        elif self.mode==2:
            self.showModeDisplay()
        self.context.showConsole(nmax=10)
        self.context.flip()

    def showModeDrawing(self):
        """Show the graphical components of the mode drawing."""
        if len(self.graph_drawing)>1:
            t=Trajectory.createFromTuples(self.graph_drawing,segment_color=mycolors.GREEN)
            p=PolynomialInterpolation(self.graph_drawing,color=mycolors.RED)
            t.show(self.context)
            p.show(self.context,200)

    def showModeConstruction(self):
        """Show the graphical components of the mode construction."""
        if len(self.graph_drawing)>1:
            t1=Trajectory.createFromTuples(self.graph_drawing,segment_color=mycolors.GREEN)
            t2=Trajectory.createFromTuples(self.graph_construction,segment_color=mycolors.BLUE)
            t3=Trajectory.createFromTuples(self.graph_display,segment_color=mycolors.RED)
            t1.show(self.context)
            t2.show(self.context)
            t3.show(self.context)
        #self.showVectors([(0,0)]+self.graph_construction,self.vectors,mycolors.RED)
        self.context.text.append("time: "+str(self.time))

    def showModeDisplay(self):
        """Show the graphical components of the mode display."""
        t3=Trajectory.createFromTuples(self.graph_display,segment_color=mycolors.RED)
        t3.show(self.context)

    def getVectors(self,graph):
        """Return the list of vectors."""
        return [Vector.createFromTwoTuples(graph[i],graph[i+1]) for i in range(len(graph)-1)]

    def showVectors(self,graph,vectors,color=mycolors.WHITE):
        """Show the vectors on the screen."""
        for i in range(len(vectors)-1):
            vectors[i].show(self.context,Point(*graph[i]),color)

    def setMode(self,mode):
        """Change the mode into another."""
        self.mode=mode
        if self.mode==0:
            self.setDrawing()
        elif self.mode==1:
            self.setConstruction()
        elif self.mode==2:
            self.setDisplay()
        self.context.text.append("mode: "+self.messages[self.mode])

    def setDrawing(self):
        """Set the attributes before starting the drawing mode."""
        self.graph_drawing=[]

    def setConstruction(self):
        """Set the attributes before starting the construction mode."""
        #Resets the values
        self.vectors=[]
        self.step=0
        p=PolynomialInterpolation(self.graph_drawing,color=mycolors.RED)
        sp=p.sample(100)
        cg=[complex(*p) for p in sp]
        a=np.fft.fft(cg)
        b=self.getCoefficients(p)
        print(self.coefficients)
        cg=np.fft.ifft(self.coefficients)
        g=[(p.real,p.imag) for p in cg]
        self.graph_display=g
        self.graph_construction=self.graph_display

    def setDisplay(self):
        """Set the attributes before starting the display mode."""
        self.graph_display=[]

    def place(self):
        """Place a point."""
        p=self.context.point()
        self.graph_drawing.append(p)

    def getTime(self):
        """Return the time of the construction."""
        return self.step/self.max_step

    time=property(getTime)

    def build(self):
        """Build the construction graph."""
        self.numpyComposeConstructionGraph()

    def numpyComposeConstructionGraph(self):
        """Uses the fourier coefficients of the fourier transform. to make the construciton graph."""
        coefficients=self.coefficients; t=self.time
        print(coefficients)
        l=len(coefficients)
        xs,ys=0,0
        wo=2*math.pi
        #wo=1
        #wo=1/10
        graph=[]
        #print("coefficients:")
        #print(coefficients)
        l=len(coefficients)
        print(l)
        h=l//2
        for i in range(l-1):
            n=int(((i+1)//2)*(-1)**(i+1))
            print("n:",n)
            z=coefficients[n+h]*cmath.exp(n*wo*t*1j)
            print(z,coefficients[n+h])
            #print("z:",z.real,z.imag)
            x=z.real; y=z.imag
            xs+=x; ys+=y
            graph.append((xs,ys))
            #print("x,y:",x,y)
            #print("xs,ys:",xs,ys)
        self.graph_construction=graph

    def getCoefficient(self,f,n):
        wo=2*math.pi
        mw=self.integral_precision
        return sum([f(w/mw)*cmath.exp(n*wo*(w/mw)*1j) for w in range(mw)])

    def getCoefficients(self,f):
        return [getCoefficient(f,n) for n in self.interval]



if __name__=="__main__":
    from mycontext  import Context
    context=Context(name="Application of the Fourier Transform.",fullscreen=False)
    fourier=Fourier(context)
    fourier()
