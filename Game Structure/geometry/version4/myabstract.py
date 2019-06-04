from math import pi,sqrt,atan,cos,sin
from cmath import polar
from mytools import timer

import math
import random
import mycolors

mean=lambda x:sum(x)/len(x)

digits=2 #Number of digits of precision of the objects when displayed


class Point:
    """Representation of a point that can be displayed on screen."""
    def origin(length=2):
        """Return the origin."""
        return Point([0 for i in range(length)])

    null=neutral=origin


    def random(corners=[-1,-1,1,1],radius=0.02,fill=False,color=mycolors.WHITE):
        """Create a random point using optional minimum and maximum."""
        xmin,ymin,xmax,ymax=corners
        x=random.uniform(xmin,xmax)
        y=random.uniform(ymin,ymax)
        return Point(x,y,radius=radius,fill=fill,color=color)

    def turnPoints(angles,points):
        """Turn the points around themselves."""
        l=len(points)
        for i in range(l-1):
            points[i].turn(angles[i],points[i+1:])

    def showPoints(surface,points):
        """Show the points on the surface."""
        for point in points:
            point.show(surface)

    def createFromVector(vector):
        """Create a point from a vector."""
        return Point(vector.x,vector.y)

    def __init__(self,*args,mode=0,size=[0.1,0.1],width=1,radius=0.05,fill=False,color=mycolors.WHITE):
        """Create a point using x, y, radius, fill and color."""
        args=list(args)
        if len(args)==1: args=args[0]
        self.components=list(args)
        self.mode=mode
        self.size=size
        self.width=width
        self.radius=radius
        self.fill=fill
        self.color=color

    def __len__(self):
        """Return the number of components of the point."""
        return len(self.components)

    def setX(self,value):
        """Set the x component."""
        self.components[0]=value

    def getX(self):
        """Return the x component."""
        return self.components[0]

    def delX(self):
        """Delete the x component and so shifting to a new one."""
        del self.components[0]

    def setY(self,value):
        """Set the y component."""
        self.components[1]=value

    def getY(self):
        """Return the y component."""
        return self.components[1]

    def delY(self):
        """Delete the y component."""
        del self.components[1]

    x=property(getX,setX,delX,"Allow the user to manipulate the x component easily.")
    y=property(getY,setY,delY,"Allow the user to manipulate the y component easily.")

    def __eq__(self,other):
        """Determine if two points are equals by comparing its components."""
        return abs(self-other)<10e-10

    def __ne__(self,other):
        """Determine if two points are unequals by comparing its components."""
        return tuple(self)!=tuple(other)

    def __call__(self):
        """Return the coordonnates of the points."""
        return [self.x,self.y]

    def __position__(self):
        """Return the coordonnates of the points."""
        return [self.x,self.y]

    def __contains__(self,other):
        """Determine if an object is in the point."""
        x,y=other
        return  self.radius>=sqrt((x-self.x)**2+(y-self.y)**2)

    def __getitem__(self,index):
        """Return x or y value using given index."""
        return self.components[index]

    def __setitem__(self,index,value):
        """Change x or y value using given index and value."""
        self.components[index]=value

    def __abs__(self):
        """Return the distance of the point to the origin."""
        return Vector.createFromPoint(self).norm

    def rotate(self,angle=pi,point=None):
        """Rotate the point using the angle and the center of rotation.
        Uses the origin for the center of rotation by default."""
        if not point: point=Point(0,0)
        v=Vector(self.x-point[0],self.y-point[1])
        v.rotate(angle)
        new_point=v(point)
        self.x,self.y=new_point

    def turn(self,angle=pi,points=[]):
        """Turn the points around itself."""
        for point in points:
            point.rotate(angle,self)

    def move(self,*step):
        """Move the point using given step."""
        self.x+=step[0]
        self.y+=step[1]

    def showCross(self,window,color=None,size=None,width=None):
        """Show the point under the form of a cross using the window."""
        if not color: color=self.color
        if not size: size=self.size
        if not width: width=self.width
        x,y=self
        sx,sy=size
        xmin=x-sx/2
        ymin=y-sy/2
        xmax=x+sx/2
        ymax=y+sy/2
        window.draw.line(window.screen,color,[xmin,ymin],[xmax,ymax],width)
        window.draw.line(window.screen,color,[xmin,ymax],[xmax,ymin],width)

    def showCircle(self,window,color=None,radius=None,fill=None):
        """Show a point under the form of a circle using the window."""
        if not color: color=self.color
        if not radius: radius=self.radius
        if not fill: fill=self.fill
        window.draw.circle(window.screen,color,[self.x,self.y],radius,fill)

    def show(self,window,color=None,mode=None,fill=None,radius=None,size=None,width=None):
        """Show the point on the window."""
        if not mode: mode=self.mode
        if mode==0 or mode=="circle":
            self.showCircle(window,color=color,radius=radius,fill=fill)
        if mode==1 or mode=="cross":
            self.showCross(window,color=color,size=size,width=width)

    def showText(self,window,text,text_size=20,color=mycolors.WHITE):
        """Show the text next to the point on the window."""
        window.print(text,self,text_size,color=color)

    def __add__(self,other):
        """Add the components of 2 objects."""
        return Point(self.x+other[0],self.y+other[1])

    def __sub__(self,other):
        """Substract the components of 2 objects."""
        return Point(self.x-other[0],self.y-other[1])

    def __ge__(self,other):
        """Determine if a point is farther to the origin."""
        return self.x**2+self.y**2>=other.x**2+other.y**2

    def __gt__(self,other):
        """Determine if a point is farther to the origin."""
        return self.x**2+self.y**2>other.x**2+other.y**2

    def __le__(self,other):
        """Determine if a point is the nearest to the origin."""
        return self.x**2+self.y**2<=other.x**2+other.y**2

    def __lt__(self,other):
        """Determine if a point is the nearest to the origin."""
        return self.x**2+self.y**2<other.x**2+other.y**2

    def __iter__(self):
        """Iterate the points of the form."""
        self.iterator=0
        return self

    def __next__(self):
        """Return the next point threw an iteration."""
        if self.iterator<len(self.components):
            self.iterator+=1
            return self.components[self.iterator-1]
        else:
            raise StopIteration

    def truncate(self):
        """Truncate the position of the point by making the x and y components integers."""
        for i in range(self.components):
            self.components[i]=int(self.components[i])

    def __str__(self):
        """Return the string representation of a point."""
        return "p("+",".join([str(round(c,digits) for c in self.components)])+")"

    def distance(self,point):
        """Return the distance between the point and another point."""
        return Vector.createFromTwoPoints(self,point).norm

    def getPosition(self):
        """Return the components."""
        return self.components

    def setPosition(self,position):
        """Set the components."""
        self.components=position

    position=property(getPosition,setPosition,"Same as component although only component should be used.")

class Direction:
    """Base class of lines and segments."""
    def __init__(self): #position,width,color):
        pass

