from myabstract import Segment, Vector, Circle
from mymanager import EntityManager
from mymotion import Motion
from myentity import Entity


def crossCircleCircle(c1, c2):
    """Return the point of collision of 2 circles c1 and c2 if there is any."""
    vector = c1.position - c2.position
    radius = c1.radius + c2.radius
    if vector.norm < radius:
        v1 = -c1.radius * vector.unit
        v2 = c2.radius * vector.unit
        p1 = v1(c1.position)
        p2 = v2(c2.position)
        s = Segment(p1, p2)
        return s.middle


def bounceCircleCircle(c1, c2, v1, v2, m1, m2, p):
    """Make 2 circles bounce on upon another by returning their velocities."""
    vt1 = Vector(p, c1.radius)
    vt2 = Vector(p, c2.radius)

    return (v1, v2)


def crossCirclesEntities(e1, e2):
    print(e1.mass)


class CircleEntityTester(EntityManager):
    def __init__(self, n=10):
        entities = [Entity(Circle.random(), Motion.random()) for i in range(n)]
        super().__init__(entities)

    def update(self):
        super().update()
        n = len(self.entities)
        for i in range(n):
            for j in range(i+1, n):
                crossCirclesEntities(self.entities[i], self.entities[j])

if __name__=="__main__":
    m = CircleEntityTester()
    m()