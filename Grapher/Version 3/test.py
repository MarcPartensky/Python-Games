from GrapherV3 import *
import math

def sigmoid(x):
  return 1/(1+math.exp(-x))

Grapher(["noise.pnoise1(x)","noise.pnoise1(x+5432)"])
