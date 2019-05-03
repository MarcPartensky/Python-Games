from mydirection import Direction
from mypoint import Point
from mysegment import Segment
from myvector import Vector

import math
import random
import mycolors

class Line(Direction):
    def random(min=-1,max=1,width=1,color=mycolors.WHITE):
        """Return a random line."""
        point=Point.random(min,max)
        angle=random.uniform(min,max)
        return Line(point,angle,width,color)

    def createFromPointAndVector(point,vector,width=1,color=mycolors.WHITE):
        """Create a line using a point and a vector with optional features."""
        angle=vector.angle()
        line=Line(point,angle,width=1,color=(255,255,255))
        return line

    def createFromTwoPoints(self,point1,point2,width=1,color=mycolors.WHITE):
        """Create a line using two points with optional features."""
        vector=Vector(point1,point2)
        angle=vector.angle()
        line=Line(point,angle,width,color)
        return line

    def __init__(self,point,angle,width=1,color=(255,255,255),correct=True):
        """Create the line using a point and a vector with optional width and color.
        Caracterizes the line with a unique system of components [neighbour point, angle].
        The neighbour point is the nearest point to (0,0) that belongs to the line.
        The angle is the orientated angle between the line itself and another line parallel
        to the x-axis and crossing the neighbour point. Its range is [-pi/2,pi/2[ which makes it unique."""
        self.point=point
        self.angle=angle
        self.width=width
        self.color=color
        if correct: self.correct()

    def correctAngle(self):
        """Correct angle which is between [-pi/2,pi/2[."""
        while self.angle>=math.pi/2:
            self.angle-=math.pi
        while self.angle<-math.pi/2:
            self.angle+=math.pi

    def correctPoint(self):
        """Correct the point to the definition of the neighbour point."""
        origin=Point([0,0])
        point=self.projectPoint(origin)
        self.point=point

    def correct(self):
        """Correct the line."""
        self.correctAngle()
        self.correctPoint()

    def getCompleteCartesianCoordonnates(self):
        """Return a,b,c according to the cartesian equation of the line: ax+by+c=0."""
        """Because there are multiple values of a,b,c for a single line, the simplest combinaision is returned."""
        v=self.vector()
        p1=self.point
        p2=v(self.point)
        if v.x==0:
            a=1
            b=0
            c=-p1.x
        else:
            a=-(p1.y-p2.y)/(p1.x-p2.x)
            b=1
            c=-(a*p1.x+b*p1.y)
        return (a,b,c)

    def getReducedCartesianCoordonnates(self):
        """Return a,b according to the reduced cartesian equation of the line: y=ax+b."""
        a=self.slope()
        b=self.ordinate()
        return (a,b)

    def getAngle(self):
        """Return the angle of the line."""
        return self.angle

    def setAngle(self,angle):
        """Set the angle of the line."""
        self.angle=angle
        self.correctAngle()

    def rotate(self,angle,point=Point(0,0)):
        """Rotate the line.""" #Incomplete
        self.angle+=angle
        self.correctAngle()

    def getPoint(self):
        """Return the neighbour point."""
        return self.point

    def setPoint(self,point):
        """Set the neighbour point to another one."""
        self.point=point
        self.correctPoint()


    def getUnitVector(self):
        """Return the unit vector of the line."""
        vector=Vector.createFromPolarCoordonnates(1,self.angle)
        return vector

    def getNormalVector(self):
        """Return the normal vector of the line."""
        vector=self.getUnitVector()
        vector.rotate(math.pi/2)
        return vector

    vector=getUnitVector

    def slope(self):
        """Return the slope of the line."""
        p1=self.point
        vector=self.getUnitVector()
        p2=vector(p1) #Because of the way the angle of a line is defined, the x component of the second point is greater than the one of the first
        Dx=p2.x-p1.x
        Dy=p2.y-p1.y
        return Dy/Dx

    def ordinate(self):
        """Return the ordinate of the line."""
        p=self.point
        a=self.slope()
        if a: return p.y-a*p.x

    def getFunction(self):
        """Return the affine function that correspond to the line."""
        a=self.slope()
        b=self.ordinate()
        return lambda x:a*x+b

    def getReciproqueFunction(self):
        """Return the reciproque of the affine function that correspond to the line."""
        a=self.slope()
        b=self.ordinate()
        return lambda y:(y-b)/a

    def evaluate(self,x):
        """Evaluate the line as a affine function."""
        function=self.getFunction()
        y=function(x)
        return y

    def devaluate(self,y):
        """Evaluate the reciproque function of the affine funtion of the line."""
        function=self.getReciproqueFunction()
        x=function(y)
        return x

    def __or__(self,other):
        """Return if 2 objects are crossing."""
        if isinstance(other,Direction):
            return self.crossLine(other)



    def crossSegment(self,other):
        """Determine if the segment is crossing with another segment."""
        if self.parallel(other): return None #If the segments are parallels then there is not point
        #Extract the slopes and ordinates
        sb=self.ordinate()
        ob=other.getLine().ordinate()
        sa=self.slope()
        oa=other.getLine().slope()
        #Find a possible intersection point using line intersection
        x=(sb-ob)/(oa-sa)
        y=sa*x+sb
        #Determine if the point of intersection belongs to both the segment and the line
        xmin,ymin,xmax,ymax=other.getCorners()
        #If it is the case return the point
        if  xmin<=x<=xmax and ymin<=y<=ymax:
            return Point(x,y,color=self.color)
        #By default if nothing is returned the function returns None


    def oldcrossLine(self,other):
        """Return the point of intersection between the two lines."""
        if self.parallel(other): return None
        #Extract the slopes and ordinates
        sb=self.ordinate()
        ob=other.ordinate()
        sa=self.slope()
        oa=other.slope()
        #Find a possible intersection point using line intersection
        x=(sb-ob)/(oa-sa)
        y=sa*x+sb
        #Return the intersection point
        return Point(x,y,color=self.color)

    def crossLine(self,other):
        """Return the point of intersection between two lines with vectors calculation."""
        a,b=self.point
        c,d=other.point
        m,n=self.vector()
        o,p=other.vector()
        if n*o-m*p==0: return None #The lines are parallels
        x=(a*n*o-b*m*o-c*m*p+d*m*o)/(n*o-m*p)
        y=(x-a)*n/m+b
        rx=round(x,15)
        ry=round(y,15)
        return Point(rx,ry)

    def parallel(self,other):
        """Determine if the line is parallel to another object (line or segment)."""
        return other.angle==self.angle

    def __contains__(self,point):
        """Determine if a point belongs to the line."""
        v1=self.vector()
        v2=Vector(self.point,point)
        scalar=v1.scalar(v2)
        return scalar


    def projectPoint(self,point):
        """Return the projection of the point on the line."""
        vector=self.getNormalVector()
        angle=vector.angle()
        line=Line(point,angle,correct=False)
        projection=self.crossLine(line)
        return projection

    def projectSegment(self,segment):
        """Return the projection of a segment on the line."""
        p1,p2=segment
        p1=self.projectPoint(p1)
        p2=self.projectPoint(p2)
        return Segment(p1,p2,segment.width,segment.color)

    def getSegmentWithinXRange(self,xmin,xmax):
        """Return the segment made of the points of the line which x component is
        between xmin and xmax."""
        yxmin=self.evaluate(xmin)
        yxmax=self.evaluate(xmax)
        p1=Point(xmin,yxmin)
        p2=Point(xmax,yxmax)
        return Segment(p1,p2)


    def getSegmentWithinYRange(self,ymin,ymax):
        """Return the segment made of the points of the line which y component is
        between ymin and ymax."""
        xymin=self.devaluate(ymin)
        xymax=self.devaluate(ymax)
        p1=Point(xymin,ymin)
        p2=Point(xymax,ymax)
        return Segment(p1,p2,width=self.width,color=self.color)

    def oldgetSegmentWithinCorners(self,corners):
        """Return the segment made of the poins of the line which are in the area
        delimited by the corners."""
        xmin,ymin,xmax,ymax=corners
        yxmin=self.evaluate(xmin)
        yxmax=self.evaluate(xmax)
        xymin=self.devaluate(ymin)
        xymax=self.devaluate(ymax)
        nxmin=max(xmin,xymin)
        nymin=max(ymin,yxmin)
        nxmax=min(xmax,xymax)
        nymax=min(ymax,yxmax)
        p1=Point(nxmin,nymin)
        p2=Point(nxmax,nymax)
        return Segment(p1,p2,width=self.width,color=self.color)

    def oldgetSegmentWithinCorners(self,corners):
        """Return the segment made of the poins of the line which are in the area
        delimited by the corners."""
        xmin,ymin,xmax,ymax=corners
        p1=Point(xmin,ymin)
        p2=Point(xmax,ymin)
        p3=Point(xmax,ymax)
        p4=Point(xmin,ymax)
        s1=Segment(p1,p2)
        s2=Segment(p2,p3)
        s3=Segment(p3,p4)
        s4=Segment(p4,p1)
        segments=[s1,s2,s3,s4]
        intersections=[]
        print(segments)
        for segment in segments:
            cross=self.crossSegment(segment)
            if cross:
                intersections.append(cross)
        print("intersections: ",intersections)
        return Segment(intersections)

    def getPointsWithinCorners(self,corners):
        """Return the segment made of the poins of the line which are in the area
        delimited by the corners."""
        xmin,ymin,xmax,ymax=corners
        p1=Point(xmin,ymin)
        p2=Point(xmax,ymin)
        p3=Point(xmax,ymax)
        p4=Point(xmin,ymax)
        v1=Vector(p1,p2)
        v2=Vector(p2,p3)
        v3=Vector(p3,p4)
        v4=Vector(p4,p1)
        l1=Line.createFromPointAndVector(p1,v1)
        l2=Line.createFromPointAndVector(p2,v2)
        l3=Line.createFromPointAndVector(p3,v3)
        l4=Line.createFromPointAndVector(p4,v4)
        lines=[l1,l3]
        points=[]
        for line in lines:
            cross=self.crossLine(line)
            if cross:
                points.append(cross)
        if not points:
            lines=[l2,l4]
            for line in lines:
                cross=self.crossLine(line)
                if cross:
                    points.append(cross)
        print("points: ",points)
        return points




    def show(self,surface,width=None,color=None):
        """Show the line on the surface."""
        if not color: color=self.color
        if not width: width=self.width
        corners=surface.getCorners()
        print("corners: ",corners)
        points=self.getPointsWithinCorners(corners)
        print(points)
        p1,p2=points
        #print("points: ",segment.p1,segment.p2)
        surface.draw.line(surface.screen,color,[p1.x,p1.y],[p2.x,p2.y],width=width)



