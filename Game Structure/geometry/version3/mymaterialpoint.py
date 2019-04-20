from mypoint import Point
from myforce import Force
from mysegment import Segment

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
        previous_motion=
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