class Vector:
    def null(d=2):
        """Return the null vector."""
        return Vector([0 for i in range(d)])

    neutral=zero=null

    def random(corners=[-1,-1,1,1],color=mycolors.WHITE,width=1,arrow=[0.1,0.5]):
        """Create a random vector using optional min and max."""
        xmin,ymin,xmax,ymax=corners
        x=random.uniform(xmin,xmax)
        y=random.uniform(ymin,ymax)
        return Vector(x,y,color=color,width=width,arrow=arrow)

    def sum(vectors):
        """Return the vector that correspond to the sum of all the vectors."""
        result=vectors[0]
        for vector in vectors[1:]:
            result+=vector
        return result

    def average(vectors):
        """Return the vector that correspond to the mean of all the vectors."""
        return Vector.sum(vectors)/len(vectors)

    mean=average

    def createFromPolarCoordonnates(norm,angle,color=mycolors.WHITE,width=1,arrow=[0.1,0.5]):
        """Create a vector using norm and angle from polar coordonnates."""
        x,y=Vector.cartesian([norm,angle])
        return Vector(x,y,color=color,width=width,arrow=arrow)

    def createFromSegment(segment,color=mycolors.WHITE,width=1,arrow=[0.1,0.5]):
        """Create a vector from a segment."""
        return Vector.createFromTwoPoints(segment.p1,segment.p2,color=color,width=width,arrow=arrow)

    def createFromTwoPoints(point1,point2,color=mycolors.WHITE,width=1,arrow=[0.1,0.5]):
        """Create a vector from 2 points."""
        x=point2.x-point1.x
        y=point2.y-point1.y
        return Vector(x,y,color=color,width=width,arrow=arrow)

    def createFromPoint(point,color=mycolors.WHITE,width=1,arrow=[0.1,0.5]):
        """Create a vector from a single point."""
        return Vector(point.x,point.y,color=color,width=width,arrow=arrow)

    def createFromLine(line,color=mycolors.WHITE,width=1,arrow=[0.1,0.5]):
        """Create a vector from a line."""
        angle=line.angle
        x,y=Vector.cartesian([1,angle])
        return Vector(x,y,color=color,width=width,arrow=arrow)

    def polar(position):
        """Return the polar position [norm,angle] using cartesian position [x,y]."""
        return list(polar(complex(position[0],position[1])))

    def cartesian(position):
        """Return the cartesian position [x,y] using polar position [norm,angle]."""
        return [position[0]*cos(position[1]),position[0]*sin(position[1])]

    def __init__(self,*args,color=(255,255,255),width=1,arrow=[0.1,0.5]):
        """Create a vector."""
        args=list(args)
        if len(args)==1: args=args[0]
        self.components=list(args)
        self.color=color
        self.width=width
        self.arrow=arrow

    def setX(self,value):
        """Set the x component."""
        self.components[0]=value

    def getX(self):
        """Return the x component."""
        return self.components[0]

    def delX(self):
        """Delete the x component and so shifting to a new one."""
        del self.components[0]

    def setY(self,value):
        """Set the y component."""
        self.components[1]=value

    def getY(self):
        """Return the y component."""
        return self.components[1]

    def delY(self):
        """Delete the y component."""
        del self.components[1]

    def getAngle(self):
        """Return the angle of a vector with the [1,0] direction in cartesian coordonnates."""
        return Vector.polar(self.components)[1]

    def setAngle(self,value):
        """Change the angle of the points without changing its norm."""
        n,a=Vector.polar(self.components)
        self.components=Vector.cartesian([n,value])

    def getNorm(self):
        """Return the angle of a vector with the [1,0] direction in cartesian coordonnates."""
        return Vector.polar(self.components)[0]

    def setNorm(self,value):
        """Change the angle of the points without changing its norm."""
        n,a=Vector.polar(self.components)
        self.components=Vector.cartesian([value,a])

    def getPosition(self):
        """Return the components."""
        return self.components

    def setPosition(self,position):
        """Set the components."""
        self.components=position

    x=property(getX,setX,delX,doc="Allow the user to manipulate the x component easily.")
    y=property(getY,setY,delY,doc="Allow the user to manipulate the y component easily.")
    norm=property(getNorm,setNorm,doc="Allow the user to manipulate the norm of the vector easily.")
    angle=property(getAngle,setAngle,doc="Allow the user to manipulate the angle of the vector easily.")
    position=property(getPosition,setPosition,doc="Same as components.")

    def show(self,context,p=Point.neutral(),color=None,width=None):
        """Show the vector."""
        if not color: color=self.color
        if not width: width=self.width
        q=self(p)
        v=-self.arrow[0]*self #wtf
        v1=v%self.arrow[1]
        v2=v%-self.arrow[1]
        a=v1(q)
        b=v2(q)
        context.draw.line(context.screen,color,p(),q(),width)
        context.draw.line(context.screen,color,q(),a(),width)
        context.draw.line(context.screen,color,q(),b(),width)

    def showText(self,surface,point,text,color=None,size=20):
        """Show the text next to the vector."""
        if not color: color=self.color
        v=self/2
        point=v(point)
        surface.print(text,tuple(point),color=color,size=size)

    def __len__(self):
        """Return the number of components."""
        return len(self.components)

    def __iter__(self):
        """Iterate the points of the form."""
        self.iterator=0
        return self

    def __next__(self):
        """Return the next point threw an iteration."""
        if self.iterator<len(self.components):
            self.iterator+=1
            return self.components[self.iterator-1]
        else:
            raise StopIteration

    def __neg__(self):
        """Return the negative vector."""
        return Vector([-c for c in self.components],width=self.width,color=self.color)

    def colinear(self,other,e=10e-10):
        """Return if two vectors are colinear."""
        return abs(self.x*other.y-self.y*other.x)<e

    __floordiv__=colinear

    def scalar(self,other):
        """Return the scalar product between two vectors."""
        return self.x*other.x+self.y*other.y

    def cross(self,other):
        """Determine if a vector crosses another using dot product."""
        return self.scalar(other)==0

    def __imul__(self,factor):
        """Multiply a vector by a given factor."""
        if type(factor)==int or type(factor)==float:
            self.x*=factor
            self.y*=factor
        else:
            raise Exception("Type "+str(type(factor))+" is not valid. Expected float or int types.")

    def __mul__(self,factor):
        """Multiply a vector by a given factor."""
        if type(factor)==int or type(factor)==float:
            return Vector(self.x*factor,self.y*factor,color=self.color,width=self.width,arrow=self.arrow)
        else:
            raise Exception("Type "+str(type(factor))+" is not valid. Expected float or int types.")

    __rmul__=__mul__ #Allow front extern multiplication using back extern multiplication with scalars

    def __truediv__(self,factor):
        """Multiply a vector by a given factor."""
        if type(factor)==Vector:
            pass
        else:
            x=self.x/factor
            y=self.y/factor
            return Vector(x,y,width=self.width,color=self.color)

    __iadd__=__radd__=__add__=lambda self,other:Vector([c1+c2 for (c1,c2) in zip(self,other)])

    def rotate(self,angle):
        """Rotate a vector using the angle of rotation."""
        n,a=Vector.polar([self.x,self.y])
        a+=angle
        self.x=n*cos(a)
        self.y=n*sin(a)

    def __mod__(self,angle):
        """Return the rotated vector using the angle of rotation."""
        n,a=Vector.polar([self.x,self.y])
        a+=angle
        return Vector(n*cos(a),n*sin(a),color=self.color,width=self.width,arrow=self.arrow)

    __imod__=__mod__

    def __getitem__(self,index):
        """Return x or y value using given index."""
        return self.position[index]

    def __setitem__(self,index,value):
        """Change x or y value using given index and value."""
        self.position[index]=value

    def __call__(self,*points):
        """Return points by applying the vector on those."""
        if len(points)==1: return points[0]+self
        return [point+self for point in points]

    def apply(self,point):
        """Return the point after applying the vector to it."""
        return self+point

    def allApply(self,points):
        """Return the points after applying the vector to those."""
        new_points=[point+self for point in points]
        return new_points

    def __xor__(self,other):
        """Return the angle between two vectors."""
        return self.angle-other.angle

    def __invert__(self):
        """Return the unit vector."""
        a=self.angle
        x,y=Vector.cartesian([1,a])
        return Vector(x,y)

    def __str__(self):
        """Return a string description of the vector."""
        return "v("+",".join([str(round(c,digits) for c in self.components)])+")"

