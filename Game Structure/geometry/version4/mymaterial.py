from copy import deepcopy

class Material:
    """Class containing physics function that can be used for all sorts of material classes."""
    def sum(objects):
        """Sum the objects."""
    #Vectors
    #Position
    def getPosition(self):
        """Return the position of the material point."""
        return self.motion.getPosition()

    def setPosition(self,position):
        """Set the position of the material point."""
        self.motion.position=Vector(position)

    def delPosition(self):
        """Set the position of the material point to (0,0)."""
        l=len(self.motion.position.position)
        for i in range(l):
            self.motion.position.position[i]=0

    #Velocity
    def getVelocity(self):
        """Return the velocity of the material point."""
        return self.motion.getVelocity()

    def setVelocity(self,velocity):
        """Set the velocity of the material point."""
        self.motion.velocity=Vector(velocity)

    def delVelocity(self):
        """Set the position of the material point to (0,0)."""
        l=len(self.motion.velocity.position)
        for i in range(l):
            self.motion.velocity.position[i]=0

    #Acceleration
    def getAcceleration(self):
        """Return the acceleration of the material point."""
        return self.motion.getAcceleration()

    def setAcceleration(self,acceleration):
        """Set the acceleration of the material point."""
        self.motion.acceleration=Vector(acceleration)

    def delAcceleration(self):
        """Set the position of the material point to (0,0)."""
        l=len(self.motion.acceleration.position)
        for i in range(l):
            self.motion.acceleration.position[i]=0

    #Components
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

    #Operations
    #Addition
    def __add__(self,other):
        """Add two material objects together."""
        object=copy.deepcopy(self)
        object.motion+=other.motion
        return object

    def __iadd__(self,other):
        """Add a material object to another."""
        self.motion+=other.motion
