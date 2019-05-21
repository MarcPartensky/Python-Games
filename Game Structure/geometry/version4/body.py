from mymaterialform import MaterialForm


class Body(MaterialForm):
    """Body inherits from material forms."""
    def __init__(self,*args,**kwargs):
        """Create a body."""
        super().__init__(*args,**kwargs)


if __name__=="__main__":
    from mysurface import Surface
    surface=Surface()
    b=Body.random()
    while surface.open:
        surface.check()
        surface.control()
        surface.clear()
        surface.show()
        b.show(surface)
        surface.flip()
