class Rect:
    """Define a pure and simple rectangle."""
    def createFromCorners(corners):
        """Create a rectangle."""
        coordonnates=Rect.getCoordonnatesFromCorners(corners)
        print("c:",coordonnates)
        return Rect(coordonnates[:2],coordonnates[2:])

    def createFromRect(rect):
        """Create a rect from a pygame rect."""
        coordonnates=Rect.getCoordonnatesFromRect(rect)
        return Rect(coordonnates[:2],coordonnates[2:])

    def createFromCoordonnates(coordonnates):
        """Create a rect using the coordonnates."""
        return Rect(coordonnates[:2],coordonnates[2:])

    def __init__(self,position,size):
        """Create a rectangle."""
        self.position=position
        self.size=size

    def getCorners(self):
        """Return the corners of the case."""
        px,py=self.position
        sx,sy=self.size
        return (px-sx/2,py-sy/2,px+sx/2,py+sy/2)

    def setCorners(self):
        """Set the corners of the case."""
        coordonnates=self.getCoordonnatesFromCorners(corners)
        self.position=coordonnates[:2]
        self.size=coordonnates[2:]

    def __contains__(self,position):
        """Determine if a position is in the rectangle."""
        x,y=position
        return (self.xmin<=x<=self.xmax) and (self.ymin<=y<=self.ymax)

    def getCoordonnates(self):
        """Return the coordonnates ofthe rectangle."""
        return self.position+self.size

    def setCoordonnates(self,coordonnates):
        """Set the coordonnates of the rectangle."""
        self.position=coordonnates[:2]
        self.size=coordonnates[2:]

    def getRect(self):
        """Return the rect of the rectangle."""
        return Rectangle.getRectFromCoordonnates(self.getCoordonnates)

    def setRect(self,rect):
        """Set the rect of the rectangle."""
        self.setCoordonnates(Rectangle.getCoordonnatesFromRect(rect))

    def getCenter(self):
        """Return the center of the rectangle."""
        return self.position

    def setCenter(self,centers):
        """Set the center of the rectangle."""
        self.position=center

    def getX(self):
        """Return the x component."""
        return self.position[0]

    def setX(self,x):
        """Set the x component."""
        self.position[0]=x

    def getY(self):
        """Return the y component."""
        return self.position[1]

    def setY(self,y):
        """Set the y component."""
        self.position[1]=y

    def getSx(self):
        """Return the size of the x component."""
        return self.size[0]

    def setSx(self,sx):
        """Set the size of the x component."""
        self.size[0]=sx

    def getSy(self):
        """Return the size of the y component."""
        return self.size[1]

    def setSy(self,sy):
        """Set the size of the y component."""
        self.size[1]=sy

    def getXmin(self):
        """Return the minimum of the x component."""
        return self.position[0]-self.size[0]/2

    def setXmin(self,xmin):
        """Set the minimum of the x component."""
        self.position[0]=xmin+self.size[0]/2

    def getYmin(self):
        """Return the minimum of the y component."""
        return self.position[1]-self.size[1]/2

    def setYmin(self,ymin):
        """Set the minimum of the y component."""
        self.position[1]=ymin+self.size[1]/2

    def getXmax(self):
        """Return the maximum of the x component."""
        return self.position[0]+self.size[0]/2

    def setXmax(self,xmax):
        """Set the maximum of the x component."""
        self.position[0]=xmax-self.size[0]/2

    def getYmax(self):
        """Return the maximum of the y component."""
        return self.position[1]+self.size[1]/2

    def setYmax(self,ymax):
        """Set the maximum of the y component."""
        self.position[1]=ymax-self.size[1]/2

    corners=property(getCorners,setCorners,"Allow the user to manipulate the corners as an attribute for simplicity.")
    rect=property(getRect,setRect,"Allow the user to manipulate the rect of the rectangle easily.")
    coordonnates=property(getCoordonnates,setCoordonnates,"Allow the user to manipulate the coordonnates of the rectangle easily for simplicity.")
    x=property(getX,setX,"Allow the user to manipulate the x component easily.")
    y=property(getY,setY,"Allow the user to manipulate the y component easily.")
    sx=property(getSx,setSx,"Allow the user to manipulate the size in x component easily.")
    sy=property(getSy,setSy,"Allow the user to manipulate the size in y component easily.")
    xmin=property(getXmin,setXmin,"Allow the user to manipulate the minimum of x component easily.")
    xmax=property(getXmax,setXmax,"Allow the user to manipulate the maximum of x component easily.")
    ymin=property(getYmin,setYmin,"Allow the user to manipulate the minimum of y component easily.")
    ymax=property(getYmax,setYmax,"Allow the user to manipulate the maximum of y component easily.")

    def getCornersFromCoordonnates(coordonnates):
        """Return the corners (top_left_corner,bottom_right_corner) using the coordonnates (position+size)."""
        """[x,y,sx,sy] -> [mx,my,Mx,My]"""
        x,y,sx,sy=coordonnates
        mx,my=x-sx/2,y-sy/2
        Mx,My=x+sx/2,y+sy/2
        corners=(mx,my,Mx,My)
        return corners

    def getCoordonnatesFromCorners(corners):
        """Return the coordonnates (position+size) using the corners (top_left_corner,bottom_right_corner)."""
        """[mx,my,Mx,My] -> [x,y,sx,sy]"""
        mx,my,Mx,My=corners
        sx,sy=Mx-mx,My-my
        x,y=mx+sx/2,my+sy/2
        coordonnates=(x,y,sx,sy)
        return coordonnates

    def getCoordonnatesFromRect(rect):
        """Return the coordonnates (position,size) using the rect (top_left_corner,size)."""
        """[x,y,sx,sy] -> [mx,my,sx,sy]"""
        mx,my,sx,sy=rect
        x,y=mx+sx/2,my+sy/2
        coordonnates=[x,y,sx,sy]
        return coordonnates

    def getRectFromCoordonnates(coordonnates):
        """Return the rect (top_left_corner,size) using the coordonnates (position,size)."""
        """[mx,my,sx,sy] -> [x,y,sx,sy]"""
        x,y,sx,sy=coordonnates
        mx,my=x-sx/2,y-sy/2
        rect=[mx,my,sx,sy]
        return rect

    def getRectFromCorners(corners):
        """Return the rect (top_left_corner,size) using the corners (top_left_corner,bottom_right_corner)."""
        """[mx,my,Mx,My] -> [mx,my,sx,sy]"""
        mx,my,Mx,My=corners
        sx,sy=Mx-mx,My-my
        rect=[mx,my,sx,sy]
        return rect

    def getCornersFromRect(rect):
        """Return the (top_left_corner,bottom_right_corner) using the corners rect (top_left_corner,size)."""
        """[mx,my,Mx,My] -> [mx,my,sx,sy]"""
        mx,my,sx,sy=rect
        Mx,My=mx+sx,my+sy
        corners=[mx,my,Mx,My]
        return corners

    def crossRect(self,other):
        """Determine the rectangle resulting of the intersection of two rectangles."""
        if self.xmax<other.xmin or self.xmin>other.xmax: return
        if self.ymax<other.ymin or self.ymin>other.ymax: return
        xmin=max(self.xmin,other.xmin)
        ymin=max(self.ymin,other.ymin)
        xmax=min(self.xmax,other.xmax)
        ymax=min(self.ymax,other.ymax)
        print([xmin,ymin,xmax,ymax])
        return Rect.createFromCorners([xmin,ymin,xmax,ymax])

    def resize(self,n=1):
        """Allow the user to resize the rectangle."""
        for i in range(2):
            self.size[i]*=n
