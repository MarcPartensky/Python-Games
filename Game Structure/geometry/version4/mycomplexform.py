from myabstract import Form,Point,Segment

import numpy as np

import random

class ComplexForm(Form):
    """The fact that complex from inherits from Form involves overloading all
    specific methods of forms which make sense in a complex form but cannot work.
    This choice was made out of pure lazyness."""

    def random(corners=[-1,-1,1,1],number=random.randint(3,10),**kwargs):
        """Create a random form using optional corners, number of points and other optional arguments."""
        points=[Point.random(corners) for i in range(number)]
        form=ComplexForm(points,**kwargs)
        form.makeSparse()
        return form

    def __init__(self,*args,**kwargs):
        """Create a complex form."""
        super().__init__(*args,**kwargs)
        #self.points=points #The points are in relative coordonnates to the position
        l=len(self.points)
        self.network=np.zeros((l,l))
        self.network.fill(1)
        self.network=np.triu(self.network)
        self.network[0][0]=0
        self.network[0][3]=0
        self.network[3][3]=0
        print(self.network)

    def segments(self):
        """Return the segments determined by the points and the network established."""
        segments=[]
        l=len(self.points)
        for j in range(l):
            for i in range(j):
                if self.network[i][j]:
                    segment=Segment(self.points[i],self.points[j])
                    segments.append(segment)
        return segments

    def show(self,surface):
        """Show the complex form on the surface."""
        for point in self.points:
            point.show(surface)
        for segment in self.segments():
            segment.show(surface)

    def getRegions(self):
        """Decompose the complex forms in multiple normal forms which cannot be cut by a segment."""
        vectors=[Vector.createFromSegment(segment) for segment in self.segments()]
        for j in range(l):
            for i in range(j):
                if self.network[i][j]:
                    segment=Segment(self.points[i],self.points[j])
                    vector=x
                    segments.append(segment)

        for vector in vectors:
            pass

        return segments

    def split(self):
        """Return all the system of forms that compose the complex forms."""
        links=[(p,0) for p in self.points]

    def countContacts(self):
        """Return the list of contacts for each points, which means how many points
        is a given point connected to."""
        return [np.sum(self.network[:][j]) for j in range(len(self.points))]


if __name__=="__main__":
    from mysurface import Surface
    surface=Surface(name="Complex Form")
    f=ComplexForm.random(number=5)
    print(f.countContacts())
    print(f.points)
    print(f.crossSelf())
    while surface.open:
        surface.check()
        surface.control()
        surface.clear()
        surface.show()
        for p in f:
            p.rotate(0.01)
        f.show(surface)
        surface.flip()
