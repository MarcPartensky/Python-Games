from mysurface import Surface
from mymaterialpoint import MaterialPoint
from myabstract import Form,Point,Vector
from mymotion import Motion
from myforce import Force

import mymaterialpoint
import myforce
import mycolors

class MaterialForm:
    def random(number=5,min=-1,max=1):
        """Create a random material form."""
        points=[MaterialPoint.random(min,max) for n in range(number)]
        return MaterialForm(points)

    def createFromForm(form,forces=[]):
        """Create a material form using a Form instance."""
        material_points=[MaterialPoint.createFromPoint(point,forces) for point in form.getPoints()]
        return MaterialForm(material_points)


    def __init__(self,points,fill=False,point_mode=0,point_radius=0.01,point_width=2,side_width=1,point_color=mycolors.WHITE,side_color=mycolors.WHITE,area_color=mycolors.WHITE):
        """Create a material form."""
        self.points=points
        self.point_mode=point_mode
        self.point_radius=point_radius
        self.point_width=point_width
        self.side_width=side_width
        self.fill=fill
        self.area_color=area_color
        self.point_color=point_color
        self.side_color=side_color

    def getPointFromMaterialPoint(self,material_point):
        """Change the type of an instance of MaterialPoint into a Point type using material_point."""
        position=material_point.getPosition()
        x,y=position
        return Point(x,y)


    def getForm(self,point_mode=None,point_radius=None,point_width=None,side_width=None,fill=None,area_color=None,point_color=None,side_color=None):
        """Return the object under a Form type by conversion."""
        if not point_mode: point_mode=self.point_mode
        if not point_radius: point_radius=self.point_radius
        if not point_width: point_width=self.point_width
        if not side_width: side_width=self.side_width
        if not fill: fill=self.fill
        if not area_color: area_color=self.area_color
        if not point_color: point_color=self.point_color
        if not side_color: side_color=self.side_color
        points=[self.getPointFromMaterialPoint(point) for point in self.points]
        form=Form(points,fill,point_mode,point_radius,point_width,side_width,point_color,side_color,area_color)
        return form

    def getPosition(self):
        """Return the position of the center of the material form."""
        form=self.getForm()
        return form.center()

    def getMotion(self):
        """Return the motion of the object."""
        return Motion.sum([motion for motion in self.points.getMotion()])

    def getMaterialPoints(self):
        """Return the material points of the form."""
        return self.points

    def setMaterialPoints(self,points):
        """Set the material points of the form."""
        self.points=points


    def show(self,window):
        """Show the form on the window."""
        form=self.getForm()
        form.show(window)

    def update(self):
        """Update the form by updating all its points."""
        for point in self.points:
            point.update()


    def getMass(self):
        """Calculate the mass of the form using its area and the mass of the material_points that define it."""
        """The way used to calculate it is arbitrary and should be improved."""
        form=self.getForm()
        mass=sum([point.getMass() for point in self.points])
        mass*=form.area()
        return mass

    def __getitem__(self,index):
        """Return the material point of number 'index'."""
        return self.points[index]

    def __setitem__(self,index,point):
        """Return the material point of number 'index'."""
        self.points[index]=point

    def showMotion(self,surface):
        """Show the motion on a surface."""
        form=self.getForm()
        center=form.center()
        x,y=center
        point_motion=Motion()
        for point in self.points:
            point_motion+=point.getMotion()
        material_center=MaterialPoint(point_motion)
        material_center.showMotion(surface)







FallingForm=lambda:MaterialForm([mymaterialpoint.FallingPoint() for i in range(5)])

if __name__=="__main__":
    surface=Surface()
    form=Form.random()
    form=MaterialForm.createFromForm(form,[Force(0.001,0),Force(0,0.001)])
    print(form[0].forces)
    print(form.getMass())
    while surface.open:
        surface.check()
        surface.clear()
        surface.control()
        surface.show()
        form.update()
        surface.draw.window.print("form.motion:"+str(form.getPosition()),(10,10))
        form.show(surface)
        form.showMotion(surface)
        surface.flip()
