from math import pi,sqrt,atan,cos,sin
from cmath import polar

import math
import random
import mycolors

mean=lambda x:sum(x)/len(x)


class Point:
    def random(min=-1,max=1,radius=0.1,fill=False,color=mycolors.WHITE):
        """Create a random point using optional minimum and maximum."""
        x=random.uniform(min,max)
        y=random.uniform(min,max)
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

    def __init__(self,*args,mode=0,size=[0.1,0.1],width=1,radius=0.1,fill=False,color=mycolors.WHITE):
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

    def __call__(self):
        """Return the coordonnates of the points."""
        return [self.x,self.y]

    def __position__(self):
        """Return the coordonnates of the points."""
        return [self.x,self.y]

    def __contains__(self,other):
        """Return bool if objects is in point."""
        ox,oy=other[0],other[1]
        if self.radius>=sqrt((ox-self.x)**2+(oy-self.y)**2):
            return True
        else:
            return False

    def __getitem__(self,index):
        """Return x or y value using given index."""
        if index==0:
            return self.x
        if index==1:
            return self.y

    def __setitem__(self,index,value):
        """Change x or y value using given index and value."""
        if index==0:
            self.x=value
        if index==1:
            self.y=value

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
        """Show the name of the point on the window."""
        window.print(text,self,size=size,color=color)

    def __add__(self,other):
        """Add the components of 2 objects."""
        return Point(self.x+other[0],self.y+other[1])

    def __sub__(self,other):
        """Substract the components of 2 objects."""
        return Point(self.x-other[0],self.y-other[1])

    def __iter__(self):
        """Iterate the points of the form."""
        self.iterator=0
        return self

    def __next__(self):
        """Return the next point threw an iteration."""
        if self.iterator < 2:
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
        return "Point:"+str(self.__dict__)

class Direction:
    def __init__(self):
        pass

class Vector:
    def random(min=-1,max=1,color=mycolors.WHITE,width=1,arrow=[0.1,0.5]):
        """Create a random vector using optional min and max."""
        x=random.uniform(min,max)
        y=random.uniform(min,max)
        return Vector(x,y,color=color,width=width,arrow=arrow)

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
        angle=line.angle()
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
        if type(args)==Point:
            self.x=args.x
            self.y=args.y
        elif type(args)==list or type(args)==tuple:
            if type(args[0])==Point and type(args[1])==Point:
                self.x=args[1].x-args[0].x
                self.y=args[1].y-args[0].y
            elif (type(args[0])==int or type(args[0])==float) and (type(args[1])==int or type(args[1])==float):
                self.x=args[0]
                self.y=args[1]
            else:
                raise Exception("The list of objects used to define the vector has not been recognised.")
        else:
            raise Exception("The object used to define the vector has not been recognised.")
        self.color=color
        self.width=width
        self.arrow=arrow


    def show(self,p,window,color=None,width=None):
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

    def colinear(self,other):
        """Return if two vectors are colinear."""
        return self.x*other.y-self.y*other.x==0

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

    def __mul__(self,factor,color=None,width=None,arrow=None):
        """Multiply a vector by a given factor."""
        if not color: color=self.color
        if not width: width=self.width
        if not arrow: arrow=self.arrow
        if type(factor)==int or type(factor)==float:
            return Vector(self.x*factor,self.y*factor,color=color,width=width,arrow=arrow)
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
        if index==0:
            return self.x
        if index==1:
            return self.y

    def __setitem__(self,index,value):
        """Change x or y value using given index and value."""
        if index==0:
            self.x=value
        if index==1:
            self.y=value

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
        return self.angle()-other.angle()

    def __invert__(self):
        """Return the unit vector."""
        a=self.angle()
        position=Vector.cartesian([1,a])
        return Vector(position)


    def __str__(self):
        """Return a string description of the vector."""
        text="Vector:"+str(self.__dict__)
        return text



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

    def center(self):
        """Return the point of the center of the segment."""
        x=(self.p1.x+self.p2.x)/2
        y=(self.p1.y+self.p2.y)/2
        return Point(x,y,color=self.color)

    def angle(self):
        """Return the angle of the segment."""
        vector=Vector.createFromSegment(self)
        return vector.angle()

    def show(self,window,color=None,width=None):
        """Show the segment using window."""
        if not color: color=self.color
        if not width: width=self.width
        window.draw.line(window.screen,color,[self.p1.x,self.p1.y],[self.p2.x,self.p2.y],width)

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
        elif index==1: self.p2=value
        else: raise Exception("The index given is not valid.")

    def length(self):
        """Return the length of the segment."""
        x=p1.x-p2.x
        y=p1.y-p2.y
        return sqrt(x**2+y**2)

    def getLine(self):
        """Return the line through the end points of the segment."""
        angle=self.angle()
        point=self.p1
        return Line(point,angle,self.width,self.color)

    def getVector(self):
        """Return the vector that goes from p1 to p2."""
        return Vector.createFromTwoPoints(p1,p2)

    def __or__(self,other):
        """Return bool for (2 segments are crossing)."""
        #Extract cartesian coordonnates
        sa=self.slope()
        sb=self.ordinate()
        oa=other.slope()
        ob=other.ordinate()
        if not sa or not oa or not sb or not ob:
            return None
        if sa==oa:
            return None
        if type(other)==Segment:
            return self.crossSegment(other)
        if type(other)==Line:
            return self.crossLine(other)

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
        return (other.angle()==self.angle())

    def crossSegment(self,other):
        """Determine if the segment is crossing with another segment."""
        if self.parallel(other): return None #If the segments are parallels then there is not point
        #Extract the slopes and ordinates
        sb=self.ordinate()
        ob=other.ordinate()
        sa=self.slope()
        oa=other.slope()
        #Find a possible intersection point using line intersection
        x=(sb-ob)/(oa-sa)
        y=sa*x+sb
        #Determine if the point of intersection belongs to both segments
        sxmin,symin,sxmax,symax=self.getCorners()
        oxmin,oymin,oxmax,oymax=self.getCorners()
        xmin=max(sxmin,oxmin)
        xmax=min(sxmax,oxmax)
        ymin=max(symin,oymin)
        ymax=min(symax,oymax)
        #If it is the case return the point
        if  xmin<=x<=xmax and ymin<=y<=ymax:
            return Point(x,y,color=self.color)
        #By default if nothing is returned the function returns None


    def crossLine(self,other):
        """Determine if the segment is crossing with a line."""
        if self.parallel(other): return None #If the segments are parallels then there is not point
        #Extract the slopes and ordinates
        sb=self.ordinate()
        ob=other.ordinate()
        sa=self.slope()
        oa=other.slope()
        #Find a possible intersection point using line intersection
        x=(sb-ob)/(oa-sa)
        y=sa*x+sb
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

    def oldshow(self,surface,width=None,color=None):
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

    def show(self,surface,width=None,color=None):
        """Show the line on the surface."""
        if not color: color=self.color
        if not width: width=self.width
        corners=surface.getCorners()
        print("corners: ",corners)
        points=self.getSegmentWithinCorners(corners)
        segment.show(surface,color=color,width=width)

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
