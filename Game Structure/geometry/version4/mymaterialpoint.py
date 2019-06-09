from myforce import Force
from mymotion import Motion
from myabstract import Point,Segment,Vector
from mycurves import Trajectory
from mymaterial import Material

import myforce
import math
import copy
import mycolors

digits=2

class MaterialPoint(Material,Point):
    def null(n=3,d=2):
        """Return the neutral material point."""
        return MaterialPoint(Motion.neutral(n=n,d=d))

    def sum(points,d=2):
        """Return the sum of the material points."""
        result=MaterialPoint.null(d=d)
        for point in points:
            result+=point
        return result

    def average(points):
        """Return the average of the material points."""
        return MaterialPoint.sum(points)/len(points)

    mean=average
    neutral=zero=null

    def random(corners=[-1,-1,1,1],**kwargs):
        """Create a random material point using optional minimum and maximum."""
        motion=Motion.random(corners)
        return MaterialPoint(motion,**kwargs)

    def createFromPoint(point,forces=[],n=3,d=2):
        """Create a material point from a Point instance."""
        motion=Motion(Vector(point),n=n,d=d) #Initializing a motion instance
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

    def delPosition(self):
        """Set the position of the material point to (0,0)."""
        l=len(self.motion.position.components)
        for i in range(l):
            self.motion.position.components[i]=0

    def getVelocity(self):
        """Return the velocity of the material point."""
        return self.motion.getVelocity()

    def setVelocity(self,velocity):
        """Set the velocity of the material point."""
        self.motion.velocity=Vector(velocity)

    def delVelocity(self):
        """Set the position of the material point to (0,0)."""
        l=len(self.motion.velocity.components)
        for i in range(l):
            self.motion.velocity.components[i]=0

    def getAcceleration(self):
        """Return the acceleration of the material point."""
        return self.motion.getAcceleration()

    def setAcceleration(self,acceleration):
        """Set the acceleration of the material point."""
        self.motion.acceleration=Vector(acceleration)

    def delAcceleration(self):
        """Set the position of the material point to (0,0)."""
        l=len(self.motion.acceleration.components)
        for i in range(l):
            self.motion.acceleration.components[i]=0

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
        acceleration=force/self.mass
        self.motion.acceleration.components=acceleration.components
        self.motion.update(t)

    def rotate(self,angle=math.pi,center=Point.origin()):
        """Rotate the point using an angle and the point of rotation."""
        point=self.getAbstract()
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

    def __getitem__(self,index):
        """Return x or y value using given index."""
        return self.getPosition()[index]

    def __setitem__(self,index,value):
        """Change x or y value using given index and value."""
        position=self.getPosition()
        position[index]=value
        self.setPosition(position)

    #Position
    def getX(self):
        """Return the x component of the position of the point."""
        return self.motion.position.position[0]

    def getY(self):
        """Return the y component of the position of the point."""
        return self.motion.position.position[1]

    def setX(self,x):
        """Set the x component of the position of the point."""
        self.motion.position.position[0]=x

    def setY(self,y):
        """Set the y component of the position of the point."""
        self.motion.position.position[1]=y

    def delX(self):
        """Set the x component of the point to 0."""
        self.motion.position.position[0]=0

    def delY(self):
        """Set the y component of the point to 0."""
        self.motion.position.position[1]=0

    #Velocity
    def getVx(self):
        """Return the x component of the velocity of the point."""
        return self.motion.velocity.position[0]

    def getVy(self):
        """Return the y component of the velocity of the point."""
        return self.motion.velocity.position[1]

    def setVx(self,vx):
        """Set the vx component of the velocity of the point."""
        self.motion.velocity.position[0]=vx

    def setVy(self,vy):
        """Set the y component of the velocity of the point."""
        self.motion.velocity.position[1]=vy

    def delVx(self):
        """Set the x component of the velocity of the point to 0."""
        self.motion.velocity.position[0]=0

    def delVy(self):
        """Set the y component of the velocity of the point to 0."""
        self.motion.position.position[1]=0

    #Acceleration
    def getAx(self):
        """Return the x component of the acceleration of the point."""
        return self.motion.acceleration.position[0]

    def getAy(self):
        """Return the y component of the acceleration of the point."""
        return self.motion.acceleration.position[1]

    def setAx(self,vx):
        """Set the vx component of the acceleration of the point."""
        self.motion.acceleration.position[0]=vx

    def setAy(self,vy):
        """Set the y component of the acceleration of the point."""
        self.motion.acceleration.position[1]=vy

    def delAx(self):
        """Set the x component of the acceleration of the point to 0."""
        self.motion.acceleration.position[0]=0

    def delAy(self):
        """Set the y component of the acceleration of the point to 0."""
        self.motion.position.position[1]=0

    #Abstract
    def getAbstract(self):
        """Return the abstract point that correspond to the point."""
        return Point(self.motion.position.position)

    def setAbstract(self,point):
        """Set the abstract point that correspond to the point."""
        self.motion.position.position=point.position

    def delAbstract(self):
        """Set the point the zero."""
        self.points=[]

    #Components
    def getComponents(self):
        """Return the components of the material point."""
        return self.abstract.components

    def setComponents(self,components):
        """Set the components of the material point to the given components."""
        self.abstract.components=components

    def delComponents(self):
        """Set the components of the material point to null."""
        self.abstract.components=[0 for i in range(len(self.abstract.components))]

    position=property(getPosition,setPosition,delPosition,"Representation of the position of the point.")
    velocity=property(getVelocity,setVelocity,delVelocity,"Representation of the velocity of the point.")
    acceleration=property(getAcceleration,setAcceleration,delAcceleration,"Representation of the acceleration of the point.")
    x=property(getX,setX,delX,"Representation of the x component of the position of the point.")
    y=property(getY,setY,delY,"Representation of the y component of the position of the point.")
    vx=property(getVx,setVx,delVx,"Representation of the x component of the velocity of the point.")
    vy=property(getVy,setVy,delVy,"Representation of the y component of the velocity of the point.")
    ax=property(getAx,setAx,delAx,"Representation of the x component of the acceleration of the point.")
    ay=property(getAy,setAy,delAy,"Representation of the y component of the acceleration of the point.")
    abstract=property(getAbstract,setAbstract,delAbstract,"Representation of the point as an abstract point.")
    components=property(getComponents,setComponents,delComponents,"Representation of the components of the material point.")


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
