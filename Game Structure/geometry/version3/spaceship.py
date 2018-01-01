from myform import Form
from mysurface import Surface
from mypoint import Point

from pygame.locals import *

class Spaceship(Form):
    def __init__(self):
        points=[Point(0,2),Point(1,-1),Point(0,0),Point(-1,-1)]
        self.life=None
        self.max_life=100
        self.damage=10
        self.motion=Motion([0,0])
        self.displacement=[Motion([0,0]),Motion([0,0])]
        Form.__init__(self,points)


    def move(self,t=1):
        """Move entity according to its acceleration, velocity and position."""
        self.velocity=[v+a*t for (v,a) in zip(self.velocity,self.acceleration)]
        self.position=[p+v*t for (p,v) in zip(self.position,self.velocity)]


    def update(self):
        self.moveTo(self.position)

    def show(self,plane):
        for side in self.sides():
            side.show(plane)
        for point in self.points:
            point.show(plane)


    def play(self,plane):
        while plane.open and self.isAlive():
            plane.check()
            plane.clear()
            self.control(plane)
            self.show(plane)
            plane.flip()

    def control(self,window):
        keys=window.press()
        if keys[K_UP]:
            self.acceleration[1]+=1
        if keys[K_DOWN]:
            self.acceleration[1]-=1
        if keys[K_LEFT]:
            self.rotate(0.1)
        if keys[K_LEFT]:
            self.rotate(-0.1)

    def attack(self,other):
        other.life-=self.dammage

    def isAlive(self):
        return self.life>0

if __name__=="__main__":
    surface=Surface()
    spaceship=Spaceship()
    while surface.open:
        surface.check()
        surface.clear()
        surface.show()
        spaceship.control(surface.draw.window)
        spaceship.show(surface)
        surface.flip()
