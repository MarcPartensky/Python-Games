from myabstract import Segment, Vector
from myanatomies import CircleAnatomy
from mymanager import EntityManager
from mymotion import Motion
from myentity import Entity
from myrectangle import Square

import math


class DeprecatedCollider:

    def __call__(self, entity1, entity2):
        if (entity1.position-entity2.position).norm < entity1.anatomy.radius + entity2.anatomy.radius:
            x1, y1 = entity1.position
            x2, y2 = entity2.position
            m1 = entity1.mass
            m2 = entity2.mass
            if x2 != x1:
                angle = -math.atan((y2 - y1) / (x2 - x1))
                ux1, uy1 = self.rotate(entity1.velocity, angle)
                ux2, uy2 = self.rotate(entity2.velocity, angle)
                v1 = Vector(self.project(ux1, ux2, m1, m2), uy1)
                v2 = Vector(self.project(ux2, ux1, m1, m2), uy2)
                entity1.velocity = self.rotate(v1, -angle)
                entity2.velocity = self.rotate(v2, -angle)

    def project(self, v1, v2, m1, m2):
        return (m1 - m2) / (m1 + m2) * v1 + (2 * m2) / (m1 + m2) * v2

    def rotate(self, velocity, angle):
        vx, vy = velocity
        nvx = vx * math.cos(angle) - vy * math.sin(angle)
        nvy = vx * math.sin(angle) + vy * math.cos(angle)
        return [nvx, nvy]


class Collider:
    def __init__(self, elasticity=1e-5):
        self.elasticity = elasticity

    def collide(self, e1, e2):
        """Determine if their is a collision or not."""
        vector = e1.position - e2.position
        radius = e1.born + e2.born
        if vector.norm < radius:
            return e1.collide(e2)
        else:
            return False


class CircleCollider(Collider):

    def cross(self, e1, e2):
        vector = e1.position - e2.position
        radius = e1.anatomy.radius + e2.anatomy.radius
        if vector.norm < radius:
            v1 = -e1.anatomy.radius * vector.unit
            v2 = e2.anatomy.radius * vector.unit
            p1 = v1(e1.position)
            p2 = v2(e2.position)
            s = Segment(p1, p2)
            return s.middle

    def collide(self, e1, e2):
        """Determine whether there is a collision or not."""
        vector = e1.position - e2.position
        radius = e1.anatomy.radius + e2.anatomy.radius
        return vector.norm < radius

    def correctOverlapping(self, e1, e2):
        # We correct the overlapping
        tangent = math.atan2(e2.y - e1.y, e2.x - e1.x)
        vector = e1.position - e2.position
        radius = e1.anatomy.radius + e2.anatomy.radius
        r = (vector.norm - radius) / 2
        angle = 0.5 * math.pi + tangent
        e1.x += r * math.sin(angle)
        e1.y -= r * math.cos(angle)
        e2.x -= r * math.sin(angle)
        e2.y += r * math.cos(angle)


class CircleCollider1(CircleCollider):
    def __call__(self, e1, e2):
        # We check the collision
        if self.collide(e1, e2):
            # We redirect the velocities
            tangent = math.atan2(e2.y - e1.y, e2.x - e1.x)
            e1.velocity.angle = 2 * tangent - e1.velocity.angle
            e2.velocity.angle = 2 * tangent - e2.velocity.angle
            e1.velocity.norm, e2.velocity.norm = e2.velocity.norm, e1.velocity.norm
            e1.velocity.norm *= 1-self.elasticity
            e2.velocity.norm *= 1-self.elasticity


class CircleCollider2(CircleCollider):
    def __call__(self, e1, e2):
        # We check the collision
        if self.collide(e1, e2):
            # We redirect the velocities
            angle = math.atan2(e2.y - e1.y, e2.x - e1.x)
            e1.velocity.angle = -angle
            e2.velocity.angle = angle
            mass = e1.mass + e2.mass
            velocity = e1.velocity + e2.velocity
            e1_velocity_norm = (velocity.norm*mass - e2.velocity.norm*e2.mass) / e1.mass
            e2_velocity_norm = (velocity.norm*mass - e1.velocity.norm*e1.mass) / e2.mass
            e1.velocity.norm = e1_velocity_norm
            e2.velocity.norm = e2_velocity_norm

            # pm = p1 + p2
            # v*m = v1*m1 + v2*m2
            # v1 = (v*m - v2*m2) / m1


class CircleCollider3(CircleCollider):
    def __call__(self, e1, e2):
        # We check the collision
        if self.collide(e1, e2):
            # We redirect the velocities
            v1 = (e1.mass-e2.mass)/(e1.mass+e2.mass) * e1.velocity + \
                 (2*e2.mass)/(e1.mass+e2.mass) * e2.velocity
            v2 = (e2.mass-e1.mass)/(e1.mass+e2.mass) * e2.velocity + \
                 (2*e1.mass)/(e1.mass+e2.mass) * e1.velocity
            e1.velocity.set(v1)
            e2.velocity.set(v2)
            # We correct the overlapping
            self.correctOverlapping(e1, e2)


class FormWithCircleCollider(Collider):
    def __call__(self, e1, e2):
        p = e1.cross(e2)
        if p:
            pass


class CircleEntityTester(EntityManager):
    def __init__(self, n=10, s=5, g=10, radius_borns=[1, 10], **kwargs):
        entities = [Entity(CircleAnatomy.random(radius_borns=radius_borns), \
                    [Motion(s*Vector.random(), 10*Vector.random(), Vector(0, -g))], friction=0) \
                    for i in range(n)]
        super().__init__(*entities, **kwargs)
        self.collider = CircleCollider3(elasticity=0.6)
        self.born = s
        self.born_elasticity = 0.5
        self.square = Square((0, 0), 2 * self.born)
        self.correctMasses()

    def correctMasses(self):
        for entity in self.entities:
            entity.mass = entity.anatomy.radius

    def update(self):
        super().update()
        for i, e1 in enumerate(self.entities):
            for e2 in self.entities[i+1:]:
                self.collider(e1, e2)
            self.limit(e1)

    def show(self):
        super().show()
        self.square.show(self.context)

    def limit(self, e):
        l = self.born_elasticity
        r = e.anatomy.radius
        if e.x > self.born - r:
            e.x = self.born - r
            e.vx *= -l
        if e.x < -self.born + r:
            e.x = -self.born + r
            e.vx *= -l
        if e.y > self.born - r:
            e.y = self.born - r
            e.vy *= -l
        if e.y < -self.born + r:
            e.y = -self.born + r
            e.vy *= -l


if __name__ == "__main__":
    m = CircleEntityTester(n=100, s=5, dt=0.01, radius_borns=[0.2, 0.3])
    m()
