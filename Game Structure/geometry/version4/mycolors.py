BLUE       = (  0,  0,255)
RED        = (255,  0,  0)
GREEN      = (  0,255,  0)
YELLOW     = (255,255,  0)
BLACK      = (  0,  0,  0)
WHITE      = (255,255,255)
GREY       = (100,100,100)
PURPLE     = (100,  0,100)
ORANGE     = (255,165,  0)
HALFGREY   = ( 50, 50, 50)
DARKGREY   = ( 20, 20, 20)
DARKRED    = ( 10, 10, 10)
DARKGREEN  = ( 10, 10, 10)
DARKBLUE   = ( 10, 10, 10)
LIGHTRED   = (255,200,200)
LIGHTGREEN = (200,255,200)
LIGHTBLUE  = (200,200,255)
LIGHTBROWN = (229,219,222)
LIGHTGREY  = (200,200,200)
BEIGE      = (199,175,138)

import random as rd


random=lambda:tuple([rd.randint(0,255) for i in range(3)])

print("mycolors imported")
