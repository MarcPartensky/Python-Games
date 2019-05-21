from myabstract import Line

class MaterialLine(Line):
    """Base class of the ground class."""
    def __init__(self,point,angle,mass,**kwargs):
        """Create a material line."""
        super().__init__(point,angle,**kwargs)
        self.mass=mass

class Ground(MaterialLine):
    """Subclass of the material line ."""
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)


if __name__=="__main__":
    from mysurface import Surface
    surface=Surface()
    line=MaterialLine()
