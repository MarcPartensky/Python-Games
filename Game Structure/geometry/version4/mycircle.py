from myabstract import Point,Vector

import mycolors

class Circle:
    def random(corners=[-1,-1,1,1],fill=0,color=mycolors.WHITE,border_color=None,area_color=None,center_color=None,radius_color=None,radius_width=1,text_color=None,text_size=20):
        """Create a random circle."""
        point=Point.random(corners)
        radius=1
        return Circle.createFromPointAndRadius(point,radius,color,fill)

    def createFromPointAndRadius(point,radius,fill=0,color=mycolors.WHITE,border_color=None,area_color=None,center_color=None,radius_color=None,radius_width=1,text_color=None,text_size=20):
        """Create a circle from point."""
        x,y=point
        return Circle(x,y,radius,color,fill)

    def __init__(self,x,y,radius=1,fill=0,color=mycolors.WHITE,border_color=None,area_color=None,center_color=None,radius_color=None,radius_width=1,text_color=None,text_size=20):
        """Create a circle object using x, y and radius and optional color and width."""
        self.x=x
        self.y=y
        self.radius=radius
        self.fill=fill
        if color:
            if not border_color: border_color=color
            if not area_color: area_color=color
            if not radius_color: radius_color=color
            if not text_color: text_color=color
        self.border_color=border_color
        self.area_color=area_color
        self.center_color=center_color
        self.radius_color=radius_color
        self.radius_width=radius_width
        self.text_color=text_color
        self.text_size=text_size

    def setPosition(self,x,y):
        """Set the position of the circle."""
        self.x=x
        self.y=y

    def center(self):
        """Return the point that correspond to the center of the circle."""
        return Point(self.x,self.y)

    def show(self,window,color=None,border_color=None,area_color=None,fill=None):
        """Show the circle on screen using the window."""
        if color:
            if not area_color: area_color=color
            if not border_color: border_color=color
        if not border_color: border_color=self.border_color
        if not area_color: area_color=self.area_color
        if not fill: fill=self.fill
        if fill: window.draw.circle(window.screen,area_color,[self.x,self.y],self.radius,True)
        window.draw.circle(window.screen,border_color,[self.x,self.y],self.radius)

    def showCenter(self,window,color=None,mode=None):
        """Show the center of the screen."""
        if not color: color=self.center_color
        if not mode: mode=self.center_mode
        self.center().show(window,mode=mode,color=color)

    def showText(self,window,text,color=None,size=None):
        """Show a text next to the circle."""
        if not color: color=self.text_color
        if not size: size=self.text_size
        self.center().showText(window,text,color=color,size=size)

    def showRadius(self,window,color=None,width=None):
        """Show the radius of the circle."""
        if not color: color=self.radius_color
        if not width: width=self.radius_width
        vector=Vector.createFromPolarCoordonnates(self.radius,0,color=color)
        vector.show(window,self.center(),width=width)
        vector.showText(surface,self.center(),"radius",size=20)


    def __call__(self):
        """Return all coordonnates of the circle."""
        return [self.x,self.y,self.radius]

    def crossCircle(self,other):
        """Determine if two circles are crossing."""
        vector=Vector.createFromTwoPoints(self.center(),other.center())
        return vector.norm()<self.radius+other.radius

if __name__=="__main__":
    from mysurface import Surface
    from myzone import Zone
    from mywindow import Window

    surface=Surface(plane=Zone(),window=Window())
    c1=Circle(4,2,2,color=mycolors.BLUE)
    c2=Circle(1,2,1,color=mycolors.BLUE)

    cs=[Circle.random(-10,10,color=mycolors.random()) for i in range(10)]

    fill=False
    c1_border_color=mycolors.random()
    c2_border_color=mycolors.random()
    c1_area_color=mycolors.random()
    c2_area_color=mycolors.random()

    while surface.open:
        surface.check()
        surface.control()
        surface.clear()
        surface.show()

        x,y=surface.point()
        c1.setPosition(x,y)
        if c1.crossCircle(c2):
            fill=False
            c1_border_color=mycolors.random()
            c2_border_color=mycolors.random()
        else:
            fill=True
            c1_area_color=mycolors.random()
            c2_area_color=mycolors.random()

        vector=Vector.createFromTwoPoints(c1.center(),c2.center())
        vector.show(surface,c1.center(),color=mycolors.GREEN)

        c1.show(surface,border_color=c1_border_color,area_color=c1_area_color,fill=fill)
        c1.showText(surface,"C1")
        c1.showRadius(surface)

        c2.show(surface,border_color=c2_border_color,area_color=c2_area_color,fill=fill)
        c2.showText(surface,"C2")
        c1.showRadius(surface)

        for c in cs:
            c.show(surface)

        surface.flip()
