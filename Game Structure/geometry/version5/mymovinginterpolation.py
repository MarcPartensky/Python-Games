#Show interpolations being made while moving the points.

#Impors
from mycontext import Context
from myabstract import Point
from myinterpolation import PolynomialInterpolation

context=Context()
l=10
points=[Point(2*x,random.randint(-5,5)) for x in range(l)]
n=0
ncp=50 #number construction points


while context.open:
    context.check()
    context.control()
    context.clear()
    context.show()

    Point.turnPoints([1/1000 for i in range(l)],points)
    p=PolynomialInterpolation(points)
    p.show(context)
    n=(n+1)%(ncp+1)

    p1=b(n/ncp)
    p2=t(n/ncp)

    #l1=Line.createFromTwoPoints(p1,p2)

    p1.show(context,color=mycolors.YELLOW,radius=0.1,fill=True)
    p2.show(context,color=mycolors.YELLOW,radius=0.1,fill=True)

    context.flip()
