class ImmutableBody(Body):
    """Define a body than cannot be moved by any other body."""
    def __init__(self,*args,**kwargs):
        super().__init(*args,**kwargs)


class Ground(ImmutableBody):
    """Define a ground that is an immutable body."""
    def __init__(self,):
        """Create a ground using its line."""
        self.mass=float('inf')

