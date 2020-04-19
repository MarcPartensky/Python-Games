from myentitygroup import EntityGroup
from myabstract import Vector
from myanatomies import FormAnatomy, SegmentAnatomy
from myasteroidanatomies import TriangleAnatomy
from myentity import LimitedEntity, LivingEntity, Entity
from mymotion import Motion, Moment
from myasteroidbase import SpiderBaseAnatomy
from myspaceshipbehaviours import Shoot
from pygame.locals import *

import mycolors
import time  # To time missiles life
import copy
import math


class SpaceShip(LivingEntity, LimitedEntity):
    """Base class of all spaceships."""
    @classmethod
    def random(cls, **kwargs):
        """Create a random spaceship."""
        motion = Motion.random(n=3, d=2)
        anatomy = FormAnatomy.random()
        return cls(anatomy, [motion], **kwargs)

    # def show(self, context):
    #     LivingEntity.show(self, context)


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
        super().__init__(anatomy, [motion, moment])


# class TriangleSpaceShip(SpaceShip):
#     @classmethod
#     def random(cls, sparse=100, **kwargs):
#         """Create a random triangle spaceship."""
#         return cls([sparse * Motion.random()], **kwargs)
#
#     def __init__(self, motion, **kwargs):
#         """Create a triangle spaceship."""
#         anatomy = FormAnatomy.createFromTuples([(1, 0), (-1, -1), (-0.5, 0), (-1, 1)], **kwargs)
#         anatomy.recenter()
#         super().__init__(anatomy, motion)
#
#     def getForm(self):
#         """Return the form."""
#         f = super().getForm()
#         f.side_color = mycolors.YELLOW
#         return f


class ShowMotionSpaceShip(SpaceShip):
    """SpaceShip that shows its motion."""

    def show(self, context):
        """Show the space ship and its motion."""
        super().show(context)
        self.showMotion(context)


class Missile(Entity):
    """Base class of all missiles."""

    def __init__(self, *args, target=None, damage=1, **kwargs):
        """Create a missile using the motion and the target."""
        self.target = target
        self.damage = damage
        super().__init__(*args, **kwargs)

    def hit(self, other):
        super().hit(other, self.damage)


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
        segment = SegmentAnatomy.createFromTuples((-0.5, 0), (0.5, 0))
        return cls(segment, [motion])

    def cross(self, other):
        p1, p2 = self.form
        if p1 in other or p2 in other:
            return True
        return False


class Shooter(SpaceShip):
    @classmethod
    def random(cls, **kwargs):
        """Create a shooter with a Shoot, TriangleAnatomy, and motion"""
        shoot = Shoot(SegmentMissile)
        anatomy = TriangleAnatomy()
        motion = Motion.random(n=3, d=2)
        return cls(anatomy, [motion], shoot)

    def __init__(self, anatomy, motions, shooting, **kwargs):
        """Space ship that can shoot."""
        self.shooting = shooting
        super().__init__(anatomy, motions, **kwargs)
        self.anatomy.side_color = mycolors.ORANGE  # Arbitrary choice made on purpose to distinguish entities for now
        self.activate()

    def shoot(self):
        return self.shooting(self.position, self.velocity, self.born)


class NShooter(Shooter):
    def __init__(self, *args, n=3, shooting_view=math.pi, **kwargs):
        super().__init__(*args, **kwargs)
        self.n = n
        self.shooting_view = shooting_view

    def shoot(self):
        """Return a missile with the same motion."""
        shooted = []
        for i in range(self.n):
            anatomy = SegmentAnatomy.createFromTuples((0, 0), (1, 0))
            angle = self.shooting_view * i / self.n
            anatomy.rotate(self.velocity.angle + angle)
            m = Motion(copy.deepcopy(self.position), copy.deepcopy(self.velocity))
            m.position += Vector.createFromPolar(self.born + 1, m.velocity.angle)
            m.velocity.norm += self.shooting_speed
            shooted.append(SegmentMissile(a, m))
        return shooted


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