class Segment(Direction):
    def null():
        """Return the segment whoose points are both the origin."""
        return Segment([Point.origin() for i in range(2)])

    def random(corners=[-1,-1,1,1],width=1,color=mycolors.WHITE):
        """Create a random segment."""
        p1=Point.random(corners)
        p2=Point.random(corners)
        return Segment(p1,p2,width,color)

    def __init__(self,*points,width=1,color=mycolors.WHITE):
        """Create the segment using 2 points, width and color."""
        if len(points)==1: points=points[0]
        if len(points)!=2: raise Exception("A segment must have 2 points.")
        self.points=points
        self.width=width
        self.color=color

    def __str__(self):
        """Return the string representation of a segment."""
        text="s("+str(self.p1)+","+str(self.p2)+")"
        return text

    def __call__(self,t=1/2):
        """Return the point C of the segment so that Segment(p1,C)=t*Segment(p1,p2)."""
        return (t*self.vector)(self.p1)

    __rmul__=__imul__=__mul__=lambda self,t: Segment(self.p1,self(t))

    def getCenter(self):
        """Return the center of the segment in the general case."""
        return Point([(self.p1[i]+self.p2[i])/2 for i in range(min(len(self.p1),len(self.p2)))])

    def setCenter(self,np):
        """Set the center of the segment."""
        p=self.getCenter()
        v=Vector.createFromTwoPoints(np,p)
        for i in range(len(self.points)):
            self.points[i]=v(self.points[i])

    def getAngle(self):
        """Return the angle of the segment."""
        return self.vector.angle

    def setAngle(self):
        """Set the angle of the segment."""
        self.vector.angle=angle

    def show(self,window,color=None,width=None):
        """Show the segment using window."""
        if not color: color=self.color
        if not width: width=self.width
        window.draw.line(window.screen,color,[self.p1.x,self.p1.y],[self.p2.x,self.p2.y],width)
        #self.showInBorders(window,color,width)

    def showInBorders(self,window,color=None,width=None):
        """Show the segment within the boundaries of the window."""
        #It it really slow and it doesn't work as expected.
        xmin,ymin,xmax,ymax=window.getCorners()
        p=[Point(xmin,ymin),Point(xmax,ymin),Point(xmax,ymax),Point(xmin,ymax)]
        f=Form(p)
        if (self.p1 in f) and (self.p2 in f):
            window.draw.line(window.screen,color,[self.p1.x,self.p1.y],[self.p2.x,self.p2.y],width)
        elif (self.p1 in f) and not (self.p2 in f):
            v=Vector.createFromTwoPoints(self.p1,self.p2)
            hl=HalfLine(self.p1,v.angle)
            p=f.crossHalfLine(hl)
            if p:
                print(len(p))
                p=p[0]
                window.draw.line(window.screen,color,[self.p1.x,self.p1.y],[p.x,p.y],width)
        elif not (self.p1 in f) and (self.p2 in f):
            v=Vector.createFromTwoPoints(self.p2,self.p1)
            hl=HalfLine(self.p2,v.angle)
            p=f.crossHalfLine(hl)
            if p:
                print(len(p))
                p=p[0]
                window.draw.line(window.screen,color,[p.x,p.y],[self.p2.x,self.p2.y],width)
        else:
            ps=f.crossSegment(self)
            if len(ps)==2:
                p1,p2=ps
                window.draw.line(window.screen,color,[p1.x,p1.y],[p2.x,p2.y],width)


    def __contains__(self,point,e=10e-10):
        """Determine if a point is in a segment."""
        if point==self.getP1(): return True
        v1=Vector.createFromTwoPoints(point,self.p1)
        v2=self.getVector()
        return (abs(v1.angle-v2.angle)<e) and (v1.norm<=v2.norm)

    def __len__(self):
        """Return the number of points."""
        return len(self.points)

    def __iter__(self):
        """Iterate the points of the form."""
        self.iterator=0
        return self

    def __next__(self):
        """Return the next point through an iteration."""
        if self.iterator<len(self.points):
            if self.iterator==0: value=self.p1
            if self.iterator==1: value=self.p2
            self.iterator+=1
            return value
        else:
            raise StopIteration

    def __getitem__(self,index):
        """Return the point corresponding to the index given."""
        return [self.points][index]

    def __setitem__(self,index,value):
        """Change the value the point corresponding value and index given."""
        self.points[index]=value

    def getLine(self,correct=True):
        """Return the line through the end points of the segment."""
        return Line(self.p1,self.angle,self.width,self.color,correct=correct)

    def getVector(self):
        """Return the vector that goes from p1 to p2."""
        return Vector.createFromTwoPoints(self.p2,self.p1)

    def setVector(self,vector):
        """Set the vector that goes from p1 to p2."""
        self.p2=vector(self.p1)

    def getLength(self):
        """Return the length of the segment."""
        return self.vector.norm

    def setLength(self,length):
        """Set the length of the segment."""
        self.vector.norm=length

    def rotate(self,angle,point=None):
        """Rotate the segment using an angle and an optional point of rotation."""
        if not point: point=self.middle
        self.p1.rotate(angle,point)
        self.p2.rotate(angle,point)

    def __or__(self,other):
        """Return bool for (2 segments are crossing)."""
        if isinstance(other,Segment):  return self.crossSegment(other)
        if isinstance(other,Line):     return self.crossLine(other)
        if isinstance(other,HalfLine): return other.crossSegment(self)
        if isinstance(other,Form):     return form.crossSegment(self)

    def getXmin(self):
        """Return the minimum of x components of the 2 end points."""
        return min(self.p1.x,self.p2.x)

    def getYmin(self):
        """Return the minimum of y components of the 2 ends points."""
        return min(self.p1.y,self.p2.y)

    def getXmax(self):
        """Return the maximum of x components of the 2 end points."""
        return max(self.p1.x,self.p2.x)

    def getYmax(self):
        """Returnt the maximum of y components of the 2 end points."""
        return max(self.p1.y,self.p2.y)

    def getMinima(self):
        """Return the minima of x and y components of the 2 end points."""
        xmin=self.getXmin()
        ymin=self.getYmin()
        return (xmin,ymin)

    def getMaxima(self):
        """Return the maxima of x and y components of the 2 end points."""
        xmax=self.getXmax()
        ymax=self.getYmax()
        return (xmax,ymax)

    def getCorners(self):
        """Return the minimum and maximum of x and y components of the 2 end points."""
        minima=self.getMinima()
        maxima=self.getMaxima()
        return minima+maxima

    def parallel(self,other):
        """Determine if the line is parallel to another object (line or segment)."""
        return (other.angle==self.angle)

    def crossSegment(self,other,e=10**-14):
        """Return the intersection point of the segment with another segment."""
        sl=self.getLine()
        ol=other.getLine()
        point=sl.crossLine(ol)
        if point:
            if point in self and point in other:
                return point

    def crossLine(self,other):
        """Return the intersection point of the segment with a line."""
        if self.parallel(other): return None
        line=self.getLine()
        point=other.crossLine(line)
        if point:
            if point in self and point in other:
                return point

    def getP1(self):
        """Return the first point of the segment."""
        return self.points[0]

    def setP1(self,p1):
        """Set the first point of the segment."""
        self.points[0]=p1

    def getP2(self):
        """Return the second point of the segment."""
        return self.points[1]

    def setP2(self,p2):
        """Set the second point of the segment."""
        self.points[1]=p2

    p1=property(getP1,setP1,"Allow the user to manipulate the first point of the segment easily.")
    p2=property(getP2,setP2,"Allow the user to manipulate the second point of the segment easily.")
    middle=center=property(getCenter,setCenter,"Representation of the center of the segment.")
    vector=property(getVector,setVector,"Representation of the vector of the segment.")
    angle=property(getAngle,setAngle,"Representation of the angle of the segment.")
    length=property(getLength,setLength,"Representation of the length of the segment.")


