from math import pi,sqrt,atan,cos,sin
from cmath import polar

import math
import random
import mycolors

mean=lambda x:sum(x)/len(x)

digits=2 #Number of digits of precision of the objects when displayed


class Point:
    def random(corners,radius=0.02,fill=False,color=mycolors.WHITE):
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

    def __init__(self,*args,mode=0,size=[0.1,0.1],width=1,radius=0.05,fill=False,color=mycolors.WHITE):
        """Create a point using x, y, radius, fill and color."""
        args=list(args)
        if len(args)==1:
            args=args[0]
            if type(args)==list or type(args)==tuple:
                self.x=args[0]
                self.y=args[1]
            else:
                raise Exception("The object used to define the point has not been recognised.")
        elif len(args)==2:
            if (type(args[0])==int and type(args[1])==int) or (type(args[0]==float) and type(args[1])==float):
                self.x=args[0]
                self.y=args[1]
            else:
                raise Exception("The list of objects used to define the point has not been recognised.")
        else:
            raise Exception("The list object used to define the point has not been recognised because it contains too many components.")

        self.mode=mode
        self.size=size
        self.width=width
        self.radius=radius
        self.fill=fill
        self.color=color

    def __eq__(self,other):
        """Determine if two points are equals by comparing its components."""
        return tuple(self)==tuple(other)

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
        if index==0: return self.x
        if index==1: return self.y

    def __setitem__(self,index,value):
        """Change x or y value using given index and value."""
        if index==0: self.x=value
        if index==1: self.y=value

    def rotate(self,angle=pi,point=[0,0]):
        """Rotate the point using the angle and the center of rotation.
        Uses the origin for the center of rotation by default."""
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
        window.draw.circle(window.screen,color,[self.x,self.y],radius,not(fill))

    def show(self,window,mode=None,color=None,size=None,width=None,radius=None,fill=None):
        """Show the point on the window."""
        if not mode: mode=self.mode
        if mode==0 or mode=="circle":
            self.showCircle(window,color=color,radius=radius,fill=fill)
        if mode==1 or mode=="cross":
            self.showCross(window,color=color,size=size,width=width)

    def showText(self,window,text,size=20,color=mycolors.WHITE):
        """Show the text next to the point on the window."""
        window.print(text,self,size=size,color=color)

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
        if self.iterator<2:
            if self.iterator==0: value=self.x
            if self.iterator==1: value=self.y
            self.iterator+=1
            return value
        else:
            raise StopIteration

    def truncate(self):
        """Truncate the position of the point by making the x and y components integers."""
        self.x=int(self.x)
        self.y=int(self.y)

    def __str__(self):
        """Return the string representation of a point."""
        x=round(self.x,digits)
        y=round(self.y,digits)
        return "p("+str(x)+","+str(y)+")"

    __repr__=__str__

class Direction:
    def __init__(self):
        pass

