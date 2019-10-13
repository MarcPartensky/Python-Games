from myinterpolation import PolynomialInterpolation
from myabstract import Point,Vector,Circle
from mycurves import Trajectory
from pygame.locals import *
from PIL import Image


import numpy as np
import mycolors
import pygame
import pickle
import cmath
import math
import cv2
import os


class Fourier:

    def transform(pts,ncfs,wo=2*math.pi):
        """Apply the true fourier transform by
        returning a dictionary of the coefficients."""
        npts=len(pts)
        h=ncfs//2
        cfs={}
        #Compute all coefficients
        for n in range(-h,h+1):
            #Compute each coefficient
            cn=0
            for iw in range(npts):
                w=iw/npts  #w is not a frequency but the variable of a parametric equation
                fw=complex(*pts[iw])
                cn+=fw*cmath.exp(-1j*n*w*wo)
            cn/=npts #should i remove this?
            cfs[n]=cn
        return cfs

    def inverseTransform(cfs,npts,wo=2*math.pi):
        """Apply the true fourier inverse transform by returning the list of the points."""
        ncfs=len(cfs)
        h=npts//2
        pts=[]
        #Compute all the points
        for it in range(npts):
            t=it/npts #t is not a time but the variable of a parametric equation of the final graph
            #Compute each point
            zpt=0
            for (n,cn) in cfs.items(): #Addition is commutative, even though the dictionary is unordered, the sum of the terms will be the same
                zpt+=cn*cmath.exp(1j*wo*n*t)
            zpt*=(npts/ncfs)
            #zpt/=ncfs
            pts.append((zpt.real,zpt.imag))
        return pts

    def build(cfs,t,wo=2*math.pi):
        """Return the 'construction graph' with a given time 't'."""
        ncfs=len(cfs)
        h=ncfs//2
        cst=[(0,0)]
        zpt=cfs[0]
        cst.append((zpt.real,zpt.imag))
        for n in range(1,h+1):
            pcf=cfs[n]*cmath.exp(1j*wo*n*t)
            ncf=cfs[-n]*cmath.exp(1j*wo*(-n)*t)
            zpt+=pcf
            cst.append((zpt.real,zpt.imag))
            zpt+=ncf
            cst.append((zpt.real,zpt.imag))
        return cst












