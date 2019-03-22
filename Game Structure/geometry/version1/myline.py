class Line:
    def __init__(self,p1,p2,width=1,color=(255,255,255)):
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
