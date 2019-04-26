from mysurface import Surface

import math
import cmath
import numpy as np

import mycolors


class Mandelbrot:

    def linearBijection(x,ensemble_entree,ensemble_sortie):
        """Renvoie la valeur de f(x) par la bijection de l'ensemble_entree et l'ensemble_sortie."""
        min1,max1=ensemble_entree
        min2,max2=ensemble_sortie
        return (x-min1)/(max1-min1)*(max2-min2)+min2

    def __init__(self,iterations=5,digits=5):
        """Create a mandelbrot set."""
        self.iterations=iterations
        self.digits=digits

    def getColor(self,number,borns):
        """Return a color using a result of the """
        minimum,maximum=borns
        k=255-int(Mandelbrot.linearBijection(number,borns,[0,255]))
        return (k,0,0)

    def evaluate(self,x,y):
        """Evaluate position using the x and y."""
        zn=complex(0,0)
        c=complex(x,y)
        for i in range(self.iterations):
            zn=zn**2+c
        n=math.sqrt(zn.real**2+zn.imag**2)
        return n

    def surevaluate(x,y):
        """Surevaluate the position using the x and y components."""
        return int(n>2)

    def smooth(self,number):
        """Smooth a number using log and round functions. This process speeds up calculation."""
        return round(math.log(number+1),self.digits)

    def smoothSupport(self,support):
        """Smooth a support using round functions. This process speeds up calculation."""
        return [round(e,self.digits) for e in support]

    def show(self,surface,precision=[10,10]):
        """Show the mandelbrot set on the surface."""
        wsx,wsy=surface.draw.window.size
        corners=surface.draw.plane.getPlaneCorners(surface.draw.window)
        mx,my,Mx,My=corners
        px,py=precision
        ux,uy=surface.draw.plane.units
        print(ux,uy)
        px/=ux
        py/=uy
        x_support=np.arange(mx,Mx,px)
        y_support=np.arange(my,My,py)
        x_support=self.smoothSupport(x_support)
        y_support=self.smoothSupport(y_support)
        lx=len(x_support)
        ly=len(y_support)
        m=np.zeros((lx,ly))

        for iy in range(ly):
            for ix in range(lx):
                x=x_support[ix]
                y=y_support[iy]
                result=self.evaluate(x,y)
                result=self.smooth(result)
                m[ix][iy]=result

        maximum=np.max(m)
        minimum=np.min(m)
        borns=[minimum,maximum]

        for iy in range(ly):
            for ix in range(lx):
                x=x_support[ix]
                y=y_support[iy]
                value=m[ix][iy]
                color=self.getColor(value,borns)
                rect=[x,y,px,py]
                surface.draw.rect(surface.draw.window.screen,color,rect,1)




    def oldShow(self,surface,precision=[0.1,0.1]):
        """Show the mandelbrot set on the surface."""

        #Convert all the coordonnates to show on screen and for calculus
        window=surface.draw.window
        wsx,wsy=window.size
        ux,uy=surface.draw.plane.units #Units of the plane (how many pixels for 1 unit to display on screen in x and y components)
        plx,ply=1/ux,1/uy
        mx,my=surface.draw.plane.getFromScreen([0,0],surface.draw.window) #Top left corner
        Mx,My=surface.draw.plane.getFromScreen(window.size,surface.draw.window) #Top right corner

        plx,ply=abs(plx),abs(ply)
        prx,pry=precision
        prx,pry=abs(prx),abs(pry)

        #Store all evaluations in a matrix m
        itx=int(abs((Mx-mx)/prx))+1
        ity=int(abs((My-my)/pry))+1
        m=np.zeros((itx,ity))
        for iy in range(0,ity):
            for ix in range(0,itx):
                x=mx+ix*prx
                y=my+iy*pry
                result=self.evaluate(x,y) #Apply real calculation for mandelbrot set
                m[ix][iy]=self.smooth(result) #Apply a log function for simplicity

        maximum=np.max(m)
        minimum=np.min(m)
        borns=[minimum,maximum]

        #Show all the evaluations using colors adapted to the matrix
        for iy in range(0,ity):
            for ix in range(0,itx):
                x=mx+ix*prx
                y=my+iy*pry
                rect=[x,y,prx,pry]
                color=self.getColor(m[ix][iy],borns)
                surface.draw.rect(surface.draw.window.screen,color,rect,1)


if __name__=="__main__":
    surface=Surface()
    mandelbrot=Mandelbrot()
    result=mandelbrot.evaluate(100,50)
    while surface.open:
        surface.check()
        surface.control()
        surface.clear()
        surface.show()
        #surface.draw.rect(surface.screen,mycolors.ORANGE,(1,1,2,3),0)
        mandelbrot.show(surface)
        surface.flip()
