from mypoint import Point
from myvector import Vector
from mysegment import Segment
from myline import Line

from mycolors import WHITE

from math import sqrt,pi

mean=lambda x:sum(x)/len(x)

class Form:
    def __init__(self,points,closed=True,fill=False,side_width=1,point_radius=5,point_color=WHITE,side_color=WHITE,area_color=WHITE):
        """Create the form object using points."""
        self.points=points
        self.point_radius=point_radius
        self.point_color=point_color
        self.side_width=side_width
        self.side_color=side_color
        self.area_color=area_color
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
        """Needed in order to allow the client to iterate the points of the form through a for loop."""
        self.iterator=0
        return self

    def __next__(self):
        """Allow the client to iterate the points of the form through a for loop."""
        if self.iterator < len(self.points):
            iterator=self.iterator
            self.iterator+=1
            return self.points[iterator]
        else:
            raise StopIteration


    def center(self,color=None):
        """Return the point of the center."""
        if not color: color=self.point_color
        mx=mean([p.x for p in self.points])
        my=mean([p.y for p in self.points])
        return Point(mx,my,color=color)

    def sides(self):
        """"Return the list of the form sides."""
        return [Segment(self.points[i%len(self.points)],self.points[(i+1)%len(self.points)],color=self.side_color,width=self.side_width) for i in range(len(self.points))]

    def show(self,window,point_color=None,side_color=None,area_color=None,side_width=None,point_radius=None,color=None,fill=None):
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
        points=[(p.x,p.y) for p in self.points]
        if len(points)>1:
            window.draw.polygon(window.screen,area_color,points,not(fill))
        for point in self.points:
            point.show(window,color=point_color,radius=point_radius)
        for side in self.sides():
            side.show(window,color=side_color,width=side_width)

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
        self=self.getSparse()

    def __contains__(self,point):
        """Return the bool: (the point is in the form)."""
        x,y=point[0],point[1]
        p1=Point(x,y)
        p2=Point(0,0)
        line=Line(p1,p2)
        line.show(window)
        #print(line.__dict__)
        for segment in self.sides():
            if segment|line:
                return True

    def inForm(self,point):
        for i in range(len(self.points)):
            A=self.points[i]


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

    def area(self):
        """Return the area of the form using its own points."""
        l=len(self.points)
        if l==0 or l==1:
            return 0
        elif l==3:
            a,b,c=[Vector(segment) for segment in self.sides()]
            A=1/4*sqrt(4*a.norm()**2*b.norm()**2-(a.norm()**2+b.norm()**2-c.norm()**2)**2)
            return A
        else:
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
