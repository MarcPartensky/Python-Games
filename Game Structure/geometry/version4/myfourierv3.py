from myinterpolation import PolynomialInterpolation
from mycontext import Context
from mycurves import Trajectory
import numpy as np
import mycolors
import random
import cmath
import math

n=10
xmin,ymin,xmax,ymax=[-1,-1,1,1]
wo=2*math.pi
nmin=-10
nmax=10
interval=list(range(nmin,nmax+1))
precision=100


points=[(random.uniform(xmin,xmax),random.uniform(ymin,ymax)) for i in range(n)]


def getCoefficient(f,n,s):
    return sum([f(w)*cmath.exp(s*w*wo*1j) for w in np.linspace(0,1,precision)])/precision

def getCoefficients(f,s=-1):
    return [getCoefficient(f,n,s) for n in interval]


def transform(f):
    """Fourier Transform."""
    zf=complexFunction(f)
    zl=getCoefficients(zf,-1)
    l=complexToTuple(zl)
    nf=PolynomialInterpolation(l)
    return nf

def inverseTransform(f):
    """Fourier Inverse Transform."""
    zf=complexFunction(f)
    zl=getCoefficients(zf,-1)
    l=complexToTuple(zl)
    nf=PolynomialInterpolation(l)
    return nf


def complexToTuple(lz):
    return [(z.real,z.imag) for z in lz]

def tupleToComplex(pts):
    return [complex(*pt) for pt in pts]


def complexFunction(f):
    return lambda x:complex(*f(x))

def tupleFunction(f):
    return lambda x:(f(x).real,f(x).imag)


if __name__=="__main__":
    context=Context()
    pt0=points
    print("points:",pt0)

    f1=PolynomialInterpolation(pt0)

    #Transform
    f2=transform(f1)
    print(f2)
    #InverseTransform
    f3=inverseTransform(f2)
    print(f3)




    #t1=Trajectory.createFromTuples(pt0,segment_color=mycolors.GREEN)
    #t2=Trajectory.createFromTuples(new_points,segment_color=mycolors.LIGHTGREEN)


    while context.open:
        context.check()
        context.control()
        context.clear()
        context.show()
        f1.show(context,200)
        f2.show(context,200)
        f3.show(context,200)
        #p1.show(context,200)

        context.flip()
