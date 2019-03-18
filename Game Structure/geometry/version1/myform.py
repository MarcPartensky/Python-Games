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
        return Form(points)
    def makeSparse(self):
        """Change the form into the one with the most sparsed points."""
        self=self.Sparse()
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
    def rotate(self,angle,center=None):
        """Rotate the form by rotating its points from the center of rotation.
        Use center of the shape as default center of rotation.""" #Actually not working
        if not center:
            C=self.center()
        for i in range(len(self.points)):
            P=self.points[i]
            v=Vector(P.x-C.x,P.y-C.y)
            v.rotate(angle)
            self.points[i]=v(C)
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
