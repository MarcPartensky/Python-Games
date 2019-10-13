from mydraw import Draw
from myrect import Rect
from mywindow import Window

import mycolors
import time

#For the camera only
from pygame.locals import *
import numpy as np
import pygame
import cv2
#For the camera only

class Camera:
    """The camera rely on opencv, pygame and numpy."""
    def __init__(self,draw,position=[0,0],build=False):
        """Create an opencv camera. By default the capture is not active, it must
        be built using the build method, or by setting build to True in the
        init method."""
        self._draw=draw
        self.position=position
        if build: self.build()

    def build(self):
        """Build the capture with opencv. Having a separate function for the
        capture allows to have more efficiency for programs that do not need the
        camera."""
        self.capture=cv2.VideoCapture(0)

    def buildWriter(self):
        """Write the videos of the camera, this is just an odd concept, nothing
        really functional."""
        self.writer=cv2.VideoWriter(0)
        raise NotImplementedError

    def show(self):
        """Show the video."""
        ret, frame = self.capture.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        self._draw.image(self._draw.window.screen,frame,self.position)

    __call__=show

    def destroy(self):
        """Destroy the camera by ending the video capture."""
        cv2.destroyAllWindows() #this might be useless
        del self.capture

    def getOn(self):
        """Determine if the camera is active."""
        return "capture" in self.__dict__

    def setOn(self,on):
        """Activate or not the camera."""
        if on: self.build()
        else: self.destroy()

    def switch(self):
        """Switch the camera, meaning:
        - if the camera is off it turnf on
        - if the camera is on it turns off"""
        if self.on: self.destroy()
        else: self.build()

    on=property(getOn,setOn)

    __bool__=getOn



class Line:
    def __init__(self,*content,time=None,separator=" "):
        """Object of line created using the text and optional time."""
        self.content=content
        self.time=time
        self.separator=separator
    def __str__(self):
        return self.separator.join(map(str,self.content))
    def __iter__(self):
        self.iterator=0
        return self
    def __next__(self):
        if self.iterator<2:
            self.iterator+=1
            if self.iterator+1==0:
                return self.content
            elif self.iterator+1==1:
                return self.time
    def getText(self):
        return self.content
    text=property(getText)

class Console:
    def __init__(self,draw,
                lines=[],
                interline=15,
                left_padding=10,
                down_padding=20,
                conversion=False,
                size=20,
                position=[0,0],
                font=None,
                max_lines_shown=10,
                duration_lines_shown=10,
                disappearance_lines_shown=10,
                colors=[mycolors.WHITE,mycolors.BLACK]):
        """Create a console."""
        self._draw=draw #Draw is protected and can only be read
        self.lines=lines #List of Lines
        self.interline=interline
        self.left_padding=left_padding
        self.down_padding=down_padding
        self.conversion=conversion
        self.size=size
        self.position=position
        self.font=font
        self.max_lines_shown=max_lines_shown
        self.duration_lines_shown=duration_lines_shown
        self.disappearance_lines_shown=disappearance_lines_shown
        self.colors=colors

    def clear(self):
        """Clear the console by removing all the lines."""
        self.lines=[]
    def __getitem__(self,i):
        """Return the i-th line."""
        return self.lines[i]
    def __setitem__(self,v,i):
        """Set the i-th line."""
        self.lines[i]=v
    def __iadd__(self,*args):
        """Add a line to the console."""
        l=Line(*args,time=time.time())
        self.lines.append(l)
    append=__iadd__
    def __call__(self,*args,show=True):
        """Display a message on the context as a console would do."""
        if len(args)>0:
            l=Line(*args,time=time.time())
            self.lines.append(l)
        if show: self.show()
    def show(self):
        """Show the console without adding a text."""
        sx,sy=self._draw.window.size
        n=len(self.lines)
        nmax=self.max_lines_shown
        dls=self.disappearance_lines_shown
        for i in range(min(n,nmax)):
            position=(self.left_padding,sy-self.interline*i-self.down_padding)
            to=self.lines[-i-1].time
            t=(time.time()-to)/self.duration_lines_shown
            if t<1:
                c1=self.colors[0]+(t**dls,)
                c2=self.colors[1]+(t**dls,)
                self._draw.print(self.lines[-i-1],position,self.size,c1,self.font,self.conversion)



