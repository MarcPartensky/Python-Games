"""Detect collisions between abstract forms."""
from myabstract import Segment, Form
from mymanager import AbstractManager

import mycolors


def crossSegmentForm(segment, form):
    for s in form.segments:
        if Segment.cross(segment, s):
            return True
    if segment.p1 in form:
        return True
    if segment.p2 in form:
        return True
    return False


class AbstractCollision:
    pass


class AbstractCollisionManager(AbstractManager):
    def __init__(self, **kwargs):
        f,s = Form.random(), Segment.random()
        super().__init__(s, f)

    def update(self):
        self.group[0].center = self.context.point()
        if crossSegmentForm(self.group[0], self.group[1]):
            self.group[0].color = mycolors.RED
        else:
            self.group[0].color = mycolors.GREEN


if __name__ == "__main__":
    m = AbstractCollisionManager()
    m()