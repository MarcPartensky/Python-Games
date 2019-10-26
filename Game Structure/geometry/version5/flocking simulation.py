from mymanager import Manager
from myabstract import Vector, Form
from mymotion import Motion
from mybody import MaterialBody
import mycolors
import random
import math


class Boid(MaterialBody):

    @classmethod
    def random(cls):
        """Create a boid with a random motion."""
        p=10*Vector.random()
        #v=Vector(0,random.uniform(0,10),color=mycolors.BLUE)
        v=5*Vector.random(color=mycolors.BLUE)
        a=Vector.null()
        m=Motion(p,v,a)
        return cls(m)

    def __init__(self, motion=Motion(n=3, d=2)):
        """Create a boid."""
        self.motion = motion
        self.anatomy = Form.createFromTuples([(0,1),(1,-1),(0,0),(-1,-1)])
        self.anatomy.rotate(-math.pi/2)
        self.anatomy.area_color=mycolors.RED
        self.anatomy.fill=True
        self.discipline = 0.1

    def adjustVelocity(self,neighbours):
        """Adjust the boid velocity to the one of its neighbours."""
        neighbours_velocities=[n.velocity for n in neighbours]
        average_velocity=Vector.average(neighbours_velocities)
        self.acceleration.set((average_velocity-self.velocity)*self.discipline)



class BoidGroup:
    @classmethod
    def random(cls, n=10):
        """Create a group of random boids."""
        boids = [Boid.random() for i in range(n)]
        return BoidGroup(boids)

    def __init__(self, boids):
        """Create a boid group using boids."""
        self.boids = boids
        self.neighbours_number = 3
        self.neighbours_radius = 20

    def show(self, context):
        """Show the object."""
        for boid in self.boids:
            boid.show(context)

    def update(self, dt=1):
        """Update the object."""
        self.adjustVelocities()
        self.updateEach(dt)

    def updateEach(self,dt):
        """Update each boid individually."""
        for boid in self.boids:
            boid.update(dt)

    def follow(self,point):
        """Follow the given point."""
        for boid in self.boids:
            boid.follow(point)

    def adjustVelocities(self):
        """Adjust the velocity of each boid to the one of its neighbours."""
        for i in range(len(self.boids)):
            neighbours=self.getNeighbours(i)
            self.boids[i].adjustVelocity(neighbours)

    def getNeighbours(self,j):
        """Return the neighbours of the b-th boid."""
        proximity=[(self.distance(i,j),i) for i in range(len(self.boids))]
        proximity.sort(key=lambda x:x[0])
        proximity=proximity[:self.neighbours_number]
        neighbours=[self.boids[p[1]] for p in proximity]
        return neighbours

    def distance(self,i,j):
        """Return the distance between the boids i and j."""
        p1=self.boids[i].position
        p2=self.boids[j].position
        return (p1-p2).norm


class Simulation(Manager):
    def random(n=10, **kwargs):
        """Create a random simulation of boids."""
        return Simulation(BoidGroup.random(n), **kwargs)

    def __init__(self, boid_group, **kwargs):
        """Create a simulation of flocking."""
        super().__init__(**kwargs)
        self.boid_group = boid_group

    def update(self):
        """Update the boid group."""
        self.boid_group.update(self.dt)
        #self.boid_group.follow(self.context.point())

    def show(self):
        """Show the boid group."""
        self.boid_group.show(self.context)


if __name__ == "__main__":
    s = Simulation.random(n=50,dt=1)
    s()
