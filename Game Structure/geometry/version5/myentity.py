from mybody import Body


class Entity(Body):
    """An entity is a body that can be alive and active."""

    def __init__(self, anatomy, *motions,
                 alive=True, friction=1e-2, active=False):
        """Create an entity."""
        super().__init__(anatomy, *motions)
        self.alive = alive
        self.friction = friction
        self.active = active

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

    def setFriction(self, friction):
        """Set the friction to the given friction."""
        self.friction = friction

    def spread(self, n):
        """Take away the entity by multiplying the norm of the position by n."""
        self.position.norm *= n

    def enlarge(self, n):
        """Enlarge the anatomy."""
        self.anatomy.enlarge(n)


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
            if self.position.x>=0:
                self.position.x = -lx
            else:
                self.position.x = lx
        if abs(self.position.y) > ly:
            if self.position.y>=0:
                self.position.y = -ly
            else:
                self.position.y = ly


if __name__ == "__main__":
    print(ResponsibleEntity.random())
    l=LimitedEntity.random()
    print(l)
    l.limit()
    print(l)
    print(l.limit)
    l.update(1)