class Line(Direction):
    def random(min=-1,max=1,width=1,color=mycolors.WHITE):
        """Return a random line."""
        point=Point.random(min,max)
        angle=random.uniform(min,max)
        return Line(point,angle,width,color)

    def createFromPointAndVector(point,vector,width=1,color=mycolors.WHITE):
        """Create a line using a point and a vector with optional features."""
        angle=vector.angle
        line=Line(point,angle,width=1,color=(255,255,255))
        return line

    def createFromTwoPoints(point1,point2,width=1,color=mycolors.WHITE):
        """Create a line using two points with optional features."""
        vector=Vector.createFromTwoPoints(point1,point2)
        angle=vector.angle
        line=Line(point1,angle,width,color)
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
        v=self.vector
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
        return Vector.createFromPolarCoordonnates(1,self.angle)

    def setUnitVector(self,vector):
        """Set the unit vector of the line."""
        self.angle=vector.angle

    def getNormalVector(self):
        """Return the normal vector of the line."""
        vector=self.getUnitVector()
        vector.rotate(math.pi/2)
        return vector

    def setNormalVector(self,vector):
        """Set the normal vector of the line."""
        self.angle=vector.angle+math.pi/2

    def getSlope(self):
        """Return the slope of the line."""
        return math.tan(angle)

    def setSlope(self,slope):
        """Set the slope of the line by changing its angle and point."""
        self.angle=math.atan(slope)

    def getOrdinate(self):
        """Return the ordinate of the line."""
        return self.point.y-self.slope*self.point.x

    def setOrdinate(self,ordinate):
        """Set the ordinate of the line by changing its position."""
        self.slope
        self.angle
        self.point

    def getFunction(self):
        """Return the affine function that correspond to the line."""
        return lambda x:self.slope*x+self.ordinate

    def setFunction(self,function):
        """Set the function of the line by changing its slope and ordinate."""
        self.ordinate=function(0)
        self.slope=function(1)-function(0)

    def getReciproqueFunction(self):
        """Return the reciproque of the affine function that correspond to the line."""
        return lambda y:(y-self.ordinate)/self.slope

    def evaluate(self,x):
        """Evaluate the line as a affine function."""
        return self.function(x)

    def devaluate(self,y):
        """Evaluate the reciproque function of the affine funtion of the line."""
        return self.getReciproqueFunction(y)

    def __or__(self,other):
        """Return the point of intersection between the line and another object."""
        if isinstance(other,Line):      return self.crossLine(other)
        if isinstance(other,Segment):   return self.crossSegment(other)
        if isinstance(other,HalfLine):  return other.crossLine(self)
        if isinstance(other,Form):      return other.crossLine(self)


    def crossSegment(self,other,e=10**-13):
        """Return the point of intersection between a segment and the line."""
        #Extract the slopes and ordinates
        line=other.getLine()
        point=self.crossLine(line)
        if not point: return None
        x,y=point
        #Determine if the point of intersection belongs to both the segment and the line
        xmin,ymin,xmax,ymax=other.getCorners()
        #If it is the case return the point
        if  xmin-e<=x<=xmax+e and ymin-e<=y<=ymax+e:
            return Point(x,y,color=self.color)
        #By default if nothing is returned the function returns None


    def crossLine(self,other):
        """Return the point of intersection between two lines with vectors calculation."""
        a,b=self.point
        c,d=other.point
        m,n=self.vector
        o,p=other.vector
        if n*o-m*p==0: return None #The lines are parallels
        x=(a*n*o-b*m*o-c*m*p+d*m*o)/(n*o-m*p)
        y=(x-a)*n/m+b
        return Point(x,y)

    def parallel(self,other):
        """Determine if the line is parallel to another object (line or segment)."""
        return other.angle==self.angle

    def __contains__(self,point,e=10e-10):
        """Determine if a point belongs to the line."""
        v1=self.vector
        v2=Vector.createFromTwoPoints(self.point,point)
        return v1.colinear(v2,e)

    def getHeight(self,point):
        """Return the height line between the line and a point."""
        return Line(point,self.normal_vector.angle)

    def distanceFromPoint(self,point):
        """Return the distance between a point and the line."""
        return Vector.createFromTwoPoints(point,self.crossLine(self.getHeight(point))).norm

    def projectPoint(self,point):
        """Return the projection of the point on the line."""
        vector=self.getNormalVector()
        angle=vector.angle
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

    def getSegmentWithinCorners(self,corners):
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
        points=[]
        for segment in segments:
            cross=self.crossSegment(segment)
            if cross:
                points.append(cross)
        if len(points)==2:
            return Segment(*points)

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
        return points

    def show(self,surface,width=None,color=None):
        """Show the line on the surface."""
        if not color: color=self.color
        if not width: width=self.width
        corners=surface.getCorners()
        segment=self.getSegmentWithinCorners(corners)
        if segment:
            p1,p2=segment
            segment.show(surface,width=width,color=color)


    vector=unit_vector=property(getUnitVector,setUnitVector,"Allow the client to manipulate the unit vector easily.")
    normal_vector=property(getNormalVector,setNormalVector,"Allow the client to manipulate the normal vector easily.")
    slope=property(getSlope,setSlope,"Allow the client to manipulate the slope of the line easily.")
    ordinate=property(getOrdinate,setOrdinate,"Allow the client to manipulate the ordinate of the line easily.")
    function=property(getFunction,setFunction,"Allow the client to manipulate the function of the line.")
    #reciproque_function=property(getReciproqueFunction,setReciproqueFunction,"Allow the user to manipulate easily the reciproque function.")



