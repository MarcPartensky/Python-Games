from myforce import Force
from mymotion import Motion
from myabstract import Point,Segment,Vector
from mycurves import Trajectory

import myforce
import math
import copy
import mycolors

digits=2

class MaterialPoint:
    def random(corners=[-1,-1,1,1],**kwargs):
        """Create a random material point using optional minimum and maximum."""
        motion=Motion.random(corners)
        return MaterialPoint(motion,**kwargs)

    def createFromPoint(point,forces=[]):
        """Create a material point from a Point instance."""
        position=Vector.createFromPoint(point)
        motion=Motion(position) #Initializing a motion instance
        return MaterialPoint(motion,forces) #Initializing a material point instance

    def __init__(self,motion=Motion(),forces=[],mass=1,color=mycolors.WHITE):
        """Create a material point."""
        self.motion=motion
        self.mass=mass
        self.forces=forces
        self.color=color

    def getTrajectory(self,t=1,split=1,**kwargs):
        """Return the trajectory of the point supposing it is not under any extern forces or restraints."""
        points=[]
        for i in range(split):
            point=self.getNextPoint(t)
            points.append(point)
        return Trajectory(points,**kwargs)


    def getSegment(self,t=1,**kwargs):
        """Return the direction made of the actual point and the future one."""
        p1=self.getPoint()
        p2=self.getNextPoint(t)
        return Segment(p1,p2,**kwargs)

    def getVector(self,t=1,**kwargs):
        """Return the vector made of the actual point and the future one."""
        p1=self.getPoint()
        p2=self.getNextPoint(t)
        return Vector.createFromTwoPoints(p1,p2,**kwargs)

    def getPoint(self,**kwargs):
        """Return the abstract point of the material point."""
        x,y=self.motion.getPosition()
        return Point(x,y,**kwargs)

    def getPosition(self):
        """Return the position of the material point."""
        return self.motion.getPosition()

    def setPosition(self,position):
        """Set the position of the material point."""
        self.motion.position=Vector(position)

    def getVelocity(self):
        """Return the velocity of the material point."""
        return self.motion.getVelocity()

    def setVelocity(self,velocity):
        """Set the velocity of the material point."""
        self.motion.velocity=Vector(velocity)

    def getAcceleration(self):
        """Return the acceleration of the material point."""
        return self.motion.getAcceleration()

    def setAcceleration(self,acceleration):
        """Set the acceleration of the material point."""
        self.motion.acceleration=Vector(acceleration)

    def getMass(self):
        """Return the mass of the material point."""
        return self.mass

    def setMass(self,mass):
        """Set the mass of the material point to the given mass."""
        self.mass=mass

    def getMotion(self):
        """Return the motion of the material point."""
        return self.motion

    def setMotion(self,motion):
        """Set the motion of the material point."""
        self.motion=motion

    def getNextPoint(self,t):
        """Return the future point."""
        return self.next(t).getPoint()

    def getNextPosition(self,t):
        """Return the next position of the object supposing there is no collisions."""
        self.motion.update(t)
        return self.getPosition()

    def getNextVelocity(self,t):
        """Return the next velocity of the object supposing there is no collisions."""
        self.motion.update(t)
        return self.getVelocity()

    def next(self,t):
        """Return the point after a t duration."""
        p=copy.deepcopy(self)
        p.update(t)
        return p

    def show(self,window,**kwargs):
        """Show the material point on the window."""
        point=self.getPoint()
        point.show(window,**kwargs)

    def showMotion(self,window):
        """Show the motion of a material point on the window."""
        position,velocity,acceleration=self.motion #Extract the vectors out of the motion.
        x,y=position
        point=Point(x,y)
        velocity.show(window,point)
        acceleration.show(window,point)

    def showText(self,*args,**kwargs):
        """Show the text on the screen."""
        p=self.getPoint()
        p.showText(*args,**kwargs)

    def update(self,t=1):
        """Update the motion of the material point."""
        force=Force.sum(self.forces)
        x,y=force
        acceleration=Vector(x,y)/self.mass
        self.motion.setAcceleration(acceleration)
        self.motion.update(t)

    def rotate(self,angle=math.pi,center=Point(0,0)):
        """Rotate the point using an angle and the point of rotation."""
        #for vector in self.motion:
            #vector.rotate(angle)
        #self.motion.position.rotate(angle)
        point=self.getPoint()
        point.rotate(angle,center)
        vector=Vector.createFromPoint(point)
        self.motion.setPosition(vector)

    def __iter__(self):
        """Iterate the position."""
        self.iterator=0
        return self

    def __next__(self):
        """Return the next point threw an iteration."""
        if self.iterator < 2:
            if self.iterator==0: value=self.motion.getPosition()[0]
            if self.iterator==1: value=self.motion.getPosition()[1]
            self.iterator+=1
            return value
        else:
            raise StopIteration

    def __str__(self):
        """Return the string representation of a point."""
        x,y=self.getPosition()
        x,y=round(x,digits),round(y,digits)
        return "mp("+str(x)+","+str(y)+")"

    __repr__=__str__

    def __getitem__(self,index):
        """Return x or y value using given index."""
        return self.getPosition()[index]

    def __setitem__(self,index,value):
        """Change x or y value using given index and value."""
        position=self.getPosition()
        position[index]=value
        self.setPosition(position)



FallingPoint=lambda :MaterialPoint(Motion.random(),[myforce.gravity])

if __name__=="__main__":
    from mysurface import Surface
    surface=Surface(name="Material Point Test")
    points=[MaterialPoint.random(color=mycolors.darken(mycolors.YELLOW)) for i in range(5)]
    while surface.open:
        surface.check()
        surface.clear()
        surface.control()
        surface.show()
        for point in points:
            point.showText(surface,point)
            point.update(t=0.1)
            t=point.getTrajectory(1,3,point_color=mycolors.darken(mycolors.RED))
            point.show(surface,color=mycolors.RED,mode="cross")
            point.showMotion(surface)
            t.show(surface)
        surface.flip()
