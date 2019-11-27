from myanatomies import SegmentAnatomy
from myabstract import Vector
from mymotion import Motion

import copy


class Update:
    def __init__(self):
        pass

    def __call__(self, dt, group):
        group.update(dt)


class ResponsibleUpdate:
    def __call__(self, dt, group, anatomy):
        group.update(dt)
        anatomy.update(dt)


class Show:
    """Show Behaviour."""
    def __init__(self):
        pass

    def __call__(self, context):
        pass


class Follow:
    def __init__(self, position):
        self.position = position


class Shoot:
    """Shooting Behaviour."""
    def __init__(self,
                 shooting_type,
                 speed=10,
                 shooting=False,
                 damage=1
                 ):
        self.type = shooting_type
        self.speed = speed
        self.shooting = shooting
        self.damage = damage

    def __bool__(self):
        return self.shooting

    def __call__(self, position, velocity, born):
        """Return a missile with the same motion."""
        s = SegmentAnatomy.createFromTuples((0, 0), (1, 0))
        s.angle = velocity.angle
        m = Motion(copy.deepcopy(position), copy.deepcopy(velocity))
        m.position += Vector.createFromPolar(born + 1, velocity.angle)
        m.velocity.norm += self.speed
        self.shooting = False
        return [self.type(s, [m], damage=self.damage)]

    def __str__(self):
        return type(self).__name__+"("+",".join(map(lambda tp: ":".join(map(str, tp)), list(self.__dict__.items())))+")"


class NShoot(Shoot):
    """Shoot n missiles."""
    def __init__(self, n,
                 view,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        self.n = n
        self.view = view

    def __call__(self, position, velocity, born):
        """Return a missile with the same motion."""
        self.shooting = False
        shooted = []
        for i in range(self.n):
            s = SegmentAnatomy.createFromTuples((0, 0), (1, 0))
            s.angle = velocity.angle
            angle = self.view * i / self.n
            s.rotate(velocity.angle + angle)
            m = Motion(copy.deepcopy(position), copy.deepcopy(velocity))
            m.position += Vector.createFromPolar(born + 1, m.velocity.angle)
            m.velocity.norm += self.speed
            shooted.append(self.type(s, [m]))
        return shooted


class Hunt:
    def __init__(self, shoot, follow):
        self.shoot = shoot
        self.follow = follow


class Limit1D:
    """Limit1D Behaviour."""
    def __init__(self, limit):
        self.limit = limit

    def __call__(self, vector):
        """Limit the norm of a vector."""
        vector.norm = min(vector.norm, self.limit)


class Limit2D:
    """Limit2D Behaviour."""

    def __init__(self, limits):
        self.limits = limits

    def __call__(self, vector):
        """Limit the x and y components of a vector."""
        lx, ly = self.limits
        if vector.x > lx:
            vector.x = -lx
        elif vector.x < -lx:
            vector.x = lx
        if vector.y > ly:
            vector.y = -ly
        elif vector.y < -ly:
            vector.y = ly


class Life:
    def __init__(self, value=1, max_value=1):
        self.value = value
        self.max_value = max_value

    def show(self, context):
        pass


from myentity import Entity
#
# class Entity:
#     def __init__(self, anatomy, motions):
#
# class SpaceShip(Entity):
#     def __init__(self, anatomy, motions, update, show):
#         super().__init__(anatomy, *motions)
#         self.update = update
#         self.show = show
#
#
# class Shooter(SpaceShip):
#     def __init__(self, anatomy, motions, update, show, shoot):
#         super().__init__(anatomy, motions, update, show)
#         self.shoot = shoot
#
#

if __name__ == "__main__":
    s = Shoot(None)
    print(s)

