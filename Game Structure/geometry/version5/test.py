def f(l):
    for e in l:
        yield e

l = list(range(5))
l[2] = [2,3]
print(list(f(l)))

for i,e in enumerate(f(l)):
    if i==2:
        e[0] = 5

print(l)
