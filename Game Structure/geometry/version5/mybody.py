from myabstract import Form, Vector, Point, Segment, Circle
from mymotion import Motion, Moment
from mymaterial import Material
from myphysics import Physics

from pygame.locals import *
from copy import deepcopy
import pygame
import logging
import copy
import mycolors
import random
import math

# Interface Anatomy
# - show(context)   //an anatomy must be responsible for drawing itself
# - __str__()           //an anatomy must be able to give a string representation
# - __contains__(point) //an anatomy must be able to tell if a point is in it
# - cross(anatomy)  //an anatomy must be able to determine if it is crossing another anatomy
# - recenter()
# - update()
# . center          //an anatomy must have a center

# image, segment and form implement anatomy


class Image(Rect):
    def __init__(self, filename):
        """Create an image."""
        self.surface = pygame.load.image(filename)

    def show(self, context):
        """"Show the image on the window."""
        self.context.draw.blit(self.surface)


class Body(Physics):

    @classmethod
    def random(cls, n=5, d=2, nm=2, nv=3, borns=[-1, 1]):
        """Create a random body."""
        anatomy = Form.random(n=n, d=d, borns=borns)
        anatomy.recenter()
        motions = []
        if nm >= 1:
            motions.append(Motion.random(n=nv, d=d))
        if nm >= 2:
            motions.append(Moment.random(n=nv, d=d))
        if nm >= 3:
            motions.extend([Motion.random(n=nv, d=d) for i in range(nm - 2)])
        return cls(anatomy, *motions)

    @classmethod
    def createFromForm(cls, anatomy, motion=Motion(), moment=Moment()):
        """Create a body from an absolute form using its motion and its angular moment."""
        motion.position = Vector(*anatomy.center)
        anatomy.points = (-motion.position).applyToPoints(anatomy.points)
        return cls(form, motion, moment)

    @classmethod
    def createFromMotionMoment(cls, anatomy, motion=Motion(), moment=Moment()):
        """Create a body from a relative anatomy, a motion and a moment."""
        return cls(form, [motion] + [moment])

    @classmethod
    def createFromRandomMotions(cls, anatomy, n=2):
        """Create a body using an anatomy and giving it 'n' random motions."""
        motions = []
        if n >= 1:
            motions.append(Motion.random())
        if n >= 2:
            motions.append(Moment.random())
        if n >= 3:
            motions.extend([Motion.random() for i in range(n - 2)])
        return cls(anatomy, *motions)

    def __init__(self, anatomy, *motions):
        """Create body using its anatomy, its motion and its angular moment."""
        self.anatomy = anatomy
        self.motions = list(motions)

    def __str__(self):
        """Return the string representation of the body."""
        return "b(" + str(self.form) + "," + ",".join(map(str, self.motions)) + ")"

    def show(self, context):
        """Show the form on the window."""
        self.form.show(context)

    def showMotion(self, context):
        """Show the motion of the body."""
        self.motion.show(context)

    def showMoment(self, context):
        """Show the moment of the body from its farthest point."""
        form = self.form
        position = self.position
        distances = [(Segment(p, position).length, p) for p in form.points]
        farthest = max(distances, key=lambda c: c[0])[1]
        angle = Vector.createFromTwoPoints(position, farthest).angle
        self.moment.show(context, farthest, angle)

    def showAll(self, context):
        """Show the body and its motions."""
        self.show(context)
        self.showMotion(context)
        self.showMoment(context)

    def update(self, dt=1):
        """Update the motions of the body using 'dt'."""
        for motion in self.motions:
            motion.update(dt)

    def updateFriction(self,friction=0.1):
        """Update the frictions of the body using the 'friction'."""
        for motion in self.motions:
            motion.velocity.norm*=(1-friction)

    def recenter(self):
        """Set the center of the relative anatomy on the origin."""
        c = self.anatomy.center
        v = -Vector(*c)
        self.anatomy.position.set(v)

    def getForm(self):
        """Return a copy of the form in absolute coordonnates."""
        form = copy.deepcopy(self.anatomy)
        form.points = self.motion.position.applyToPoints(form.points)
        if len(self.motions) == 1:  # Ugly fix for general case
            form.rotate(self.velocity.angle)
        else:
            form.rotate(self.moment.position.norm)
        return form

    def setForm(self, form):
        """Set the form of the body using the absolute form."""
        self.position.set(Vector(*form.center))
        self.anatomy = form.center

    form = absolute = property(getForm, setForm)

    def __contains__(self, point):
        """Determine if a point is in the body."""
        return point in self.form

    def react(self, event):
        """React to a given event by making an action."""
        pass

    def follow(self, point):
        """Update the motion in order for a body to follow a given point."""
        position = Vector(*point)
        v = position - self.position
        self.acceleration.set(v)

    def getCenter(self):
        """Return the center."""
        return Point(*self.position)

    def setCenter(self, center):
        """Set the new center."""
        self.position.set(Vector(*center))

    center = property(getCenter, setCenter)

    def cross(self, other):
        """Determine if the body is crossing with the other body."""
        return self.form.cross(other.form)

    def getBorn(self):
        """Return the born of the body."""
        c = self.anatomy.center
        lengths = [Segment(c, p).length for p in self.anatomy.points]
        return max(lengths)

    def setBorn(self, born):
        """Set the born of the body."""
        c = self.anatomy.center
        f = born / self.born
        for point in self.points:
            point *= f

    born = property(getBorn, setBorn)

    def getPoints(self):
        """Return the points of the form of the body."""
        return self.form.points

    def setPoints(self, points):
        """Set the points of the form of the body."""
        self.form.points = points

    points = property(getPoints, setPoints)

    def getCircle(self):
        """Return the circle that borns the body."""
        return Circle(*self.position, self.born)


