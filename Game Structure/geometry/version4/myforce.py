from myabstract import Vector
from mymotion import Motion

p=2 #Number of digits of precision of the objects when displayed


class Force(Vector):
    def null(d=2):
        """Return the null force."""
        return Force([0 for i in range(d)])
    neutral=zero=null

    def sum(forces,d=2):
        """Return the sum of the forces."""
        result=Force.null(d)
        for force in forces:
            result+=force
        return result

    def __init__(self,*args,**kwargs):
        """Create a force."""
        super().__init__(*args,**kwargs)

    def __call__(self,material_object):
        """Apply a force on a motion."""
        material_object.acceleration.components=self.abstract.components
        #Keep the other parameters such as the color

    def show(self,surface):
        """New dope show method especially for the forces."""
        raise Exception("Not operational")

    def __str__(self):
        """Return the string representation of the object."""
        x=round(self.x,p)
        y=round(self.y,p)
        return "f("+str(x)+","+str(y)+")"

    def getAbstract(self):
        """Return the object into its simple vector form."""
        return Vector(self.components)

    def setAbstract(self,vector):
        """Set the abstract vector to a new vector."""
        self.components=vector.components

    def delAbstract(self):
        """Set the abstract vector to null."""
        self.setNull()

    abstract=property(getAbstract,setAbstract,delAbstract,"Reperesentaion of the abstract vector of the force.")

class ForceField:
    def __init__(self,force,area):
        """Create a force field object."""
        self.force=force
        self.area=area

    def __contains__(self,body):
        """Determine if a body is contained in the force field."""
        #This function should be able to determine which proportion of the object is contained in the force
        #field in order to apply some of the force
        pass


    def exert(self,body):
        """Exert the force of the force field to the object."""
        pass




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