class Vector:
    def random(min=-1,max=1,color=mycolors.WHITE,width=1,arrow=[0.1,0.5]):
        """Create a random vector using optional min and max."""
        x=random.uniform(min,max)
        y=random.uniform(min,max)
        return Vector(x,y,color=color,width=width,arrow=arrow)

    def sum(vectors):
        """Return the vector that correspond to the sum of all the vectors."""
        result=Vector(0,0)
        for vector in vectors:
            result+=vector
        return result

    def mean(vectors):
        """Return the vector that correspond to the mean of all the vectors."""
        vector=Vector.sum(vectors)
        return vector/len(vectors)

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
        if len(args)==1:
            args=args[0]
            self.x,self.y=args
        else:
            self.x,self.y=args
        self.color=color
        self.width=width
        self.arrow=arrow


    def show(self,window,p,color=None,width=None):
        """Show the vector."""
        if not color: color=self.color
        if not width: width=self.width
        q=self(p)
        v=-self.arrow[0]*self #wtf
        v1=v%self.arrow[1]
        v2=v%-self.arrow[1]
        a=v1(q)
        b=v2(q)
        window.draw.line(window.screen,color,p(),q(),width)
        window.draw.line(window.screen,color,q(),a(),width)
        window.draw.line(window.screen,color,q(),b(),width)

    def showText(self,surface,point,text,color=None,size=20):
        """Show the text next to the vector."""
        if not color: color=self.color
        v=self/2
        point=v(point)
        surface.print(text,tuple(point),color=color,size=size)

    def __iter__(self):
        """Iterate the points of the form."""
        self.iterator=0
        return self

    def __next__(self):
        """Return the next point threw an iteration."""
        if self.iterator<2:
            if self.iterator==0: value=self.x
            if self.iterator==1: value=self.y
            self.iterator+=1
            return value
        else:
            raise StopIteration

    def __neg__(self):
        """Return the negative vector."""
        x=-self.x
        y=-self.y
        return Vector(x,y,width=self.width,color=self.color)

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

    def __add__(self,other):
        """Add two vectors together."""
        return Vector(self.x+other.x,self.y+other.y,width=self.width,color=self.color)

    def __iadd__(self,other):
        """Add a vector to another."""
        self.x+=other.x
        self.y+=other.y
        return self

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
        return tuple(self)[index]

    def __setitem__(self,index,value):
        """Change x or y value using given index and value."""
        if index==0: self.x=value
        if index==1: self.y=value

    def __call__(self,*points):
        """Return points by applying the vector on those."""
        new_points=[point+self for point in points]
        if len(points)==1:
            return new_points[0]
        else:
            return new_points

    def apply(self,point):
        """Return the point after applying the vector to it."""
        return self+point

    def allApply(self,points):
        """Return the points after applying the vector to those."""
        new_points=[point+self for point in points]
        return new_points

    def angle(self):
        """Return the angle of a vector with the [1,0] direction in cartesian coordonnates."""
        return Vector.polar([self.x,self.y])[1]

    def norm(self):
        """Return the angle of a vector with the [1,0] direction in cartesian coordonnates."""
        return Vector.polar([self.x,self.y])[0]

    def __xor__(self,other):
        """Return the angle between two vectors."""
        return self.angle-other.angle

    def __invert__(self):
        """Return the unit vector."""
        a=self.angle
        position=Vector.cartesian([1,a])
        return Vector(position)


    def __str__(self):
        """Return a string description of the vector."""
        x=round(self.x,digits)
        y=round(self.y,digits)
        text="v("+str(x)+","+str(y)+")"
        return text

    __repr__=__str__



