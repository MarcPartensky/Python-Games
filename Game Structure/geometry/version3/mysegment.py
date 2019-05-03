from mydirection import Direction
from myvector import Vector
#from myline2 import Line
from mypoint import Point
import mycolors

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
        return Line(point,angle,width,color)

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


if __name__=="__main__":
    from mysurface import Surface
    surface=Surface()
    segment=Segment.random()
    while surface.open:
        surface.check()
        surface.control()
        surface.clear()
        surface.show()
        segment.show(surface)
        surface.flip()
