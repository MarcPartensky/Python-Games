class Curve:
    def __init__(self,points,degree=1):
        self.points=points
        self.degree=degree
        self.coefficients=[0 for i in range(self.degree+1)]

    def evaluate(self,x):
        y=0
        for n,coefficient in enumerate(self.coefficients):
            y+=coefficient*x**n
        return y

    def cost(self):
        s=0
        for A in self.points:
            x,y=A
            z=self.evaluate(x)
            s+=(z-y)**2
        return s


"""
M(x,y) appartient a D:y=ax+b
A(xa,ya)


MA=sqrt((x-xa)**2+(y-ya)**2)





"""
