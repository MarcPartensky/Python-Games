from mywindow import Window
from mysurface import Surface
from mydraw import Draw

from math import sqrt,atan,pi,cos,sin,pi
from cmath import polar
from mycolors import *


from mypoint import Point
from myform import Form
from myvector import Vector

import random
import time




if __name__=="__main__":
    real_window=Window(size=[1440,900],fullscreen=True)
    draw=Draw(window=real_window)
    window=Surface(draw) #Create not a real window but a surface to display on screen.
    #window=Window(fullscreen=True)
    p1=Point(1,-6)
    p2=Point(-2,4)
    p3=Point(8,5)
    p4=Point(4,4,color=(0,255,0))
    points=[p1,p3,p2,p4]
    f=Form([Point(random.randint(-10,10),random.randint(-10,10)) for i in range(10)])
    #f.show(window)
    f2=f.getSparse()
    p1.show(window)
    p2.show(window)
    v1=Vector(p2[0]-p1[0],p2[1]-p1[1],color=(255,0,0))

    while window.open:
        window.check()
        window.clear()
        window.draw.control()
        v1.rotate(0.1)
        v2=v1%(pi/2)
        v2.color=GREEN
        v2.rotate(0.1)
        f2.rotate(0.1)
        center=f2.center()
        center.color=BLUE
        #center.radius=0.1
        A=v1(center)
        window.draw.show()
        center.show(window)
        v1.show(center,window)
        v2.show(A,window)
        f2.show(window)
        window.flip()
    #Segment(f[0],f[1],color=(255,0,0)).center().show(window)
    #print(p4 in f)
    #window.clear()
    #p4.show(window)
    #a=Line(p4,p2,color=(255,0,0))
    #b=Segment(p1,p3,color=(255,255,0))
    #a.show(window)
    #b.show(window)
    #p=b|a
    #window()
    #a=Vector(1,5)
