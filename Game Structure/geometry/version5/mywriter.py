from mymanager import Manager
from pygame.locals import *
import time


d={
    K_a: "a",
    K_b: "b",
    K_c: "c"
}

print(K_a)
print(K_z)


alphabet="abcdefghijklmnopqrstuvwxyz"

class Writer(Manager):
    def __init__(self):
        super().__init__()
        self.context.console(" ")
        self.typing=False


    def reactKeyDown(self,key):
        if key==K_0:
            self.switchTyping()
        if self.typing:
            self.reactTyping(key)
        else:
            super().reactKeyDown(key)

    def switchTyping(self):
        """Switch the typing mode."""
        self.typing=not(self.typing)
        if self.typing:
            self.context.console("Typing activated.")
            self.context.console("")
        else:
            self.context.console("Typing deactivated.")

    def reactTyping(self,key):
        if 97<=key<=122:
            self.add(alphabet[key-97])
        if key==K_SLASH:
            self.add("/")
        if key==K_LEFTPAREN:
            self.add("(")
        if key==K_RIGHTPAREN:
            self.add(")")
        if key==K_PERIOD:
            self.add(".")
        if key==K_SPACE:
            self.add(" ")
        if key==K_COMMA:
            self.context.console.lines[-1].content.append("")
        if key==8:
            self.delete()
        if key==K_RETURN:
            self.context.console.lines[-1].eval()
            self.context.console("")
        if key==K_LALT:
            self.context.console.lines[-1].eval()

    def add(self,c):
        self.context.console.lines[-1].content[-1]+=c
        self.context.console.lines[-1].time=time.time()

    def delete(self,n=1):
        self.context.console.lines[-1].content[-1]=self.context.console.lines[-1].content[-1][:-n]
        self.context.console.lines[-1].time=time.time()


w=Writer()
w()
