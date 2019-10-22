from myabstract import Form, Vector, Point, Segment, Circle
from mymotion import Motion
from mymaterial import Material
from myphysics import Physics

from pygame.locals import *
from copy import deepcopy
import pygame
import logging
import copy
import mycolors
import random

# Interface Anatomy
# - show(context)   //an anatomy must be responsible for drawing itself
# - str()           //an anatomy must be able to give a string representation
# - contains(point) //an anatomy must be able to tell if a point is in it
# - cross(anatomy)  //an anatomy must be able to determine if it is crossing another anatomy
# . center          //an anatomy must have a center

# image, segment and form implement anatomy


class Image(Rect):
    def __init__(self, filename):
        """Create an image."""
        self.surface = pygame.load.image(filename)

    def show(self, context):
        """"Show the image on the window."""
        self.context.draw.blit(self.surface)


class Body(Material):
    def random(corners=[-1, -1, 1, 1], n=5):
        """Create a random body."""
        form = Form.random(corners, n)
        motion = Motion.random(n=2, d=3)
        moment = Motion.random(n=2, d=3)
        print(motion.acceleration)
        return Body(form, motion, moment)

    def createFromAbsolute(form, motion=Motion(), moment=Motion(d=1)):
        """Create a body from an absolute form using its motion and its angular moment."""
        motion.position = Vector(*form.center)
        form.points = (-motion.position).applyToPoints(form.points)
        return Body(form, motion, moment)

    def __init__(self, form, motion=Motion(d=2), moment=Motion(d=1)):
        """Create body using its anatomy, its motion and its angular moment.
        #Attributes:
        #self.form,self.motion,self.moment
        #Properties:
        #self.absolute"""
        self.form = form
        self.motion = motion
        self.moment = moment

    def __str__(self):
        """Return the string representation of the body."""
        return "b(" + str(self.form) + "," + str(self.motion) + ")"

    def show(self, context):
        """Show the form on the window."""
        self.absolute.show(context)

    def showMotion(self, context):
        """show the motion of the body."""
        self.velocity.show(context, self.position)
        self.acceleration.show(context, self.position)

    def showMoment(self, context):
        """Show the moment of the body."""
        self.moment.show(context, self.position)

    def update(self, dt=1):
        """Move entity according to its acceleration, velocity and position."""
        self.motion.update(dt)
        self.moment.update(dt)

    def getAbsolute(self):
        """Return a copy of the form in absolute coordonnates."""
        p = Point(*tuple(copy.deepcopy(self.position)))
        f = copy.deepcopy(self.form)
        f.center = p
        f.rotate(self.moment.position[0])
        return f

    def setAbsolute(self, form):
        """Set the form of the body using the absolute form."""
        self.position = Vector(*form.center)
        p = Point(*tuple(copy.deepcopy(-self.position)))
        form.center = p
        self.form = form

    absolute = property(getAbsolute, setAbsolute)

    def __contains__(self, point):
        """Determine if a point is in the body."""
        return point in self.absolute

    def react(self, event):
        """React to a given event by making an action."""
        pass

    def follow(self, point, speed=1 / 100):
        """Update the motion in order for a body to follow a given point."""
        v = Vector(*point)
        self.velocity = (v - self.position) / 10
        if self.velocity.norm > 1:
            self.velocity.norm = 1


class PhysicalBody(Physics, Body):

    def createFromAbsolute(form, motion=Motion(), moment=Motion(d=1)):
        """Create a body from an absolute form using its motion and its angular moment."""
        motion.position = Vector(*form.center)
        form.points = (-motion.position).applyToPoints(form.points)
        return PhysicalBody(anatomy, motions)

    def __init__(self, anatomy, motions=[Motion(n=3, d=2), Motion(n=2, d=1)], mass=1):
        """Create body using form and optional name."""
        Physics.__init__(motions, mass)
        self.anatomy = anatomy

    def __str__(self):
        """Return the string representation of a physical body."""
        return "phb" + super().__str__()

    def centrate(self):
        """Centrate the anatomy."""
        pass

    def goto(self, position):
        """Orientate the velocity to get to a position."""
        v = position - self.position
        self.velocity.angle = v.angle


