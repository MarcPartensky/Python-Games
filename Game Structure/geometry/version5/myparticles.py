from mymanager import Manager
from myphysics import Physics
from myabstract import Point,Vector
from mymotion import Motion

import math

class Particle(Physics):
    made=0
    def random(name=None):
        """Create a random particle using its motions' dimensions."""
        return Particle([Motion.random(n=3,d=2),Motion.random(n=2,d=1)],name=name)

    def __init__(self,motions,name=None):
        """Create a particle using its motions."""
        super().__init__(motions)
        Particle.made+=1
        if name is None: name="prt"+str(Particle.made)
        self.name=name

    def showAll(self,context):
        """Show the particle and its name."""
        self.show(context)
        #self.showName(context)
        self.showComponents(context)

    def show(self,context):
        """Show a point."""
        self.point.show(context)
        self.vector.show(context,self.point)

    def showName(self,context):
        """Show the name of the particle."""
        self.point.showText(context,self.name,text_size=10,conversion=True)


    def showComponents(self,context):
        """Show the str of the particle."""
        self.point.showText(context,str(self),text_size=10,conversion=True)

    def getPoint(self):
        """Return the points associated with the particle."""
        return Point(*self.position)

    def getVector(self):
        """Return the vector associated with the rotation of the particle."""
        angle=self.angle[0]
        angle%=(2*math.pi)
        return Vector.createFromPolarCoordonnates(1,angle)

    def getSpin(self):
        """The name of spin is surely not appropritate at all, but for now it
        will do i guess."""
        return self.angle[0]

    point=property(getPoint)
    vector=property(getVector)
    spin=property(getSpin)

class ParticleGroup:

    def random(n):
        """Create n random particles."""
        return ParticleGroup([Particle.random() for i in range(n)])

    def __init__(self,particles):
        """Create all particles."""
        self.particles=particles

    def show(self,context):
        """Show all particles."""
        for particle in self.particles:
            particle.showAll(context)


    def __getitem__(self,index):
        """Return the particle of index 'index'."""
        return self.particles[index]

    def update(self,dt):
        """Update the particle group."""
        self.soloUpdate(dt)

    def soloUpdate(self,dt):
        """Update all the particles independently of the others."""
        for particle in self.particles:
            particle.update(dt)

    def updateFromSpin(self):
        """Technically, the particles with the same spin will repel themselves,
        whereas the particles with opposed spins will attract themselves."""
        #Good luck............
        raise NotImplementedError



class ParticlesManager(Manager):
    def __init__(self,n=10,dt=1e-2):
        """Create the particles manager."""
        super().__init__()
        self.particle_group=ParticleGroup.random(n)
        self.context.console(n,'particles created')
        self.dt=dt

    def show(self):
        """show the particles."""
        self.particle_group.show(self.context)

    def update(self):
        """Update the particles."""
        self.particle_group.update(self.dt)


    def getParticles(self):
        """Return the particles group."""
        return self.particle_group

    def setParticles(self,particles):
        """Set the particle group."""
        self.particle_group=particles

    def getTime(self):
        """Return the time based on the counter and the dt."""
        return self.dt*self.counter

    particles=property(getParticles,setParticles)
    t=time=property(getTime)





if __name__=="__main__":
    m=ParticlesManager()
    print(m.particles[0])
    m()
