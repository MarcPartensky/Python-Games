from myabstract import Point,Segment,Form

import random
import mycolors

class Trajectory:
    def __init__(self,points,segment_color=mycolors.WHITE,point_color=mycolors.WHITE):
        """Create a trajectory using the list of points."""
        self.points=points
        self.segment_color=segment_color
        self.point_color=point_color

    def segments(self):
        """Return the segments that connect the points."""
        return [Segment(self.points[i],self.points[i+1]) for i in range(len(self.points)-1)]

    def show(self,surface):
        """Show the trajectory on the surface."""
        self.showPoints(surface)
        self.showSegments(surface)

    def showPoints(self,surface,color=None):
        """Show the point on the surface."""
        if not color: color=self.point_color
        for point in self.points:
            point.show(surface,color=color)

    def showSegments(self,surface,color=None):
        """Show the segments on the surface."""
        if not color: color=self.segment_color
        for segment in self.segments():
            segment.show(surface,color=color)

class CurvedForm(Form):
    def __init__(self,*args,**kwargs):
        """Create a bezier form."""
        super().__init__(*args,**kwargs)
    def show(self,surface):
        """Show the curved form on the screen."""
        b=BezierCurve(self.points+[self.points[0]])
        b.show(surface)



class BezierCurve:
    def __init__(self,points,point_color=mycolors.WHITE,segment_color=mycolors.WHITE):
        """Create a bezier curve object using 3 points."""
        self.points=points
        self.segment_color=segment_color
        self.point_color=point_color

    def getPoints(self):
        """Return the points of the bezier curve."""
        return self.points

    def setPoints(self):
        """Set the points of the bezier curve."""

    def __call__(self,t):
        """Return the point."""
        points=self.getPoints()
        if len(points)==0:
            return None
        elif len(points)==1:
            return points[0]
        elif len(points)==2:
            segment=Segment(points[0],points[1])
            point=segment.center()
            return point
        elif len(points)==3:
            p1,p2,p3=points
            s1=Segment(p1,p2)
            s2=Segment(p2,p3)
            ps1=s1(t)
            ps2=s2(t)
            s=Segment(ps1,ps2)
            return s(t)
        else:
            while len(points)>3:
                segments=[Segment(points[i],points[i+1]) for i in range(len(points)-1)]
                points=[segment(t) for segment in segments]
            b=BezierCurve(points)
            return b(t)

    def show(self,surface,p=50):
        """Show the bezier curve on the surface."""
        points=[self(i/p) for i in range(p)]
        segments=[Segment(points[i],points[i+1]) for i in range(p-1)]
        self.showPoints(surface,points)
        self.showSegments(surface,segments)


    def getConstruction(self,t):
        """Return the construction segments of the form."""
        points=self.getPoints()
        construction=[]
        while len(points)>=2:
            segments=[Segment(points[i],points[i+1]) for i in range(len(points)-1)]
            points=[segment(t) for segment in segments]
            construction.append(segments)
        return construction


    def showConstruction(self,surface,t):
        """Show the construction of the form at the t position."""
        construction=self.getConstruction(t)
        print(construction)
        l=len(construction)
        for i in range(l):
            k=255*(i+1)/l
            color=(0,0,k)
            for segment in construction[i]:
                print(segment)
                segment.show(surface,color=color,width=2)

    def showPoints(self,surface,points,color=None):
        """Show the points on the surface."""
        if not color: color=self.point_color
        for point in points:
            point.show(surface,color=color,radius=0.01)

    def showSegments(self,surface,segments,color=None):
        """Show the segments on the surface."""
        if not color: color=self.segment_color
        for segment in segments:
            segment.show(surface,color=color,width=2)



class Arrow(BezierCurve):
    """Join 2 objects with an arrow."""
    def __init__(self,points,point_color=mycolors.WHITE,segment_color=mycolors.WHITE,vector_color=mycolors.WHITE):
        super().__init__(self,points,point_color,segment_color,vector_color)

    def show(self,surface,p=50):
        """Show the arrow on the screen."""
        points=[self(i/p) for i in range(p)]
        segments=[Segment(points[i],points[i+1]) for i in range(p-1)]
        vectors=[Vector(points[i],points[i+1]) for i in range(0,p-1,5)]
        self.showPoints(surface,points)
        self.showSegments(surface,segments)
        self.showVectors(surface,vectors)

    def showVectors(self,surface,vectors,color=None):
        """Show the vectors on the surface."""
        if not color: color=self.vector_color
        for vector in vectors:
            vector.show(surface,color=color)




if __name__=="__main__":
    from mysurface import Surface
    surface=Surface()
    l=10
    points=[Point(2*x,random.randint(-5,5)) for x in range(l)]
    t=Trajectory(points,segment_color=mycolors.GREY)
    b=BezierCurve(points,segment_color=mycolors.RED)
    #b=CurvedForm(points)
    n=0

    while surface.open:
        surface.check()
        surface.control()
        surface.clear()
        surface.show()

        Point.turnPoints([1/1000 for i in range(l)],points)
        n=(n+1)%50
        b.showConstruction(surface,n/50)

        t.show(surface)
        b.show(surface)

        b(n/50).show(surface,color=mycolors.YELLOW,radius=0.1,fill=True)


        surface.flip()
