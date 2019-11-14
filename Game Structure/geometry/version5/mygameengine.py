from mycontext import Surface


class Game:
    """Main class to use in future games."""

    def __init__(self, context, levels):
        """Create a game engine."""
        self.context = context
        self.levels = levels
        self.stage = None

    def play(self):
        """Main loop of the game engine."""
        while self.on:
            self.events()
            self.update()
            self.show()

    def events(self):
        """Update and keep all the keys."""
        self.keys = self.context.press()

    def update(self):
        """Update all the entities."""
        self.levels[self.stage].set(self.keys)
        self.levels[self.stage].update()

    def show(self):
        """Show the entities on screen."""
        self.system.show(self.context)


class Level:
    def __init__(self, system):
        """Create a level using a system of entities."""
        self.system = system

    def play(self):
        """Main loop of the game engine."""
        while self.on:
            self.events()
            self.update()
            self.show()

    def events(self):
        """Update and keep all the keys."""
        self.keys = self.context.press()

    def set(self, keys):
        """Save the actual keys to update later on."""
        self.system.set(keys)

    def update(self):
        """Update the level. This method should be overloaded by the clients."""
        self.system.update()


class System:
    """Handles all the entities of the game, allow the client to control them
    without difficulty."""

    def __init__(self, static=[], dynamic=[], fields=[]):
        """Create a system using static and dynamic entities with force fields."""
        self.static = static
        self.dynamic = dynamic
        self.fields = fields

    def set(self, keys):
        """Save the actual keys to update later on."""
        self.keys = keys

    def update(self):
        """Update all the entities making sure they interact with each others
        the right way."""
        self.updateControls()
        self.updateForces()
        self.updatePhysics()

    def updateControls(self):
        """Update all the controls of the entities."""
        pass

    def updateForces(self):
        """Update all the forces of the dynamic objects."""
        for field in self.fields:
            for entity in self.dynamic:
                if entity in field:
                    entity.subject(field)

    def updatePhysics(self):
        """Update all the objects according to physics rules."""

    def show(self, context):
        """Show all the entities on the screen."""
        self.showStatic()
        self.showDynamic()

    def showStatic(self):
        """Show all the statics entities on screen."""
        for entity in self.static:
            entity.show(self.context)

    def showDynamic(self):
        """Show all the dynamics entities on screen."""
        for entity in self.dynamic:
            entity.show(self.context)


if __name__ == "__main__":
    context = Surface()
    system = System()
    game = GameEngine(context)
