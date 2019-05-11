from mymaterialform import MaterialForm
from myabstract import Point,Form

import math

class MaterialFormHandler:
    def __init__(self,material_forms):
        """Create material form collider object."""
        self.forms=material_forms

    def update(self,t):
        """Update the forms and deal with its collisions."""
        for form in self.forms:
            form.update(t)

    def rotate(self,angle=math.pi/2,point=[0,0]):
        """Rotate the forms using an angle and a point."""
        for form in self.forms:
            form.rotate(angle,point)


    def collide(self,object1,object2):
        """Deal with the collisions of two objects 'object1' and 'object2'."""
        #I've got no clue how to do such a thing
        #I just know that i need the motions of the forms, the coordonnates of its points and their masses.
        ap1=object1.getPoints()
        bp1=[p1.getNext() for p1 in ap1]
        ls1=[Segment(a1,b1) for (a1,b1) in zip(ap1,bp1)]
        ap2=object2.getPoints()
        bp2=[p2.getNext() for p2 in ap2]
        ls2=[Segment(a2,b2) for (a2,b2) in zip(ap2,bp2)]
        points=[]
        for s1 in ls1:
            for s2 in ls2:
                point=s1|s2
                if point:
                    points.append(point)
        return points

    def show(self,surface):
        """Show the material forms on the surface."""
        for form in self.forms:
            form.show(surface)

if __name__=="__main__":
    from mysurface import Surface
    surface=Surface()
    ps1=[Point(0,0),Point(0,1),Point(1,1),Point(1,0)]
    f1=Form(ps1)
    f1=MaterialForm.createFromForm(f1)
    ps2=[Point(0,0),Point(0,2),Point(2,2),Point(2,0)]
    f2=Form(ps2)
    f2=MaterialForm.createFromForm(f2)
    forms=[f1,f2]
    handler=MaterialFormHandler(forms)

    while surface.open:
        surface.check()
        surface.control()
        surface.clear()
        surface.show()
        handler.update(0.1)
        handler.rotate(0.1)
        handler.show(surface)
        surface.flip()
