class object:
    def __init__(self,*args):
        self.position=list(args)
    def __setitem__(self,index,value):
        self.position[index]=value
    def __getitem__(self,index):
        return self.position[index]
    def __add__(self,other,prout):
        return "caca"+prout

class position:
    def __init__(self,x):
        self.x=x
    def __int__(self):
        return self.x

o=object()
print(o+*[o,"wesh"])

#o=object(2,1)
#o[0]+=3
#print(o[0],o[1],o.position)

#x=position(3)

#print(int(x))