class PlayableShooter(Shooter, PlayableSpaceShip):
    """Shooter that can be played by a player and so reacts to a space key event."""
    def __init__(self, *args, **kwargs):
        Shooter.__init__(self, *args, **kwargs)

    def reactKeyDown(self, key):
        """React to a key down event."""
        if key == K_SPACE:
            self.shooting.shooting = True


class Follower(MaxSpeedSpaceShip):
    """Entity that follows a target. It can be used to make self-guided missiles, or hunters."""
    def __init__(self, *args, target=None, **kwargs):
        """Create a follower entity."""
        self.target = target
        # if "target" in kwargs:
        #     self.target = kwargs.pop("target")
        # else:
        #     self.target = None
        super().__init__(*args, **kwargs)

    def update(self, dt):
        """Update the entity and follow it."""
        super().update(dt)
        if self.target is not None:
            self.acceleration.set(self.target.position - self.position)


class Hunter(Shooter, Follower):
    """Create a spaceship that hunts its targets."""
    def __init__(self, *args, shooting_view=2*math.pi, cool_down=3, **kwargs):
        super().__init__(*args, **kwargs)
        self.shooting_view = shooting_view
        self.cool_down = cool_down
        self.time = time.time()

    def update(self, dt):
        """Update the entity, follow it, and shoot at it when in range and in view."""
        super().update(dt)
        if self.target is not None:
            if time.time() - self.time > self.cool_down:
                self.hunt(dt)

    def hunt(self, dt):
        """Hunt the target supposing it exists."""
        v1 = self.target.position - self.position
        v2 = self.velocity
        if abs(v1.angle - v2.angle) <= self.shooting_view:
            distance = (self.position - self.target.position).norm
            if distance <= self.getShootingRange():
                self.shooting.shooting = True
                self.time = time.time()

    def getShootingRange(self):
        return self.shooting.speed * self.shooting.duration

    def retarget(self, target):
        self.target = target


class Asteroid(LivingEntity):
    """Mother class of all asteroids."""
    @classmethod
    def random(cls, n=5, size=5, life_factor=1/10, **kwargs):
        """Create a random asteroid."""
        a = FormAnatomy.random(n)
        mt = Motion.random(n=2, d=2)
        mm = Moment.random(n=2, d=1)
        a.enlarge(size)
        return cls(a, [mt, mm], alive=True, max_life=a.area*life_factor, **kwargs)


class SegmentMissilesGroup(EntityGroup):
    @classmethod
    def random(cls, n=20):
        """Create a random segment."""
        entities = [SegmentMissile.random() for i in range(n)]
        entities = dict(zip(range(len(entities)), entities))
        return cls(entities)


class GamePlayer(PlayableShooter, ShowMotionSpaceShip):
    @classmethod
    def random(cls, **kwargs):
        anatomy = TriangleAnatomy()
        motion = Motion.random(n=3, d=2)
        shoot = Shoot(SegmentMissile)
        return cls(anatomy, motion, shoot, **kwargs)

    def __init__(self, anatomy, motion, shoot, **kwargs):
        """Create a game player using its anatomy, motion, shoot attributes and kwargs."""
        PlayableShooter.__init__(self, anatomy, [motion], shoot, **kwargs)


class GameHunter(Hunter):
    @classmethod
    def random(cls, **kwargs):
        anatomy = TriangleAnatomy()
        motion = Motion.random(n=3, d=2)
        shoot = Shoot(SegmentMissile)
        return cls(anatomy, motion, shoot, **kwargs)

    def __init__(self, anatomy, motion, shoot, **kwargs):
        """Create a game player using its anatomy, motion, shoot attributes and kwargs."""
        super().__init__(anatomy, [motion], shoot, **kwargs)


if __name__ == "__main__":
    from mymanager import EntityManager

    class SpaceShipTester(EntityManager):
        def __init__(self, *entities, **kwargs):
            player = GamePlayer.random()
            entities = [player] + list(entities)
            super().__init__(*entities, **kwargs)

    t = SpaceShipTester()
    t()
