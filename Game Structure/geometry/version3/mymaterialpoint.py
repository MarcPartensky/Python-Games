from mypoint import Point
from myforce import Force

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

class MaterialPoint:
    def __init__(self,motion,forces=[]):
        self.next_motion=motion
        self.previous_motion=motion
