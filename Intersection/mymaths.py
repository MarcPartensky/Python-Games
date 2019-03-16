import math

def mean(*args):
    l=allout(args)
    return sum([e for e in l])/len(l)

def prod(*args):
    l=allout(args)
    r=1
    for e in l:
        r*=e
    return r

def sum(*args):
    l=allout(args)
    r=0
    for e in l:
        r+=e
    return r


sign=lambda x:x>=0

def sign2(x):
    if x>0:
        return 1
    elif x<0:
        return -1
    else:
        return 0

def container(object):
    if type(object)==str:
        return False
    try:
        a=object[0]
        return True
    except:
        return False

"""
def sum(*args):
    r=0
    for e in args:
        if container(e):
            for x in e:
                r+=sum(x)
        else:
            r+=e
    return r
"""

def out(l):
    if container(l):
        r=[]
        for e2 in l:
            if container(e2):
                r+=e2
            else:
                r.append(e2)
        return r
    else:
        return l

def allout(l):
    if container(l):
        r=[]
        for e2 in l:
            if container(e2):
                r+=allout(e2)
            else:
                r.append(e2)
        return r
    else:
        return l

def analyse(l):
    r=[]
    if container(l):
        for e in l:
            r.append(analyse(e))
    else:
        r.append(type(l))
    return r

bijection=lambda x,i1,i2:(i2[1]-i2[0])/(i1[1]-i1[0])*(x-i1[0])+i2[0]

pi=PI=math.pi
e=E=euler=math.e

if __name__=="__main__":
    l1=[1,[3,1],[1,2,[2,1]],3]
    l2=["12",["1","6"],"manger"]
    print(analyse(l2))
