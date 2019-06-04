from mysurface import Surface
from myabstract import Vector

import mycolors
import copy

class Motion:
    #Class functions
    #Operations
    def neutral(n=3,d=2):
        """Return the neutral motion."""
        #The dimension d still needs to be implemented for the vectors.
        return Motion([Vector.neutral() for i in range(n)])

    def sum(motions):
        """Return the sum of the motions together."""
        result=motions[0]
        for motion in motions[1:]:
            result+=motion
        return result

    def average(motions):
        """Return the average of the motions."""
        return Motion.sum(motions)/len(motions)

    #Random
    def random(corners=[-1,-1,1,1],n=3,d=2):
        """Create a random motion using optional minimum and maximum."""
        return Motion([Vector.random(corners) for i in range(n)])

    #Object functions
    #Initializing
    def __init__(self,*vectors,n=3):
        """Create a motion using vectors."""
        if len(vectors)==1: vectors=vectors[0]
        if len(vectors)==0: vectors=[Vector.neutral() for i in range(3)]
        self.vectors=vectors
        if len(self.vectors)>=1: self.position.color     = mycolors.GREEN
        if len(self.vectors)>=2: self.velocity.color     = mycolors.BLUE
        if len(self.vectors)>=3: self.acceleration.color = mycolors.RED

    #Showing
    def show(self,context):
        """Show the motion on the screen from the origin of the plane."""
        for vector in self.vectors:
            vector.show(context)

    #Updating the motion
    def update(self,t=1,n=None):
        """Update the motion according to physics."""
        if not n: n=len(self.vectors)-1
        self.vectors[:n]=[v+d*t for (v,d) in zip(self.vectors[:n],self.vectors[1:n+1])]

    #Representation
    def __str__(self):
        """Return the str representation of the motion."""
        return "Motion("+",".join([str(v) for v in self.vectors])+")"

    #Iterations
    def __iter__(self):
        """Iterate the vectors."""
        self.iterator=0
        return self

    def __next__(self):
        """Return the next vector of the iteration."""
        if self.iterator<len(self.vectors):
            self.iterator+=1
            return self.vectors[self.iterator-1]
        else:
            raise StopIteration

    #Time behaviour
    def next(self,t=1):
        """Return the next motion using its actual one using optional time t."""
        acceleration=Vector([a for a in self.acceleration])
        velocity=Vector([v+a*t for (v,a) in zip(self.velocity,self.acceleration)])
        position=Vector([p+v*t for (p,v) in zip(self.position,self.velocity)])
        return Motion(position,velocity,acceleration)

    def previous(self,t=1):
        """Return the previous motion using its actual one using optional time t."""
        acceleration=Vector([a for a in self.acceleration])
        velocity=Vector([v-a*t for (v,a) in zip(self.velocity,self.acceleration)])
        position=Vector([p-v*t for (p,v) in zip(self.position,self.velocity)])
        return Motion(position,velocity,acceleration)

    #Length
    def __len__(self):
        """Return the number of vectors."""
        return len(self.vectors)

    #Items
    def __getitem__(self,index):
        """Return the vector of index 'index.'"""
        return self.vectors[index]

    def __setitem__(self,index,vector):
        """Set the vector of index 'index.'"""
        self.vectors[index]=vector


    #Vectors
    #Position
    def getPosition(self):
        """Return the position of the motion."""
        return self.vectors[0]

    def setPosition(self,position):
        """Set the position of the motion using position."""
        self.vectors[0]=position

    def delPosition(self):
        """Set the position to zero."""
        self.vectors[0]=Vector([0 for i in range(len(self.vectors[0].position))])

    #Velocity
    def getVelocity(self):
        """Return the velocity of the motion."""
        return self.vectors[1]

    def setVelocity(self,velocity):
        """Set the velocity of the motion using velocity."""
        self.vectors[1]=velocity

    def delVelocity(self):
        """Set the velocity to zero."""
        self.vectors[1]=Vector([0 for i in range(len(self.vectors[1].position))])

    #Acceleration
    def getAcceleration(self):
        """Return the acceleration of the motion."""
        return self.vectors[2]

    def setAcceleration(self,acceleration):
        """Set the acceleration of the motion."""
        self.vectors[2]=acceleration

    def delAcceleration(self):
        """Set the acceleration to zero."""
        self.vectors[2]=Vector([0 for i in range(len(self.vectors[2].position))])

    #Operations
    __radd__=__iadd__=__add__=lambda self,other:Motion(*[v1+v2 for (v1,v2) in zip(self,other)]) #Addition
    __rsub__=__isub__=__sub__=lambda self,other:Motion(*[v1-v2 for (v1,v2) in zip(self,other)]) #Substraction
    __rmul__=__imul__=__mul__=lambda self,other:Motion(*[v*other for v in self])                #Multiplication
    __rtruediv__=__itruediv__=__truediv__=lambda self,other:Motion(*[v/other for v in self])    #Division
    __rfloordiv__=__ifloordiv__=__floordiv__=lambda self,other:Motion(*[v//other for v in self])    #Division

    #Properties
    position=property(getPosition,setPosition,delPosition,"Allow the user to manipulate the position.")
    velocity=property(getVelocity,setVelocity,delVelocity,"Allow the user to manipulate the velocity.")
    acceleration=property(getAcceleration,setAcceleration,delAcceleration,"Allow the user to manipulate the acceleration.")
    #Other derivatives in order...
    #jerk=property(getJerk,setJerk,delJerk,"Representation of the jerk.")
    #snap=jounce=property(getSnap,setSnap,delSnap,"Representation of the snap.")
    #pop=property(getPop,setPop,delPop,"Representation of the pop.")

if __name__=="__main__":
    from mysurface import Context
    context=Context(name="Motion")
    motion1=Motion.random()
    motion2=Motion.random()
    motion=motion1+motion2
    motion=Motion.sum([Motion.random() for i in range(10)]+[motion]) #Summing 10 motions together
    print(motion)
    while context.open:
        context.check()
        context.control()
        context.clear()
        context.show()
        motion.show(context)
        context.flip()
