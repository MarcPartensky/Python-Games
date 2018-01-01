from myform import Form
from mysurface import Surface
from myforce import gravity,propulsion

class Body:
    def __init__(self,form,name="Unnamed entity"):
        """Create body using form and optional name."""
        self.name=name
        self.form=form
        self.next_motion=Motion()
        self.previous_motion=Motion()
        self.max_motion=Motion()# Not working
        #self.forces={"gravity":gravity,"propulsion":propulsion}
        self.forces={"propulsion:",propulsion}

    def getMass(self):
        """Return the mass of the object using the area."""
        area=self.form.area()
        k=1
        mass=k*area
        return mass


    def spawn(self,base):
        pass

    def show(self,window):
        """Show the form on the window."""
        self.form.show()

    def move(self,t=1):
        """Move entity according to its acceleration, velocity and position."""
        self.motion(t)
        self.last_motion(t)

    def moveToward(self,position):
        """Changes the force corresponding to the propulsion."""
        #self.direction=
        pass

    def apply(self,forces):
        """Apply the forces on the body."""
        resulting_force=sum(self.forces)
        self.next_motion.acceleration=resulting_force

    def __call__(self):
        pass


    def control(self,window):
        """Control the view of the plane."""
        keys=window.press()
        if keys[K_UP]:
            self.forces["propulsion"][1]=1
        if keys[K_DOWN]:
            self.forces["propulsion"][1]=-1
        if keys[K_LEFT]:
            self.forces["propulsion"][0]=-1
        if keys[K_RIGHT]:
            self.forces["propulsion"][0]=1



if __name__=="__main__":
    surface=Surface()
    body=Body()
    body.spawn()
    while surface.open:
        surface.check()
        surface.clear()
        body.control()
        body.show(window)
        surface.flip()
