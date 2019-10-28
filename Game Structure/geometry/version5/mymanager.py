from mycontext import Context
from pygame.locals import *
import pygame


class SimpleManager:
    """Manage a program using the context by many having functions that can be
    overloaded to make simple and fast programs.
    This process allow the user to think directly about what the program does,
    instead of focusing on how to display things.
    The way it works is by making the main class of the program inheriting from
    this one."""

    def __init__(self, name="SimpleManager"):
        """Create a context manager with the optional name."""
        self.context = Context(name=name)

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
                self.context.open = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.context.open = False
                if event.key == K_SPACE:
                    self.setMode((self.mode + 1) % 3)
                if event.key == K_f:
                    self.context.switch()  # Set or reverse fullscreen
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.context.draw.plane.zoom([1.1, 1.1])
                if event.button == 5:
                    self.context.draw.plane.zoom([0.9, 0.9])

    def update(self):
        """Update the context manager."""
        pass

    def show(self):
        """Show the context manager."""
        self.context.refresh()
        self.context.control()
        self.context.flip()


class oldManager:  # This manager is deprecated
    """Manage a program using the context by many having functions that can be
    overloaded to make simple and fast programs.
    This process allow the user to think directly about what the program does,
    instead of focusing on how to display things.
    The way it works is by making the main class of the program inheriting from
    this one."""

    def __init__(self, context):
        """Create a context manager."""
        self.context = context

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

    def react(self, event):
        """React to a given event."""
        self.reactToQuit(event)
        if event.type == KEYDOWN:
            self.reactToKeyboard(event)
            return

    def reactToQuit(self, event):
        """Close the context if the quit button is pressed."""
        if event.type == pygame.QUIT:
            self.context.open = False

    def reactToKeyboard(self):
        """React to the keyboards buttons being pressed."""
        self.reactToEscape()

    def reactToEscape(self):
        """React to the button escape."""
        if event.key == K_ESCAPE:
            self.context.open = False


class Manager:
    def __init__(self, name="Manager", dt=10e-3):
        """Create a manager using a context, this methods it to be overloaded."""
        self.context = Context(name=name)
        self.count = self.context.count
        self.pause = False
        self.dt = dt

    def __call__(self):
        """Call the main loop, this method is to be overloaded."""
        self.main()

    def main(self):
        """Main loop of the simple manager."""
        self.setup()  # Name choices inspired from processing
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
            if event.type == QUIT:
                self.switchQuit()
            if event.type == KEYDOWN:
                self.reactKeyDown(event.key)
            if event.type == MOUSEBUTTONDOWN:
                self.reactMouseButtonDown(event.button)
            if event.type == MOUSEMOTION:
                self.reactMouseMotion(event)

    def switchQuit(self):
        """React to a quit event."""
        self.context.open = not(self.context.open)

    def reactKeyDown(self, key):
        """React to a keydown event."""
        if key == K_ESCAPE:
            self.switchQuit()
        if key == K_f:
            self.switchFullscreen()
        if key == K_1:
            self.switchCapture()
        if key == K_2:
            self.switchCaptureWriting()
        if key == K_3:
            self.switchScreenWriting()
        if key == K_SPACE:
            self.switchPause()

    def switchScreenWriting(self):
        """Swtich the screen writing mode."""
        if self.context.camera.screen_writing:
            self.context.camera.screen_writer.release()
        self.context.camera.switchScreenWriting()
        if self.context.camera.screen_writing:
            self.context.console('The screen is being written.')
        else:
            self.context.console('The screen video has been released')
            self.context.console('and is not being written anymore.')

    def switchCaptureWriting(self):
        """Switch the capture writing mode."""
        if self.context.camera.capture_writing:
            self.context.camera.capture_writer.release()
        self.context.camera.switchCaptureWriting()
        if self.context.camera.capture_writing:
            self.context.console('The capture is being written.')
        else:
            self.context.console('The capture video has been released')
            self.context.console('and is not being written anymore.')

    def switchPause(self):
        """React to a pause event."""
        self.pause = not(self.pause)
        if self.pause:
            self.context.console('The system is paused.')
        else:
            self.context.console('The system is unpaused.')

    def switchCapture(self):
        """React to a capture event."""
        self.context.camera.switchCapture()
        if self.context.camera.capturing:
            self.context.console('The camera capture is turned on.')
        else:
            self.context.console('The camera capture is turned off.')

    def switchFullscreen(self):
        """React to a fullscreen event."""
        self.context.switch()
        if self.context.fullscreen:
            self.context.console("The fullscreen mode is set.")
        else:
            self.context.console("The fullscreen mode is unset.")

    def reactMouseButtonDown(self, button):
        """React to a mouse button down event."""
        if button == 4:
            self.context.draw.plane.zoom([1.1, 1.1])
        if button == 5:
            self.context.draw.plane.zoom([0.9, 0.9])

    def reactMouseMotion(self, event):
        """React to a mouse motion event."""
        pass

    def updateLoop(self):
        """Update the manager while in the loop."""
        if not self.pause:
            self.update()
            self.count()
        self.context.camera.write()  # Write on the camera writers if they are on

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
        self.showCamera()
        self.context.console.show()
        self.context.flip()

    def show(self):
        """Show the graphical components on the context. This method is to be
        overloaded."""
        pass

    def showCamera(self):
        """Show the camera if active."""
        if self.context.camera.capturing:
            self.context.camera.show()

    def counter():
        doc = "The Counter property."
        def fget(self):
            """Bind the counter of the manager to the one of the context."""
            return self.context.counter
        def fset(self, counter):
            """Set the counter of the context."""
            self.context.counter = counter
        return locals()
    counter = property(**counter())




class BodyManager(Manager):
    """Manage the bodies that are given when initalizing the object."""
    @classmethod
    def createRandomBodies(cls, t, n=5, **kwargs):
        """Create random bodies using their class t.
        The bodies of the class t must have a random method."""
        bodies = [t.random() for i in range(n)]
        return cls(bodies, **kwargs)

    def __init__(self, bodies, following=False, **kwargs):
        """Create a body manager using its bodies and optional arguments for the context."""
        super().__init__(**kwargs)
        self.bodies = bodies
        self.following = following

    def update(self):
        """Update the bodies."""
        self.updateFollowers()
        self.updateBodies()

    def updateFollowers(self):
        """Update the bodies that are followers."""
        #This is not implemented correctly for now."""
        p=self.context.point()
        if self.following:
            for body in self.bodies:
                body.follow(p)

    def updateBodies(self):
        """Update the bodies individually."""
        for body in self.bodies:
            body.update(self.dt)

    def show(self):
        """Show the bodies."""
        self.showBodies()

    def showBodies(self):
        """Show all the bodies individually."""
        for body in self.bodies:
            body.show(self.context)


if __name__ == "__main__":
    cm = Manager()
    cm()
