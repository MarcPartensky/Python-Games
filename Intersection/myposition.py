from math import sqrt,cos,sin
from cmath import polar
from numpy import array,dot

class Position:
    base="xyztabcdefhijklmnopqrsuvw"
    angle_base="ab"

    def __init__(self,*data,base=None,system="cartesian"):
        """Save a position using cartesian coordonnates."""
        self.system=system
        if self.system is "cartesian": self.data=array(data)
        if self.system is "polar":     self.data=polar(list(data))
        if base: self.base=base
        else:    self.base=Position.base[:len(self.data)]
    def __call__(self):
        return list(self.data)
    def __str__(self,system="cartesian"):
        """Gives a representation of the position."""
        if system is "cartesian":
            return " ".join([str(self.base[i])+"="+str(self.data[i]) for i in range(len(self.data))])
        if system is "polar":
            pass

    x=lambda self:self.data[self.base.index("x")]
    y=lambda self:self.data[self.base.index("y")]
    z=lambda self:self.data[self.base.index("z")]
    t=lambda self:self.data[self.base.index("t")]
    __repr__=__str__
    __add__=lambda self,other:self.data+other.data
    __sub__=lambda self,other:self.data-other.data


    def __mul__(self,other):
        if type(other) is Position:
            return Position(dot(self.data,other.data))
        else:
            return Position([self.data*other])


    def __sub__(self,other):
        pass
    def __len__(self):
        """Return number of dimension of the position."""
        return len(self.data)

    def polar(self,position=None):
        """Return an array of the polar coordonnates using optionnal position."""
        if not position: position=self.data
        position=list(position)
        if len(position)==2:
            return array(polar(complex(*position)))
        else:
            raise Exception(str(position)+" is not a cartesian position.")

    def cartesian(self,position=None):
        """Return an array of the cartesian position using optional polar position."""
        if not position: position=self.data
        if len(position)==2:
            return array([position[0]*cos(position[1]),position[0]*sin(position[1])])
        else:
            raise Exception(str(position)+" is not a polar position.")

a=Position(2,6)
b=Position(2,4)
print((a*b).data)

print(a.polar())
print(a.cartesian())
print(Position.polar(a.data))

print(a)
