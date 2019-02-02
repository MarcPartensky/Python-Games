from mywindow import Window
from mypanel import Panel

class Button:
    def __init__(self,name="Unnamed Button",pannel=None,window):
        """Create a button object using name, pannel and window."""
        self.name=name
        self.pannel=pannel
        self.position=position
        self.size=size
        self.coordonnates=self.position+self.size

    def show(self):
        pass

    def __call__(self,click,cursor):
        if not click:
            return False
        else:
            cx,cy=cursor
            x,y=self.position
            sx,sy=self.size
            if x<=cx<=x+sx and y<=cy<=y+sy:
                return True
            else:
                return False
