"""
The goal of this program is to make an interpolation of the points of any
curve in order to make it a parametric function.


There are 2 main types of interpolations:
- Polynomial Interpolation:
- Bezier Interpolation:
"""

from marclib.polynomial import Polynomial

#Deprectated function
def directInterpolation(points,t):
    x=[pt[0] for pt in points]
    y=[pt[1] for pt in points]
    plx=Polynomial.createFromInterpolation(range(len(x)),x)
    ply=Polynomial.createFromInterpolation(range(len(y)),y)
    l=len(pts)
    mst=100



class PolynomialInterpolation:
    """Make an interpolation using the lagrangian polynomial interpolator
    over list of n-dimensional points."""

    def __init__(self,points,create=True):
        """Create the interpolation using a list of n-dimensional points."""
        self.points=points
        if create: self.create()

    def create(self):
        """Create the components useful for the interpolation which are the
        split components and the lagrangian polynomials."""
        self.createComponents()
        self.createPolynomials()

    def createComponents(self):
        """Split its components of each point in separate lists."""
        self.components=[[pt[i] for pt in self.points] for i in range(len(self.points[0]))]

    def createPolynomials(self):
        """Create its polynomials using its components."""
        lpts=len(self.points)
        self.polynomials=[Polynomial.createFromInterpolation(range(lpts),c) for c in self.components]

    def __call__(self,t):
        """Evaluate the parametric interpolation for the input 't' between 0 and 1."""
        lcps=len(self.components)
        return tuple([self.polynomials[i](t) for i in range(lcps)])

    def sample(self,n):
        """Make a sample of the interpolation for n points."""
        lpts=len(self.points)
        l=lpts-1
        return [self(l*t/n) for t in range(n+1)]

class BezierInterpolation:
    """Make an interpolation using the bezier interpolation over a list of
    n-dimensional points."""

    def __init__(self,points,create=True):
        """Create the interpolation using a list of n-dimensional points."""
        self.points=points
        if create: self.create()

    def create(self):
        pass

    def __call__(self):
        pass

    def sample(self,n):
        """Make a sample of the interpolation for n points."""
        lpts=len(self.points)
        l=lpts-1
        #return [self(lpts*t) for t in np.linspace(0,1,n)]
        return [self(l*t/n) for t in range(n+1)]


if __name__=="__main__":
    #To show the points
    from mycontext import Context
    import mycolors
    #To create the points
    import random

    context=Context()

    #Parameters
    h=1; w=1
    xmin=-w
    xmax=w
    ymin=-h
    ymax=h
    n=5

    #Creation of the points
    pts=[(random.uniform(xmin,xmax),random.uniform(ymin,ymax)) for i in range(n)]

    """ Tests:
    Calculations for n points in dimension 2:

    x=[pt[0] for pt in pts]
    y=[pt[1] for pt in pts]
    plx=Polynomial.createFromInterpolation(range(len(x)),x)
    ply=Polynomial.createFromInterpolation(range(len(y)),y)
    print(plx)
    print(ply)
    l=len(pts)
    mst=100
    npts=[(plx(l*st/mst),ply(l*st/mst)) for st in range(mst)]
    grapher=Grapher(context,functions=[plx,ply])
    """

    #Final version
    interpolation=PolynomialInterpolation(pts)
    npts=interpolation.sample(200) #Sample 200 points by interpolation

    #Main loop of the context
    while context.open:
        context.check()
        context.control()
        context.clear()
        context.show()
        context.draw.lines(context.screen,mycolors.GREEN,pts,width=3,connected=False)
        context.draw.lines(context.screen,mycolors.RED,npts,connected=False)
        context.flip()
