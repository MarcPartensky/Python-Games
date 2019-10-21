from myabstract import Form
from mymaterialform import MaterialForm
from myplane import Plane


class Game(Manager):
    def __init__(self, name, **kwargs):
        """Create a game."""
        super().__init__(**kwargs)
        self.context.name = name
        self.levels = []
        self.level = 0


class Level:
    def __init__(self, entities):
        """Create a level."""
        self.entities = entities

    def update(self):
        """Update all the entities."""
        for entity in self.entities:
            entity.update()

    def show(self, map):
        """Show all the entities."""
        for entity in self.entities:
            entity.show(map)


class Entity(Body):
    def __init__(self):
        """Create a new entity."""
        pass


class Asteroid(Physics):
    def __init__(self, absolute):
        """Create an asteroid."""
        super().__init__(*args, **kwargs)

    def show(self, context):
        """Show the asteroid on the context."""
        self.form.show(context)

    form = property(getForm)


class Spaceship(MaterialForm):
    def __init__(self, *args, **kwargs):
        """Create a space ship."""
        super().__init__(*args, **kwargs)

    def update(self):
        """Update the spaceship."""
        pass

    def control(self):
        """Control the spaceship."""
        pass

    def shoot(self, vector):
        """Return a missile that follow the vector."""
        motion = self.getMotion()
        return Missile(motion)


class Missile(MaterialForm):
    def __init__(self, motion):
        """Create a missile."""
        super().__init__(*args, **kwargs)


class Player:
    def __init__(self):
        """Create a player."""


if __name__ == "__main__":
    from mycontext import Context
    context = Context()
    game = Game(context)
