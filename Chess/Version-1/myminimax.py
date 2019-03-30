import time

class Minimax:
    def __init__(self,object,start=0):
        self.start=start
        self.value=self.decompose(object)

    def decompose(self,object,n=0):
        if type(object) is list:
            decomposition=[]
            for x in object:
                decomposition.append(self.decompose(x,n+1))
            if n%2==self.start:
                value=max(decomposition)
            else:
                value=min(decomposition)
            self.choice=decomposition.index(value)
            return value
        else:
            return object


if __name__=="__main__":
    object=[[[1,3],[4,4]],[2,5]]
    m=Minimax(object)
    #m.decompose(object)
    print(m.choice)