class VisualFourier:
    """Show an application of the fourier transform."""

    #Instance methods
    def __init__(self,context,image=None,coefficients=[]):
        """Initialization."""
        self.context=context
        self.coefficients=coefficients

        #Graphs
        self.graphs=[[],[],[]]

        #Mode
        self.mode=0
        self.step=0
        self.max_step=1000
        self.messages=['drawing','construction','display']
        self.pause=False

        #Precision settings
        self.coefficients_number=100
        self.sample_number=100
        self.display_number=100 #Number of points of the display graph
        self.integral_precision=100

        #Optional settings
        #Graph shown
        self.show_image=True
        self.show_polynomial=False
        self.show_drawing=True
        self.show_display=True
        self.show_vectors=True
        self.show_circles=True
        #Graph color
        self.color_polynomial=mycolors.BLUE
        self.color_drawing=mycolors.GREEN
        self.color_display=mycolors.RED
        self.color_vectors=mycolors.WHITE
        self.color_circles=mycolors.GREY

        #Set the image for sampling
        if image is None:
            self.image=None
            self.show_image=False
        else:
            self.image=self.context.loadImage(image)
            #Trying to convert a pygame image into a pil image that can be used for the canny algorithm.
            #s=self.image.get_size()
            #self.image=pygame.image.tostring(self.image,"RGBA",False)
            #self.image=Image.frombytes("RGBA",s,self.image)
            #self.image=cv2.Canny(self.image,50,150)

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
                if event.key == K_SPACE or event.key == K_MENU or event.key == K_q:
                    self.setMode((self.mode+1)%3)
                if event.key == K_0:
                    self.show_polynomial= not(self.show_polynomial)
                if event.key == K_1:
                    self.show_image= not(self.show_image)
                if event.key == K_2:
                    self.show_drawing= not(self.show_drawing)
                if event.key == K_3:
                    self.show_display= not(self.show_display)
                if event.key == K_4:
                    self.show_vectors= not(self.show_vectors)
                if event.key == K_5:
                    self.show_circles= not(self.show_circles)
                if event.key == K_r:
                    self.mode=0
                    self.graphs=[[],[],[]]
                    self.coefficients=[]
                if event.key == K_z:
                    self.drawing = self.drawing[:-1]
                if event.key == K_s:
                    self.save() #Save the coefficients and the graphs
                if event.key == K_a:
                    self.screenshot() #Save a picture the screen
                if event.key == K_p:
                    self.pause = not(self.pause)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (event.button == 1) and (self.mode == 0): self.place()
                if event.button == 4: self.context.draw.plane.zoom([1.1,1.1])
                if event.button == 5: self.context.draw.plane.zoom([0.9,0.9])


    def main(self):
        """Code inside the loop."""
        if self.mode==0: #drawing
            pass
        elif self.mode==1: #construction
            if self.step>self.max_step:
                self.mode=2
            else:
                self.construction=Fourier.build(self.coefficients,self.time)
                self.display.append(self.construction[-1])
                if not self.pause:
                    self.context.text.append("time: "+str(self.time))
                    self.step+=1
        elif self.mode==2: #display
            pass

    def show(self):
        """Show the graph."""
        self.context.control()
        self.context.clear()
        self.context.show()
        drawing,construction,display=range(3)
        if self.show_image and self.image:
            self.context.draw.image(self.context.screen,self.image,(0,0))

        if self.mode==0:
            if self.show_polynomial:
                self.drawPolynomial(drawing,self.color_polynomial)
            if self.show_drawing:
                self.drawGraph(drawing,self.color_drawing)
        elif self.mode==1:
            if self.show_polynomial:
                self.drawPolynomial(drawing,self.color_polynomial)
            if self.show_drawing:
                self.drawGraph(drawing,self.color_drawing)
            if self.show_vectors:
                self.drawVectors(construction,self.color_vectors)
            if self.show_circles:
                self.drawCircles(construction,self.color_circles)
            if self.show_display:
                self.drawGraph(display,self.color_display)
        elif self.mode==2:
            if self.show_polynomial:
                self.drawPolynomial(drawing,self.color_polynomial)
            if self.show_drawing:
                self.drawGraph(drawing,self.color_drawing)
            if self.show_display:
                self.drawGraph(display,self.color_display)

        if self.pause: self.context.print("Pause",size=40,conversion=False)
        self.context.showConsole()
        self.context.flip()

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
            self.setDrawingMode()
        elif self.mode==1:
            self.setConstructionMode()
        elif self.mode==2:
            self.setDisplayMode()
        self.context.text.append("mode: "+self.messages[self.mode])

    def setDrawingMode(self):
        """Set the attributes before starting the drawing mode."""
        pass

    def setConstructionMode(self):
        """Set the attributes before starting the construction mode."""
        self.step=0
        self.display=[]
        t=Trajectory.createFromTuples(self.drawing)
        l=t.sample(self.sample_number)
        self.coefficients=Fourier.transform(l,self.coefficients_number)

    def setDisplayMode(self):
        """Set the attributes before starting the display mode."""
        self.display=Fourier.inverseTransform(self.coefficients,self.display_number)

    def place(self):
        """Place a point."""
        p=self.context.point()
        self.drawing.append(p)

    def screenshot(self):
        """Make a screenshot of the window."""
        self.context.draw.window.screenshot()

    def save(self,filename="Fourier1",directory="FourierObjects"):
        """Save the sampled graph and fourier's coefficients."""
        path=directory+"/"+filename
        dictionary={
            "coefficients":     self.coefficients,
            "drawing":          self.drawing,
            "construction":     self.construction,
            "display":          self.display
            }
        pickle.dump(dictionary,open(path,'wb'))

    def load(self,filename="Fourier",directory="FourierObjects"):
        """Load the fourier's coefficients."""
        path=directory+"/"+filename
        dictionary=pickle.load(open(path,'rb'))
        self.coefficients=  dictionary["coefficients"]
        self.display=       dictionary["display"]
        self.construction=  dictionary["construction"]
        self.drawing=       dictionary["drawing"]
        print(self.coefficients)
        print(self.display)
        print(self.drawing)
        print(self.construction)

    def getTime(self):
        """Return the time of the construction."""
        return self.step/self.max_step

    time=property(getTime)


    #Graphical functions
    def distance(self,p1,p2):
        """Return the distance between 2 points."""
        return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

    def drawVectors(self,index,color):
        """Draw the vectors from the points."""
        graph=self.graphs[index]
        for i in range(len(graph)-1):
            v=Vector.createFromTwoTuples(graph[i],graph[i+1],color=color)
            v.showFromTuple(self.context,graph[i])

    def drawCircles(self,index,color):
        """Draw the circles from the points."""
        graph=self.graphs[index]
        for i in range(len(graph)-1):
            radius=self.distance(graph[i],graph[i+1])
            c=Circle.createFromPointAndRadius(graph[i],radius,color=color)
            c.show(self.context)

    def drawGraph(self,index,color,connected=False,width=1,conversion=True):
        """Draw the graph."""
        graph=self.graphs[index]
        if len(graph)>1:
            self.context.draw.lines(self.context.screen,color,graph,connected,width,conversion)

    def drawPolynomial(self,index,color,precision):
        """Draw the polynomial interpolation of the points."""
        graph=self.graphs[index]
        if len(graph)>1:
            p=PolynomialInterpolation(graph,color)
            p.show(self.context,precision)

    #Properties
    def getDrawing(self):
        return self.graphs[0]
    def setDrawing(self,graph):
        self.graphs[0]=graph
    def getConstruction(self):
        return self.graphs[1]
    def setConstruction(self,graph):
        self.graphs[1]=graph
    def getDisplay(self):
        return self.graphs[2]
    def setDisplay(self,graph):
        self.graphs[2]=graph

    drawing=property(getDrawing,setDrawing)
    construction=property(getConstruction,setConstruction)
    display=property(getDisplay,setDisplay)

if __name__=="__main__":
    from mycontext  import Context

    sj="saint jalm.jpg"
    vl="valentin.png"
    tm="tetedemarc.png"
    pm="profiledemarc.jpg"

    context=Context(name="Application of the Fourier Transform.",fullscreen=False)
    fourier=VisualFourier(context,image=None)
    #fourier.load()
    print(fourier.drawing)
    fourier()
    #fourier.save()
