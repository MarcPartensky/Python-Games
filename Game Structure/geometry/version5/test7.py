from mymotion import Motion


m=Motion.random()
print(m)
m*=10
print(m)

def f():
    global a
    a=1

def g():
    global a
    a+=1


f()
print(a)

g()

print(a)
