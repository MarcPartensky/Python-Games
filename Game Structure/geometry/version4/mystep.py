from myabstract import Segment,Point
import mycolors
import math


class Step(Segment):
    """A step is a segment which show method has been overloaded to look like a vector."""
    def random(corners=[-1,-1,1,1]):
        """Create a random step."""
        p1=Point.random(corners)
        p2=Point.random(corners)
        return Step(p1,p2)

    def __init__(self,*args,**kwargs):
        """Create a step."""
        super().__init__(*args,**kwargs)
        self.color=mycolors.YELLOW

    def __str__(self):
        """Return the str representation of the step."""
        return "st("+",".join([str(c) for c in self.points])+")"

    def show(self,context):
        """Show the step on the context."""
        self.vector.show(context,self.p1,color=self.color)
        t1=1-self.vector.arrow[0]*math.cos(self.vector.arrow[1])
        t2=0
        self.showBar(context,t1,0.05)
        self.showBar(context,t2,0.05)


    def showBar(self,context,t,l):
        """Show the bar."""
        v=self.getVector()
        v*=l
        p=self(t)
        v.rotate(math.pi/2)
        p1=v(p)
        v.rotate(math.pi)
        p2=v(p)
        s=Segment(p1,p2)
        s.color=self.color
        s.show(context)


if __name__=="__main__":
    from mysurface import Surface
    surface=Surface()
    o=Point.origin()
    s=Step.random()
    print(s)
    while surface.open:
        surface.check()
        surface.control()
        surface.clear()
        surface.show()
        s.rotate(0.001,o)
        o.show(surface)
        s.show(surface)
        surface.flip()
