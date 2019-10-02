class ImmutableBody(Body):
    """Define a body than cannot be moved by any other body."""
    def __init__(self,*args,**kwargs):
        super().__init(*args,**kwargs)


class Ground(ImmutableBody):
    """Define a ground that is an immutable body."""
    def __init__(self,):
        """Create a ground using its line."""
        self.mass=float('inf')

#(m1+m2)v=m1v1+m2v2
#m*v**2=m1*v1**2+m2*v2**2
