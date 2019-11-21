from myspaceship import SegmentMissile
from myabstract import Segment, Vector
from mymotion import Motion

import copy


class Update:
    def __init__(self):
        pass

    def __call__(self, dt, group):
        group.update(dt)


class ResponsibleUpdate(Update):

    def __call__(self, dt, group, anatomy):
        super().__call__(group, dt)
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
                 shooting_speed=10,
                 shooting_type=SegmentMissile,
                 damage=1
                 ):
        self.shooting_speed = shooting_speed
        self.shooting_type = shooting_type
        self.damage = damage

    def shoot(self, position, velocity, born):
        """Return a missile with the same motion."""
        s = Segment.createFromTuples((0, 0), (1, 0))
        s.rotate(velocity.angle)
        m = Motion(copy.deepcopy(position), copy.deepcopy(velocity))
        m.position += Vector.createFromPolar(born + 1, velocity.angle)
        m.velocity.norm += self.shooting_speed
        return [self.shooting_type(s, m, damage=self.damage)]


class NShoot(Shoot):
    def __init__(self, n,
                 shooting_view,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        self.n = n
        self.shooting_view = shooting_view

    def __call__(self):
        """Return a missile with the same motion."""
        self.shooting = False
        shooted = []
        for i in range(self.n):
            s = Segment.createFromTuples((0, 0), (1, 0))
            angle = self.shooting_view * i / self.n
            s.rotate(self.velocity.angle + angle)
            m = Motion(copy.deepcopy(self.position), copy.deepcopy(self.velocity))
            m.position += Vector.createFromPolar(self.born + 1, m.velocity.angle)
            m.velocity.norm += self.shooting_speed
            shooted.append(self.shooting_type(s, m))
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