class Context(Rect):
    """The context is an object that allows the user to display graphical objects
    on the screen in a virtual mathematical plane."""

    def createFromSizeAndCorners(size,corners,**kwargs):
        c=Context(size=size,**kwargs)
        c.corners=corners
        return c

    def __init__(self,draw=None,console=None,camera=None,**kwargs):
        """Create a context using the optional draw, console and camera, with
        some of the draw's arguments for the window.
        If those are not given, they will be created automatically."""
        if draw is None:    draw=Draw(**kwargs)
        if console is None: console=Console(draw)
        if camera is None:  camera=Camera(draw)
        self.draw=draw
        self.console=console
        self.camera=camera
        self.screen=self.draw.window.screen
        self.clear=self.draw.clear
        self.flip=self.draw.window.flip
        self.press=self.draw.window.press
        self.build=self.draw.window.build
        self.click=self.draw.window.click
        self.__call__=self.draw.window.__call__
        self.wait=self.draw.window.wait
        self.control=self.draw.control
        self.events=self.draw.window.events
        self.checking=self.draw.window.checking
        self.loadImage=self.draw.window.loadImage
        self.print=self.draw.print
        self.update=self.draw.window.update
        self.switch=self.draw.window.switch
        self.append=self.console.append
        self.count=self.window.count

    def getKeys(self):
        """Return the keys of the window."""
        return self.press()

    def getCorners(self):
        """Return the corners of the surface shown."""
        return self.draw.plane.getCorners(self.draw.window)

    def setCorners(self,corners):
        """Set the corners of the plane using the new corners."""
        self.draw.plane.setCorners(corners,self.draw.window)

    def getRect(self):
        """Return the rect of the surface shown."""
        return Plane.getRectFromCorners(self.getCorners())

    def setRect(self,rect):
        """Set the rect of the surface shown."""
        self.draw.plane.setCorners(Plane.getCornersFromRect(rect))

    def getCoordonnates(self):
        """Return the coordonnates of the surface shown."""
        return Plane.getCoordonnatesFromCorners(self.getCorners())

    def setCoordonnates(self,coordonnates):
        """Set the coordonnates of the surface shown."""
        self.draw.plane.setCorners(Plane.getCornersFromCoordonnates(coordonnates))

    def getPosition(self):
        """Return the position of the surface shown."""
        return self.draw.plane.position

    def setPosition(self,position):
        """Set the position of the surface shown."""
        self.draw.plane.position=position

    def getSize(self):
        """Return the size of the surface shown."""
        return self.draw.window.size

    def setSize(self,size):
        """Set the size of the surface shown."""
        self.draw.window.size=size

    def getUnits(self):
        """Return the units of the surface shown."""
        return self.draw.plane.units

    def setUnits(self,units):
        """Set the units of the surface shown."""
        self.draw.plane.units=units

    def point(self):
        """Adapt the position of the cursor in plane's coordonnates."""
        x,y=self.draw.window.point()
        x,y=self.draw.plane.getFromScreen([x,y],self.draw.window)
        return (x,y)

    def check(self):
        """Check if the surface is open."""
        self.draw.window.check()
        self.open=self.draw.window.open

    def __call__(self):
        """Calling the surface allow the user to move on screen."""
        while self.open:
            self.check()
            self.draw.plane.control(self.draw.window)
            self.draw.window.clear()
            self.draw.plane.show(self.draw.window)
            self.flip()

    def __contains__(self,position):
        """Determine if a position is in the context."""
        return self.draw.plane.contains(position,self.draw.window)

    def show(self):
        """Show the plane on screen."""
        self.draw.plane.show(self.draw.window)

    def refresh(self):
        """Refresh the context by clearing the screen and showing the plane."""
        self.draw.window.clear()
        self.draw.plane.show(self.draw.window)

    def controlZoom(self):
        """Control the zoom of the surface's plane."""
        self.draw.plane.controlZoom(self.draw.window)

    def controlPosition(self):
        """Control the position of the surface's plane."""
        self.draw.plane.controlPosition(self.draw.window)

    def getFromScreen(self,position):
        """Behave like the get from screen of the plan without having to put the window in parameter."""
        return self.draw.plane.getFromScreen(position,self.draw.window)

    def blit(self,image,position):
        """Blit a given image to a given position."""
        sx,sy=self.image.size()


    def transform(self,image,size):
        """Change the size of an image."""
        return self.draw.window.transform(image,size)

    def getOpen(self):
        return self.draw.window.open

    def setOpen(self,open):
        self.draw.window.open=open

    def __enter__(self):
        """Opening the context."""
        self.check()
        self.control()
        self.clear()
        self.show()
        print("went in")
        return self

    def __exit__(self):
        """Ending the context."""
        print("going out")
        self.flip()
        if self.open:
            self.__enter__()

    def getWidth(self):
        """Return the width of the window."""
        return self.size[0]

    def setWidth(self,width):
        """Set the width of the window."""
        self.size[0]=width

    def getHeight(self):
        """Return the height of the window."""
        return self.size[1]

    def setHeight(self,height):
        """Set the height of the window."""
        self.size[1]=height

    def __bool__(self):
        """Determine if the context is opened or not."""
        return self.open

    def getText(self):
        """Text is an alias for console and can be read."""
        return self.console

    def setText(self,value):
        """Text is an alias for console and can be written."""
        self.console=value

    def showConsole(self,*args):
        """Show the console, this function is a fix for deprecated programs."""
        self.console.show(*args)

    def getCounter(self):
        """Return the window counter."""
        return self.draw.window.counter

    def setCounter(self,coutner):
        """Set the window counter."""
        self.draw.window.counter=counter

    def getPlane(self):
        """Return the draw's plane."""
        return self.draw.plane

    def setPlane(self,plane):
        """Set the draw's plane."""
        self.plane=plane

    def getWindow(self):
        """Return the draw's window."""
        return self.draw.window

    def setWindow(self,window):
        """Set the draw's window."""
        self.draw.window=window


    def getFullscreen(self):
        """Determine if the context is in fullscreen mode."""
        return self.draw.window.fullscreen

    def setFullscreen(self,fullscreen):
        """Set the fullscreen mode."""
        self.draw.window.fullscreen

    window=property(getWindow,setWindow)
    plane=property(getPlane,setPlane)

    corners=property(getCorners,setCorners,"Allow the user to manipulate the corners of the surface easily.")
    rect=property(getRect,setRect,"Allow the user to manipulate the rect of the surface easily.")
    coordonnates=property(getCoordonnates,setCoordonnates,"Allow the user to manipulate the coordonnates of the surface easily.")
    position=property(getPosition,setPosition,"Allow the user to manipulate the position of the surface easily.")
    size=property(getSize,setSize,"Allow the user to manipulate the size of the surface easily.")
    units=property(getUnits,setUnits,"Allow the user to manipulate the units of the surface easily.")
    keys=property(getKeys,"Allow the user to manipulate the keys of the surface easily.")
    open=property(getOpen,setOpen)
    width=property(getWidth,setWidth)
    height=property(getHeight,setHeight)
    text=property(getText,setText)
    counter=property(getCounter,setCounter)
    fullscreen=property(getFullscreen,setFullscreen)


Surface=Context #Ugly fix for deprectated programs

if __name__=="__main__":
    context=Context(name="Context test")
    context.camera.build()
    context.console.duration_lines_shown=2
    context.console.max_lines_shown=40
    #context.corners=[0,0,1,1]
    print(context.corners)
    print(bool(context))
    while context:
        context.count()
        context.check()
        context.update()
        context.control()
        context.clear()
        context.show()

        context.camera()
        context.console(context.counter)

        if context.counter>100:
            context.camera.destroy()

        context.flip()
