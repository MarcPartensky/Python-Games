from myvector import Vector

import copy

class Force:
    def random(min=-1,max=1):
        """Return a random force."""
        vector=Vector.random(min,max)
        return Force(vector)

    def sum(forces):
        """Return the force that correspond to the sum of the forces."""
        resulting_force=Force(Vector())
        for force in forces:
            resulting_force+=force
        return resulting_force

    def __init__(self,vector,name="Unnamed"):
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

    def __iadd__(self,other):
        """Add a force to another."""
        self.vector+=other.vector
        return self


    def __str__(self):
        """Print the name of the force and its vector."""
        text="Force:name:"+self.name+",vector:"+str(self.vector)
        return text

    __repr__=__str__

    def __iter__(self):
        """Iterate using its internal vector."""
        return iter(self.vector)

    def __next__(self):
        """Return next component depending on the components of the internal vector."""
        return next(self.vector)

down=Vector([0,-1])
gravity=Force(9.81*down)

if __name__=="__main__":
    zero=Vector([0,0])
    propulsion=Force(zero)


    random_force=Force.random()
    random_force+=gravity
    print(random_force)


    result=Force.sum([gravity,propulsion])
    print(result)

    x,y=result
    print(x,y) #Unpacking is compatible for vectors
