from math import pi,sqrt,atan,cos,sin
import random
mean=lambda x:sum(x)/len(x)

import mycolors

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

if __name__=="__main__":
    from mysurface import Surface
    from myvector import Vector
    surface=Surface(fullscreen=True)
    p1=Point(0,0,color=mycolors.RED,fill=True)
    p2=Point(5,0,color=mycolors.GREEN,fill=True)
    p3=Point(10,0,color=mycolors.BLUE,fill=True)
    p4=Point(15,0,color=mycolors.YELLOW,fill=True)
    p5=Point(20,0,color=mycolors.ORANGE,fill=True)
    points=[p1,p2,p3,p4,p5]
    points=[Point(5*i,0,radius=0.2) for i in range(10)]
    angles=[i/1000 for i in range(1,len(points))]
    while surface.open:
        surface.check()
        surface.control()
        surface.clear()
        surface.show()
        Point.turnPoints(angles,points)
        Point.showPoints(surface,points)
        surface.flip()