class HalfLine(Line):
    def createFromLine(line):
        """Create a half line."""
        return HalfLine(line.point,line.angle)

    def __init__(self,point,angle,color=mycolors.WHITE,width=1):
        """Create a half line."""
        super().__init__(point,angle,color=color,width=width,correct=False)

    def getLine(self,correct=True):
        """Return the line that correspond to the half line."""
        return Line(self.point,self.angle,correct=correct)

    def getPoint(self):
        """Return the point of the half line."""
        return self.point

    def setPoint(self,point):
        """Set the point of the half line."""
        self.point=point

    def show(self,surface,width=None,color=None):
        """Show the line on the surface."""
        if not color: color=self.color
        if not width: width=self.width
        xmin,ymin,xmax,ymax=surface.getCorners()
        points=[Point(xmin,ymin),Point(xmax,ymin),Point(xmax,ymax),Point(xmin,ymax)]
        form=Form(points)
        points=form.crossHalfLine(self)
        if points:
            surface.draw.line(surface.screen,color,self.point,points[0],width)

    def __contains__(self,point,e=10e-10):
        """Determine if a point is in the half line."""
        v1=self.vector
        v2=Vector.createFromTwoPoints(self.point,point)
        return abs(v1.angle-v2.angle)<e

    def __or__(self,other):
        """Return the intersection point between the half line and another object."""
        if isinstance(other,Line):      return self.crossLine(other)
        if isinstance(other,Segment):   return self.crossSegment(other)
        if isinstance(other,HalfLine):  return self.crossHalfLine(other)
        if isinstance(other,Form):      return form.crossHalfLine(self)

    def crossHalfLine(self,other):
        """Return the point of intersection of the half line with another."""
        ml=self.getLine(correct=False)
        ol=other.getLine(correct=False)
        point=ml.crossLine(ol)
        if point:
            if (point in self) and (point in other):
                return point

    def crossLine(self,other):
        """Return the point of intersection of the half line with a line."""
        ml=self.getLine(correct=False)
        point=ml.crossLine(other)
        if point:
            if (point in self) and (point in other):
                return point

    def crossSegment(self,other):
        """Return the point of intersection of the half line with a segment."""
        ml=self.getLine(correct=False)
        ol=other.getLine(correct=False)
        point=ml.crossLine(ol)
        if point:
            if (point in self) and (point in other):
                return point

    def __str__(self):
        """Return the string representation of a half line."""
        return "hl("+str(self.point)+","+str(self.angle)+")"



