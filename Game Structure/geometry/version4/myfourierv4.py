import random
import cmath
import math

npts=100+1
ncfs=20+1
xmin,ymin,xmax,ymax=[-1,-1,1,1]
wo=2*math.pi

#pts

pts=[(random.uniform(i,i+1),random.uniform(ymin,ymax)) for i in range(npts)]
#iterate=lambda i:int(((i+1)//2)*(-1)**(i+1)) #This has not been used at the end


def transform(pts,ncfs):
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


def originialInverseTransform(cfs,npts):
    ncfs=len(cfs)
    h=npts//2
    pts=[]
    #Compute all the points
    csts=[]
    for it in range(npts):
        t=it/npts
        cst=[]
        zpt=cfs[0]
        cst.append((zpt.real,zpt.imag))
        for n in range(1,h+1):
            pcf=cfs[n]*cmath.exp(1j*wo*n*t)
            ncf=cfs[-n]*cmath.exp(1j*wo*(-n)*t)
            zpt+=pcf
            cst.append((zpt.real,zpt.imag))
            zpt+=ncf
            cst.append((zpt.real,zpt.imag))
        pts.append((zpt.real,zpt.imag))
        csts.append(cst)
    return (pts,csts)

def inverseTransform(cfs,npts):
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


def build(cfs,t):
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


cfs=transform(pts,ncfs)
print(cfs)

pts2=inverseTransform(cfs,npts)
print(pts2)


"""
Draft:

fermi={0:0, 1:50-30j, -1:18+8j, 2:12-10j, -2:-14-60j, 3:20+20j}
elephant=inverseTransform(fermi,200)
#n>0
#cn=(an-ibn)/2
#n<0
#cn=(an+ibn)/2


print(pts[0],pts2[0])
#fermi={0:50-30j,18+8j}
"""


if __name__=="__main__":
    from mycontext import Context
    from myabstract import Vector, Circle
    import mycolors

    def distance(p1,p2):
        """Return the distance between 2 points."""
        return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

    def drawVectors(context,color,points):
        """Draw the vectors from the points."""
        for i in range(len(points)-1):
            v=Vector.createFromTwoTuples(points[i],points[i+1],color=color)
            v.showFromTuple(context,points[i])

    def drawCircles(context,color,points):
        """Draw the circles from the points."""
        for i in range(len(points)-1):
            radius=distance(points[i],points[i+1])
            c=Circle.createFromPointAndRadius(points[i],radius,color=color)
            c.show(context)

    trace=[]
    context=Context(fullscreen=False)
    n=0
    mn=1000
    while context.open:
        context.check()
        context.control()
        context.clear()
        context.show()

        #Update the variables
        n=(n+1)%mn
        t=n/mn
        cst=build(cfs,t)
        trace.append(cst[-1])

        #Show the graphical components
        context.draw.lines(context.screen,mycolors.GREEN,pts,connected=False,width=1,conversion=True)
        drawVectors(context,mycolors.WHITE,cst)
        drawCircles(context,mycolors.GREY,cst)
        if len(trace)>1: #Its not easy to draw lines from 1 single point
            context.draw.lines(context.screen,mycolors.BLUE,trace,connected=False,width=1,conversion=True)
        #context.draw.lines(context.screen,mycolors.RED,pts2,connected=False,width=1,conversion=True) #Inverse Transform test
        #context.draw.lines(context.screen,mycolors.WHITE,elephant,connected=True,width=1,conversion=True) #Fermi test

        context.flip()
