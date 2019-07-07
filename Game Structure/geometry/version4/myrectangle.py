from myabstract import Form,Point
from myrect import Rect
import mycolors


class Rectangle(Form,Rect):
    """Uses multiple inheritance in order to be a rectangle that can be displayed."""
    def createFromRect(rect):
        """Create a rectangle using a rect."""
        return Rectangle(rect.position,rect.size)

    def __init__(self,position,size,fill=False,point_mode=0,point_radius=0.01,point_width=1,side_width=1,color=None,point_color=mycolors.WHITE,side_color=mycolors.WHITE,area_color=mycolors.WHITE,point_show=True,side_show=True):
        """Create an abstract rectangle."""
        Rect.__init__(self,position,size)
        self.side_width=side_width
        if color: self.point_color=self.side_color=self.area_color=color
        self.point_radius=point_radius
        self.point_color=point_color
        self.side_color=side_color
        self.area_color=area_color
        self.point_show=point_show
        self.side_show=side_show
        self.fill=fill

    def getPoints(self):
        """Return the points that correspond to the extremities of the rectangle."""
        xmin,ymin,xmax,ymax=self.getCorners()
        p1=Point(xmin,ymin)
        p2=Point(xmax,ymin)
        p3=Point(xmax,ymax)
        p4=Point(xmin,ymax)
        return [p1,p2,p3,p4]

    def setPoints(self,points):
        """Set the points that correspond to the extremities of the rectangle."""
        xmin=min([p.x for p in points])
        xmax=max([p.x for p in points])
        ymin=min([p.y for p in points])
        ymax=max([p.y for p in points])
        corners=[xmin,ymin,xmax,ymax]
        coordonnates=self.getCoordonnatesFromCorners(corners)
        self.position=coordonnates[:2]
        self.size=coordonnates[2:]

    points=property(getPoints,setPoints,"Allow the user to manipulate the points of the rectangle.")

if __name__=="__main__":
    from mysurface import Surface
    surface=Surface(name="Rectangle Test")
    r1=Rectangle([0,0],[3,2],side_color=mycolors.BLUE)
    r2=Rectangle([-1,-1],[2,1],side_color=mycolors.BLUE)
    print(r1.size)
    while surface.open:
        surface.check()
        surface.control()
        surface.clear()
        surface.show()
        r1.position=surface.point()
        r1.show(surface,fill=True)
        r2.show(surface,fill=True)
        r1.center.show(surface,color=mycolors.RED,mode="cross")
        r=r1.crossRect(r2)
        if r:
            r=Rectangle.createFromRect(r)
            r.show(surface,color=mycolors.GREEN,fill=True)
        surface.flip()
