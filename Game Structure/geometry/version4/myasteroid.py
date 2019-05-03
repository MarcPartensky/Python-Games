from myabstract import Form
from mymaterialform import MaterialForm
from myplane import Plane

class Game:
    def __init__(self,window):
        """Create a game."""
        self.name="Asteroid"
        self.window=window
        self.window.name=self.name
        self.window.build()
        self.levels=[]

    def __call__(self):
        """Main loop of the game."""
        while surface.open:
            surface.check()


    def show(self):
        """Show the entities on screen."""

class Map(Plane):
    def __init__(self,*args,**kwargs):



class Level:
    def __init__(self,entities):
        """Create a level."""
        self.entities=entities

    def update(self):
        """Update all the entities."""
        for entity in self.entities:
            entity.update()

    def show(self,map):
        """Show all the entities."""
        for entity in self.entities:
            entity.show(map)

class Entity:
    def __init__(self):
        """Create a new entity."""



class Asteroid(MaterialForm,Entity):
    def __init__(self,*args,**kwargs):
        """Create an asteroid."""
        super().__init__(*args,**kwargs)

    def update(self):
        """Update the asteroid."""
        pass

class Spaceship(MaterialForm):
    def __init__(self,*args,**kwargs):
        """Create a space ship."""
        super().__init__(*args,**kwargs)

    def update(self):
        """Update the spaceship."""
        pass

    def control(self):
        """Control the spaceship."""
        pass

    def shoot(self,vector):
        """Return a missile that follow the vector."""
        motion=self.getMotion()
        return Missile(motion)




class Missile(MaterialForm):
    def __init__(self,motion):
        """Create a missile."""
        super().__init__(*args,**kwargs)

    def update(self):



class Player:
    def __init__(self):
        """Create a player."""


if __name__=="__main__":
    surface=Surface()
    game=Game(surface)
