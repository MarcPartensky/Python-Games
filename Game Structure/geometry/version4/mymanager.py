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





class Manager:
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



if __name__=="__main__":
    context=Context()
    cm=Manager(context)
    print(cm.__dict__)
    print(ContextManager.__dict__)
    cm()
