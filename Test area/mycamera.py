from myentity import Entity
import time

class Camera(Entity):
    def __init__(self,position,size,borders):
        """Create camera object using position, size and borders."""
        Entity.__init__(self,position=position,size=size,borders=borders)
    def __call__(self,direction):
        """Return vision using direction."""
        self.direction=self.polar(direction)
        self.update()
        return vision
