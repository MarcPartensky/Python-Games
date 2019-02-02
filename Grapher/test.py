#import os
#path=+"/"
#print(path)
#os.chdir(path)

import os
import sys
abspath=os.path.abspath("../Grapher/Version 2/")
print(abspath)
#path=sys.path.insert(0, abspath)
sys.path.append(abspath)
#print(path)

from ..GrapherV2 import *
#import GrapherV2
import random
Grapher(["random.betavariate(1,1)","random.gauss(1,x)"])
