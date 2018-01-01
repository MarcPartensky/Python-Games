class Minimax:
    def __init__(self,tree,start=0,choice=None):
        self.start=start
        self.tree=tree
        self.choice=choice
        self.tree=self.remove_empty(self.tree)

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

    def remove_empty(self,tree):
        if type(tree)!=list:
            return tree
        else:
            new_tree=[]
            for i in range(len(tree)):
                if tree[i]!=[]:
                    new_element=self.remove_empty(tree[i])
                    if new_element!=[]:
                        new_tree.append(new_element)
            return new_tree



    def __call__(self):
        #print(self.tree)
        if self.tree!=[]:
            value=self.decompose(self.tree)
        return self.choice


if __name__=="__main__":
    tree=[[1,2,[[5,5,1]],5,1,5,1,],[[[],[]]]]
    minimax=Minimax(tree)
    print(minimax.tree)
