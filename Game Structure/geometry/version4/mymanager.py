from pygame.locals import *
from mycontext import Context

import pygame


class SimpleManager:
    """Manage a program using the context by many having functions that can be
    overloaded to make simple and fast programs.
    This process allow the user to think directly about what the program does,
    instead of focusing on how to display things.
    The way it works is by making the main class of the program inheriting from
    this one."""

    def __init__(self,context):
        """Create a context manager."""
        self.context=context

    def __call__(self):
        """Call the main loop."""
        while self.context.open:
            self.events()
            self.update()
            self.show()

    def events(self):
        """Deal with all the events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.context.open=False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.context.open=False
                if event.key == K_SPACE:
                    self.setMode((self.mode+1)%3)
                #if event.key == K_f:
                #    pygame.display.toggle_fullscreen()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: self.context.draw.plane.zoom([1.1,1.1])
                if event.button == 5: self.context.draw.plane.zoom([0.9,0.9])

    def update(self):
        """Update the context manager."""
        pass

    def show(self):
        """Show the context manager."""
        self.context.refresh()
        self.context.control()
        self.context.flip()





class Manager2:
    """Manage a program using the context by many having functions that can be
    overloaded to make simple and fast programs.
    This process allow the user to think directly about what the program does,
    instead of focusing on how to display things.
    The way it works is by making the main class of the program inheriting from
    this one."""

    def __init__(self,context):
        """Create a context manager."""
        self.context=context

    def __call__(self):
        """Call the main loop."""
        self.main()

    def main(self):
        """Execute the main loop."""
        self.loop()

    def loop(self):
        """Main loop."""
        while self.context.open:
            self.perform()

    def perform(self):
        """Execute the content of the main loop."""
        self.detect()
        self.update()
        self.show()


    def debug(self):
        self.context.console(str(ContextManager.__dict__['react'].__dict__))

    def update(self):
        """Update the context manager."""
        pass

    def show(self):
        """Show the context manager."""
        self.context.refresh()
        self.context.control()
        self.debug()

        self.context.flip()

    def detect(self):
        """Deal with all the events."""
        for event in pygame.event.get():
            self.react(event)

    def react(self,event):
        """React to a given event."""
        self.reactToQuit(event)
        if event.type == KEYDOWN:
            self.reactToKeyboard(event)
            return

    def reactToQuit(self,event):
        """Close the context if the quit button is pressed."""
        if event.type == pygame.QUIT:
            self.context.open=False

    def reactToKeyboard(self):
        """React to the keyboards buttons being pressed."""
        self.reactToEscape()

    def reactToEscape(self):
        """React to the button escape."""
        if event.key == K_ESCAPE:
            self.context.open=False





class Manager:
    def __init__(self,title="Unnamed"):
        """Create a manager using a context, this methods it to be overloaded."""
        self.context=Context(name=title)

    def __call__(self):
        """Call the main loop, this method is to be overloaded."""
        self.main()

    def main(self):
        """Main loop of the simple manager."""
        self.setup() #Name choices inspired from processing
        while self.context.open:
            self.loop()

    def setup(self):
        """Code executed before the loop."""
        pass

    def loop(self):
        """Code executed during the loop."""
        self.eventsLoop()
        self.updateLoop()
        self.showLoop()

    def eventsLoop(self):
        """Deal with the events in the loop."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.reactQuit()
            if event.type == KEYDOWN:
                self.reactKeyDown(event.key)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.reactMouseButtonDown(event.button)


    def reactQuit(self,event):
        """React to a quit event."""
        self.context.open=False

    def reactKeyDown(self,key):
        """React to a keydown event."""
        if key == K_ESCAPE:
            self.context.open=False

    def reactMouseButtonDown(self,button):
        """React to a mouse button down event."""
        if button == 4: self.context.draw.plane.zoom([1.1,1.1])
        if button == 5: self.context.draw.plane.zoom([0.9,0.9])



    def updateLoop(self):
        """Update the manager while in the loop."""
        self.update()

    def update(self):
        """Update the components of the manager of the loop. This method is to be
        overloaded."""
        pass

    def showLoop(self):
        """Show the graphical components and deal with the context in the loop."""
        self.context.control()
        self.context.clear()
        self.context.show()
        self.show()
        self.context.showConsole()
        self.context.flip()

    def show(self):
        """Show the graphical components on the context. This method is to be
        overloaded."""
        pass







if __name__=="__main__":
    cm=Manager()
    cm()
