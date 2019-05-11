from myabstract import Point,Segment

class Branch:
    def __init__(self,n=1,g=0):
        """Create a branch."""
        self.n=n
        self.g=g

    def children(self):
        """Return the childen branches of the branch."""
        children=[Branch(self.n*2,self.g+1)]
        a=(self.n-1)//3
        if a%2==1:
            children.append(Branch(a,self.g+1))
        return children

    def show(self,surface):
        """Show the branch to the surface."""
        p=self.point()
        for c in self.children():
            pc=c.point()
            s=Segment(p,pc)
            s.show(surface)

    def point(self):
        """Return the point associated to the branch."""
        return Point(self.n,self.g)

class Tree:
    """Syracuse tree."""
    def __init__(self,limit=10):
        """Create a syracuse tree."""
        self.branches=[]
        self.limit=limit

    def __call__(self,branch=Branch()):
        """Calculate the branches recursively."""
        if branch.g<self.limit:
            for c in branch.children():
                self.branches.append(c)
                self(c)

    def show(self,surface):
        """Show the tree on the surface."""
        for branch in self.branches:
            branch.show(surface)

if __name__=="__main__":
    from mysurface import Surface
    surface=Surface()
    tree=Tree()
    tree()
    while surface.open:
        surface.check()
        surface.control()
        surface.clear()
        surface.show()
        tree.show(surface)
        surface.flip()
