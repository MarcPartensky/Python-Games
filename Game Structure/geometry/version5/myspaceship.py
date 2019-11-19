from myentitygroup import EntityGroup
from myabstract import Form, Segment, Vector
from myentity import LimitedEntity, LivingEntity, Entity
from mymotion import Motion, Moment
from myasteroidbase import SpiderBaseAnatomy
from pygame.locals import *

import mycolors
import time  # To time missiles life
import copy

from mymanager import BodyManager


class SpaceShip(LimitedEntity, LivingEntity):
    """Base class of all spaceships."""
    @classmethod
    def random(cls, **kwargs):
        """Create a random spaceship."""
        motion = Motion.random()
        form = Form.random()
        return cls(form, motion, **kwargs)


class SpaceBase(LimitedEntity):
    """SpaceBase of spaceships."""


class SpiderBase(SpaceBase):
    """Base that can look like a spider."""

    @classmethod
    def random(cls, **kwargs):
        """Create random motions for the spider base."""
        motion = Motion.random(n=2, d=2)
        moment = Moment.random(n=2, d=1)
        return cls(motion, moment, **kwargs)

    def __init__(self, motion, moment, **kwargs):
        """Create a spider base using the motion and optional parameters for the spider base anatomy."""
        anatomy = SpiderBaseAnatomy(**kwargs)
        super().__init__(anatomy, motion, moment)


class TriangleSpaceShip(SpaceShip):
    @classmethod
    def random(cls, sparse=100, **kwargs):
        """Create a random triangle spaceship."""
        return cls(sparse * Motion.random(), **kwargs)

    def __init__(self, motion, **kwargs):
        """Create a triangle spaceship."""
        anatomy = Form.createFromTuples([(1, 0), (-1, -1), (-0.5, 0), (-1, 1)], **kwargs)
        anatomy.recenter()
        super().__init__(anatomy, motion)

    def getForm(self):
        """Return the form."""
        f = super().getForm()
        f.side_color = mycolors.YELLOW
        return f


class ShowMotionSpaceShip(SpaceShip):
    """SpaceShip that shows its motion."""

    def show(self, context):
        """Show the space ship and its motion."""
        super().show(context)
        self.showMotion(context)


class Missile(Entity):
    """Base class of all missiles."""

    def __init__(self, anatomy, motion, target=None, friction=0, **kwargs):
        """Create a missile using the motion and the target."""
        super().__init__(anatomy, motion, friction=friction, **kwargs)
        self.target = target


class ShortMissile(Missile):
    """Missile with a limited life expectancy."""

    def __init__(self, *args, duration=3, **kwargs):
        """Create a missile with a limited life expectancy."""
        super().__init__(*args, **kwargs)
        self.duration = duration
        self.time = time.time()

    def update(self, dt):
        """Update a short missile."""
        super().update(dt)
        if time.time() - self.time > self.duration:
            self.die()


class SegmentMissile(ShortMissile):
    """Base class of any missile."""
    @classmethod
    def random(cls):
        """Create a segment missile with a random motion."""
        motion = Motion.random()
        segment = Segment.createFromTuples((-0.5, 0), (0.5, 0))
        return cls(segment, motion)

    def __init__(self, segment, motion, **kwargs):
        """Create a segment missile."""
        super().__init__(segment, motion, **kwargs)


class Shooter(SpaceShip):
    def __init__(self, *args, shooting_speed=10, **kwargs):
        """Space ship that can shoot."""
        super().__init__(*args, **kwargs)
        self.shooting = False
        self.anatomy.side_color = mycolors.ORANGE
        self.shooting_speed = shooting_speed
        self.activate()

    def shoot(self):
        """Return a missile with the same motion."""
        self.shooting = False
        s = Segment.createFromTuples((0, 0), (1, 0))
        s.rotate(self.velocity.angle)
        m = Motion(copy.deepcopy(self.position), copy.deepcopy(self.velocity))
        m.position += Vector.createFromPolar(self.born + 1, m.velocity.angle)
        m.velocity.norm += self.shooting_speed
        return SegmentMissile(s, m)


class MaxSpeedSpaceShip(SpaceShip):
    """Spaceship with max speed."""

    def __init__(self, *args, max_speed=10, **kwargs):
        """Crate a spaceship with a given max speed."""
        super().__init__(*args, **kwargs)
        self.max_speed = max_speed

    def update(self, dt):
        """Update the MaxSpeedSpaceShip using dt."""
        super().update(dt)
        self.velocity.norm = min(self.velocity.norm, self.max_speed)


class PlayableSpaceShip(MaxSpeedSpaceShip):
    """Spaceship that can be controlled and played by the user."""

    def reactMouseMotion(self, position):
        """Follow the mouse by changing the velocity."""
        self.acceleration.set(Vector(*position) - self.position)

    def show(self, context):
        """Show the playable spaceship."""
        super().show(context)
        self.showMotion(context)


class PlayableShooter(PlayableSpaceShip, Shooter):
    """Shooter that can be played by a player and so reacts to a space key event."""

    def reactKeyDown(self, key):
        """React to a key down event."""
        if key == K_SPACE:
            self.shooting = True


