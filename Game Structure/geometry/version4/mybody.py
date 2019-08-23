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
    def random(corners=[-1,-1,1,1],n=5):
        """Create a random body."""
        form=Form.random(corners,n)
        motion=Motion.random(n=2,d=3)
        moment=Motion.random(n=2,d=3)
        print(motion.acceleration)
        return Body(form,motion,moment)

    def createFromAbsolute(form,motion=Motion(),moment=Motion(d=1)):
        """Create a body from an absolute form."""
        motion.position=Vector(*form.center)
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

    def showMotion(self,context):
        """show the motion of the body."""
        self.velocity.show(context,self.position)
        self.acceleration.show(context,self.position)

    def showMoment(self,context):
        """Show the moment of the body."""
        self.moment.show(context,self.position)

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

    absolute=property(getAbsolute,setAbsolute)

    def __contains__(self,point):
        """Determine if a point is in the body."""
        return point in self.absolute

    def react(self,event):
        """React to a given event by making an action."""
        pass

    def follow(self,point,speed=1/100):
        """Update the motion in order for a body to follow a given point."""
        v=Vector(*point)
        self.velocity=(v-self.position)/10
        if self.velocity.norm>1:
            self.velocity.norm=1


class PhysicalBody(Body):
    def __init__(self,form,motion=Motion(d=2),moment=Motion(d=1),mass=1):
        """Create body using form and optional name."""
        self.form=form
        self.motion=motion
        self.moment=moment
        self.mass=mass







if __name__=="__main__":
    from mysurface import Surface
    surface=Surface(fullscreen=True)
