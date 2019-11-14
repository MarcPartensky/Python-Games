def principale():
    for n in range(1,10000):
        if test(n):
            return n

def test(n):
    n1=list(str(n))
    n2=list(str(9*n))
    n2.reverse()
    return n1==n2

print(principale())
