from myabstract import Form,Point,Segment
import random
import mycolors

class AbstractHandler:
    """Allow the user to manipulate forms easily."""
    def __init__(self,objects=[]):
        """Create an abstract handler using the forms."""
        self.objects=objects

    def show(self,surface):
        """Show the abstract handler on the surface."""
        surface.clear()
        surface.show()
        self.showObjects(surface)
        self.showCollisions(surface)

    def showCollisions(self,surface):
        """Show the collisions of all objects between themselves."""
        l=len(self.objects)
        for i in range(l):
            for j in range(i+1,l):
                if self.objects[i]|self.objects[j]:
                    self.objects[i].color=mycolors.RED
                    self.objects[j].color=mycolors.RED
                else:
                    self.objects[i].color=mycolors.WHITE
                    self.objects[j].color=mycolors.WHITE

    def showObjects(self,surface):
        """Show the objects on the surface."""
        for object in self.objects:
            object.show(surface)

    def update(self,surface):
        """Update the objects of the AbstractHandler."""
        #self.updatePanel()
        self.updateObjects(surface)

    def updateObjects(self,surface):
        """Update the objects of the AbstractHandler."""
        for object in self.objects:
            object.update(surface)

    def __call__(self,surface):
        """Main loop of the AbstractHandler."""
        while surface.open:
            surface.check()
            surface.control()
            self.show(surface)
            self.update(surface)
            surface.flip()


class RotatingForm(Form):
    def random(corners=[-1,-1,1,1],number=random.randint(1,10),**kwargs):
        """Create a random rotating form."""
        points=[Point.random(corners) for i in range(number)]
        form=RotatingForm(points,**kwargs)
        form.makeSparse()
        return form

    def update(self,surface):
        """Rotate the form."""
        self.rotate(0.01)

class RotatingSegment(Segment):
    def random(corners=[-1,-1,1,1],width=1,color=mycolors.WHITE):
        """Create a random segment."""
        p1=Point.random(corners)
        p2=Point.random(corners)
        return RotatingSegment(p1,p2,width,color)

    def update(self,surface):
        """Rotate the segment."""
        self.rotate(-0.01)




if __name__=="__main__":
    from mysurface import Surface
    surface=Surface(name="Abstract Handler")
    f1=RotatingForm.random()
    f2=RotatingForm.random([-5,0,5,5])
    s3=RotatingSegment.random()
    fs=[f1,f2,s3]
    a=AbstractHandler(fs)
    a(surface)
