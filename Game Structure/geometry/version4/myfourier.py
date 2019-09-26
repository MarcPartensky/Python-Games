import pygame
import mycolors
import scipy
import math
import cmath
import time
import numpy as np

from marclib.polynomial import Polynomial
from functools import reduce
from myabstract import Vector,Point
from pygame.locals import *

#DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


prod=lambda l:reduce(lambda a,b: a*b,l)
factorial=lambda n:factorial(n-1) if n>0 else 1

class Fourier:
    def __init__(self,context):
        """Initialization."""
        self.context=context
        self.graph_drawing=[]
        self.graph_construction=[]
        self.graph_display=[]
        self.sample_precision=100
        self.coefficients_number=100
        self.display_number=100
        self.period=100
        self.mode=0
        self.messages=['drawing', 'construction', 'display']
        self.coefficients=[]
        self.context.text.append("mode: "+self.messages[self.mode])
        self.duration=None
        self.time=0
        self.step=0
        self.speed=1/100
        self.vectors=[]

    def __call__(self):
        """Main loop."""
        while self.context.open:
            self.main()
            self.events()
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
                #if event.key == K_f:
                #    pygame.display.toggle_fullscreen()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: self.context.draw.plane.zoom([1.1,1.1])
                if event.button == 5: self.context.draw.plane.zoom([0.9,0.9])


    def main(self):
        """Code inside the loop."""
        if self.mode==0: #drawing
            self.draw()
            self.graph_drawing=self.cleanGraph(self.graph_drawing)
            #if len(self.graph_drawing)>1:
            #    self.function_interpolation=self.polynomialInterpolation2D(self.graph_drawing,1)
            #    self.graph_interpolation=self.sample(self.function_interpolation,len(self.graph_drawing))
        elif self.mode==1: #construction
            self.step+=1
            self.time=self.speed*self.step
            #print(self.time/self.duration)
            if self.duration is not None:
                if self.time>self.duration:
                    self.mode=2
            self.graph_construction=self.discreteComplexComposeGraph(self.coefficients,self.time) #complex now
            self.vectors=self.getVectors([(0,0)]+self.graph_construction)
            self.graph_display.append(self.graph_construction[-1])

        elif self.mode==2:
            self.draw()

    def show(self):
        """Show the graph."""
        self.context.control()
        self.context.clear()
        self.context.show()
        if self.mode==0:
            self.showGraph(self.graph_drawing,mycolors.GREEN)
            #if len(self.graph_drawing)>1:
            #    self.showGraph(self.graph_interpolation,mycolors.YELLOW)
        elif self.mode==1:
            self.showGraph(self.graph_drawing,mycolors.GREEN)
            self.showGraph(self.graph_construction,mycolors.RED)
            self.showGraph(self.graph_display,mycolors.BLUE)
            self.showVectors([(0,0)]+self.graph_construction,self.vectors,mycolors.RED)
            self.context.text.append("time: "+str(self.time))
            #self.context.print("coefficients:"+str(self.coefficients),(1000,850),size=20,conversion=False,color=mycolors.GREEN)
        elif self.mode==2:
            self.showGraph(self.graph_display,mycolors.BLUE)
        self.context.showConsole(nmax=10)
        self.context.flip()

    def showGraph(self,graph,color=mycolors.WHITE):
        """Draw the graph."""
        l=len(graph)
        for i in range(l-1):
            self.context.draw.line(self.context.screen,color,graph[i],graph[i+1])


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
        self.graph_construction=[]
        self.graph_display=[]
        self.graph_drawing=self.cleanGraph(self.graph_drawing)
        #self.graph_drawing=self.takeGraphSamples(self.graph_drawing)[:]
        print(self.graph_drawing)
        self.coefficients=self.discreteComplexDecomposeGraph(self.graph_drawing)
        self.graph_construction=self.discreteComplexComposeGraph(self.coefficients,0)
        self.time=0
        self.step=0
        print(self.coefficients)

    def setDisplay(self):
        """Set the attributes before starting the display mode."""
        self.graph_display=[self.complexCompose(self.coefficients,(t+1)/self.display_number)[-1] for t in range(self.display_number)]

    def sample(self,f,N,p=100):
        """Take a sample of the function to get a graph using the function and the number of points of the graph."""
        return [f(x) for x in np.linspace(0,N,p)]

    def takeGraphSamples(self,graph):
        """Take some samples of the drawing."""
        t=self.getTotalDistance(graph)
        return [self.takeGraphSample(graph,t*i/self.sample_precision,t) for i in range(self.sample_precision)]

    def takeGraphSample(self,graph,z,t):
        """Take a sample of the drawing according the the distance made from the start z and the total."""
        s=0
        for i in range(len(graph)-1):
            d=self.getDistance(graph[i],graph[i+1])
            s+=d
            if z<s:
                return self.takeSegmentSample(graph[i],graph[i+1],(z-s+d)/d)

    def takeSegmentSample(self,p1,p2,degree):
        """Take a point from a segment."""
        return [c1*(1-degree)+c2*(degree) for (c1,c2) in zip(p1,p2)]

    def getTotalDistance(self,points):
        """Return the distance of the path made by the points."""
        return sum([self.getDistance(points[i],points[i+1]) for i in range(len(points)-1)])

    def getDistance(self,p1,p2):
        """Return the distance between two points."""
        return sum([(p1[i]-p2[i])**2 for i in range(2)])

    def getPeriod(self,coefficients):
        """Return the period of the coefficients."""
        return max([prod(coefficients[i]) for i in range(4)])

    def cleanGraph(self,graph):
        """Clean the points by removing the ones that are coinciding."""
        i=0
        while i+1<len(graph):
            if self.getDistance(graph[i],graph[i+1])==0:
                del graph[i+1]
            else:
                i+=1
        return graph

    def cleanGraph2(self,graph):
        """Clean the graph by removing all consecutives duplicates."""
        return [graph[i] for i in range(len(graph)-1) if graphp[i]!=graph[i+1]]

    def draw(self):
        """Allow the user to draw the graph."""
        if context.click():
            self.place()

    def place(self):
        """Place a point."""
        p=self.context.point()
        self.graph_drawing.append(p)

    def decompose(self,graph):
        """Decompose the points into 2 signals the coefficients corresponding to the drawing."""
        x=[graph[i][0] for i in range(len(graph))]
        y=[graph[i][1] for i in range(len(graph))]
        return self.transform(x)+self.transform(y)

    def complexDecompose(self,graph):
        """Decompose the graph into 2 list of complex coefficients from the fourier transform."""
        z=[complex(*graph[i]) for i in range(len(graph))]
        return self.complexTransform(z)

    def polynomialInterpolation(self,s):
        """Transform a discrete signal into a continuous one.
        Using the lagrangian interpolation of polynomials"""
        #print(s)
        #s[i]=xi,s[j]=xj
        return Polynomial.createFromInterpolation(s,range(len(s)))
        #return Polynomial(s,T)

    def polynomialInterpolation2D(self,graph,T):
        """Transform a discrete graph into a continuous one.
        Using the lagrangian interpolation of polynomials"""
        x=[graph[i][0] for i in range(len(graph))]
        y=[graph[i][1] for i in range(len(graph))]
        return lambda t:(self.polynomialInterpolation(x)(t),self.polynomialInterpolation(y)(t))

    def transform(self,s):
        """Decompose a signal 's' using the fourier transform."""
        T=len(s)
        N=self.coefficients_number
        #wo=2*math.pi/T
        wo=1
        a=[2/T*sum([s[t]*math.cos(n*wo*t) for t in range(T)]) for n in range(N)]
        b=[2/T*sum([s[t]*math.sin(n*wo*t) for t in range(T)]) for n in range(N)]
        return [a,b]

    def complexTransform(self,z):
        """Decompose a signal 's' using the complex fourier transform."""
        N=self.coefficients_number
        T=self.period
        #wo=2*math.pi/N
        #an=[1/N*sum([z[t]*cmath.exp(complex(0,-n*k)) for t in range(T)]) for n in range(-(N-1)//2,(N-1)//2+1)]
        a=lambda n:1/T*sum([z[t]*cmath.exp(-1j*n*t) for t in range(T)])
        #a=lambda n:1/T*scipy.integrate.quad(z[t]*cmath.exp(-1j*n*t),0,T)
        c=[a(n) for n in range(-N,N+1)]
        return c

    def discreteComplexDecompose(self,graph):
        """Decompose the graph in its complex fourier coefficients."""
        z=[complex(*graph[i]) for i in range(len(graph))]
        return self.discreteComplexTransform(z)

    def discreteComplexTransform(self,s):
        """Application of the complex fourier transform with a discrete signal 's'."""
        N=len(s)
        return sum([s[n]*cmath.exp(2j*cmath.pi*k*n/N) for n in range(N)])/N

    def discreteComplexDecomposeGraph(self,graph):
        """Decompose the graph in its complex fourier coefficients."""
        s=[complex(*graph[i]) for i in range(len(graph))]
        N=len(s)
        M=self.coefficients_number
        d=0
        c=[]
        for k in range(-M//2,M//2):
            d+=sum([s[n]*cmath.exp(2j*cmath.pi*k*n/N) for n in range(N)])/N
            c.append(d)
        return c

    def scipyTranform(self,s):
        """Find the fourier transform using the scipy module."""
        l=len(s)
        wo=2*math.pi/l
        a=2/scipy.integrate.quad(math.cos(n*wo*t),t,-inf,inf)
        b=2/scipy.integrate.quad(math.sin(n*wo*t),t,-inf,inf)

    def compose(self,coefficients,t=1,N=None):
        """Return the graph corresponding to the coefficients of the fourier transform."""
        xa,xb,ya,yb=coefficients
        l=max(len(xa),len(xb),len(ya),len(yb))
        return [(self.inverseTransform(xa,xb,t,N),self.inverseTransform(ya,yb,t,N))]

    def fastCompose(self,coefficients,t=1,N=None):
        """Return the construction graph using the coefficients of the fourier transform but fast."""
        xa,xb,ya,yb=coefficients
        l=max(len(xa),len(xb),len(ya),len(yb))
        g=[]
        xs,ys=0,0
        if N is None: N=l
        wo=2*math.pi/N
        for n in range(N):
            xs+=xa[n]*math.cos(n*wo*t)+xb[n]*math.sin(n*wo*t)
            ys+=ya[n]*math.cos(n*wo*t)+yb[n]*math.sin(n*wo*t)
            #xs+=xa[n]*math.cos(n*wo*t)
            #ys+=yb[n]*math.sin(n*wo*t)

            g.append((xs,ys))
        return g

    def complexCompose(self,coefficients,t=1):
        """Return the graph corresponding to the fourier transform using complex coefficients."""
        c=coefficients
        N=len(c)//2
        s=lambda t,n:c[n+N]*cmath.exp(1j*n*t)
        a=0
        g=[]
        z=[]

        #for i in range(len(c)):
        #    if i==0: n=0
        #    elif i%2==1: n=(i+1)//2
        #    elif i%2==0: n=-i//2
        #    pass

        #print([a[1] for a in z])
        #z=sorted(z,key=lambda x:1,reverse=True)
        #print([a[1] for a in z])
        #z=[a[0] for a in z]

        for n in range(-N,N+1):
            a+=s(t,n)
            g.append((a.real,a.imag))

        return g

    def inverseTransform(self,a,b,t=1,N=None):
        """Return a graph from the inverse transform of fourier using the list of coefficents 'a' and 'b' using time 't'."""
        #T=max(len(a),len(b)) #it's better to throw an error than having something that doesn't work the way expected.
        if N is None:
            N=self.coefficients_number
        wo=2*math.pi/N
        return [sum([a[n]*math.cos(n*wo*t)+b[n]*math.sin(n*wo*t) for n in range(N)])]

    def complexInverseTransform(self,S,t=1):
        """Return a list of points using the a discrete complex inverse transform using fourier."""
        N=self.display_number
        wo=2*cmath.pi/N
        return sum([S[k+(N-1)//2]*cmath.exp(complex(0,n*k*wo))+S[-k+(N-1)//2]*cmath.exp(-complex(0,n*k*wo)) for k in range(-(N-1)//2,(N-1)//2+1)])

    def discreteComplexCompose(self,c,n):
        """Compose a graph using the complex fourier coefficients."""
        z=self.discreteComplexInverseTransform(c,n)
        return (z.real,z.imag)

    def discreteComplexInverseTransform(self,S,n):
        """Application of the complex fourier inverse transform with a discrete signal 's'."""
        N=len(S)
        M=N/2
        return sum([S[k+M]*cmath.exp(2j*cmath.pi*k*n/N)+S[-k+M]*cmath.exp(-2j*cmath.pi*k*n/N) for k in range(M+1)])

    def discreteComplexComposeGraph(self,S,n):
        """Second application of the complex fourier inverse transform with a discrete signal 's'
        that returns a graph."""
        N=len(S)
        M=N//2
        g=[]
        d=0
        for k in range(M):
            d+=S[k+M]*cmath.exp(2j*cmath.pi*k*n/N)+S[-k+M]*cmath.exp(-2j*cmath.pi*k*n/N)
            g.append((d.real,d.imag))
        return g




if __name__=="__main__":
    from mycontext  import Context
    context=Context(name="Application of the Fourier Transform.",fullscreen=False)
    fourier=Fourier(context)
    fourier.coefficients=[[0,1,2,0.5],[0,1,5,2],[0,-2,1,6],[0,-4,3,1]]
    #fourier.coefficients=[(3+5j),(2+1j),(0-0.5j),(1+3.5j),(2-1j)]
    #fourier.mode=1
    fourier()