class Follower(MaxSpeedSpaceShip):
    """Entity that follows a target. It can be used to make self-guided missiles, or hunters."""

    def __init__(self, *args, **kwargs):
        """Create a follower entity."""
        if "target" in kwargs:
            self.target = kwargs.pop("target")
        else:
            self.target = None
        super().__init__(*args, **kwargs)

    def update(self, dt):
        """Update the entity and follow it."""
        super().update(dt)
        if self.target is not None:
            self.acceleration.set(self.target.position - self.position)


class Hunter(Shooter, Follower):
    """Create a spaceship that hunts its targets."""

    def __init__(self, *args, shooting_view=1, **kwargs):
        """Create a hunter spaceship using spaceship arguments and view."""
        if "shooting_view" in kwargs:
            self.shooting_view = kwargs.pop("shooting_view")
        else:
            self.shooting_view = 1
            super().__init__(*args, **kwargs)

    def update(self, dt):
        """Update the entity, follow it, and shoot at it when in range and in view."""
        super().update(dt)
        if self.target is not None:
            self.hunt(dt)

    def hunt(self, dt):
        """Hunt the target supposing it exists."""
        v1 = self.target.position - self.position
        v2 = self.velocity
        if abs(v1.angle - v2.angle) <= self.shooting_view:
            distance = (self.position - self.target.position).norm
            if distance <= self.getShootingRange(dt):
                self.shooting = True

    def getShootingRange(self, dt):
        return self.velocity.norm * dt


class Asteroid(Entity):
    """Mother class of all asteroids."""

    @classmethod
    def random(cls, n=5, **kwargs):
        """Create a random asteroid."""
        a = Form.random(n)
        mt = Motion.random(n=2, d=2)
        mm = Moment.random(n=2, d=1)
        return cls(a, mt, mm, **kwargs)


class SpaceshipGameGroup:
    """Group of groups."""

    @classmethod
    def random(cls, nmissiles, nspaceships, **kwargs):
        """Return a random group."""
        missiles = MissileGroup.random(nmissiles)
        spaceships = SpaceShipGroup.random()
        return cls(missiles, spaceships, **kwargs)

    def __init__(self, groups):
        """Create a super group using the groups."""
        super().__init__(**kwargs)
        self.groups = groups

    def update(self, dt):
        """Update with shooting."""
        self.updateGroups(dt)
        self.updateShooting(dt)

    def reactKeyDown(self, key):
        """React to a key down event."""
        self.missiles.reactKeyDown(key)
        self.spaceships.reactKeyDown(key)

    def reactMouseMotion(self, position):
        """React to a mouse motion event."""
        self.missiles.reactMouseMotion(position)
        self.spaceships.reactMouseMotion(position)

    def reactMouseButtonDown(self, button, position):
        """React to a mouse button down event."""
        self.missiles.reactMouseButtonDown(button, )
        self.missiles.reactMouseButtonDown(button, )

    def updateShooting(self):
        """Add the shooted missiles."""
        self.missiles.group.append(self.spaceships.getShooted())


class MissileGroup:
    def updateAlives(self, dt):
        """Update alived missiles by kill."""
        self.updateEach(dt)


class SegmentMissilesGroup(EntityGroup):

    @classmethod
    def random(cls, n=20):
        """Create a random segment."""
        entities = [SegmentMissile.random() for i in range(n)]
        entities = dict(zip(range(len(entities)), entities))
        return cls(entities)


class SpaceShipTester(BodyManager):
    """Tester of spaceships."""

    @classmethod
    def random(cls, n=20, **kwargs):
        """Create random bodies."""
        bodies = [PlayableSpaceship.random()]
        bodies += [TriangleSpaceShip.random() for i in range(n)]
        bodies += [SegmentMissile.random()]
        return cls(bodies, **kwargs)

    def makeSparse(self, n=10):
        """Sparse the bodies."""
        for body in self.bodies:
            body.motion *= n

    def setRandomColors(self):
        """Set the colors of the bodies to random."""
        for body in self.bodies:
            for vector in body.motion:
                vector.color = mycolors.random()

    def spread(self, n=10):
        """Spread randomly the bodies."""
        for body in self.bodies:
            body.motion = n * Motion.random()

    def reactKeyDown(self, key):
        """React to a keydown event."""
        super().reactKeyDown(key)
        for body in self.bodies:
            body.reactKeyDown(key)

    def reactMouseMotion(self, event):
        """React to a mouse motion event."""
        super().reactMouseMotion(event)
        position = self.context.getFromScreen(tuple(event.pos))
        for body in self.bodies:
            body.reactMouseMotion(position)

    def reactMouseButtonDown(self, event):
        """React to a mouse button down event."""
        super().reactMouseButtonDown(event)
        position = self.context.getFromScreen(tuple(event.pos))
        for body in self.bodies:
            body.reactMouseButtonDown(event.button, position)


class GamePlayer(PlayableShooter, TriangleSpaceShip, ShowMotionSpaceShip):
    pass


class GameHunter(Hunter, TriangleSpaceShip):
    pass




if __name__ == "__main__":
    t = SpaceShipTester.random()
    t()
