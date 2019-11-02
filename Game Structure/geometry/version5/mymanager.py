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

    def __init__(self, name="SimpleManager",**kwargs):
        """Create a context manager with the optional name."""
        self.context = Context(name=name,**kwargs)
        self.pause=False

    def __call__(self):
        """Call the main loop."""
        while self.context.open:
            self.events()
            if not self.pause:
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
                    self.pause=not(self.pause)
                if event.key == K_f:
                    self.context.switch()  # Set or reverse fullscreen
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.context.draw.plane.zoom([1.1, 1.1])
                if event.button == 5:
                    self.context.draw.plane.zoom([0.9, 0.9])

    def update(self):
        """Update the context manager."""

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
    def __init__(self, name="Manager", dt=10e-3,**kwargs):
        """Create a manager using a context, this methods it to be overloaded."""
        self.context = Context(name=name,**kwargs)
        self.count = self.context.count
        self.pause = False
        self.dt = dt
        # Typing stuff
        self.typing = False
        self.alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.caps_numbers = ")!@#$%^&*("
        self.numbers = "0123456789"
        self.typing = False
        self.shiftlock = False
        self.capslock = False
        self.altlock = False

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
        self.reactAlways(key)
        if self.typing:
            self.reactTyping(key)
        else:
            self.reactMain(key)

    def reactAlways(self,key):
        """React to a key whether or not the typing mode is on."""
        # print(key) for debugging the keys
        if key == K_ESCAPE:
            self.switchQuit()
        if key==K_SLASH or key==K_BACKSLASH:
            if not self.typing:
                self.context.console("Typing activated.")
            self.typing=True
        if key==K_BACKQUOTE:
            self.switchTyping()

    def reactLock(self,key):
        """React to a locking key."""
        if key==K_CAPSLOCK:
            self.capslock=not(self.capslock)
        elif key==K_LSHIFT or key==K_RSHIFT:
            self.shiftlock=True
        elif key==K_LALT or key==K_RALT:
            self.altlock=True

    def reactTyping(self,key):
        """React to a typing event."""
        self.reactLock(key)
        if self.altlock:
            self.reactAltCase(key)
        elif self.capslock or self.shiftlock:
            self.reactUpperCase(key)
        else:
            self.reactLowerCase(key)

        if key==K_SPACE:
            self.write(" ")
        elif key==8:
            self.delete()
        if key==K_LCTRL:
            self.context.console.nextArg()
        elif key==K_UP:
            self.context.console.back()
        elif key==K_DOWN:
            self.context.console.forward()
        elif key==K_RETURN:
            self.eval()
            self.context.console.nextLine()

    def eval(self):
        """Execute a line."""
        content=self.context.console.line.content
        if content[0]=="/":
            for command in content[1:]:
                try:
                    self.context.console(str(eval(command)))
                except:
                    self.context.console("Invalid command.")
        if content[0]=="\\":
            for command in content[1:]:
                try:
                    exec(command)
                    self.context.console("Command "+command+" executed.")
                except Exception as e:
                    self.context.console(str(e))
        self.context.console.eval()

    def reactAltCase(self,key):
        """React when typing with alt key pressed."""
        if key==K_e:
            self.write("`") #Stupid
        elif key==167:
            self.write("´")

    def reactLowerCase(self,key):
        """React when typing in lower case."""
        d={K_COMMA:",",K_PERIOD:".",K_SEMICOLON:";",K_LEFTBRACKET:"[",
        K_RIGHTBRACKET:"]",39:"'",45:"-",K_EQUALS:"="}
        if 48<=key<=57:
            self.write(self.numbers[key-48])
        elif 97<=key<=122:
            self.write(self.alphabet[key-97])
        elif key in d:
            self.write(d[key])
        elif key==K_SLASH:
            if not self.context.console.line.empty:
                self.context.console.nextLine()
            self.write("/")
            self.context.console.nextArg()
        elif key==K_BACKSLASH:
            if not self.context.console.line.empty:
                self.context.console.nextLine()
            self.write("\\")
            self.context.console.nextArg()


    def reactUpperCase(self,key):
        """React to a key when typing in uppercase."""
        d={59:":''",44:"<",46:">",47:"?",
        45:"_",39:"\"",61:"+"}
        if 48<=key<=57:
            self.write(self.caps_numbers[key-48])
        elif 97<=key<=122:
            self.write(self.alphabet[key-97].upper())
        elif key in d:
            self.write(d[key])

    def write(self,c):
        """Write some content."""
        self.context.console.lines[-1].content[-1]+=c
        self.context.console.lines[-1].refresh()
        self.shiftlock=False
        self.altlock=False

    def delete(self,n=1):
        """Delete some content."""
        self.context.console.lines[-1].content[-1]=self.context.console.lines[-1].content[-1][:-n]
        self.context.console.lines[-1].refresh()

    def reactMain(self,key):
        """React as usual when not typing."""
        self.context.control()
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

    def switchTyping(self):
        """Switch the typing mode."""
        self.typing=not(self.typing)
        if self.typing:
            self.context.console("Typing activated.")
            self.context.console.nextLine()
        else:
            self.context.console("Typing deactivated.")

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
        if not self.typing: #Ugly fix for easier praticial use
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
        # This is not implemented correctly for now."""
        p = self.context.point()
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


class BlindManager(Manager):
    """Ugly way to make a manager without camera."""
    def __init__(self,camera=False,**kwargs):
        super().__init__(camera=camera,**kwargs)

if __name__ == "__main__":
    cm = Manager()
    cm()
