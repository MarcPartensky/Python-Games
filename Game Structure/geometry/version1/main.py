from mypoint import Point
from myform import Form
from myvector import Vector
from mywindow import Window

from random import randint

window=Window()
wsx,wsy=window.size
X=wsx//4
Y=wsy//4

posAlea=lambda :[randint(X,3*X),randint(Y,3*Y)]


f1=Form([Point(*posAlea()) for i in range(5)])
f1=f1.getSparse()
f2=Form([Point(*posAlea()) for i in range(5)])
f2=f2.getSparse()

#f1.points[0].color=(255,0,0)
#f1.points[1].color=(255,0,0)

while window.open:
    window.check()
    window.clear()
    f1.rotate(0.01,f1[0])
    #f1.rotate(-0.01)
    f2.rotate(0.02,f1[1])
    f2.rotate(-0.03)
    f1.show(window)
    f2.show(window)
    f1.center(color=(0,255,0)).show(window)
    f2.center(color=(0,255,0)).show(window)
    if f1*f2:
        f1.color(RED)
        f2.color(RED)
    else:
        f1.color(WHITE)
        f2.color(WHITE)
    f1[0].show(window,color=(255,0,0))
    f1[1].show(window,(255,0,0))

    window.flip()
