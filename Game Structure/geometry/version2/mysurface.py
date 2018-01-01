from mywindow import Window
from mydraw import Draw

class Surface:
    def __init__(self,draw=Draw()):
        self.draw=draw
        self.screen=self.draw.window.screen
        self.open=self.draw.window.open
        self.check=self.draw.window.check
        self.clear=self.draw.clear
        self.flip=self.draw.window.flip

class Surface2(Window):
    def __init__(self,draw=Draw()):
        Window.__init__(self)
        self.draw=draw



if __name__=="__main__":
    surface=Surface()
