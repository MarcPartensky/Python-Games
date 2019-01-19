import random

done=False
a=float(0)
v=0
x=0

a_factor=0.01
v_factor=0.01

while not done:
    a=random.randint(-1,1)
    v+=a*a_factor
    x+=v*v_factor
    print(a,v,x)
