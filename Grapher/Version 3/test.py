from GrapherV3 import Grapher
from math import exp,sin,cos,atan

def sigmoid(x):
  return 1/(1+exp(-x))

a,b,c=10,2,1.5
sigmoid_gota=lambda x:1/(1+exp(-a*(b*x-c)))
sinus = lambda x:-cos(3*x)/2+1/2
artan = atan
square= lambda x:x**4

functions=[sigmoid_gota,sinus,atan,square]

polynome=lambda x:x**4+2*x**3-x**2-6*x-3

functions=[polynome]

Grapher(functions)