if __name__=="__main__":
    from mysurface import Surface
    surface=Surface(fullscreen=True)
    p1=Point(1,0,radius=0.05,color=mycolors.YELLOW)
    p2=Point(1,1,radius=0.05,color=mycolors.YELLOW)
    origin=Point(0,0)

    print("Creating Line")
    l1=Line(origin,math.pi/4,correct=False)
    l2=Line(p1,math.pi/2,correct=False)
    print("l1.vector: ",l1.vector())
    print("l2.vector: ",l2.vector())
    intersection=l1.crossLine(l2)
    print("intersection: ",intersection)

    print("point: ",l2.point)
    #surface.draw.window.pause()
    print("scalar product:",p2 in l1)
    #surface()



    while surface.open:
        #Surface specific commands
        surface.check()
        surface.control()
        surface.clear()
        surface.show()

        #Actions
        l1.rotate(0.01,p2)
        l2.rotate(-0.02,p1)
        p=l1|l2
        o=Point(0,0)
        p3=l2.projectPoint(o)

        #Show
        surface.draw.window.print("l1.angle: "+str(l1.angle),(10,10))
        surface.draw.window.print("l2.angle: "+str(l2.angle),(10,30))

        o.show(surface,color=mycolors.GREY)
        o.showText(surface,"origin")

        p3.showText(surface,"origin's projection")
        p3.show(surface,color=mycolors.LIGHTGREY)

        if p:
            p.show(surface,color=mycolors.RED)
            p.showText(surface,"intersection point",color=mycolors.RED)


        p1.show(surface)
        p1.showText(surface,"p1")

        p2.show(surface)
        p2.showText(surface,"p2")

        l1.show(surface,color=mycolors.GREEN)
        l1.point.show(surface,color=mycolors.LIGHTGREEN,mode="cross",width=3)
        l1.vector().show(l1.point,surface,color=mycolors.LIGHTGREEN,width=3)

        l2.show(surface,color=mycolors.BLUE)
        l2.point.show(surface,color=mycolors.LIGHTBLUE,mode="cross",width=3)
        l2.vector().show(l2.point,surface,color=mycolors.LIGHTBLUE,width=3)

        #Flipping the screen
        surface.flip()
