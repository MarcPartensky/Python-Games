from myabstract import Form, Segment
from mymanager import BodyManager
from mymotion import Motion
from mybody import Body
import mycolors

class Entity(Body):
    """An entity is a body that can be alive or not."""
    def __init__(self,anatomy,*motions,alive=False):
        """Create an entity."""
        super().__init__(anatomy,*motions)
        self.alive=alive

    def spawn(self):
        """Spawn the entity."""
        self.alive=True

    def respawn(self):
        """Respawn an entity by simply spawning it."""
        self.spawn()


class FrictionBody(Body):
    """Add some friction to a body."""

    def __init__(self,*args,friction=0.1):
        """Create a body with friction."""
        super().__init__(*args)
        self.friction=friction

    def update(self,dt):
        """Update the spaceship."""
        super().update(dt)
        self.updateFriction()

    def updateFriction(self):
        """Add some friction."""
        self.velocity.norm*=(1-self.friction)

class FrictionEntity(FrictionBody,Entity):
    def __init__(self,*args,friction=0.1,alive=True):
        """Create an entity that has friction."""
        Entity.__init__(*args,alive)
        self.friction=friction


class SpaceShip(FrictionBody):
    def __init__(self, anatomy, motion):
        """Create a space ship."""
        super().__init__(anatomy, motion)



class TriangleSpaceShip(SpaceShip):
    @classmethod
    def random(cls, sparse=100, **kwargs):
        """Create a random triangle spaceship."""
        return cls(sparse*Motion.random(), **kwargs)

    def __init__(self, motion, **kwargs):
        """Create a triangle spaceship."""
        anatomy = Form.createFromTuples([(1, 0), (-1, -1), (-0.5, 0), (-1, 1)])
        anatomy.recenter()
        super().__init__(anatomy, motion, **kwargs)

    def getForm(self):
        """Return the form."""
        f = super().getForm()
        f.side_color=mycolors.YELLOW
        print(f.side_color)
        return f

    def show(self, context):
        """Show the space ship and its motion."""
        super().show(context)
        self.showMotion(context)


class Missile(FrictionBody):
    """Base class of all missiles."""
    def __init__(self,anatomy,motion,target=None,**kwargs):
        """Create a missile using the motion and the target."""
        super().__init__(anatomy,motion,**kwargs)
        self.target=target


class SegmentMissile(Missile):
    """Base class of any missile."""
    @classmethod
    def random(cls):
        """Create a segment missile with a random motion."""
        motion=Motion.random()
        segment=Segment.createFromTuples((-0.5,0),(0.5,0))
        return cls(segment,motion)

    def __init__(self,segment,motion,**kwargs):
        """Create a segment missile."""
        super().__init__(segment,motion,**kwargs)




class Shooter(SpaceShip):
    def __init__(self,jadskfjlkas,**kwargs):
        """Space ship that can shoot."""
        super().__init__(*args,**kwargs)
        self.ajdfklajsflka=fajdfkajlkjf
        self.shooting=False

    def update(self):
        pass


    def react(self,event):
        if event==K_SPACE:
            self.shooting=True




    def show(self):
        pass

class BodyGroup:
    """Group of bodies that handle themselves."""
    def __init__(self,bodies):
        """Create a body group using the list of bodies."""
        self.bodies=bodies

    def updateEach(self,dt):
        """Update each body."""
        for body in self.alives:
            body.update(dt)

    def showEach(self,context):
        """Show each body."""
        for body in self.alives:
            body.show(context)

    def respawnDeads(self):
        """Respawn all the deads."""
        for dead in self.deads:
            dead.respawn()

    def checkCollisions(self):
        """Determine the id of the entities that are in collisions."""
        collisions=[]
        len(self.bodies)
        #for i in range():

    def getAlives(self):
        """Return the bodies that are alives."""
        return [body for body in self.bodies if body.alive]

    def getDeads(self):
        """Return all the deads."""
        return [body for body in self.bodies if not body.alive]

    alives = property(getAlives)
    deads = property(getDeads)


class SpaceShipGroup(BodyGroup):
    """Group of space ships that handle themselves."""
    def __init__(self,spaceships):
        """Create a group of spaceships using the list of spaceships."""
        super().__init__(spaceships)

class SpaceShipTester(BodyManager):
    """Tester of spaceships."""
    pass

if __name__ == "__main__":
    # b1=TriangleSpaceShip.random()
    # bs=[b1]
    b=SegmentMissile.random()
    bs = [TriangleSpaceShip.random() for i in range(20)]+[b]
    bm = SpaceShipTester(bs, following=True, dt=0.1)
    bm()