class MaterialBody(Material):
    """Unlike the other bodies, the material body only has one motion."""

    def __init__(self, anatomy, motion):
        """Create a material body from its anatomy and its motion."""
        self.anatomy = anatomy
        self.motion = motion

    @classmethod
    def createFromAbsolute(cls, absolute, motion):
        """Create a simple body from its absolute anatomy and its motion."""
        return cls(anatomy, motion)

    @classmethod
    def random(cls, nv=2, d=2):
        """Return a random simple body."""
        motion = Motion.random(n=nv, d=d)
        anatomy = Form.random(n=5)
        return cls(anatomy, motion)

    def __init__(self,  anatomy, motion):
        """Create a simple body."""
        self.motion = motion
        self.anatomy = anatomy
        self.center()

    def __str__(self):
        """Return the string representation of the body."""
        return "b(" + str(self.anatomy) + "," + str(",".join(map(str, self.motions))) + ")"

    def center(self):
        """Center the anatomy."""
        c = self.anatomy.center
        v = -Vector(*c)
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
        self.velocity.show(context, self.position)
        self.acceleration.show(context, self.position)

    def update(self, dt=1):
        """Update the simple body."""
        self.motion.update(dt)

    def follow(self, position):
        """Follow the cursor."""
        a = Vector(*position)
        b = self.position
        v = Vector(a - b)
        self.velocity.angle = v.angle
        # self.velocity.norm=min(v.norm,1)

    def __contains__(self, other):
        """Determine if the object other is in the absolute anatomy."""
        return other in self.getAbsolute()

    def getAbsolute(self):
        """Return the absolute anatomy of the body which means its form after
        changing the position depending on its motion."""
        anatomy = deepcopy(self.anatomy)
        anatomy.position = self.motion.position  # change its position
        anatomy.rotate(self.velocity.angle)  # change its rotation
        return anatomy

    absolute = property(getAbsolute)


if __name__ == "__main__":
    from mymanager import Manager

    class BodyTester(Manager):
        def __init__(self):
            super().__init__()
            self.bodies = {
                'b': Body.random(n=30)
            }

        def update(self):
            for body in self.bodies.values():
                body.update(self.dt)

        def show(self):
            for body in self.bodies.values():
                body.showAll(self.context)
                body.center.show(self.context)
    m = BodyTester()
    m()
