import pygame

class Paint:
    def __init__(self,tools=[]):
        self.name="Paint"
        self.tools=tools
        self.sets=[]
    def draw(self,input):
        pass
    def show(self):
        pass

if __name__=="__main__":
    window=Window("Paint")
    paint=Paint(window)
    paint()
