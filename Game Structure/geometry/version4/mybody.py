from myabstract import Form,Vector,Point,Segment,Circle
from mymotion import Motion
from mymaterial import Material

from pygame.locals import *
import pygame
import logging
import copy
import mycolors

# Interface Anatomy
# - show(context)   //an anatomy must be responsible for drawing itself
# - str()           //an anatomy must be able to give a string representation
# - contains(point) //an anatomy must be able to tell if a point is in it
# - cross(anatomy)  //an anatomy must be able to determine if it is crossing another anatomy
# . center          //an anatomy must have a center

#image, segment and form implement anatomy

class Image(Rect):
    def __init__(self,filename):
        """Create an image."""
        self.surface=pygame.load.image(filename)
    def show(self,context):
        """"Show the image on the window."""
        self.context.draw.blit(self.surface)


class Body(Material):
    def createFromAbsolute(form,motion=Motion(),moment=Motion(d=1)):
        """Create a body from an absolute form."""
        motion.position=Vector(*form.center)
        print(motion.position)
        form.points=(-motion.position).applyToPoints(form.points)
        return Body(form,motion,moment)

    def __init__(self,form,motion=Motion(d=2),moment=Motion(d=1)):
        """Create body using form and optional name."""
        self.form=form
        self.motion=motion
        self.moment=moment

    def __str__(self):
        """Return the string representation of the body."""
        return "b("+str(self.form)+","+str(self.motion)+")"

    def show(self,context):
        """Show the form on the window."""
        self.absolute.show(context)

    def update(self,dt=1):
        """Move entity according to its acceleration, velocity and position."""
        self.motion.update(dt)
        self.moment.update(dt)

    def getAbsolute(self):
        """Return a copy of the form in absolute coordonnates."""
        p=Point(*tuple(copy.deepcopy(self.position)))
        f=copy.deepcopy(self.form)
        f.center=p
        f.rotate(self.moment.position[0])
        return f

    def setAbsolute(self,form):
        """Set the form of the body using the absolute form."""
        self.position=Vector(*form.center)
        p=Point(*tuple(copy.deepcopy(-self.position)))
        form.center=p
        self.form=form


    def __contains__(self,point):
        """Determine if a point is in the body."""
        return point in self.absolute

    def follow(self,point,speed=1/100):
        """Update the motion in order for a body to follow a given point."""
        v=Vector(*point)
        self.velocity=(v-self.position)/10
        if self.velocity.norm>1:
            self.velocity.norm=1

    absolute=property(getAbsolute,setAbsolute)



if __name__=="__main__":
    from mysurface import Surface
    surface=Surface(fullscreen=True)

    dt=1

    form=Form([Point(0,1),Point(0,0),Point(1,0),Point(1,1)],area_color=mycolors.BLUE,fill=True)
    #form=Circle(copy.deepcopy(Point.origin()),radius=1,fill=True,color=mycolors.BLUE)
    body=Body(form)
    missile=None

    def createRandomBody():
        form=5*Form.random(n=5)
        form.side_color=mycolors.RED
        form.area_color=mycolors.BLACK
        form.fill=True
        motion=Motion(10*Vector.random(),Vector.random(),Vector.null())
        moment=Motion(Vector([1]),Vector([0.1]))
        return Body(form,motion,moment)

    n=10
    bodies=[createRandomBody() for i in range(n)]



    while surface.open:
        #Surface
        surface.check()
        #surface.control()
        surface.clear()
        surface.show()
        surface.controlZoom()

        #Control
        body.control(surface,v=0.1)
        new_missile=body.shoot(surface)
        if new_missile is not None:
            missile=new_missile

        #Update
        for i in range(len(bodies)):
            #bodies[i].motion.velocity=copy.deepcopy(-bodies[i].motion.position/1000)
            bodies[i].follow(body.position)
            bodies[i].update(dt)
        body.update(dt)
        if missile is not None:
            missile.update(dt)


        if missile:
            for i in range(len(bodies)):
                p=bodies[i].absolute.crossSegment(missile.absolute)
                print(p)
                if len(p)>0:
                    bodies[i]=createRandomBody()



        #Show
        for body_ in bodies:
            body_.absolute.showAll(surface)
        body.show(surface)
        if missile is not None:
            missile.show(surface)
            missile.absolute.p2.show(surface,color=mycolors.ORANGE)


        surface.draw.plane.position=copy.deepcopy(body.position)
        if missile is not None:
            surface.draw.window.print(str(missile.velocity),(10,10),20)

        surface.flip()
