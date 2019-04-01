from myform import Form
from myplane3 import Plane
from mypoint import Point

class Spaceship(Form):
    def __init__(self):
        points=[Point(0,10),Point(10,-10),Point(-10,-10)]
        self.life=None
        self.max_life=100
        self.damage=10
        Form.__init__(self,points)

    def spawn(self,plane):
        self.life=self.max_life
        self.position=[0,0]
        #self.extent=5 #Only an idea.

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

    def control(self,other):
        pass

    def attack(self,other):
        other.life-=self.dammage

    def isAlive(self):
        return self.life>0

    def __call__(self,plane):
        self.spawn(plane)
        self.play(plane)

if __name__=="__main__":
    plane=Plane()
    spaceship=Spaceship()
    spaceship(plane)
