from mypoint import Point
from myforce import Force
from mysegment import Segment
from mymotion import Motion
from myvector import Vector

class OldMaterialPoint(Point):
    def __init__(self,forces=[]):
        """Create a material point."""
        self.forces=forces
    def apply(self):
        """Apply the forces on the point."""
        for forces in self.force:
            pass
        #Problem: the point doesn't have an acceleration, nor a velocity
        #It's not possible to apply a force without having a motion.

class OldMaterialPoint2:
    def __init__(self,motions,forces=[]):
        """Create a material point using a list of motions and some forces."""
        """The list of motions can be of any size as long as the first motions corresponds to the previous one, and the last one is the next one."""
        self.motions=motions #0: previous , (1:now), -1:next
        self.forces=forces

    def getNextMotion(self):
        """Get the next motion."""
        return self.motions[-1]

    def setNextMotion(self,motion):
        """Change the next motion."""
        self.motions[-1]=motion

    def getPreviousMotion(self):
        """Get the previous motion."""
        return self.motions[0]

    def setPreviousMotion(self,motion):
        """Change the internal previous motion."""
        self.motions[0]=motion

    def apply(self,force=None):
        """Apply a force on the next_motion."""
        if not force: force=sum(self.forces)
        previous_motion=self.getPreviousMotion()
        next_motion=self.getNextMotion()
        previous_motion=None
        next_motion=force(next_motion)

    def update(self,t=1):
        """Update the motions after the forces being applied, using time 't'."""
        pass

    def switch(self):
        """Switch the motions between themselves."""
        """The previous motion becomes the next one and so on."""
        """Only the last one remains unchanged."""
        for i in range(1,len(self.motions)):
            self.motions[i]=self.motions[i+1]

    def show(self,window):
        """Show the material point on screen."""
        previous_motion=self.getPreviousMotion()
        next_motion=self.getNextMotion()
        previous_position=previous_motion.getPosition()
        next_position=previous_motion.getPosition()

class MaterialPoint:
    def random(min=-1,max=1):
        """Create a random material point using optional minimum and maximum."""
        motion=Motion.random()
        return MaterialPoint(motion)

    def __init__(self,motion=Motion(),mass=1,forces=[]):
        """Create a material point."""
        self.motion=motion
        self.mass=mass
        self.forces=forces

    def getPosition(self):
        """Return the position of the material point."""
        return self.motion.getPosition()

    def setPosition(self,position):
        """Set the position of the material point."""
        self.motion.position=Vector(position)

    def getVelocity(self):
        """Return the velocity of the material point."""
        return self.motion.getVelocity()

    def setVelocity(self,velocity):
        """Set the velocity of the material point."""
        self.motion.velocity=Vector(velocity)

    def getAcceleration(self):
        """Return the acceleration of the material point."""
        return self.motion.getAcceleration()

    def setAcceleration(self,acceleration):
        """Set the acceleration of the material point."""
        self.motion.acceleration=Vector(acceleration)

    def show(self,window):
        """Show the material point on screen."""
        position=self.getPosition()
        x,y=position
        point=Point(x,y)
        point.show(window)

    def update(self,t=1):
        """Update the motion of the material point."""
        force=Force.sum(self.forces)
        x,y=force
        acceleration=Vector(x,y)/self.mass
        self.motion.setAcceleration(acceleration)
        self.motion.update(t)

    def __iter__(self):
        """Iterate the position."""
        self.iterator=0
        return self

    def __next__(self):
        """Return the next point threw an iteration."""
        if self.iterator < 2:
            if self.iterator==0: value=self.motion.getPosition()[0]
            if self.iterator==1: value=self.motion.getPosition()[1]
            self.iterator+=1
            return value
        else:
            raise StopIteration

if __name__=="__main__":
    from mysurface import Surface
    surface=Surface()
    points=[MaterialPoint.random() for i in range(5)]
    while surface.open:
        surface.check()
        surface.clear()
        surface.control()
        surface.show()
        for point in points:
            point.show(surface)
            point.update()
        surface.flip()
