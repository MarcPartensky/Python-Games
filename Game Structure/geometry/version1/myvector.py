from math import cos,sin
from cmath import polar
from mysegment import Segment
from mypoint import Point
from myline import Line

class Vector:
    def polar(position):
        """Return the polar position [norm,angle] using cartesian position [x,y]."""
        return list(polar(complex(position[0],position[1])))

    def cartesian(position):
        """Return the cartesian position [x,y] using polar position [norm,angle]."""
        return [position[0]*cos(position[1]),position[0]*sin(position[1])]


    def __init__(self,*args,arrow=(3,3),width=1,color=(255,255,255)):
        """Create a vector."""
        args=list(args)
        if len(args)==1:
            args=args[0]
        if type(args)==Segment:
            self.x=args.p2.x-args.p1.x
            self.y=args.p2.y-args.p1.y
        elif type(args)==Line:
            self.x=args.vector.x
            self.y=args.vector.y
        elif type(args)==Point:
            self.x=args.x
            self.y=args.y
        elif type(args)==list or type(args)==tuple:
            if type(args[0])==Point and type(args[1])==Point:
                self.x=args[1].x-args[0].x
                self.y=args[1].y-args[0].y
            elif type(args[0])==int and type(args[1])==int:
                self.x=args[0]
                self.y=args[1]
            elif type(args[0])==float and type(args[1])==float:
                self.x=args[0]
                self.y=args[1]
            else:
                raise Exception("The list of objects used to define the vector has not been recognised.")
        else:
            raise Exception("The object used to define the vector has not been recognised.")
        self.width=width
        self.color=color

    def show(self,p,window,color=None):
        """Show the vector."""
        if not color:
            color=self.color
        p1=Point(p[0],p[1],color=self.color)
        p2=Point(self.x+p[0],self.y+p[1],color=self.color)
        s=Segment(p1,p2,width=self.width,color=self.color)
        s.show(window)

    def __neg__(self):
        """Return the negative vector."""
        x=-self.x
        y=-self.y
        return Vector(x,y,width=self.width,color=self.color)

    def colinear(self,other):
        """Return if two vectors are colinear."""
        return self.x*other.y-self.y*other.x==0

    def scalar(self,other):
        """Return the scalar product between two vectors."""
        return self.x*other.x+self.y*other.y

    def __mul__(self,factor):
        """Multiply a vector by a given factor."""
        if type(factor)==Vector:
            pass
        else:
            self.x*=factor
            self.y*=factor
    def __truediv__(self,factor):
        """Multiply a vector by a given factor."""
        if type(factor)==Vector:
            pass
        else:
            self.x/=factor
            self.y/=factor

    def __add__(self,other):
        """Add two vectors together."""
        return Vector(self.x+other.x,self.y+other.y,width=self.width,color=self.color)

    def rotate(self,angle):
        """Rotate a vector using the angle of rotation."""
        n,a=Vector.polar([self.x,self.y])
        a+=angle
        self.x=n*cos(a)
        self.y=n*sin(a)

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
        points=[point+self for point in points]
        if len(points)==1:
            return points[0]
        else:
            return points

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
        n,a=self.polar()
