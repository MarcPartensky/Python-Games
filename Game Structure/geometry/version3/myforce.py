from myvector import Vector

import copy

class Force:
    def __init__(self,vector,name="Unnamed Force"):
        """Create a force."""
        self.vector=vector
        self.name=name

    def __call__(self,motion):
        """Apply a force on a motion."""
        new_motion=copy.deepcopy(motion)
        new_motion.acceleration=self.vector
        return new_motion

    def __add__(self,other):
        """Added two forces together."""
        vector=self.vector+other.vector
        name=self.name+" and "+other.name
        return Force(vector,name)

    def __str__(self):
        """Print the name of the force and its vector."""
        text="Force: name:   "+self.name+"\n         vector: "+str(self.vector)
        return text

    __repr__=__str__




down=Vector([0,-1])
gravity=Force(9.81*down)

zero=Vector([0,0])
propulsion=Force(zero)

sum=gravity+propulsion
print(sum)
