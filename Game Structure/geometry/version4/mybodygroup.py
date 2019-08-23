from mybody import Body
from pygame.locals import *


class BodyGroup:
    def __init__(self,bodies):
        """Create a body group with the list of bodies."""
        self.bodies=bodies

    def react(self,event):
        """React to a given event."""
        self.reactEach(event)
        self.reactAll(event)

    def reactEach(self,event):
        """Make each body react to a given event."""
        for body in self.bodies:
            body.react(event)

    def reactAll(self,event):
        """Make all bodies react to a same given event."""
        pass

    def update(self,dt=1):
        """Update the group."""
        self.updateBodies(dt)

    def updateBodies(self,dt=1):
        """Update each body."""
        for body in self.bodies:
            body.update(dt)

    def show(self,context):
        """Show each body."""
        for body in self.bodies:
            body.show(context)

    def showMotion(self,context):
        """Show each body motion."""
        for body in self.bodies:
            body.showMotion(context)

    def anyColliding(self):
        l=len(self.bodies)
        for i in range(l):
            for j in range(i+1,l):
                self.colliding()

    def __len__(self):
        """Return the number of bodies."""
        return len(self.bodies)



if __name__=="__main__":
    from mysurface import Context
    context=Context()
    bl=[Body.random(),Body.random()]
    bg=BodyGroup(bl)
    while context.open:
        context.clear()
        context.show()
        context.control()
        for event in context.events():
            context.checking(event)
            bg.react(event)
        bg.update(dt=0.01)
        bg.show(context)
        bg.showMotion(context)
        context.flip()
