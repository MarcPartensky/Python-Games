from mysurface import Surface
from mymaterialpoint import MaterialPoint
from myform import Form
from mypoint import Point

import mymaterialpoint

class MaterialForm:
    def random(number=5,min=-1,max=1):
        """Create a random material form."""
        points=[MaterialPoint.random(min,max) for n in range(number)]
        return MaterialForm(points)

    def createFromForm(form):
        """Create a material form using a Form instance."""
        material_points=[MaterialPoint.createFromPoint(point) for point in form.getPoints()]
        return MaterialForm(material_points)


    def __init__(self,points):
        """Create a material form."""
        self.points=points

    def getPointFromMaterialPoint(self,material_point):
        """Change the type of an instance of MaterialPoint into a Point type using material_point."""
        position=material_point.getPosition()
        x,y=position
        return Point(x,y)


    def getForm(self):
        """Return the object under a Form type by conversion."""
        points=[self.getPointFromMaterialPoint(point) for point in self.points]
        form=Form(points)
        return form

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
        mass=sum([point.mass for point in self.points])
        mass*=form.area
        return mass



FallingForm=lambda:MaterialForm([mymaterialpoint.FallingPoint() for i in range(5)])

if __name__=="__main__":
    surface=Surface()
    #form=MaterialForm.random()
    form=FallingForm()
    print(form.getMass())
    while surface.open:
        surface.check()
        surface.clear()
        surface.control()
        surface.show()
        form.update()
        form.show(surface)
        surface.flip()
