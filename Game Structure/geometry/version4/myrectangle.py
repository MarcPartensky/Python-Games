from myabstract import Form,Point
from myrect import Rect
import mycolors


class Rectangle(Form,Rect):
    """Uses multiple inheritance in order to be a rectangle that can be displayed."""
    def createFromRect(rect,**kwargs):
        """Create a rectangle using a rect."""
        return Rectangle(rect.position,rect.size,**kwargs)

    def __init__(self,position,size,fill=False,point_mode=0,point_size=[0.01,0.01],point_radius=0.01,point_width=1,point_fill=False,side_width=1,color=None,point_color=mycolors.WHITE,side_color=mycolors.WHITE,area_color=mycolors.WHITE,cross_point_color=mycolors.WHITE,cross_point_radius=0.01,cross_point_mode=0,cross_point_width=1,cross_point_size=[0.1,0.1],point_show=True,side_show=True,area_show=False):
        """Create an abstract rectangle with coordonnates."""
        Rect.__init__(self,position,size)

        self.point_mode=point_mode
        self.point_size=point_size
        self.point_width=point_width
        self.point_radius=point_radius
        self.point_color=point_color or color
        self.point_show=point_show
        self.point_fill=point_fill

        self.side_width=side_width
        self.side_color=side_color or color
        self.side_show=side_show

        self.area_color=area_color or color
        self.area_show=area_show or fill

        self.cross_point_color=cross_point_color
        self.cross_point_radius=cross_point_radius
        self.cross_point_mode=cross_point_mode
        self.cross_point_width=cross_point_width
        self.cross_point_size=cross_point_size


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
    from mycontext import Surface
    surface=Surface(name="Rectangle Test")
    r1=Rectangle([0,0],[3,2],side_width=3,side_color=mycolors.BLUE,area_color=mycolors.WHITE,area_show=True)
    r2=Rectangle([-1,-1],[2,1],side_width=3,side_color=mycolors.BLUE,area_color=mycolors.WHITE,area_show=True)
    print(r1.size)
    while surface.open:
        surface.check()
        surface.control()
        surface.clear()
        surface.show()
        r1.position=surface.point()
        r1.show(surface)
        r2.show(surface)
        r1.center.show(surface,color=mycolors.RED,mode="cross")
        r=r1.crossRect(r2)
        if r:
            r=Rectangle.createFromRect(r,area_color=mycolors.GREEN,area_show=True,side_width=2,side_color=mycolors.RED)
            r.show(surface)
        surface.flip()
