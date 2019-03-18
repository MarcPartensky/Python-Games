from geometry.version1 import *
from mywindow import Window

import random

window=Window()
wsx,wsy=window.size

posAlea=lambda :[random.randint(0,wsx),random.randint(0,wsy)]


form=Form([Point(posAlea())]) for i in range(10)]

while window.open:
    window.check()
    form.rotate(0.1)
    form.show()
