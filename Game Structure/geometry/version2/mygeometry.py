WHITE=(255,255,255)

from mywindow import Window

from mymaths import sign2,mean
from math import sqrt,atan,pi,cos,sin
from cmath import polar

import random
import time




if __name__=="__main__":
    window=Window()
    p1=Point(15,62)
    p2=Point(250,400)
    p3=Point(800,500)
    p4=Point(400,400,color=(0,255,0))
    points=[p1,p3,p2,p4]
    f=Form([Point(random.randint(1,700),random.randint(1,600)) for i in range(10)],color=(0,0,255))
    #f.show(window)
    f2=f.getSparse()
    p1.show(window)
    p2.show(window)
    v=Vector(p2[0]-p1[0],p2[1]-p1[1],color=(255,0,0))
    center=f2.center()
    while window.open:
        window.check()
        window.clear()
        #v.rotate(0.1)
        v.show(center,window)
        f2.rotate(0.1)
        time.sleep(0.1)
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
