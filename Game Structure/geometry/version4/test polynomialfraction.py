from marclib.polynomial import Polynomial,RationalFunction
from mynewgrapher import Grapher
from mycontext import Context


if __name__=="__main__":
    p1=Polynomial([0,6,1,6,5])
    q1=Polynomial([0,5,2,1,-2])
    f1=RationalFunction(p1,q1)

    p2=Polynomial([0,5,2,1,-2])
    q2=Polynomial([0,6,1,6,5])
    f2=RationalFunction(p2,q2)

    f=f1+f2

    print(f.poles)

    context=Context()
    g=Grapher(context,[f1,f2,f])
    g()
