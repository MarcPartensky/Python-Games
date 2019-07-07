from myabstract import Form,Vector
from mybody import Body
from mymotion import Motion
from mysurface import Context
import socket

import mycolors
import copy

class AsteroidGame:
    def createRandomBody(self):
        """Create a random body."""
        form=5*Form.random(n=5)
        form.side_color=mycolors.RED
        form.area_color=mycolors.BLACK
        form.fill=True
        motion=Motion(10*Vector.random(),Vector.random(),Vector.null())
        moment=Motion(Vector([1]),Vector([0.1]))
        return Body(form,motion,moment)

    def showInfo(self):
        """Show informations about the bodies on the game."""
        if self.missile is not None:
            self.context.draw.window.print(str(self.missile.velocity),(10,10),20)
