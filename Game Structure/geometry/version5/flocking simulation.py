from mymanager import Manager
from myabstract import Vector
from mymotion import Motion
from mymaterial import Material


class Boid(Material):
    def __init__(self, motion=Motion(n=3, d=2), form=):
        """Create a boid."""
        self.motion = motion
        self.form = form

    def update(self):
        """Update the boid."""
        self.motion.update()

    def show(self):
        """Show the boid."""
        self.form.show(self.context)


class BoidGroup:
    @classmethod
    def random(cls, n=10):
        """Create a group of random boids."""
        boids = [Boid.random() for i in range(n)]
        return BoidGroup(boids)

    def __init__(self, boids):
        """Create a boid group using boids."""
        self.boids = boids

    def show(self, context):
        """Show the object."""
        for boid in self.boids:
            boid.show(context)

    def update(self, dt=1):
        """Update the object."""
        for boid in self.boids:
            boid.update(dt)


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

    def show(self):
        """Show the boid group."""
        self.boid_group.show(self.context)


if __name__ == "__main__":
    s = Simulation()
    s()