class Form:
    def random(corners=[-1,-1,1,1],number=random.randint(1,10),**kwargs):
        """Create a random form using the point_number, the minimum and maximum position for x and y components and optional arguments."""
        points=[Point.random(corners) for i in range(number)]
        form=Form(points,**kwargs)
        form.makeSparse()
        return form

    def anyCrossing(forms):
        """Determine if any of the forms are crossing."""
        if len(forms)==1:forms=forms[0]
        l=len(forms)
        for i in range(l):
            for j in range(i+1,l):
                if forms[i].crossForm(forms[j]):
                    return True
        return False

    def allCrossing(forms):
        """Determine if all the forms are crossing."""
        if len(forms)==1:forms=forms[0]
        l=len(forms)
        for i in range(l):
            for j in range(i+1,l):
                if not forms[i].crossForm(forms[j]):
                    return False
        return True

    def cross(*forms):
        """Return the points of intersection between the crossing forms."""
        if len(forms)==1:forms=forms[0]
        l=len(forms)
        points=[]
        for i in range(l):
            for j in range(i+1,l):
                points.extend(forms[i].crossForm(forms[j]))
        return points


    def intersectionTwoForms(form1,form2):
        """Return the form which is the intersection of two forms."""
        if form1==None: return form2
        if form2==None: return form1
        if form1==form2==None: return None
        points=form1.crossForm(form2)
        if not points: return None
        for point in form1.points:
            if point in form2:
                points.append(point)
        for point in form2.points:
            if point in form1:
                points.append(point)
        form=Form(points)
        form.makeSparse()
        return form

    def intersection(forms):
        """Return the form which is the intersection of all the forms."""
        result=forms[0]
        for form in forms[1:]:
            result=Form.intersectionTwoForms(result,form)
        return result


    def unionTwoForms(form1,form2):
        """Return the union of two forms."""
        intersection_points=set(form1.crossForm(form2))
        if intersection_points:
            all_points=set(form1.points+form2.points)
            points=all_points.intersection(intersection_points)
            return [Form(points)]
        else:
            return [form1,form2]

    def union(forms):
        """Return the union of all forms."""
        """This function must be recursive."""
        if len(forms)==2:
            return Form.unionTwoForms(forms[0],forms[1])
        else:
            pass

        result=forms[0]
        for form in forms[1:]:
            result.extend(Form.union(form,result))
        return result


    def __init__(self,points,fill=False,point_mode=0,point_size=[0.01,0.01],point_radius=0.01,point_width=1,point_fill=False,side_width=1,color=None,point_color=mycolors.WHITE,side_color=mycolors.WHITE,area_color=mycolors.WHITE,cross_point_color=mycolors.WHITE,cross_point_radius=0.01,cross_point_mode=0,cross_point_width=1,cross_point_size=[0.1,0.1],point_show=True,side_show=True,area_show=False):
        """Create the form object using points."""
        self.points=points

        self.point_mode=point_mode
        self.point_size=point_size
        self.point_width=point_width
        self.point_radius=point_radius
        self.point_color=point_color or color
        self.point_show=point_show
        self.point_fill=point_fill

        self.side_width=side_width
        self.side_color=side_color or color
        self.side_show=side_show

        self.area_color=area_color or color
        self.area_show=area_show or fill

        self.cross_point_color=cross_point_color
        self.cross_point_radius=cross_point_radius
        self.cross_point_mode=cross_point_mode
        self.cross_point_width=cross_point_width
        self.cross_point_size=cross_point_size

    def setFill(self,fill):
        """Set the form to fill its area when shown."""
        self.area_show=fill

    def getFill(self):
        """Return if the area is filled."""
        return self.area_show

    fill=property(getFill,setFill,"Allow the user to manipulate easily if the area is filled.")

    def __iadd__(self,point):
        """Add a point to the form."""
        self.points.append(point)
        return self

    def __isub__(self,point):
        """Remove a point to the form."""
        self.points.remove(point)
        return self

    def __iter__(self):
        """Iterate the points of the form."""
        self.iterator=0
        return self

    def __next__(self):
        """Return the next point threw an iteration."""
        if self.iterator < len(self.points):
            iterator=self.iterator
            self.iterator+=1
            return self.points[iterator]
        else:
            raise StopIteration

    def __eq__(self,other):
        """Determine if 2 forms are the same which check the equalities of their components."""
        return sorted(self.points)==sorted(other.points)

    def getCenter(self):
        """Return the point of the center."""
        mx=mean([p.x for p in self.points])
        my=mean([p.y for p in self.points])
        return Point(mx,my,color=self.point_color,radius=self.point_radius)

    def setCenter(self,center):
        """Set the center of the form."""
        p=center-self.getCenter()
        for point in self.points:
            point+=p

    def getSegments(self):
        """"Return the list of the form sides."""
        return [Segment(self.points[i%len(self.points)],self.points[(i+1)%len(self.points)],color=self.side_color,width=self.side_width) for i in range(len(self.points))]

    def setSegments(self,segments):
        """Set the segments of the form by setting its points to new values."""
        self.points=[s.p1 for s in segments]

    def showAll(self,surface,**kwargs):
        """Show the form using a window."""
        #,window,point_color=None,side_color=None,area_color=None,side_width=None,point_radius=None,color=None,fill=None,point_show=None,side_show=None
        if not "point_show" in kwargs: kwargs["point_show"]=self.point_show
        if not "side_show" in kwargs:  kwargs["side_show"]=self.side_show
        if not "area_show" in kwargs:  kwargs["area_show"]=self.area_show
        if kwargs["area_show"]:  self.showAllArea(surface,**kwargs)
        if kwargs["side_show"]:  self.showAllSegments(surface,**kwargs)
        if kwargs["point_show"]: self.showAllPoints(surface,**kwargs)

    def showFast(self,surface,point=None,segment=None,area=None):
        """Show the form using the surface and optional objects to show."""
        if point:   self.showPoints(surface)
        if segment: self.showSegments(surface)
        if area:    self.showArea(surface)

    def show(self,surface):
        """Show the form using the surface and optional objects to show."""
        if self.point_show:   self.showPoints(surface)
        if self.side_show:    self.showSegments(surface)
        if self.area_show:    self.showArea(surface)

    def showFastArea(self,surface,color=None):
        """Show the area of the form using optional parameters such as the area
        of the color."""
        if not color: color=self.area_color
        ps=[tuple(p) for p in self.points]
        if len(ps)>1: surface.draw.polygon(surface.screen,color,ps,False)

    def showAllArea(self,surface,**kwargs):
        """Show the area of the form using optional parameters such as the area
        of the color. This function is slower than the previous one because it
        checks if the dictionary or attributes contains the area_color."""
        if not "area_color" in kwargs: kwargs["area_color"]=self.area_color
        ps=[tuple(p) for p in self.points]
        if len(ps)>1: surface.draw.polygon(surface.screen,kwargs["area_color"],ps,False)

    def showArea(self,surface):
        """Show the area of the form."""
        ps=[tuple(p) for p in self.points]
        if len(ps)>1: surface.draw.polygon(surface.screen,self.area_color,ps,False)

    def showPoints(self,surface):
        """Show the points."""
        for point in self.points:
            point.show(surface)

    def showFastPoints(self,surface,
                        color=None,
                        mode=None,
                        radius=None,
                        size=None,
                        width=None,
                        fill=None):
        """Show the points of the form using optional parameters."""
        if not color:  color=self.point_color
        if not radius: radius=self.point_radius
        if not mode:   mode=self.point_mode
        if not size:   size=self.point_size
        if not width:  width=self.point_width
        if not fill:   fill=self.point_fill
        for point in self.points:
            point.show(surface,color,mode,fill,radius,size,width)

    def showAllPoints(self,surface,**kwargs):
        """Show the points of the form using optional parameters.
        This method is slower than the previous one because it checks if the
        dictionary of attributes contains the arguments."""
        if not "point_color"  in kwargs: kwargs["point_color"]=  self.point_color
        if not "point_radius" in kwargs: kwargs["point_radius"]= self.point_radius
        if not "point_mode"   in kwargs: kwargs["point_mode"]=   self.point_mode
        if not "point_size"   in kwargs: kwargs["point_size"]=   self.point_size
        if not "point_width"  in kwargs: kwargs["point_width"]=  self.point_width
        if not "point_fill"   in kwargs: kwargs["point_fill"]=   self.point_fill
        for point in self.points:
            point.show(surface,
                color=kwargs["point_color"],
                mode=kwargs["point_mode"],
                fill=kwargs["point_fill"],
                radius=kwargs["point_radius"],
                size=kwargs["point_size"],
                width=kwargs["point_width"])

    @timer
    def showFastSegments(self,surface,color=None,width=None):
        """Show the segments of the form."""
        if not color: color=self.segment_color
        if not width: width=self.segment_width
        for segment in self.segments:
            segment.show(surace,color,width)

    def showSegments(self,surface):
        """Show the segments without its parameters."""
        for segment in self.segments:
            segment.show(surface)

    def showAllSegments(self,surface,**kwargs):
        """Show the segments of the form."""
        if not "side_color" in kwargs: kwargs["side_color"]=self.side_color
        if not "side_width" in kwargs: kwargs["side_width"]=self.side_width
        for segment in self.segments:
            segment.show(surface,color=kwargs["side_color"],width=kwargs["side_width"])

    def showFastCrossPoints(self,surface,color=None,mode=None,radius=None,width=None,size=None):
        """Show the intersection points of the form crossing itself."""
        points=self.crossSelf()
        if not color: color=self.cross_point_color
        if not mode: mode=self.cross_point_mode
        if not radius: radius=self.cross_point_radius
        if not width: width=self.cross_point_width
        if not size: size=self.cross_point_size
        for point in points:
            point.show(surface,color=color,mode=mode,radius=radius,width=width,size=size)

    def showCrossPoints(self,surface):
        """Show the intersection points of the form crossing itself."""
        for point in self.cross_points:
            point.show(surface)

    def __or__(self,other):
        """Return the points of intersections with the form and another object."""
        if isinstance(other,HalfLine):  return self.crossHalfLine(other)
        if isinstance(other,Line):       return self.crossLine(other)
        if isinstance(other,Segment):   return self.crossSegment(other)
        if isinstance(other,Form):      return self.crossForm(other)

    def crossForm(self,other):
        """Return the bool: (2 sides are crossing)."""
        points=[]
        for myside in self.sides:
            for otherside in other.sides:
                point=myside|otherside
                if point:
                    points.append(point)
        return points

    def crossDirection(self,other):
        """Return the list of the points of intersection between the form and a segment or a line."""
        points=[]
        for side in self.sides:
            cross=side|other
            if cross: points.append(cross)
        return points

    def crossHalfLine(self,other):
        """Return the list of points of intersection in order between the form and a half line."""
        points=[]
        for side in self.sides:
            cross=other.crossSegment(side)
            if cross: points.append(cross)
        hp=other.getPoint()
        objects=[(p,Vector.createFromTwoPoints(p,hp).norm) for p in points]
        objects=sorted(objects,key=lambda x:x[1])
        points=[p for (p,v) in objects]
        return points

    def crossLine(self,other):
        """Return the list of the points of intersection between the form and a line."""
        points=[]
        for side in self.sides:
            cross=side.crossLine(other)
            if cross:
                points.append(cross)
        return points

    def crossSegment(self,other):
        """Return the list of the points of intersection between the form and a segment."""
        points=[]
        for side in self.sides:
            cross=side.crossSegment(other)
            if cross:
                points.append(cross)
        return points

    def crossSelf(self,e=10e-10):
        """Return the list of the points of intersections between the form and itself."""
        results=[]
        l=len(self.segments)
        for i in range(l):
            for j in range(i+1,l):
                point=self.segments[i].crossSegment(self.segments[j])
                if point:
                    if point in self.points:
                        results.append(point)
        return results

    def convex(self):
        """Return the bool (the form is convex)."""
        x,y=self.center
        angles=[]
        l=len(self.points)
        for i in range(l-1):
            A=self.points[(i+l-1)%l]
            B=self.points[i%l]
            C=self.points[(i+1)%l]
            u=Vector(A.x-B.x,A.y-B.y)
            v=Vector(C.x-B.x,C.y-B.y)
            angle=v^u
            if angle>pi:
                return True
        return False

    def getSparse(self): #as opposed to makeSparse which keeps the same form and return nothing
        """Return the form with the most sparsed points."""
        center=self.center
        cx,cy=center[0],center[1]
        list1=[]
        for point in self.points:
            px,py=point.position
            vector=Vector(px-cx,py-cy)
            angle=vector.polar()[1]
            list1.append((angle,point))
        list1=sorted(list1,key=lambda x:x[0])
        points=[element[1] for element in list1]
        return Form(points,fill=self.fill,side_width=self.side_width,point_radius=self.point_radius,point_color=self.point_color,side_color=self.side_color,area_color=self.area_color)

    def makeSparse(self):
        """Change the form into the one with the most sparsed points."""
        form=self.getSparse()
        self.points=form.points

    def __contains__(self,point):
        """Return the boolean: (the point is in the form)."""
        x,y=point[0],point[1]
        p1=Point(x,y)
        p2=Point(0,0)
        line=Line.createFromTwoPoints(p1,p2)
        for segment in self.sides:
            if segment.crossLine(line):
                return True
        return False

    def rotate(self,angle,C=None):
        """Rotate the form by rotating its points from the center of rotation.
        Use center of the shape as default center of rotation.""" #Actually not working
        if not C: C=self.center
        for i in range(len(self.points)):
            P=self.points[i]
            v=Vector(P.x-C.x,P.y-C.y)
            v.rotate(angle)
            self.points[i]=v(C)

    def move(self,step):
        """Move the object by moving all its points using step."""
        x,y=step
        for point in self.points:
            l=min(len(step),len(point.position))
            for i in range(l):
                point.position[i]=step[i]

    def setPosition(self,position):
        """Move the object to an absolute position."""
        self.center.position=position

    def getPosition(self,position):
        """Return the position of the geometric center of the form."""
        return self.center.position

    def addPoint(self,point):
        """Add a point to the form."""
        self.points.append(point)

    def addPoints(self,points):
        """Add points to the form."""
        self.points.extend(points)

    __append__=addPoint
    __extend__=addPoints

    def removePoint(self,point):
        """Remove a point to the form."""
        self.point.remove(point)

    __remove__=removePoint

    def update(self,keys):
        """Update the points."""
        for point in self.points:
            point.update(keys)

    def __getitem__(self,index):
        """Return the point of index index."""
        return self.points[index]

    def __setitem__(self,index,value):
        """Change the points of a form."""
        self.points[index]=value

    def area(self):
        """Return the area of the form using its own points.
        General case in 2d only for now..."""
        l=len(self.points)
        if l<3: #The form has no point, is a single point or a segment, so it has no area.
            return 0
        elif l==3: #The form is a triangle, so we can calculate its area.
            a,b,c=[Vector.createFromSegment(segment) for segment in self.sides]
            A=1/4*sqrt(4*a.norm**2*b.norm**2-(a.norm**2+b.norm**2-c.norm**2)**2)
            return A
        else: #The form has more points than 3, so we can cut it in triangles.
            area=0
            C=self.center
            for i in range(l):
                A=self.points[i]
                B=self.points[(i+1)%l]
                triangle=Form([A,B,C])
                area+=Form.area(triangle)
            return area

    def __len__(self):
        """Return number of points."""
        return len(self.points)

    def __xor__(self,other):
        """Return the list of forms that are in the union of 2 forms."""
        if type(other)==Form: other=[other]
        return Form.union(other+[self])

    def __and__(self,other):
        """Return the list of forms that are in the intersection of 2 forms."""
        points=form.crossForm(other)
        points+=[point for point in self.points if point in other]
        points+=[point for point in other.points if point in self]
        if points: return Form(points)

    def setColor(self,color):
        """Color the whole form with a new color."""
        self.point_color=color
        self.side_color=color
        self.area_color=color

    def getColor(self):
        """Return the color of the segments because it is the more widely used."""
        return self.side_color

    def delColor(self):
        """Set the color of the form."""
        self.side_color=mycolors.WHITE
        self.point_color=mycolors.WHITE
        self.area_color=mycolors.WHITE

    def setPointColor(self,color):
        """Set the color of the points of the form."""
        for point in self.points:
            point.color=color

    def setPointMode(self,mode):
        """Set the mode of the points."""
        for point in self.points:
            point.mode=mode

    def setPointFill(self,fill):
        """Set the fill of the points."""
        for point in self.points:
            self.fill=fill

    def setPointKey(self,key,value):
        """Set the value of the points with the key and the value."""
        for point in self.points:
            point.__dict__[key]=value

    def setPointKeys(self,keys,values):
        """Set the values of the points with the keys and the values."""
        l=min(len(keys),len(values))
        for i in range(l):
            for point in self.points:
                point.__dict__[keys[i]]=values[i]

    getCrossPoints=crossSelf


    #points=         property(getPoints,setPoints,"Represents the points.") #If I do this, the program will be very slow...
    sides=segments= property(getSegments,setSegments,"Represents the segments.")
    center=point=   property(getCenter,setCenter,"Represents the center.")
    color=          property(getColor,setColor,delColor,"Represents the color.")
    cross_points=   property(getCrossPoints, "Represents the point of intersections of the segments.")
    #cross_points=   property(getCrossPoints,setCrossPoints,delCrossPoints, "Represents the point of intersections of the segments.")
    #point_color=    property(getPointColor,setPointColor,delPointColor,"Represents the color of the points.")
    #point_mode=     property(getPointMode,setPointMode,delPointMode,"Represents the mode of the points.")
    #point_fill=     property(getPointFill,setPointFill,delPointFill,"Represents the fill of the circle that represents the point.")
    #point_radius=   property(getPointRadius,setPointRadius,delPointRadius,"Represents the radius of the circle that represents the point.")
    #point_size=     property(getPointSize,setPointSize,delPointSize,"Represents the size of the cross that represents the point.")
    #point_width=    property(getPointWidth,setPointWidth,delPointWidth,"Represents the width of the cross that represents the point.")
    #segment_color=  property(getSegmentColor,setSegmentColor,delSegmentColor,"Represents the color of the segments.")
    #segment_width=  property(getSegmentWidth,setSegmentWith,delSegmentWidth,"Represents the width of the segments.")

