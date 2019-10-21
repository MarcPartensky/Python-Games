from mymotion import Motion
from mymaterial import Material


class Physics(Material): #,Rotational?
    """Create a physical object that can have multiples motions for describing
    the way the objects move in any space. Because a physical object is also a
    material object it makes it easy to use in practice."""

    #Should a physical object possess a mass????????

    def createFromNumber(n):
        """Create n motions."""
        return Physics([Motion() for i in range(n)])

    def random(n=2):
        """Create n random physical objects."""
        return Physics([Motion.random() for i in range(n)])

    def __init__(self, motions=[Motion(n=3, d=2), Motion(n=3, d=1)], mass = 1):
        """Create a physical object using its motions, by default a physical
        has 2 motions but it can have more."""
        self.motions = motions
        self.mass = mass

    def __neg__(self):
        """Set to negative all the motions."""
        return Physics([-m for m in self.motions])

    def __add__(self, other):
        """Add two physical objects."""
        return Physics([m1 + m2 for (m1, m2) in zip(self.motions, other.motions)])

    def __sub__(self, other):
        """Substract 2 motions."""
        return self + (-other)

    def __str__(self):
        """Return the string representation of the physical object."""
        return "Physics(" + ",".join(map(str, self.motions)) + ")"

    # Properties
    def getMotion(self):
        """Return self.motions[0]."""
        return self.motions[0]

    def setMotion(self, motion):
        """Set self.motions[0]."""
        self.motions[0] = motion

    def getMoment(self):
        """Return self.motions[1]."""
        return self.motions[1]

    def setMoment(self, moment):
        """Set the moment."""
        self.motions[1] = moment

    def update(self, dt=1):
        """Update the physical object."""
        for motion in self.motions:
            motion.update(dt)

    def getPosition(self):
        """Return the position of the physical object."""
        return self.motion.position

    def setPosition(self, position):
        """Set the position of the physical object."""
        self.motion.position = position

    def getAngle(self):
        """Return the angle of the physical object."""
        return self.moment.position

    def setAngle(self, angle):
        """Set the angle of the physical object."""
        self.moment.position = angle

    motion = property(getMotion, setMotion)
    moment = property(getMoment, setMoment)
    position = property(getPosition, setPosition)
    angle = property(getAngle, setAngle)


if __name__ == "__main__":
    #from mycontext import Context
    p1 = Physics.random()
    p2 = Physics.random()
    p3 = p1 - p2
    p3.update()
    print(p3)
