from myabstract import Form,Point
from myrect import Rect
import mycolors


class Rectangle(Rect,Form):
    """Uses multiple inheritance in order to be a rectangle that can be displayed."""

    @classmethod
    def cross(cls,r1,r2):
        """Return Rectangle of the intersection of the rectangles r1 and r2."""
        if isinstance(r1,cls) and isinstance(r2,cls):
            r=Rect.cross(r1,r2)
            if r: return cls.createFromRect(r)
        elif isinstance(r1,Form) and isinstance(r2,Form):
            return Form.cross(r1,r2)

    @classmethod
    def random(cls,borns=[-1,1],size_borns=[0,1],**kwargs):
        """Create a random rectangle."""
        rect=Rect.random(borns,size_borns)
        return cls.createFromRect(rect,**kwargs)

    @classmethod
    def createFromRect(cls,rect,**kwargs):
        """Create a rectangle using a rect."""
        return cls(rect.position,rect.size,**kwargs)

    def __init__(self,position,
                    size,
                    fill=False,
                    point_mode=0,
                    point_size=[0.01,0.01],
                    point_radius=0.01,
                    point_width=1,
                    point_fill=False,
                    side_width=1,
                    color=None,
                    point_color=mycolors.WHITE,
                    side_color=mycolors.WHITE,
                    area_color=mycolors.WHITE,
                    cross_point_color=mycolors.WHITE,
                    cross_point_radius=0.01,
                    cross_point_mode=0,
                    cross_point_width=1,
                    cross_point_size=[0.1,0.1],
                    point_show=True,
                    side_show=True,
                    area_show=False):
        """Create an abstract rectangle with coordinates."""
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
        xmin,ymin,xmax,ymax=self.corners
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
        self.corners=[xmin,ymin,xmax,ymax]

    points=property(getPoints,setPoints,"Allow the user to manipulate the points of the rectangle.")

class Square(Rectangle):
    """Create a square that unherits from rectangle."""
    def __init__(self,position,length,**kwargs):
        size=(length,length)
        super().__init__(position,size,**kwargs)


if __name__=="__main__":
    from mycontext import Context
    from myabstract import Point
    context=Context(name="Rectangle Test")
    p=Point.random(radius=0.5)
    r1=Rectangle([0,0],[3,2],side_width=3,side_color=mycolors.BLUE,area_color=mycolors.WHITE,area_show=True)
    r2=Square([-1,-1],2,side_width=3,side_color=mycolors.BLUE,area_color=mycolors.WHITE,area_show=True)
    while context:
        context.check()
        context.control()
        context.clear()
        context.show()
        r1.position=context.point()
        if p in r1:
            r1.side_color=mycolors.YELLOW
        else:
            r1.side_color=mycolors.WHITE
        r1.show(context)
        r2.show(context)
        r1.center.show(context,color=mycolors.RED,mode="cross")
        r=Rectangle.cross(r1,r2)
        if r:
            r=Rectangle.createFromRect(r,area_color=mycolors.GREEN,area_show=True,side_width=2,side_color=mycolors.RED)
            r.show(context)
        if p in r1:
            p.show(context)
            context.console("inside")
        context.flip()
