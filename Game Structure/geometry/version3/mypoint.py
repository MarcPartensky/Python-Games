from math import pi,sqrt,atan,cos,sin
mean=lambda x:sum(x)/len(x)


class Point:
    def __init__(self,*args,radius=0.1,fill=False,color=(255,255,255)):
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
        Uses [0,0] for the center of rotation by default."""
        s=Vector(self.x,self.y)
        v=Vector(self.x-point[0],self.y-point[1])
        sn,sa=s.polar()
        vn,va=v.polar()
        self.x=s.x+vn*cos(sa+va)
        self.y=s.y+vn*sin(sa+va)
    def move(self,*step):
        """Move the point using given step."""
        self.x+=step[0]
        self.y+=step[1]
    def moveTo(self,position):
        """Move the point to position using given position."""
        pass
    def show(self,window,color=None,radius=None,fill=None):
        """Show a point using window."""
        if not color: color=self.color
        if not radius: radius=self.radius
        if not fill: fill=self.fill
        window.draw.circle(window.screen,color,[self.x,self.y],radius,not(fill))
    def __add__(self,other):
        """Add the components of 2 objects."""
        return Point(self.x+other[0],self.y+other[1])
    def __sub__(self,other):
        """Substract the components of 2 objects."""
        return Point(self.x-other[0],self.y-other[1])
