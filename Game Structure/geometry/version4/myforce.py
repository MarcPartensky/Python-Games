from myabstract import Vector
from mymotion import Motion

p=2 #Number of digits of precision of the objects when displayed


class Force(Vector):
    def __init__(self,*args,**kwargs):
        """Create a force."""
        super().__init__(*args,**kwargs)

    def __call__(self,motion):
        """Apply a force on a motion."""
        new_motion=copy.deepcopy(motion)
        new_motion.acceleration=self.vector
        return new_motion

    def show(self,surface):
        """New dope show method especially for the forces."""
        raise Exception("Not operational")

    def __str__(self):
        """Return the string representation of the object."""
        x=round(self.x,p)
        y=round(self.y,p)
        return "f("+str(x)+","+str(y)+")"



down=Vector([0,-1])
gravity=Force(0,-9.81)

if __name__=="__main__":
    zero=Vector([0,0])
    propulsion=Force(0,0)

    random_force=Force.random()
    print(random_force)
    random_force+=gravity
    print(random_force)

    result=Force.sum([gravity,propulsion,random_force])
    print("Force.sum:",result)

    x,y=result
    print(x,y) #Unpacking is compatible for vectors
