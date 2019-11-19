from pygame.locals import KEYDOWN, MOUSEBUTTONDOWN, MOUSEMOTION
from myrectangle import Rectangle
from mybody import Body

import mycolors

class Entity(Body):
    """An entity is a body that can be alive and active."""

    def __init__(self, anatomy, *motions,
                 life=1, max_life=1,
                 alive=None, active=False,
                 friction=1e-2, ):
        """Create an entity."""
        super().__init__(anatomy, *motions)
        self.max_life = max_life
        if alive is None:
            self.life = life
        else:
            if alive:
                self.life = max_life
            else:
                self.life = 0
        self.active = active
        self.friction = friction

    def getAlive(self):
        return self.life > 0

    def setAlive(self, alive):
        if alive:
            self.life = self.max_life
        else:
            self.life = 0

    alive = property(getAlive, setAlive)

    def hit(self, damage):
        """Receive damage."""
        self.life = max(self.life - damage, 0)

    def __str__(self):
        """Return the string representation of an entity."""
        return type(self).__name__ + "(" + str(self.form) + "," + \
               ",".join(map(str, self.motions)) + ")"

    def spawn(self):
        """Spawn the entity."""
        self.alive = True

    def respawn(self):
        """Respawn an entity by simply spawning it."""
        self.spawn()

    def die(self):
        """Kill the entity by setting alive status to false."""
        self.alive = False

    def update(self, dt):
        """Update the spaceship."""
        super().update(dt)
        self.updateFriction()

    def updateFriction(self):
        """Add some friction."""
        self.velocity.norm *= (1 - self.friction)

    def activate(self):
        """Activate the entity to events."""
        self.active = True

    def deactivate(self):
        """Deactivate the entity to events."""
        self.active = False

    def reactKeyDown(self, key):
        """React to a key down event."""
        pass

    def reactMouseMotion(self, position):
        """React to a mouse motion event."""
        pass

    def reactMouseButtonDown(self, button, position):
        """React to a mouse button down event."""
        pass

    def react(self, event):
        """React to the pygame events."""
        if event.type == KEYDOWN:
            self.reactKeyDown(event.key)
        elif event.type == MOUSEBUTTONDOWN:
            self.reactMouseButtonDown(event.button, event.pos)
        elif event.type == MOUSEMOTION:
            self.reactMouseMotion(event.pos)

    def setFriction(self, friction):
        """Set the friction to the given friction."""
        self.friction = friction


class LivingEntity(Entity):
    def showLife(self, context):
        """Show the life with a rectangle."""
        r1, r2 = self.life_rectangles
        r2.show(context)
        r1.show(context)

    @property
    def life_rectangles(self):
        margin = 0.1
        x, y = self.x, self.y
        y -= (self._born + margin)
        w, h = self._born, margin
        w1 = w * self.life/self.max_life
        x1 = x-w/2+w1/2
        r1 = Rectangle([x1, y], [w1, h], area_color=mycolors.GREEN, fill=True, point_show=False)
        r2 = Rectangle([x, y], [w, h], side_color=mycolors.WHITE, point_show=False)
        return [r1, r2]

    def show(self, context):
        super().show(context)
        self.showLife(context)


class ResponsibleEntity(Entity):
    """Entity which updates its anatomy."""
    def update(self, dt):
        """Update the motion and anatomy."""
        super().update(dt)
        self.anatomy.update(dt)


class LimitedEntity(Entity):
    def __init__(self, *args, limits=[100, 100], **kwargs):
        """Create an entity which stays within the given limits."""
        super().__init__(*args, **kwargs)
        self.limits = limits

    def update(self, dt):
        """Update the limited group and limit it."""
        super().update(dt)
        self.limit()

    def limit(self):
        """Limit the position of the entity."""
        lx, ly = self.limits
        if abs(self.position.x) > lx:
            if self.position.x >= 0:
                self.position.x = -lx
            else:
                self.position.x = lx
        if abs(self.position.y) > ly:
            if self.position.y >= 0:
                self.position.y = -ly
            else:
                self.position.y = ly


if __name__ == "__main__":
    entity = LivingEntity.random(nv=2)
    entity.life = 0.5

    from mymanager import EntityManager
    m = EntityManager(entity)
    m()