class Circle:
    def random(min=-1,max=1,fill=0,color=mycolors.WHITE,border_color=None,area_color=None,center_color=None,radius_color=None,radius_width=1,text_color=None,text_size=20):
        """Create a random circle."""
        point=Point.random(min,max)
        radius=1
        return Circle.createFromPointAndRadius(point,radius,color,fill)

    def createFromPointAndRadius(point,radius,fill=0,color=mycolors.WHITE,border_color=None,area_color=None,center_color=None,radius_color=None,radius_width=1,text_color=None,text_size=20):
        """Create a circle from point."""
        return Circle(point.position,radius,color,fill)

    def __init__(self,*args,radius,fill=False,color=mycolors.WHITE,border_color=None,area_color=None,center_color=None,radius_color=None,radius_width=1,text_color=None,text_size=20):
        """Create a circle object using x, y and radius and optional color and width."""
        if len(args)==1: args=args[0]
        self.position=args
        self.radius=radius
        self.fill=fill
        if color:
            if not border_color: border_color=color
            if not area_color: area_color=color
            if not radius_color: radius_color=color
            if not text_color: text_color=color
        self.border_color=border_color
        self.area_color=area_color
        self.center_color=center_color
        self.radius_color=radius_color
        self.radius_width=radius_width
        self.text_color=text_color
        self.text_size=text_size

    def getX(self):
        """Return the x component of the circle."""
        return self.position[0]

    def setX(self,value):
        """Set the x component of the circle."""
        self.position[0]=value

    def getY(self):
        """Return the y component of the circle."""
        return self.position[1]

    def setY(self,value):
        """Set the y component of the circle."""
        self.position[1]=value

    def getPoint(self):
        """Return the point that correspond to the center of the circle."""
        return Point(self.position)

    def setPoint(self,point):
        """Set the center point of the circle by changing the position of the circle."""
        self.position=point.position

    x=property(getX,setX,"Allow the user to manipulate the x component easily.")
    y=property(getY,setY,"Allow the user to manipulate the y component easily.")
    center=point=property(getPoint,setPoint,"Allow the user to manipulate the point easily.")


    def center(self):
        """Return the point that correspond to the center of the circle."""
        return Point(self.position)

    def show(self,window,color=None,border_color=None,area_color=None,fill=None):
        """Show the circle on screen using the window."""
        if color:
            if not area_color: area_color=color
            if not border_color: border_color=color
        if not border_color: border_color=self.border_color
        if not area_color: area_color=self.area_color
        if not fill: fill=self.fill
        if fill: window.draw.circle(window.screen,area_color,[self.x,self.y],self.radius,True)
        window.draw.circle(window.screen,border_color,[self.x,self.y],self.radius)

    def showCenter(self,window,color=None,mode=None):
        """Show the center of the screen."""
        if not color: color=self.center_color
        if not mode: mode=self.center_mode
        self.center.show(window,mode=mode,color=color)

    def showText(self,window,text,color=None,size=None):
        """Show a text next to the circle."""
        if not color: color=self.text_color
        if not size: size=self.text_size
        self.center.showText(window,text,color=color,size=size)

    def showRadius(self,window,color=None,width=None):
        """Show the radius of the circle."""
        if not color: color=self.radius_color
        if not width: width=self.radius_width
        vector=Vector.createFromPolarCoordonnates(self.radius,0,color=color)
        vector.show(window,self.center,width=width)
        vector.showText(surface,self.center,"radius",size=20)

    def __call__(self):
        """Return the main components of the circle."""
        return [self.position,self.radius]

    def isCrossingCircle(self,other):
        """Determine if two circles are crossing."""
        vector=Vector.createFromTwoPoints(self.center,other.center)
        return vector.norm<self.radius+other.radius

    def crossCircle(self,other):
        """Return the intersections points of two circles maybe crossing."""
        pass #Math are involved...
        return points


