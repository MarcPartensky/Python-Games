from myabstract import Form, Point
from myentity import ResponsibleEntity
from mymotion import Motion, Moment
from myspaceship import Asteroid


import mycolors
import random
import noise
import math


class PerlinAsteroid:

    @classmethod
    def random(cls, n=1,**kwargs):
        """Return a perlin asteroid with a random phase."""
        return cls(n * random.random(),**kwargs)

    def __init__(self, phase=0, precision=100, color=mycolors.WHITE, radius=1):
        """Object of perlin asteroid:"""
        self.phase = phase
        self.precision = precision
        self.color = color
        self.radius = radius
        self.noise_max = 2
        self.wo = 2 * math.pi
        self.form = self.getForm()

    def update(self, dt):
        """Update the perlin asteroid."""
        self.form = self.getForm()
        self.phase += dt

    def show(self, context):
        """Show the form."""
        self.form.show(context)

    @property
    def points(self):
        """Return the points of the perlin asteroid."""
        points = []
        wo = self.wo
        nm = self.noise_max
        off = self.phase
        rd = self.radius
        for i in range(self.precision):
            a = i / self.precision * wo
            xoff = nm * (math.cos(a + off) + 1) / 2
            yoff = nm * (math.sin(a + off) + 1) / 2
            r = noise.pnoise2(xoff + off, yoff + off)
            r = (r + 1) / 2
            x = rd * r * math.cos(a)
            y = rd * r * math.sin(a)
            points.append((x, y))
        return points

    def getForm(self):
        """Return the form of the perlin asteroid."""
        return Form.createFromTuples(self.points, color=self.color)

    def __str__(self):
        """Return the complete string representation of an object."""
        return type(self).__name__ + "({})".format(",".join(
            [":".join(map(str, e)) for e in self.__dict__.items()]))


class PerlinAsteroidAnatomy(Form):
    """This is the anatomy of a perlin asteroid using adapter pattern."""

    @classmethod
    def random(cls, n=1, **kwargs):
        """Create a random perlin asteroid using given sparse magnitude."""
        return cls(PerlinAsteroid.random(n, **kwargs))

    def __init__(self, perlin_asteroid):
        """Create a perlin asteroid anatomy."""
        self.perlin_asteroid = perlin_asteroid
        self.updatePoints()

    def show(self, context):
        """Show the perlin asteroid anatomy."""
        self.perlin_asteroid.show(context)

    def update(self, dt):
        """Update the perlin asteroid."""
        self.perlin_asteroid.update(dt)

    def updatePoints(self):
        """Return the points of the asteroid anatomy to the perlin asteroid."""
        self.points = list(map(lambda p: Point(*p), self.perlin_asteroid.points))

    def __str__(self):
        """Return the complete string representation of an object."""
        return type(self).__name__ + "({})".format(",".join(
            [":".join(map(str, e)) for e in self.__dict__.items()]))

    def enlarge(self, n):
        """Enlarge the anatomy."""
        self.perlin_asteroid.radius *= n


class PerlinAsteroidEntity(ResponsibleEntity, Asteroid):
    @classmethod
    def random(cls,**kwargs):
        """Return a random perlin asteroid entity."""
        p=PerlinAsteroidAnatomy.random()
        m1=Motion.random(n=2)
        m2=Moment.random(d=1,n=2)
        return cls(p,m1,m2,**kwargs)

if __name__ == "__main__":
    from mymanager import EntityManager
    #pa = PerlinAsteroid.random()
    #paa = PerlinAsteroidAnatomy.random()
    pae=PerlinAsteroidEntity.random()
    m=EntityManager(pae)
    m()
