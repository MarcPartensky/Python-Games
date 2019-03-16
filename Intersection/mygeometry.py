WHITE=(255,255,255)

from mywindow import Window

from mymaths import sign2,mean
from math import sqrt,atan,pi,cos,sin
import random
from cmath import polar

class Figure:
    def __init__(self,segments,color=WHITE):
        """Create a figure object."""
        self.segments=segments
        self.color=color
    def show(self,window):
        """Show segments."""
        for segment in self.segments:
            segment.show(window)


class Form:
    def __init__(self,points,closed=True,fill=False,width=1,color=WHITE):
        """Create the form object using points."""
        self.points=points
        self.closed=closed
        self.fill=fill
        self.width=1
        self.color=color
    def __add__(self,point):
        """Add a point to the form."""
        self.points+=point
    def __sub__(self,point):
        """Remove a point to the form."""
        self.points.remove(point)
    def center(self):
        """Return the point of the center."""
        mx=mean([p.x for p in self.points])
        my=mean([p.y for p in self.points])
        return Point(mx,my)
    def sides(self):
        """"Return the list of the form sides."""
        return [Segment(self.points[i%len(self.points)],self.points[(i+1)%len(self.points)],color=self.color,width=self.width) for i in range(len(self.points))]
    def show(self,window):
        """Show the form using a window."""
        for point in self.points:
            point.show(window)
        for side in self.sides():
            side.show(window)
    def __or__(self,other):
        """Return the bool: (2 sides are crossing)."""
        for myside in self.sides():
            for otherside in other.sides():
                if myside|otherside:
                    return True
        return False
    def connex(self):
        """Return the bool (the form is connex)."""
        pass
    def sparse(self):
        """Return the form with the most sparsed points."""
        pass
    def __contains__(self,point):
        """Return the bool: (the point is in the form)."""
        x,y=point[0],point[1]
        p1=Point(x,y)
        p2=Point(0,0)
        line=Line(p1,p2)
        line.show(window)
        print(line.__dict__)
        for segment in self.sides():
            if segment|line:
                return True
        return False
        #Trace une ligne passant par
    def rotate(self,angle,center=None):
        """Rotate the form by rotating its points from the center of rotation.
        Use center of the shape as default center of rotation.""" #Actually not working
        if not center:
            center=self.center()
        c=self.center()
        for i in range(len(self.points)):
            self.points[i].rotate(angle,center)
        """for point in self.points:
            point.rotate(angle,center) #rotate should have a second optional argument that does the same thing than above"""

    def move(self,*step):
        """Move the object by moving all its points using step."""
        x,y=step[0],step[1]
        for i in range(len(self.points)):
            self.points[i].x+=x
            self.points[i].y+=y
    def moveTo(self,position):
        """Move the object to an absolute position."""
        x,y=position[0],position[1]
        cx,cy=self.center()
        for i in range(len(self.points)):
            vx=self.points[i].x-cx
            vy=self.points[i].y-cy
            self.points[i].x=vx+x
            self.points[i].y=vy+y


    def moveUntil(self,position):
        """Move the object to the position until the point is hit."""
        pass

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
    def triangleArea(self,form):
        """Return the area of a triangle of type form."""
        a,b,c=form.sides()
        A=1/4*sqrt(4*a.l**2*b.l**2-(a.l**2+b.l**2-c.l**2)**2)
    def __len__(self):
        """Return number of points."""
        return len(self.points)


class Polygon:
    def __init__(self,points,fill=False,width=1,color=WHITE,showpoints=True):
        """Create the polygon using points, fill, width, color and showpoints."""
        self.points=points
        self.fill=fill
        self.width=1
        self.color=color
        self.showpoints=showpoints
    def show(self,window):
        """Show the polygon using window."""
        positions=[[p.x,p.y] for p in self.points]
        window.draw.polygon(window.screen,self.color,positions,self.width)
        if self.showpoints:
            for point in self.points:
                point.show(window)
        return False
    def update(self):
        pass