if __name__=="__main__":
    from mysurface import Surface
    surface=Surface(name="Abstract Demonstration",fullscreen=True)

    p1=Point(10,0,radius=0.05,color=mycolors.YELLOW)
    p2=Point(20,20,radius=0.05,color=mycolors.YELLOW)
    #origin=Point(0,0)
    origin=Point.origin()

    l1=HalfLine(origin,math.pi/4)
    l2=Line(p1,math.pi/2,correct=False)
    s1=Segment(p1,p2)



    while surface.open:
        #Surface specific commands
        surface.check()
        surface.control()
        surface.clear()
        surface.show()

        #Actions
        l1.rotate(0.01,p2)
        l2.rotate(-0.02,p1)
        s1.rotate(0.03)

        p=l1|l2

        o=Point(0,0)
        p3=l2.projectPoint(o)
        f=Form([p1,p2,p3],area_color=mycolors.RED,fill=True)

        #Show
        surface.draw.window.print("l1.angle: "+str(l1.angle),(10,10))
        surface.draw.window.print("l2.angle: "+str(l2.angle),(10,30))
        surface.draw.window.print("f.area: "+str(f.area()),(10,50))

        f.show(surface)
        f.center.show(surface)


        s1.show(surface)

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
        l1.vector.show(surface,l1.point,color=mycolors.LIGHTGREEN,width=3)

        l2.show(surface,color=mycolors.BLUE)
        l2.point.show(surface,color=mycolors.LIGHTBLUE,mode="cross",width=3)
        l2.vector.show(surface,l2.point,color=mycolors.LIGHTBLUE,width=3)

        #Flipping the screen
        surface.flip()