class NewBody(Physics):
    """
    A simple body is composed of its motion and its anatomy.
    An atomy must have:
    - the following attributes:
        - position
    - the following methods:
        - show
        - rotate
    """

    @classmethod
    def createFromAbsolute(cls, absolute, motion):
        """Create a simple body from its absolute anatomy and its motion."""
        return cls(anatomy, motion)

    @classmethod
    def random(cls,nm=1,nv=2,d=2):
        """Return a random simple body."""
        # The implemenation of the motion is not rigorous but this is pratical
        #motions = [Motion([Vector.random() for iv in range(nv)]) for im in range(nm)]
        motions = [Motion.random(n=nv,d=d) for im in range(nm)]
        anatomy = Form.random(n=5)
        # By default a random anatomy is a form
        # because the forms implements the interface anatomy.
        return cls(anatomy, motions)

    def __init__(self,  anatomy, motions):
        """Create a simple body."""
        self.motions = motions
        self.anatomy = anatomy
        self.center()

    def __str__(self):
        """Return the string representation of the body."""
        return "b(" + str(self.anatomy) + "," + str(",".join(map(str,self.motions))) + ")"

    def center(self):
        """Center the anatomy."""
        c=self.anatomy.center
        v=-Vector(*c)
        self.anatomy.position=v

    def show(self, context):
        """Show the simple body on the context."""
        self.showAbsolute(context)
        self.showMotion(context)

    def showAnatomy(self, context):
        """Show the anatomy on the context."""
        self.anatomy.show(context)

    def showAbsolute(self, context):
        """Show the body on the context."""
        self.getAbsolute().show(context)

    def showMotion(self, context):
        """Show the motion of the body on the context."""
        self.velocity.show(context,self.position)
        self.acceleration.show(context,self.position)

    def update(self, dt=1):
        """Update the simple body."""
        self.motion.update(dt)

    def follow(self, position):
        """Follow the cursor."""
        a=Vector(*position)
        b=self.position
        v=Vector(a-b)
        self.velocity.angle=v.angle
        #self.velocity.norm=min(v.norm,1)

    def __contains__(self, other):
        """Determine if the object other is in the absolute anatomy."""
        return other in self.getAbsolute()

    def getAbsolute(self):
        """Return the absolute anatomy of the body which means its form after
        changing the position depending on its motion."""
        anatomy = deepcopy(self.anatomy)
        anatomy.position=self.motion.position  # change its position
        anatomy.rotate(self.velocity.angle)  # change its rotation
        return anatomy

    absolute = property(getAbsolute)


class MaterialBody(Material):
    """Unlike the other bodies, the material body only has one motion."""
    def __init__(self,anatomy,motion):
        """Create a material body from its anatomy and its motion."""
        self.anatomy = anatomy
        self.motion = motion

    @classmethod
    def createFromAbsolute(cls, absolute, motion):
        """Create a simple body from its absolute anatomy and its motion."""
        return cls(anatomy, motion)

    @classmethod
    def random(cls,nv=2,d=2):
        """Return a random simple body."""
        motion = Motion.random(n=nv,d=d)
        anatomy = Form.random(n=5)
        return cls(anatomy, motion)

    def __init__(self,  anatomy, motion):
        """Create a simple body."""
        self.motion = motion
        self.anatomy = anatomy
        self.center()

    def __str__(self):
        """Return the string representation of the body."""
        return "b(" + str(self.anatomy) + "," + str(",".join(map(str,self.motions))) + ")"

    def center(self):
        """Center the anatomy."""
        c=self.anatomy.center
        v=-Vector(*c)
        self.anatomy.position.set(v)

    def show(self, context):
        """Show the simple body on the context."""
        self.showAbsolute(context)
        self.showMotion(context)

    def showAnatomy(self, context):
        """Show the anatomy on the context."""
        self.anatomy.show(context)

    def showAbsolute(self, context):
        """Show the body on the context."""
        self.getAbsolute().show(context)

    def showMotion(self, context):
        """Show the motion of the body on the context."""
        self.velocity.show(context,self.position)
        self.acceleration.show(context,self.position)

    def update(self, dt=1):
        """Update the simple body."""
        self.motion.update(dt)

    def follow(self, position):
        """Follow the cursor."""
        a=Vector(*position)
        b=self.position
        v=Vector(a-b)
        self.velocity.angle=v.angle
        #self.velocity.norm=min(v.norm,1)

    def __contains__(self, other):
        """Determine if the object other is in the absolute anatomy."""
        return other in self.getAbsolute()

    def getAbsolute(self):
        """Return the absolute anatomy of the body which means its form after
        changing the position depending on its motion."""
        anatomy = deepcopy(self.anatomy)
        anatomy.position=self.motion.position  # change its position
        anatomy.rotate(self.velocity.angle)  # change its rotation
        return anatomy

    absolute = property(getAbsolute)


if __name__ == "__main__":
    from mycontext import Context
    context = Context(fullscreen=False)
    ru = random.uniform
    form1 = Form.random(n=4)
    motion1 = Motion(Vector(0, 0), Vector(ru(-1, 1), ru(-1, 1)), Vector(0, 0))
    moment1 = Motion(Vector([0]), Vector([ru(-1, 1)]), Vector([0]))
    b1 = Body(form1, motion1, moment1)
    # b=Body.random()
    while context.open:
        context.check()
        context.clear()
        context.show()
        context.control()
        b1.show(context)
        b1.update(0.1)
        context.flip()
