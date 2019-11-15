from myabstract import Form

f1 = Form.random()
f2 = Form.random()


c=f1.center

print("inside:",c in f1)

print(f1.cross(f2))

s=f1.sides[0]

m=s(1/2)

print(s.__contains__(m, e=1e-1))

# TODO: crossing problem between forms first
