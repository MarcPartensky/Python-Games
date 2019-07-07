class Missile(Body):
    def __init__(self,form,motion=Motion(d=2),moment=Motion(d=1)):
        """Create body using form and optional name."""
        self.form=form
        self.motion=motion
        self.moment=moment


class Spaceship(Body):
    def __init__(self,form,motion=Motion(d=2),moment=Motion(d=1)):
        """Create body using form and optional name."""
        self.form=form
        self.motion=motion
        self.moment=moment
        self.missiles=[]
