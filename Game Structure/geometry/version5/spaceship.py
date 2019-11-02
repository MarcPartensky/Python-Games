from myabstract import Form, Segment
from mymanager import BodyManager,Manager
from mymotion import Motion
from mybody import Body
import mycolors

import numpy as np

class Entity(Body):
    """An entity is a body that can be alive or not."""
    def __init__(self,anatomy,*motions,alive=True):
        """Create an entity."""
        super().__init__(anatomy,*motions)
        self.alive=alive

    def spawn(self):
        """Spawn the entity."""
        self.alive=True

    def respawn(self):
        """Respawn an entity by simply spawning it."""
        self.spawn()

    def kill(self):
        """Kill the entity by setting alive status to false."""
        self.alive=False


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


class Missile(Entity):
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
        self.shooting=False

    def update(self):
        pass

    def react(self,event):
        if event==K_SPACE:
            self.shooting=True

    def shoot(self):
        return SegmentMissile(*self.motion)

    def show(self):
        pass

class EntityGroup:
    """Group of entities that handle themselves."""

    @classmethod
    def random(cls,n=5,np=3,nm=2,nv=2,dv=2):
        """Create a random entity group using the optional number of entities 'n'."""
        entities=[Entity.random(n=np,nm=nm,nv=nv,d=dv) for i in range(n)]
        entities=dict(zip(range(len(entities)),entities))
        return cls(entities)

    def __init__(self,entities):
        """Create a body group using the dictionary of entities."""
        self.entities=entities
        self.updateAlives()

    def updateAlives(self):
        """Update the ids of alive entities."""
        self.alives=dict([(id,entity) for (id,entity) in self.entities.items() if entity.alive])
        #Recurrent data that must be updated.
        #It is better to proceed that way for efficiency

    @property
    def deads(self):
        """Return the ids of dead entities."""
        return {k:v for k,v in self.entities.items() if k not in self.alives}

    def spawnEach(self):
        """Spawn each entity."""
        for entity in self.entities.values():
            entity.spawn()
        self.alives=self.entities.keys()

    def updateEach(self,dt):
        """Update each entity alive."""
        for entity in self.alives.values():
            entity.update(dt)

    def showEach(self,context):
        """Show each entity alive."""
        for entity in self.alives.values():
            entity.show(context)

    def respawnDeads(self):
        """Respawn each dead entity."""
        for entity in self.deads.values():
            entity.respawn()

    def getCollisions(self):
        """Return the list of couples of collisions detected between alive entities."""
        collisions=[]
        keys=list(self.alives.keys())
        n=len(keys)
        for i in range(n):
            for j in range(i+1,n):
                id1=keys[i]
                id2=keys[j]
                e1=self.alives[id1]
                e2=self.alives[id2]
                if e1.cross(e2):
                    collisions.append((id1,id2))
        return collisions

    def getCollided(self,collisions):
        """Return the ids of collided entities."""
        ids=list(set(np.reshape(collisions,2*len(collisions))))
        return dict([(id,self.entities[id]) for id in ids])

    def kill(self,collided):
        """Kill entities with their ids."""
        for entity in collided:
            entity.kill()

    def spread(self,n=10):
        """Spread randomly the entities."""
        for entity in self.entities.values():
            entity.motion=n*Motion.random()

    def followEach(self,point):
        """Make each entity follow the point."""
        for entity in self.alives.values():
            entity.follow(point)

    def getMaxBorn(self):
        """Return the borns of all entities."""
        return max([e.born for e in self.alives.values()])

    def setMaxBorn(self,born):
        """Set the max born of all the entities."""
        f=born/self.maxborn

    maxborn=property(getMaxBorn,setMaxBorn)

    def getCollisionsWithCircles(self):
        """Return all circle collisions."""
        collisions=[]
        keys=list(self.alives.keys())
        n=len(keys)
        for i in range(n):
            for j in range(i+1,n):
                id1=keys[i]
                id2=keys[j]
                e1=self.alives[id1]
                e2=self.alives[id2]
                if (e1.position-e2.position).norm<e1.born+e2.born:
                    if e1.cross(e2):
                        collisions.append((id1,id2))
        return collisions


class SegmentMissilesGroup(EntityGroup):

    @classmethod
    def random(cls,n=20):
        """Create a random segment."""
        entities=[SegmentMissile.random() for i in range(n)]
        entities=dict(zip(range(len(entities)),entities))
        return cls(entities)


class SpaceShipTester(BodyManager):
    """Tester of spaceships."""
    @classmethod
    def random(cls,n=20,**kwargs):
        """Create random bodies."""
        bodies=[TriangleSpaceShip.random() for i in range(n)]
        bodies+=[SegmentMissile.random()]
        return cls(bodies,**kwargs)

    def makeSparse(self,n=10):
        """Sparse the bodies."""
        for body in self.bodies:
            body.motion*=n

    def setRandomColors(self):
        """Set the colors of the bodies to random."""
        for body in self.bodies:
            for vector in body.motion:
                vector.color=mycolors.random()

    def spread(self,n=10):
        """Spread randomly the bodies."""
        for body in self.bodies:
            body.motion=n*Motion.random()


class GroupManager(Manager):
    @classmethod
    def random(cls,**kwargs):
        """Create a random entity group."""
        group=EntityGroup.random(**kwargs)
        return cls(group)

    def __init__(self,group,**kwargs):
        """Create a body group manager using the group and optional arguments."""
        super().__init__(**kwargs)
        self.group=group


    def update(self):
        """Update the group."""
        collisions=self.group.getCollisions()
        collided=self.group.getCollided(collisions)
        self.group.kill(collided)
        self.group.updateAlives()
        self.group.updateEach(self.dt)

    def show(self):
        """Show the group."""
        self.group.showEach(self.context)


class GroupTester(GroupManager):
    def __init__(self,*args,**kwargs):
        super().__init__(*args)
        self.group.spread(100)
        self.following=True

    def update(self):
        """Update without collisions checks."""
        #self.group.updateEach(self.dt)
        self.updateWithCollisions()

    def updateWithCollisions(self):
        """Update the group."""
        self.group.followEach(self.context.point())
        #collisions=self.group.getCollisionsWithCircles()
        collisions=[]
        collided=self.group.getCollided(collisions)
        if len(collided)!=0:
            self.group.kill(collided)
            self.group.updateAlives()
        self.group.updateEach(self.dt)


if __name__ == "__main__":
    #bm = SpaceShipTester.random(following=True, dt=0.1)
    #bm()
    gt=GroupTester.random(n=20)
    print(gt.group.alives)
    gt()
