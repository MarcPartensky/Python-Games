class Minimax:
    def __init__(self,tree,start=0,choice=None):
        self.start=start
        self.tree=tree
        self.choice=choice
        self.tree=self.rem_empty(self.tree)

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

    def rem_none(self,l):
        if type(l) != list:
            return
        l[:] = [i for i in l if i is not []]
        for e in l:
            self.rem_none(e)

    def rem_empty(self,l):
        if type(l)==list: return [self.rem_empty(e) for e in l if e!=[]]
        else: return l


    def __call__(self):
        #print(self.tree)
        if self.tree!=[]:
            value=self.decompose(self.tree)
        return self.choice
