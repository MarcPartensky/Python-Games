from mymanager import Manager
from pygame.locals import *
import time


#K_SLASH: "/"



maj={
}




#print(K_CAPSLOCK)
print(K_1)
print(K_9)
print(K_0)


class Writer(Manager):
    def __init__(self):
        super().__init__()
        self.context.console(" ")
        self.alphabet="abcdefghijklmnopqrstuvwxyz"
        self.caps_numbers=")!@#$%^&*("
        self.numbers="0123456789"
        self.typing=False
        self.shiftlock=False
        self.capslock=False

    def eventsLoop(self):
        super().eventsLoop()
        self.shiftlock=False

    def reactKeyDown(self,key):
        """React to a keydown event."""
        if key==96:
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


    def reactLock(self,key):
        """React to a locking key."""
        if key==1073741881:
            self.capslock=not(self.capslock)
        if key==K_LSHIFT or key==K_RSHIFT:
            self.shiftlock=True

    def reactTyping(self,key):
        """React to a typing event."""
        self.reactLock(key)
        print(key)

        if self.capslock or self.shiftlock:
            if 48<=key<=57:
                self.write(self.caps_numbers[key-48])
            if 97<=key<=122:
                self.write(self.alphabet[key-97].upper())
        else:
            if 48<=key<=57:
                self.write(self.numbers[key-48])
            if 97<=key<=122:
                self.write(self.alphabet[key-97])
            if key==K_SLASH:
                self.write("/")
            if key==K_PERIOD:
                self.write(".")
            if key==K_COMMA:
                self.context.console.lines[-1].content.append("")
        if key==K_SPACE:
            self.write(" ")
        if key==8:
            self.delete()
        if key==K_RETURN:
            self.context.console.lines[-1].eval()
            self.context.console("")
        if key==K_LALT:
            self.context.console.lines[-1].eval()

    def write(self,c):
        self.context.console.lines[-1].content[-1]+=c
        self.context.console.lines[-1].time=time.time()

    def delete(self,n=1):
        self.context.console.lines[-1].content[-1]=self.context.console.lines[-1].content[-1][:-n]
        self.context.console.lines[-1].time=time.time()


w=Writer()
w()
