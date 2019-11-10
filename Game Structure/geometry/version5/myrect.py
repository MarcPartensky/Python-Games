import random

class Rect:
    """Define a pure and simple rectangle."""

    @classmethod
    def cross(cls,r1,r2):
        """Determine the rectangle resulting of the intersection of two rectangles."""
        if r1.xmax<r2.xmin or r1.xmin>r2.xmax: return
        if r1.ymax<r2.ymin or r1.ymin>r2.ymax: return
        xmin=max(r1.xmin,r2.xmin)
        ymin=max(r1.ymin,r2.ymin)
        xmax=min(r1.xmax,r2.xmax)
        ymax=min(r1.ymax,r2.ymax)
        return Rect.createFromCorners([xmin,ymin,xmax,ymax])

    @classmethod
    def random(cls,borns=[-1,1],borns_size=[0,1]):
        """Create a random rect."""
        x=random.uniform(*borns)
        y=random.uniform(*borns)
        sx=random.uniform(*borns_size)
        sy=random.uniform(*borns_size)
        return cls((x,y),(sx,sy))

    @classmethod
    def createFromCorners(cls,corners):
        """Create a rectangle."""
        coordinates=Rect.getCoordinatesFromCorners(corners)
        return cls(coordinates[:2],coordinates[2:])

    @classmethod
    def createFromRect(cls,rect):
        """Create a rect from a pygame rect."""
        coordinates=Rect.getCoordinatesFromRect(rect)
        return cls(coordinates[:2],coordinates[2:])

    @classmethod
    def createFromCoordinates(cls,coordinates):
        """Create a rect using the coordinates."""
        return cls(coordinates[:2],coordinates[2:])

    def __init__(self,position,size):
        """Create a rectangle using its position and size."""
        self.position=list(position)
        self.size=list(size)

    def __str__(self,n=2):
        """Return the string representation of a rect."""
        r=round(self,n)
        return "Rect(pos="+str(r.position)+",size="+str(r.size)+")"

    def __round__(self,n=2):
        """Round the components of the rect."""
        x=round(self.x,n)
        y=round(self.y,n)
        sx=round(self.sx,n)
        sy=round(self.sy,n)
        return Rect([x,y],[sx,sy])

    def __contains__(self,position):
        """Determine if a position is in the rectangle."""
        x,y=position
        return (self.xmin<=x<=self.xmax) and (self.ymin<=y<=self.ymax)

    # def cross(self,other):
    #     """Determine the rectangle resulting of the intersection of two rectangles."""
    #     if self.xmax<other.xmin or self.xmin>other.xmax: return
    #     if self.ymax<other.ymin or self.ymin>other.ymax: return
    #     xmin=max(self.xmin,other.xmin)
    #     ymin=max(self.ymin,other.ymin)
    #     xmax=min(self.xmax,other.xmax)
    #     ymax=min(self.ymax,other.ymax)
    #     return Rect.createFromCorners([xmin,ymin,xmax,ymax])

    def resize(self,n=1):
        """Allow the user to resize the rectangle."""
        for i in range(2):
            self.size[i]*=n

    #properties
    #corners
    def getCorners(self):
        """Return the corners of the case."""
        px,py=self.position
        sx,sy=self.size
        return (px-sx/2,py-sy/2,px+sx/2,py+sy/2)

    def setCorners(self):
        """Set the corners of the case."""
        coordinates=self.getCoordinatesFromCorners(corners)
        self.position=coordinates[:2]
        self.size=coordinates[2:]

    #coordinates
    def getCoordinates(self):
        """Return the coordinates ofthe rectangle."""
        return self.position+self.size

    def setCoordinates(self,coordinates):
        """Set the coordinates of the rectangle."""
        self.position=coordinates[:2]
        self.size=coordinates[2:]

    #rect
    def getRect(self):
        """Return the rect of the rectangle."""
        return Rect.getRectFromCoordinates(self.getCoordinates())

    def setRect(self,rect):
        """Set the rect of the rectangle."""
        self.setCoordinates(Rect.getCoordinatesFromRect(rect))


    #center
    def getCenter(self):
        """Return the center of the rectangle."""
        return self.position

    def setCenter(self,centers):
        """Set the center of the rectangle."""
        self.position=center

    #x component
    def getX(self):
        """Return the x component."""
        return self.position[0]

    def setX(self,x):
        """Set the x component."""
        self.position[0]=x

    #y component
    def getY(self):
        """Return the y component."""
        return self.position[1]

    def setY(self,y):
        """Set the y component."""
        self.position[1]=y

    #sx component
    def getSx(self):
        """Return the width."""
        return self.size[0]

    def setSx(self,sx):
        """Set the width."""
        self.size[0]=sx

    #sy component
    def getSy(self):
        """Return the height."""
        return self.size[1]

    def setSy(self,sy):
        """Set the height."""
        self.size[1]=sy

    #xmin component
    def getXmin(self):
        """Return the minimum of the x component."""
        return self.position[0]-self.size[0]/2

    def setXmin(self,xmin):
        """Set the minimum of the x component."""
        self.position[0]=xmin+self.size[0]/2

    #ymin component
    def getYmin(self):
        """Return the minimum of the y component."""
        return self.position[1]-self.size[1]/2

    def setYmin(self,ymin):
        """Set the minimum of the y component."""
        self.position[1]=ymin+self.size[1]/2

    #xmax component
    def getXmax(self):
        """Return the maximum of the x component."""
        return self.position[0]+self.size[0]/2

    def setXmax(self,xmax):
        """Set the maximum of the x component."""
        self.position[0]=xmax-self.size[0]/2

    #ymax component
    def getYmax(self):
        """Return the maximum of the y component."""
        return self.position[1]+self.size[1]/2

    def setYmax(self,ymax):
        """Set the maximum of the y component."""
        self.position[1]=ymax-self.size[1]/2

    corners=property(getCorners,setCorners,"Allow the user to manipulate the corners as an attribute for simplicity.")
    rect=property(getRect,setRect,"Allow the user to manipulate the rect of the rectangle easily.")
    coordinates=property(getCoordinates,setCoordinates,"Allow the user to manipulate the coordinates of the rectangle easily for simplicity.")
    x=property(getX,setX,"Allow the user to manipulate the x component easily.")
    y=property(getY,setY,"Allow the user to manipulate the y component easily.")
    sx=width=property(getSx,setSx,"Allow the user to manipulate the size in x component easily.")
    sy=height=property(getSy,setSy,"Allow the user to manipulate the size in y component easily.")
    xmin=property(getXmin,setXmin,"Allow the user to manipulate the minimum of x component easily.")
    xmax=property(getXmax,setXmax,"Allow the user to manipulate the maximum of x component easily.")
    ymin=property(getYmin,setYmin,"Allow the user to manipulate the minimum of y component easily.")
    ymax=property(getYmax,setYmax,"Allow the user to manipulate the maximum of y component easily.")

    def getCornersFromCoordinates(coordinates):
        """Return the corners (top_left_corner,bottom_right_corner) using the coordinates (position+size)."""
        """[x,y,sx,sy] -> [mx,my,Mx,My]"""
        x,y,sx,sy=coordinates
        mx,my=x-sx/2,y-sy/2
        Mx,My=x+sx/2,y+sy/2
        corners=(mx,my,Mx,My)
        return corners

    def getCoordinatesFromCorners(corners):
        """Return the coordinates (position+size) using the corners (top_left_corner,bottom_right_corner)."""
        """[mx,my,Mx,My] -> [x,y,sx,sy]"""
        mx,my,Mx,My=corners
        sx,sy=Mx-mx,My-my
        x,y=mx+sx/2,my+sy/2
        coordinates=(x,y,sx,sy)
        return coordinates

    def getCoordinatesFromRect(rect):
        """Return the coordinates (position,size) using the rect (top_left_corner,size)."""
        """[x,y,sx,sy] -> [mx,my,sx,sy]"""
        mx,my,sx,sy=rect
        x,y=mx+sx/2,my+sy/2
        coordinates=[x,y,sx,sy]
        return coordinates

    def getRectFromCoordinates(coordinates):
        """Return the rect (top_left_corner,size) using the coordinates (position,size)."""
        """[mx,my,sx,sy] -> [x,y,sx,sy]"""
        x,y,sx,sy=coordinates
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


if __name__=="__main__":
    r1=Rect.random()
    r2=Rect.random()
    print(r1,r2)
    print(r1.corners)
    print(r1.coordinates)
    print(r1.rect)
    print(r1.x,r1.y)
    print(r1.sx,r1.sy)
    print(r1.width,r1.height)
    r=Rect.cross(r1,r2)
    print(r)
