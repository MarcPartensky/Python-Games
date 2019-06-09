from myabstract import Form,Vector
from mymotion import Motion
from myforce import Force,gravity

from pygame.locals import *
import copy

class Body:
    def __init__(self,form,name="Unnamed entity"):
        """Create body using form and optional name."""
        self.name=name
        self.form=form
        self.motion=Motion()
        #self.forces={"gravity":gravity,"propulsion":propulsion}
        self.forces={"propulsion":Force(0,0)}
        self.frixion=0.8

    def getMass(self):
        """Return the mass of the object using the area."""
        return self.form.area

    def spawn(self,position=(0,0)):
        """Make the body spawn."""
        x,y=position
        self.motion.setPosition(Vector(x,y))
        self.motion.setVelocity(Vector(0,0))
        self.motion.setAcceleration(Vector(0,0))

    def show(self,window):
        """Show the form on the window."""
        position=self.motion.getPosition()
        form=copy.deepcopy(self.form)
        form.move(position)
        form.show(window)

    def move(self,t=1):
        """Move entity according to its acceleration, velocity and position."""
        self.motion.update(t)

    def applyForces(self):
        """Apply the forces on the body."""
        forces=[force for force in self.forces.values()]
        force=Force.mean(forces)
        x,y=force
        m=self.getMass()
        acceleration=Vector(x,y)/m
        self.motion.setAcceleration(acceleration)

    def applyFrixion(self):
        """Apply the frixion on the body."""
        velocity=self.motion.getVelocity()
        velocity=velocity*self.frixion
        print(velocity)
        self.motion.setVelocity(velocity)

    def update(self,t=1):
        """Update the body by updatings its motion."""
        self.applyForces()
        self.applyFrixion()
        self.move(t)

    def control(self,window):
        """Control the view of the plane."""
        keys=window.press()
        if keys[K_UP]:
            self.forces["propulsion"][1]=1
        if keys[K_DOWN]:
            self.forces["propulsion"][1]=-1
        if keys[K_LEFT]:
            self.forces["propulsion"][0]=-1
        if keys[K_RIGHT]:
            self.forces["propulsion"][0]=1



if __name__=="__main__":
    from mysurface import Surface
    surface=Surface()
    form=Form.random()
    body=Body(form)
    body.spawn()
    while surface.open:
        surface.check()
        #surface.control()
        surface.clear()
        surface.show()
        surface.controlZoom()
        body.control(surface)
        body.update(t=0.1)
        body.show(surface)
        position=body.motion.getPosition()
        surface.draw.plane.position=position
        surface.flip()
