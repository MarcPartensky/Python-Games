class Vector:
    def __init__(self,*args,arrow=(3,3),width=1,color=WHITE):
        """Create a vector."""
        self.x=args[0]
        self.y=args[1]
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
        return self.polar()[1]

    def __xor__(self,other):
        """Return the angle between two vectors."""
        return self.angle()-other.angle()
