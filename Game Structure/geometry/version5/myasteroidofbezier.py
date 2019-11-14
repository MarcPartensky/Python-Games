from mycurves import BezierForm
from mymotion import Motion, Moment
from myentity import Entity

class BezierAsteroid(Entity):
    @classmethod
    def random(cls,**kwargs):
        """Create a random bezier asteroid."""
        a=BezierForm.random(**kwargs)
        mt=Motion.random(n=2,d=2)
        mm=Moment.random(n=2,d=1)
        return cls(a,mt,mm)


if __name__=="__main__":
    from mymanager import Manager
    class AnatomyTester(Manager):
        def __init__(self,anatomy,**kwargs):
            super().__init__(**kwargs)
            self.anatomy=anatomy
        def show(self):
            self.anatomy.show(self.context)
        def update(self):
            self.anatomy.rotate(0.1)

    caa= CurvedAsteroidAnatomy.random(,
    t=AnatomyTester(caa)
    t()
