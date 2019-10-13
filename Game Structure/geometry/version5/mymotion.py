from myabstract import Vector

import mycolors
import copy

class Motion:
    #Class functions
    #Operations
    def null(n=3,d=2):
        """Return the neutral motion."""
        #The dimension d still needs to be implemented for the vectors.
        return Motion([Vector.null(d=d) for i in range(n)])

    neutral=zero=null

    def sum(motions):
        """Return the sum of the motions together."""
        result=Motion.null()
        for motion in motions:
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
    def __init__(self,*vectors,n=3,d=2):
        """Create a motion using vectors."""
        if vectors!=():
            if type(vectors[0])==list:
                vectors=vectors[0]
        self.vectors=list(vectors)
        self.vectors+=[Vector.neutral(d=d) for i in range(n-len(self.vectors))]
        if len(self.vectors)>=1: self.position.color     = mycolors.GREEN
        if len(self.vectors)>=2: self.velocity.color     = mycolors.BLUE
        if len(self.vectors)>=3: self.acceleration.color = mycolors.RED

    #Showing
    def show(self,context):
        """Show the motion on the screen from the origin of the plane."""
        for vector in self.vectors:
            vector.show(context)

    #Updating the motion
    def update(self,t=1):
        """Update the motion according to physics."""
        self.vectors[:-1]=[v+d*t for (v,d) in zip(self.vectors[:-1],self.vectors[1:])]

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


    def __neg__(self):
        """Return the motions made of the negative vectors."""
        return Motion(*[-v for v in self.vectors])

    __radd__=__add__=lambda self,other:Motion(*[v1+v2 for (v1,v2) in zip(self.vectors,other.vectors)]) #Addition
    __rsub__=__sub__=lambda self,other:Motion(*[v1-v2 for (v1,v2) in zip(self.vectors,other.vectors)]) #Substraction
    __rmul__=__mul__=lambda self,other:Motion(*[v*other for v in self.vectors])                        #Multiplication
    __rtruediv__=__truediv__=lambda self,other:Motion(*[v/other for v in self.vectors])                #Division
    __rfloordiv__=__floordiv__=lambda self,other:Motion(*[v//other for v in self.vectors])             #Floor Division

    def __iadd__(self,other):
        """Add the other motion to the motion."""
        self.vectors=[v1+v2 for (v1,v2) in zip(self.vectors,other.vectors)]
        return self

    def __isub__(self,other):
        """Substract the other motion to the motion."""
        self.vectors=[v1-v2 for (v1,v2) in zip(self.vectors,other.vectors)]
        return self

    def __imul__(self,other):
        """Multiply a motion by a scalar."""
        self.vectors=[v*other for v in self.vectors]
        return self

    def __itruediv__(self,other):
        """Divide a motion by a scalar."""
        self.vectors=[v/other for v in self.vectors]
        return self

    def __ifloordiv__(self,other):
        """Divide motion by a scalar according to euclidian division."""
        self.vectors=[v//other for v in self.vectors]
        return self


    #Properties
    position=property(getPosition,setPosition,delPosition,"Allow the user to manipulate the position.")
    velocity=property(getVelocity,setVelocity,delVelocity,"Allow the user to manipulate the velocity.")
    acceleration=property(getAcceleration,setAcceleration,delAcceleration,"Allow the user to manipulate the acceleration.")
    #Other derivatives in order...
    #jerk=property(getJerk,setJerk,delJerk,"Representation of the jerk.")
    #snap=jounce=property(getSnap,setSnap,delSnap,"Representation of the snap.")
    #pop=property(getPop,setPop,delPop,"Representation of the pop.")

class Moment(Motion):
    #Class functions
    #Operations
    def null(n=3,d=2):
        """Return the neutral motion."""
        #The dimension d still needs to be implemented for the vectors.
        return Moment([Vector.null(d=d) for i in range(n)])

    neutral=zero=null

    def sum(motions):
        """Return the sum of the motions together."""
        result=Moment.null()
        for motion in motions:
            result+=motion
        return result

    def average(motions):
        """Return the average of the motions."""
        return Moment.sum(motions)/len(motions)

    #Random
    def random(corners=[-1,-1,1,1],n=3,d=2):
        """Create a random motion using optional minimum and maximum."""
        return Moment([Vector.random(corners) for i in range(n)])

    #Object functions
    #Initializing
    def __init__(self,*vectors,n=3,d=2):
        """Create a motion using vectors."""
        if vectors!=():
            if type(vectors[0])==list:
                vectors=vectors[0]
        self.vectors=list(vectors)
        self.vectors+=[Vector.neutral(d=d) for i in range(n-len(self.vectors))]
        if len(self.vectors)>=1: self.position.color     = mycolors.GREEN
        if len(self.vectors)>=2: self.velocity.color     = mycolors.BLUE
        if len(self.vectors)>=3: self.acceleration.color = mycolors.RED


if __name__=="__main__":
    from mycontext import Context
    context=Context(name="Motion")
    motion1=Motion.random()
    motion2=Motion.random()
    motion=motion1+motion2
    motion=Motion.sum([Motion.random() for i in range(9)]+[motion]) #Summing 10 motions together
    print(motion)
    while context.open:
        context.check()
        context.control()
        context.clear()
        context.show()
        motion.show(context)
        context.flip()
