from mysurface import Surface
from myvector import Vector

class Motion:
    def __init__(self,position=Vector([0.,0.]),velocity=Vector([0.,0.]),acceleration=Vector([0.,0.])):
        self.position=position
        self.velocity=velocity
        self.acceleration=acceleration

    def __call__(self,t=1):
        """Move entity according to its acceleration, velocity and position."""
        self.velocity=[v+a*t for (v,a) in zip(self.velocity,self.acceleration)]
        self.position=[p+v*t for (p,v) in zip(self.position,self.velocity)]

    def __str__(self):
        """Return the str representation of the motion."""
        text="Motion: position: "+str(self.position)+", velocity: "+str(self.velocity)+" and acceleration: "+str(self.acceleration)
        return text

    __repr__=__str__

    def previous(self,t=1):
        """Return the previous motion using its actual one using optional time t."""
        previous_acceleration=Vector([a for a in self.acceleration])
        previous_velocity=Vector([v-a*t for (v,a) in zip(self.velocity,self.acceleration)])
        previous_position=Vector([p-v*t for (p,v) in zip(self.position,self.velocity)])
        previous_motion=Motion(previous_position,previous_velocity,previous_acceleration)
        return previous_motion

    def next(self,t=1):
        """Return the next motion using its actual one using optional time t."""
        next_acceleration=Vector([a for a in self.acceleration])
        next_velocity=Vector([v+a*t for (v,a) in zip(self.velocity,self.acceleration)])
        next_position=Vector([p+v*t for (p,v) in zip(self.position,self.velocity)])
        next_motion=Motion(next_position,next_velocity,next_acceleration)
        return next_motion

    def __getitem__(self,index):
        """Return the position, velocity or acceleration using the index."""
        if index==0:   return self.position
        elif index==1: return self.velocity
        else:          return self.acceleration

    def __setitem__(self,index,vector):
        """Set the position, velocity or acceleration using the index."""
        if index==0:   self.position=vector
        elif index==1: self.velocity=vector
        else:          self.acceleration=vector

    def getPosition(self):
        """Return the position of the motion."""
        return self.position

    def getVelocity(self):
        """Return the velocity of the motion."""
        return self.velocity

    def getAcceleration(self):
        """Return the acceleration of the motion."""
        return self.acceleration

    def setPosition(self,position):
        """Set the position of the motion using position."""
        self.position=position

    def setVelocity(self,velocity):
        """Set the velocity of the motion using velocity."""
        self.velocity=velocity

    def setAcceleration(self,acceleration):
        """Set the acceleration of the motion."""
        self.acceleration=acceleration

    def



if __name__=="__main__":
    surface=Surface()
    while surface.open:
        surface.check()
        surface.clear()
