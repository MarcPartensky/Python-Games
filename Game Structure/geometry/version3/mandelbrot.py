from mysurface import Surface

import math
import cmath
import numpy as np

class Mandelbrot:
    def __init__(self,iterations=5):
        self.iterations=iterations

    def getColor(self,number,max):
        """Return a color using a result of the """
        #k=int(255-number/max*255)
        k=int(255-abs(math.log(number))/100*255)
        #print(k)
        return (k,k,k)

    def evaluate(self,x,y):
        """Evaluate position using the x and y."""
        zn=complex(0,0)
        c=complex(x,y)
        for i in range(self.iterations):
            zn=zn**2+c
        n=math.sqrt(zn.real**2+zn.imag**2)
        return n

    def show(self,surface,precision=[0.1,0.1]):
        """Show the mandelbrot set on the surface."""

        #Convert all the coordonnates to show on screen and for calculus
        window=surface.draw.window
        wsx,wsy=window.size
        ux,uy=surface.draw.plane.units #Units of the plane (how many pixels for 1 unit to display on screen in x and y components)
        plx,ply=1/ux,1/uy
        mx,my=surface.draw.plane.getFromScreen([0,0],surface.draw.window) #Top left corner
        Mx,My=surface.draw.plane.getFromScreen(window.size,surface.draw.window) #Top right corner

        plx,ply=abs(plx),abs(ply)
        if not precision: precision=[plx,ply]
        prx,pry=precision
        prx,pry=abs(prx),abs(pry)
        print("pr",prx,pry)

        #Store all evaluations in a matrix m
        itx=int(abs((Mx-mx)/prx))+1
        ity=int(abs((My-my)/pry))+1
        m=np.zeros((itx,ity))
        for iy in range(0,ity):
            for ix in range(0,itx):
                x=mx+ix*prx
                y=my+iy*pry
                m[ix][iy]=self.evaluate(x,y)

        #Show all the evaluations using colors adapted to the matrix
        for iy in range(0,ity):
            for ix in range(0,itx):

                x=mx+ix*prx
                y=my+iy*pry
                print(x,y)
                rect=[x,y,prx,pry]
                color=self.getColor(m[ix][iy],max)
                #print(rect)
                surface.draw.rect(surface.draw.window.screen,color,rect,0)

if __name__=="__main__":
    surface=Surface()
    mandelbrot=Mandelbrot()
    while surface.draw.window.open:
        surface.check()
        surface.show()
        surface.control()
        mandelbrot.show(surface)
        surface.draw.window.flip()
