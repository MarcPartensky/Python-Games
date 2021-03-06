from myabstract import Circle,Vector
from mymotion import Motion
from mymaterial import Material
from mybody import Body
from myforce import Force

import math

G=6.67408e-11

class Galaxy:
    def __init__(self):
        pass


class System:
    def __init__(self):
        self.astres=[Star()]+[Astre() for i in range()]
    def __call__(self,context,dt):
        while context.open:
            self.update(dt)
            self.show(context)
    def show(self,context):
        context.check()
        context.control()
        context.clear()
        context.show()
        self.showAstres(context)
        context.flip()
    def showAstres(self,context):
        for astre in self.astres:
            astre.show(context)
    def update(self,dt):
        self.updateAstres(dt)
    def updateAstres(self,dt):
        for astre in self.astres:
            astre.update(dt)
    def distance(self,astre1,astre2):
        return math.sqrt(sum([(c1-c2)**2 for (c1,c2) in zip(astre1.position,astre2.position)]))
    def attraction(self,astre1,astre2):
        """Return the force of attraction of the 2 astres together."""
        norm=G*astre1.mass*astre2.mass/self.distance(astre1,astre2)
        return Force.createFromPolarCoordonnates(norm,angle)

class Astre(Body):
    def __init__(self,name="Unnamed",radius,mass,motion,color):
        self.name=name
        self.radius=radius
        self.mass=mass
        self.motion=motion
        self.color=color
    def show(self,context):
        x,y=self.position
        c=Circle(x,y,self.radius,self.color)
        c.show(context)
        c.showText(self.name)
    def update(self,t):
        self.motion.update(t)


class Planet(Astre):
    def __init__(self):
        pass

    def show(self,context):
        pass


class Star(Astres):
    def __init__(self):
        pass



if __name__=="__main__":
    from mysurface import Context
    context=Context()
    s=System()
    s()
