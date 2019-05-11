class Angle(float):
    def __new__(self,value):
        """Create a new angle."""
        return float.__new__(self,value)

    def __init__(self,value):
        """Create an angle object."""
        float.__init__(value)

    def __str__(self):
        """Return the string representation of the angle."""
        return str(float(self))+" C"

    def show(self,surface,points):
        """Show the angle between the points."""
        p1,p2,p3=points
        



a=Angle(3)
print(a)
