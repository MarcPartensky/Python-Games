from myabstract import Line

class MaterialLine(Line):
    """Base class of the ground class."""
    def __init__(self,*args,**kwargs):
        """Create a material line."""
        super().__init__(*args,**kwargs)

class Ground(MaterialLine):
    """Subclass of the material line ."""
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
