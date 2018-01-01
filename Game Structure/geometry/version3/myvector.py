from mysegment import Segment
from mypoint import Point
from myline import Line

from math import cos,sin
from cmath import polar

from mywindow import Window
from mysurface import Surface

class Vector:
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

    def __str__(self):
        """Return a string description of the vector."""
        text="Vector: x,y:   "+str(self.x)+", "+str(self.y)+", color: "+str(self.color)+", width: "+str(self.width)+" and arrow: "+str(self.arrow)
        return text

    __repr__=__str__



if __name__=="__main__":
    window=Surface()
    p1=Point(5,1)
    p2=Point(5,4)
    p3=Point(3,2)
    v1=Vector(p1,p2)
    print(v1) #Give a string representation of the vector
    v2=0.8*v1 #Multiply vector by scalar 0.8
    p4=v2(p1)
    v2.color=(255,0,0)
    p4.color=(0,255,0)
    while window.open:
        window.check()
        window.clear()
        window.show()
        window.control() #Specific to surfaces
        v1.show(p1,window)
        v2%=0.3 #Rotate the form by 0.3 radian
        v2.show(p1,window)
        p2.show(window)
        p4.show(window)
        window.flip()
