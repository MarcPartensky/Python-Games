from mymanager import BodyManager
from mycurves import Trajectory
from myabstract import Point
from mybody import Body

import random

# Interface Anatomy
# - show(context)   //an anatomy must be responsible for drawing itself
# - __str__()           //an anatomy must be able to give a string representation
# - __contains__(point) //an anatomy must be able to tell if a point is in it
# - cross(anatomy)  //an anatomy must be able to determine if it is crossing another anatomy
# - recenter()
# - update()
# . center          //an anatomy must have a center

# image, segment and form implement anatomy


class Anatomy:
    """Interface anatomy."""
    @classmethod
    def random(cls):
        raise NotImplementedError("This method must be overloaded.")
    def __init__(self):
        raise NotImplementedError("This method must be overloaded.")
    #def update(self):
    #    raise NotImplementedError("This method must be overloaded.")
    def show(self,context):
        raise NotImplementedError("This method must be overloaded.")
    def rotate(self,r):
        raise NotImplementedError("This method must be overloaded.")


class TrajectoryAnatomy(Trajectory):
    @classmethod
    def random(cls,nmin=5,nmax=20):
        """Create a random trajectory anatomy."""
        n=random.randint(nmin,nmax)
        ru=random.uniform
        points=[(ru(-10,10),ru(-10,10)) for i in range(n)]
        return cls.createFromTuples(points)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def rotate(self,angle):
        """Rotate around its center."""
        c=Point(*self.center)
        for point in self.points:
            point.rotate(angle,c)


#ta=TrajectoryAnatomy.random()
#print(type(ta))
#b=Body.createFromRandomMotions(ta)


if __name__=="__main__":
    #m=BodyManager([b])
    #m()