class Segment(Direction):
    def random(min=-1,max=1,width=1,color=mycolors.WHITE):
        """Create a random segment."""
        p1=Point.random(min,max)
        p2=Point.random(min,max)
        return Segment(p1,p2,width,color)

    def __init__(self,p1,p2,width=1,color=mycolors.WHITE):
        """Create the segment using 2 points, width and color."""
        self.p1=p1
        self.p2=p2
        self.width=width
        self.color=color

    def __str__(self):
        """Return the string representation of a segment."""
        text="s("+str(self.p1)+","+str(self.p2)+")"
        return text

    __repr__=__str__

    def __call__(self,t=1/2):
        """Return the point C of the segment so that Segment(p1,C)=t*Segment(p1,p2)."""
        tx=t*(self.p2.x-self.p1.x)
        ty=t*(self.p2.y-self.p1.y)
        v=Vector(tx,ty)
        p=v(self.p1)
        return p

    def __mul__(self,t):
        """Return the point C of the segment so that Segment(p1,C)=t*Segment(p1,p2)."""
        return Segment(self.p1,self(t))

    def center(self):
        """Return the point of the center of the segment."""
        x=(self.p1.x+self.p2.x)/2
        y=(self.p1.y+self.p2.y)/2
        return Point(x,y,color=self.color)

    middle=center

    def angle(self):
        """Return the angle of the segment."""
        vector=Vector.createFromSegment(self)
        return vector.angle()

    def show(self,window,color=None,width=None):
        """Show the segment using window."""
        if not color: color=self.color
        if not width: width=self.width
        window.draw.line(window.screen,color,[self.p1.x,self.p1.y],[self.p2.x,self.p2.y],width)

    def __contains__(self,point,e=10e-10):
        """Determine if a point is in a segment."""
        if point==self.p1: return True
        v1=Vector.createFromTwoPoints(point,self.p1)
        v2=self.getVector()
        a1=v1.angle()
        a2=v2.angle()
        n1=v1.norm()
        n2=v2.norm()
        return (abs(a1-a2)%(2*math.pi))<e and (n1<=n2)

    def __len__(self):
        """Return the number of points."""
        return 2

    def __iter__(self):
        """Iterate the points of the form."""
        self.iterator=0
        return self

    def __next__(self):
        """Return the next point threw an iteration."""
        if self.iterator<2:
            if self.iterator==0: value=self.p1
            if self.iterator==1: value=self.p2
            self.iterator+=1
            return value
        else:
            raise StopIteration

    def __getitem__(self,index):
        """Return the point corresponding to the index given."""
        return [self.p1,self.p2][index]

    def __setitem__(self,index,value):
        """Change the value the point corresponding value and index given."""
        if index==0: self.p1=value
        if index==1: self.p2=value

    def length(self):
        """Return the length of the segment."""
        x=p1.x-p2.x
        y=p1.y-p2.y
        return sqrt(x**2+y**2)

    def getLine(self,correct=True):
        """Return the line through the end points of the segment."""
        angle=self.angle()
        point=self.p1
        return Line(point,angle,self.width,self.color,correct=correct)

    def getVector(self):
        """Return the vector that goes from p1 to p2."""
        return Vector.createFromTwoPoints(self.p2,self.p1)

    vector=getVector

    def rotate(self,angle,point=None):
        """Rotate the segment using an angle and an optional point of rotation."""
        if not point: point=self.middle()
        self.p1.rotate(angle,point)
        self.p2.rotate(angle,point)

    def __or__(self,other):
        """Return bool for (2 segments are crossing)."""
        if isinstance(other,Segment): return self.crossSegment(other)
        if isinstance(other,Line): return self.crossLine(other)
        if isinstance(other,HalfLine): return other.crossSegment(self)
        if isinstance(other,Form): return form.crossSegment(self)

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
        if not point: return None
        x,y=point
        sxmin,symin,sxmax,symax=self.getCorners()
        oxmin,oymin,oxmax,oymax=self.getCorners()
        xmin=max(sxmin,oxmin)
        xmax=min(sxmax,oxmax)
        ymin=max(symin,oymin)
        ymax=min(symax,oymax)
        if  xmin-e<=x<=xmax+e and ymin-e<=y<=ymax+e:
            return Point(x,y,color=self.color)

    def crossLine(self,other):
        """Return the intersection point of the segment with a line."""
        if self.parallel(other): return None #If the segments are parallels then there is not point
        #Extract the slopes and ordinates
        line=self.getLine()
        point=other.crossLine(line)
        if not point: return None
        x,y=point
        #Determine if the point of intersection belongs to both the segment and the line
        xmin,ymin,xmax,ymax=self.getCorners()
        #If it is the case return the point
        if  xmin<=x<=xmax and ymin<=y<=ymax:
            return Point(x,y,color=self.color)
        #By default if nothing is returned the function returns None


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

    def createFromTwoPoints(point1,point2,width=1,color=mycolors.WHITE):
        """Create a line using two points with optional features."""
        vector=Vector.createFromTwoPoints(point1,point2)
        angle=vector.angle()
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
        m,n=self.vector()
        o,p=other.vector()
        if n*o-m*p==0: return None #The lines are parallels
        x=(a*n*o-b*m*o-c*m*p+d*m*o)/(n*o-m*p)
        y=(x-a)*n/m+b
        return Point(x,y)

    def parallel(self,other):
        """Determine if the line is parallel to another object (line or segment)."""
        return other.angle==self.angle

    def __contains__(self,point,e=10e-10):
        """Determine if a point belongs to the line."""
        v1=self.vector()
        v2=Vector.createFromTwoPoints(self.point,point)
        return v1.colinear(v2,e)

    def getHeight(self,point):
        """Return the height line between the line and a point."""
        vector=self.getNormalVector()
        angle=vector.angle()
        line=Line(point,angle)
        return line


    def distanceFromPoint(self,point):
        """Return the distance between a point and the line."""
        line=self.getHeight(point)
        intersection=self.crossLine(line)
        vector=Vector.createFromTwoPoints(point,intersection)
        return vector.norm()

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
        v1=self.vector()
        v2=Vector.createFromTwoPoints(self.point,point)
        return abs(v1.angle()-v2.angle())<e

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
    def random(corners,number=random.randint(1,10),**kwargs):
        """Create a random form using the point_number, the minimum and maximum position for x and y components and optional arguments."""
        points=[Point.random(corners) for i in range(number)]
        form=Form(points,**kwargs)
        form.makeSparse()
        return form

    def __init__(self,points,fill=False,point_mode=0,point_radius=0.01,point_width=1,side_width=1,color=None,point_color=mycolors.WHITE,side_color=mycolors.WHITE,area_color=mycolors.WHITE,point_show=True,side_show=True):
        """Create the form object using points."""
        self.points=points
        self.point_radius=point_radius
        self.side_width=side_width
        if color: self.point_color=self.side_color=self.area_color=color
        self.point_color=point_color
        self.side_color=side_color
        self.area_color=area_color
        self.point_show=point_show
        self.side_show=side_show
        self.fill=fill

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
        return self.points==other.points

    def center(self,color=None,radius=None):
        """Return the point of the center."""
        if not color: color=self.point_color
        if not radius: radius=self.point_radius
        mx=mean([p.x for p in self.points])
        my=mean([p.y for p in self.points])
        return Point(mx,my,color=color,radius=radius)

    def sides(self):
        """"Return the list of the form sides."""
        return [Segment(self.points[i%len(self.points)],self.points[(i+1)%len(self.points)],color=self.side_color,width=self.side_width) for i in range(len(self.points))]

    def show(self,window,point_color=None,side_color=None,area_color=None,side_width=None,point_radius=None,color=None,fill=None,point_show=None,side_show=None):
        """Show the form using a window."""
        if color:
            area_color=color
            side_color=color
            point_color=color
        if not area_color: area_color=self.area_color
        if not point_color: point_color=self.point_color
        if not side_color: side_color=self.side_color
        if not side_width: side_width=self.side_width
        if not point_radius: point_radius=self.point_radius
        if not fill: fill=self.fill
        if not point_show: point_show=self.point_show
        if not side_show: side_show=self.side_show
        points=[(p.x,p.y) for p in self.points]
        if len(points)>1 and fill:
            window.draw.polygon(window.screen,area_color,points,not(fill))
        if point_show:
            for point in self.points:
                point.show(window,color=point_color,radius=point_radius)
        if side_show:
            for side in self.sides():
                side.show(window,color=side_color,width=side_width)

    def __or__(self,other):
        """Return the points of intersections with the form and another object."""
        if isinstance(other,HalfLine):  return self.crossHalfLine(other)
        if isintance(other,Line):       return self.crossLine(other)
        if isinstance(other,Segment):   return self.crossSegment(other)
        if isinstance(other,Form):      return self.crossForm(other)

    def crossForm(self,other):
        """Return the bool: (2 sides are crossing)."""
        points=[]
        for myside in self.sides():
            for otherside in other.sides():
                point=myside|otherside
                if point:
                    points.append(point)
        return points

    def crossDirection(self,other):
        """Return the list of the points of intersection between the form and a segment or a line."""
        points=[]
        for side in self.sides():
            cross=side|other
            if cross: points.append(cross)
        return points

    def crossHalfLine(self,other):
        """Return the list of points of intersection in order between the form and a half line."""
        points=[]
        for side in self.sides():
            cross=other.crossSegment(side)
            if cross: points.append(cross)
        hp=other.getPoint()
        objects=[(p,Vector.createFromTwoPoints(p,hp).norm()) for p in points]
        objects=sorted(objects,key=lambda x:x[1])
        points=[p for (p,v) in objects]
        return points



    def crossLine(self,other):
        """Return the list of the points of intersection between the form and a line."""
        points=[]
        for side in self.sides():
            cross=side.crossLine(other)
            if cross:
                points.append(cross)
        return points

    def crossSegment(self,other):
        """Return the list of the points of intersection between the form and a segment."""
        points=[]
        for side in self.sides():
            cross=side.crossSegment(other)
            if cross:
                points.append(cross)
        return points

    def convex(self):
        """Return the bool (the form is convex)."""
        center=self.center()
        cx,cy=center[0],center[1]
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
        center=self.center()
        cx,cy=center[0],center[1]
        list1=[]
        for point in self.points:
            px,py=point.x,point.y
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
        for segment in self.sides():
            if segment.crossLine(line):
                return True
        return False

    def rotate(self,angle,C=None):
        """Rotate the form by rotating its points from the center of rotation.
        Use center of the shape as default center of rotation.""" #Actually not working
        if not C:
            C=self.center()
        for i in range(len(self.points)):
            P=self.points[i]
            v=Vector(P.x-C.x,P.y-C.y)
            v.rotate(angle)
            self.points[i]=v(C)

    def move(self,step):
        """Move the object by moving all its points using step."""
        x,y=step[0],step[1]
        for i in range(len(self.points)):
            self.points[i].x+=x
            self.points[i].y+=y

    def setPosition(self,position):
        """Move the object to an absolute position."""
        x,y=position[0],position[1]
        cx,cy=self.center()
        for i in range(len(self.points)):
            vx=self.points[i].x-cx
            vy=self.points[i].y-cy
            self.points[i].x=vx+x
            self.points[i].y=vy+y

    def getPosition(self,position):
        """Return the position of the geometric center of the form."""
        center=self.center()
        x,y=center[0],center[1]
        return [x,y]

    def getPoints(self):
        """Return the points of the form."""
        return self.points

    def setPoints(self,points):
        """Set the points of the form."""
        self.points=points

    def addPoint(self,point):
        """Add a point to the form."""
        self.points.append(point)

    __append__=addPoint

    def removePoint(self,point):
        """Remove a point to the form."""
        self.point.remove(point)

    __remove__=removePoint

    def update(self,input):
        """Update the points."""
        for point in self.points:
            point.update(input)

    def __getitem__(self,index):
        """Return the point of index index."""
        return self.points[index]

    def __setitem__(self,index,value):
        """Change the points of a form."""
        self.points[index]=value

    def area(self):
        """Return the area of the form using its own points."""
        l=len(self.points)
        if l<3: #The form has no point, is a single point or a segment, so it has no area.
            return 0
        elif l==3: #The form is a triangle, so we can calculate its area.
            a,b,c=[Vector.createFromSegment(segment) for segment in self.sides()]
            A=1/4*sqrt(4*a.norm()**2*b.norm()**2-(a.norm()**2+b.norm()**2-c.norm()**2)**2)
            return A
        else: #The form has more points than 3, so we can cut it in triangles.
            area=0
            C=self.center()
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
        pass

    def __and__(self,other):
        """Return the list of forms that are in the intersection of 2 forms."""
        pass

    def color(self,_color=mycolors.WHITE):
        """Color the whole form with a new color."""
        self.point_color=_color
        self.side_color=_color
        self.area_color=_color



if __name__=="__main__":
    from mysurface import Surface
    surface=Surface(name="Abstract Demonstration",fullscreen=True)

    p1=Point(10,0,radius=0.05,color=mycolors.YELLOW)
    p2=Point(20,20,radius=0.05,color=mycolors.YELLOW)
    origin=Point(0,0)

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
        f.center().show(surface)


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
        l1.vector().show(surface,l1.point,color=mycolors.LIGHTGREEN,width=3)

        l2.show(surface,color=mycolors.BLUE)
        l2.point.show(surface,color=mycolors.LIGHTBLUE,mode="cross",width=3)
        l2.vector().show(surface,l2.point,color=mycolors.LIGHTBLUE,width=3)

        #Flipping the screen
        surface.flip()
