from mymaterialform import MaterialForm
from mymaterialpoint import MaterialPoint
from myabstract import Vector,Segment
from mymotion import Motion
import itertools
import mycolors

class MaterialCollider:
    """Class made especially to deal with one to one collisions."""
    def __init__(self):
        """Create a collider."""
        pass

    def set(self,object1,object2):
        """Set the objects of the collider."""
        self.object1=object1
        self.object2=object2

    def collide(self):
        """Deal with the collisions of two objects."""
        pass

    def getCollisionInstant(self):
        """Return the instant of the collision of two objects."""
        bt=1
        #steps=itertools.combinations(itertoolself.object1.steps,self.object2.steps)
        allsteps=[(s1,s2) for s1 in self.object1.steps for s2 in self.object2.steps]
        points=[self.isColliding(steps) for steps in allsteps]
        allsteps=itertools.compress(allsteps,points)
        instants=list(map(self.getInstant,allsteps))
        return min(instants+[1])

    def isColliding(self,steps):
        """Determine is the steps are colliding."""
        return steps[0].crossSegment(steps[1]) is not None

    def getInstant(self,steps):
        """Return the minimum of the instant of the point to the begining of the segments."""
        st1=steps[0]
        st2=steps[1]
        p=st1.crossSegment(st2)
        t1=Segment(st1.p1,p).length/st1.length
        t2=Segment(st1.p2,p).length/st2.length
        return min(t1,t2)


    def getCollisionPoints(self):
        """Return the points of collisions of the steps of the two objects."""
        points=[]
        for step1 in self.object1.steps:
            for step2 in self.object2.steps:
                point=step1.crossSegment(step2)
                if point:
                    points.append(point)
        return points


    def __call__(self,object1,object2):
        """Deal with the collisions of two objects."""
        pass
        return [object1,object2]

    def isInContact(self):
        """Determine if the two objects are actually in contact or not."""
        return self.object1.abstract|self.object2.abstract != []

class MaterialGroup:
    """Class used to manipulate groups of material objects together."""
    def __init__(self,*objects,collider=MaterialCollider()):
        """Create a material group with the list of objects."""
        self.objects=objects
        self.collider=collider

    def show(self,context):
        """Show all the objects on screen."""
        for object in self.objects:
            object.show(context)

        l=len(self.objects)
        for i in range(l):
            for j in range(1,l):
                self.collider.set(self.objects[i],self.objects[j])
                if self.collider.isInContact():
                    for s1 in self.objects[i].segments:
                        for s2 in self.objects[j].segments:
                            points=self.objects[i]|self.objects[j]

                            for point in points:
                                point.show(context,mode="cross",color=mycolors.YELLOW,width=3)
                            self.objects[i].side_color=mycolors.RED
                            self.objects[j].side_color=mycolors.RED


    def update(self,dt=1):
        """Update all the objects together accounting for their collisions."""
        for object in self.objects:
            object.update(dt)

    def getCollisionInstant(self,dt=1):
        """Return precisely the time of the first collision between all objects."""
        bt=1
        l=len(self.objects)
        for i in range(l):
            for j in range(1,l):
                self.collider.set(self.objects[i],self.objects[j])
                t=self.collider.getCollisionInstant()
                if t<bt:
                    bt=t
        return t

    def directUpdate(self,dt=1):
        """Update all the objects without accounting for their collisions."""
        for object in self.objects:
            object.update(dt)

    def collideWithGroup(self,group):
        """Deal with the collisions of the object of the group with another group."""
        pass

if __name__=="__main__":
    from mysurface import Context
    context=Context(name="Material Group Test")
    f1=MaterialForm.random()
    f1.motion=Motion(Vector(0,2),Vector(0,-0.5),Vector(0,-0.1))
    f2=MaterialForm.random()
    f2.motion=Motion.null()
    g=MaterialGroup(f1,f2)
    t=g.getCollisionInstant(1)
    print(t)
    while context.open:
        context.check()
        context.control()
        context.clear()
        context.show()
        g.update(dt=0.01)
        g.show(context)
        context.flip()