class Point:
    def __init__(self,*args,radius=5,fill=False,color=WHITE):
        """Create a point using x, y, radius, fill and color."""
        self.x=args[0]
        self.y=args[1]
        self.n=sqrt(self.x**2+self.y**2)
        self.a=atan(self.y/self.x)
        self.radius=radius
        self.fill=fill
        self.color=color
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
        Uses [0,0] for the center of rotation by default."""
        s=Vector(self.x,self.y)
        v=Vector(self.x-point[0],self.y-point[1])
        sn,sa=s.polar()
        vn,va=v.polar()
        self.x=s.x+vn*cos(sa+va)
        self.y=s.y+vn*sin(sa+va)
        print(self.x,self.y)
    def move(self,*step):
        """Move the point using given step."""
        self.x+=step[0]
        self.y+=step[1]
    def moveTo(self,position):
        """Move the point to position using given position."""
        pass
    def show(self,window):
        """Show a point using window."""
        window.draw.circle(window.screen,self.color,[int(self.x),int(self.y)],self.radius,not self.fill)
    def __add__(self,other):
        """Add two points together by making the sum of their components."""
        """ if other.color==self.color:
            color=self.color
        else:
            color=None
        if other.width=self.width:
            width=self.width
        else:
            width=None
        if"""
        return Point(self.x+other[0],self.y+other[1])
    def __sub__(self,other):
        return Point(self.x-other[0],self.y-other[1])

class Line:
    def __init__(self,p1,p2,width=1,color=WHITE):
        """Create the line using 2 points, width and color."""
        self.width=width
        self.color=color
        if p1.x!=p2.x:
            self.a=(p2.y-p1.y)/(p2.x-p1.x)
        else:
            self.a=None
        if self.a!=None:
            self.b=p1.y-self.a*p1.x
        else:
            self.b=None
    def evaluate(self,x):
        """Evaluate the affine function corresponding to the line using x."""
        return self.a*x+self.b
    def show(self,window):
        """Show the line using window."""
        wcmx,wcmy,wcMx,wcMy=window.coordonnates
        my=self.evaluate(wcmx)
        My=self.evaluate(wcMx)
        window.draw.line(window.screen,self.color,[wcmx,my],[wcMx,My],self.width)
    def __or__(self,other):
        """Return bool for (2 lines are crossing)."""
        if self.a==other.a:
            return None
        x=(self.b-other.b)/(other.a-self.a)
        y=self.a*x+self.b
        return Point(x,y)


class Segment(Line):
    def __init__(self,p1,p2,width=1,color=WHITE):
        """Create the segment using 2 points, width and color."""
        Line.__init__(self,p1,p2,width,color)
        self.p1=p1
        self.p2=p2
    def center(self):
        """Return the point of the center of the Segment."""
        x=(self.p1.x+self.p2.x)/2
        y=(self.p1.y+self.p2.y)/2
        return Point(x,y,color=self.color)
    def show(self,window):
        """Show the segment using window."""
        window.draw.line(window.screen,self.color,[self.p1.x,self.p1.y],[self.p2.x,self.p2.y],self.width)
    def __len__(self):
        """Return the length of the segment."""
        x=p1.x-p2.x
        y=p1.y-p2.y
        return sqrt(x**2+y**2)

    def __or__(self,other):
        """Return bool for (2 segments are crossing)."""
        if not self.a or not other.a or not self.b or not other.b:
            return None
        if self.a==other.a:
            return None
        x=(self.b-other.b)/(other.a-self.a)
        y=self.a*x+self.b
        if type(other)==Segment:
            mx=max(min(self.p1.x,self.p2.x),min(other.p1.x,other.p2.x))
            Mx=min(max(self.p1.x,self.p2.x),max(other.p1.x,other.p2.x))
            my=max(min(self.p1.y,self.p2.y),min(other.p1.y,other.p2.y))
            My=min(max(self.p1.y,self.p2.y),max(other.p1.y,other.p2.y))
            if  mx<=x<=Mx and my<=y<=My:
                return Point(x,y,color=self.color)
            else:
                return None
        if type(other)==Line:
            mx=min(self.p1.x,self.p2.x)
            Mx=max(self.p1.x,self.p2.x)
            my=min(self.p1.y,self.p2.y)
            My=max(self.p1.y,self.p2.y)
            if  mx<=x<=Mx and my<=y<=My:
                return Point(x,y,color=self.color)
            else:
                return None
        else:
            return None

class Vector:
    def __init__(self,*args,arrow=(3,3),width=1,color=WHITE):
        """Create a vector."""
        a=list(*args)
        print(a)
        self.x=a[0]
        self.y=a[1]
        self.width=width
        self.color=color
    def show(self,p,window):
        """Show the vector."""
        print(p[0],p[1])
        p2=Point(self.x+p[0],self.y+p[1],color=self.color)
        s=Segment(p1,p2,width=self.width,color=self.color)
        s.show(window)
    def __neg__(self):
        """Return the negative vector."""
        x=-self.x
        y=-self.y
        return Vector(x,y,width=self.width,color=self.color)
    def polar(self):
        """Return the polar coordonnates for the x and y position of the object."""
        return list(polar(complex(self.x,self.y)))
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
    def __add__(self,other):
        """Add two vectors together."""
        return Vector(self.x+other.x,self.y+other.y,width=self.width,color=self.color)
    def rotate(self,angle):
        """Rotate a vector using the angle of rotation."""
        n,a=self.polar()
        a+=angle
        self.x+=n*cos(a)
        self.y+=n*sin(a)
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




class Wrapper:
    def __init__(self,form):
        self.form=form
    def update(self):
        pass

if __name__=="__main__":
    window=Window()
    p1=Point(15,62)
    p2=Point(250,400)
    p3=Point(800,500)
    p4=Point(400,400,color=(0,255,0))
    points=[p1,p2,p3,p4]
    for point in points:
        point.show(window)
    #f=Form([p1,p2,p3],color=(0,0,255))
    #f.show(window)
    #Segment(f[0],f[1],color=(255,0,0)).center().show(window)
    #print(p4 in f)
    #window.clear()
    #p4.show(window)
    #a=Line(p4,p2,color=(255,0,0))
    #b=Segment(p1,p3,color=(255,255,0))
    #a.show(window)
    #b.show(window)
    #p=b|a
    a=p2-p1
    a=Vector(a)
    b=Vector(60,-20)
    a.show(p2,window)
    b.show(p2,window)
    window()



    #print(list(p))


a=Vector(1,5)
