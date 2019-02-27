a = [1,2,3,[]]
c = [5,6,7,[]]
b = [a, [], c]

def rem_none(l):
    if type(l) != list:
        return
    l[:] = [i for i in l if i is not None]
    for e in l:
        rem_none(e)

def rem_empty(l):
    if type(l)==list: return [rem_empty(e) for e in l if e!=[]]
    else: return l


def rem_empty2(l):
    if not type(l)==list:
        return l
    else:
        if len(l)>0:
            print("before:",l)
            a=[rem_empty2(e) for e in l if e is not []]
            print("after:",l)
            return a


#rem_none(b)

print(b)
d=rem_empty(b)
print(d)
