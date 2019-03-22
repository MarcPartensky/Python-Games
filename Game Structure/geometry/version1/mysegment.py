from myline import Line

class Segment(Line):
    def __init__(self,p1,p2,width=1,color=(255,255,255)):
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
        """Return the number of points."""
        return 2
    def __getitem__(self,index):
        """Return the point corresponding to the index given."""
        return [self.p1,self.p2][index]
    def __setitem__(self,index,value):
        """Change the value the point corresponding value and index given."""
        if index==0:
            self.p1==value
        elif index==1:
            self.p2==value
        else:
            raise Exception("The index given is not valid.")
    def length(self):
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
