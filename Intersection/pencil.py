from geometry import *

class Pencil:
    def __init__(self,name="Unnammed",color=WHITE):
        self.name=name
        self.color=color
        self.points=[]
        self.forms=[]
    def __call__(self,window):
        if window.click():
            self.points.append(Point(window.point(),WHITE))

    def show(self,window):
        for point in self.points:
            point.show(window)
        for form in self.forms:
            form.show(window)


    def click(self,window):
        pass
