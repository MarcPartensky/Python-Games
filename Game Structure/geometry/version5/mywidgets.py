from mymanager import Manager
from myrectangle import Rectangle
from mymenu import Button as mButton
from myabstract import Segment,Circle,Point
from functools import reduce
from pygame.locals import *

import mycolors
import operator
import pygame
import random

old_styles={
    "text": {
        "default":mycolors.WHITE,
        "hovered":mycolors.WHITE,
        "focused":mycolors.WHITE,
        "clicked":mycolors.WHITE},
    "background": {
        "default":None,
        "hovered":None,
        "focused":None,
        "clicked":None},
    "bordure": {
        "default":mycolors.WHITE,
        "hovered":mycolors.WHITE,
        "focused":mycolors.WHITE,
        "clicked":mycolors.WHITE}}




class Widget:
    def __init__(self,state=0,reference=[]):
        """Create a widget."""
        self.state=state
        self.reference=reference

    def update(self):
        """Update the button."""
        self.updateColors()

    def reactKeyDown(self,key):
        """React to a keydown event."""
        if key==K_RETURN:
            self.state=0

    def reactMouseMotion(self,position):
        """React to a mouse motion event."""
        if position in self:
            if self.state==0:
                self.state=1
        elif self.state==3:
            self.state=2
        elif self.state!=2:
            self.state=0

    def reactMouseButtonDown(self,button,position):
        """React to a mouse button down event."""
        if button==1:
            if position in self:
                if self.state>=2:
                    self.state=0
                else:
                    self.state=3
            else:
                self.state=0

    @property
    def default(self):
        """Determine if the button is inactive."""
        return self.state==0

    @property
    def hovered(self):
        """Determine if the button is hovered."""
        return self.state==1

    @property
    def focused(self):
        """Determine if the button is focused."""
        return self.state==2

    @property
    def clicked(self):
        """Determine if the button is clicked."""
        return self.state==3



class Slider(Segment,Widget):
    @classmethod
    def random(cls):
        """Return a random slider."""
        s=Segment.random()
        return cls(*s.points)

    def __init__(self,*points,
                borns=[0,1],
                relative_value=0,
                radius=1,
                state=0,
                error=1e-2,
                round_precision=2,
                styles=[
                    [mycolors.WHITE,mycolors.GREEN,mycolors.BLUE,mycolors.RED], #Segment
                    [mycolors.WHITE,mycolors.GREEN,mycolors.BLUE,mycolors.RED], #Cursor bordure
                    [mycolors.BLACK for i in range(4)] #Cursor area
                ],
                **kwargs):
        """Create a slider."""
        super().__init__(*points,**kwargs)
        self.state=state
        self.borns=borns
        self.relative_value=relative_value
        self.radius=radius
        self.styles=styles
        self.error=1e-2
        self.round_precision=round_precision
        self.update()

    def __contains__(self,position):
        """Determine if the position is on the slider."""
        b1=Segment.__contains__(self,position,e=self.error)
        b2=(position in self.cursor)
        return b1 or b2

    def update(self):
        """Update the colors."""
        self.updateColors()

    def reactMouseMotion(self,position):
        """React to a mouse motion event."""
        super().reactMouseMotion(position)
        if self.state>=2:
            self.updateValue(position)

    def updateValue(self,position,):
        """Update the value."""
        l=self.line
        p=l.projectPoint(Point(*position))
        s=Segment(self.p1,p)
        if abs(s.angle-self.angle)<=self.error:
            length=s.length
        else:
            length=-s.length
        self.relative_value=length/self.length
        self.relative_value=max(self.relative_value,0)
        self.relative_value=min(self.relative_value,1)

    def updateColors(self):
        """Update the colors for the slider."""
        self.color=self.styles[0][self.state]
        self.circle_color=self.styles[1][self.state]
        self.circle_area_color=self.styles[2][self.state]

    def show(self,context):
        """Show the slider on screen."""
        self.showSegments(context)
        self.showCursor(context)
        self.showValue(context)

    def showSegments(self,context):
        """Show 2 segments instead of 1 to avoid crossing the circle of the
        cursor."""
        s1,s2=self.segments
        s1.show(context)
        s2.show(context)

    def showValue(self,context):
        """Show the actual value of the slider."""
        context.print(str(round(self.value,self.round_precision)), \
                    self.middle.position)

    def showCursor(self,context):
        """Show the cursor of the slider."""
        self.cursor.show(context)

    @property
    def segments(self):
        """Return 2 segments instead of 1 to avoid crossing the circle of the
        cursor."""
        rv=self.relative_value
        r=self.radius
        l=self.length
        x1=max(rv-r/l,0)
        x2=min(rv+r/l,1)
        p1=self(x1)
        p2=self(x2)
        s1=Segment(self.p1,p1,color=self.color)
        s2=Segment(self.p2,p2,color=self.color)
        return (s1,s2)

    @property
    def cursor(self):
        """Return the point associated with the cursor."""
        return Circle(*self(self.relative_value),radius=self.radius,
                color=self.circle_color,area_color=self.circle_area_color)

    def getValue(self):
        """Return the absolute value using the borns and the relative value."""
        a,b=self.borns
        return a+self.relative_value*(b-a)

    def setValue(self,value):
        """Set the absolute value using the borns and the relative value."""
        a,b=self.borns
        self.relative_value=(value-a)/(b-a)

    value=property(getValue,setValue)

class Button(Rectangle,Widget):
    """
    States of the Buttons:
            - 0 for default
            - 1 for hover
            - 2 for focus
            - 3 for click
    """
    @classmethod
    def random(cls):
        """Return a random button."""
        r=Rectangle.random()
        return cls(r.position,r.size)

    def __init__(self,
                position,
                size,
                text="Button",
                text_size=1,
                police="monospace",
                bold=False,
                italic=False,
                centered=True,
                converted=True,
                state=0,
                styles=[
                    [mycolors.WHITE,mycolors.GREEN,mycolors.BLUE,mycolors.RED], #Text
                    [mycolors.WHITE,mycolors.GREEN,mycolors.BLUE,mycolors.RED], #Bordure
                    [mycolors.BLACK for i in range(4)] #Background
                ],
                **kwargs):
        """Create a button using its position, size and optional states and
        color attributes."""
        Rectangle.__init__(self,position,size,**kwargs)
        self.state=state
        self.styles=styles
        self.text=text
        self.text_size=text_size
        self.police = police
        self.bold = bold
        self.italic = italic
        self.centered=centered
        self.converted=converted

    def updateColors(self):
        """Update the color of the button depending on the state of the button."""
        self.text_color=self.styles[0][self.state]
        self.side_color=self.styles[1][self.state]
        self.area_color=self.styles[2][self.state]

    def show(self,context,**kwargs):
        """Show the button."""
        super().show(context,**kwargs)
        self.showText(context)

    def showText(self,context):
        """Show the text of the button."""
        if self.converted:
            text_size=self.text_size*max(context.units)
        else:
            text_size=self.text_size
        font=pygame.font.SysFont(self.police,int(text_size),self.bold,self.italic)
        font_surface=font.render(self.text,True,self.text_color)
        sfx,sfy=font_surface.get_size()
        x,y=context.getToScreen(self.position)
        if self.centered:
            position=(x-sfx//2,y-sfy//2)
        else:
            position=(x,y)
        context.draw.window.blit(font_surface,position)

class WidgetManager(Manager):
    def __init__(self,widgets,**kwargs):
        """Create a widget manager."""
        super().__init__(**kwargs)
        self.widgets=widgets
        self.updating=False
        self.updateWidgets()

    def reactKeyDown(self,key):
        """React to a keydown event."""
        super().reactKeyDown(key)
        for widget in self.widgets:
            widget.reactKeyDown(key)
        self.updating=True

    def reactMouseMotion(self,event):
        """React to a mouse motion event."""
        super().reactMouseMotion(event)
        position=self.context.getFromScreen(tuple(event.pos))
        for widget in self.widgets:
            widget.reactMouseMotion(position)
        self.updating=True

    def reactMouseButtonDown(self,event):
        """React to a mouse button down event."""
        super().reactMouseButtonDown(event)
        position=self.context.getFromScreen(tuple(event.pos))
        for widget in self.widgets:
            widget.reactMouseButtonDown(event.button,position)
        self.updating=True

    def update(self):
        if self.updating:
            self.updateWidgets()
            self.updating=False

    def updateWidgets(self):
        """Update each widget."""
        for widget in self.widgets:
            widget.update()

    def show(self):
        """Show the widgets."""
        for widget in self.widgets:
            widget.show(self.context)

class WidgetManager2(Manager):
    def __init__(self,widgets={},**kwargs):
        """Create the widgets manager using the widgets and manager arguments."""
        super().__init__(**kwargs)
        self.widgets=widgets
        self.updating=False
        self.updateWidgets()

    def addSlider(self,ref,borns,position=(10,10),size=(0,10),conversion=False):
        """Add a slider of NOTHING AT ALL."""
        self.monitor[ref]=Slider(position,size,borns)

    def updateWidgets(self):
        """Check for each widgets if the values they are binded to changed of
        state and update them if so."""
        for (reference,widget) in self.widgets.items():
            value=self.read(reference)
            widget.value=value

    def updateWidgetsValue(self):
        """Check for each widgets if the values they are binded to changed of
        state and update them if so."""
        for (reference,widget) in self.widgets.items():
            self.write(reference,widget.value)

    def update(self):
        """Update the widgets."""
        if self.updating:
            self.updateWidgets()
            self.updating=False

    def show(self):
        """Show the widgets."""
        for widget in self.widgets.values():
            widget.show(self.context)

    def reactKeyDown(self,key):
        """React to a keydown event."""
        super().reactKeyDown(key)
        for widget in self.widgets.values():
            widget.reactKeyDown(key)
        self.updating=True

    def reactMouseMotion(self,event):
        """React to a mouse motion event."""
        super().reactMouseMotion(event)
        position=self.context.getFromScreen(tuple(event.pos))
        for widget in self.widgets.values():
            widget.reactMouseMotion(position)
        self.updating=True

    def reactMouseButtonDown(self,event):
        """React to a mouse button down event."""
        super().reactMouseButtonDown(event)
        position=self.context.getFromScreen(tuple(event.pos))
        for widget in self.widgets.values():
            widget.reactMouseButtonDown(event.button,position)
        self.updating=True

    def write(self,reference,value):
        """Write the given value into the variable of the given reference."""
        pass

    def read(self,reference):
        """Return the value of the variable of the given reference."""
        return reduce(operator.getitem,self,path)



class WidgetTester:
    """Create a alphabet of buttons."""
    @classmethod
    def createAlphabetButtons(cls):
        """Create an alphabet of buttons."""
        buttons=[Button((i,0),(0.9,0.9),letter) for (i,letter) in \
                        enumerate("abcdefghijklmnopqrstuvwxyz")]
        return cls(buttons)

    @classmethod
    def createSliders(cls,n=10):
        """Create some random sliders."""
        sliders=[Slider.createFromTuples((-2*i,-10),(-2*i,10)) for i in range(0,n)]
        return cls(sliders)

    @classmethod
    def createSlidersAndButtons(cls,nsliders=5,nbuttons=5,sparse=10):
        """Create some sliders and some buttons."""
        sliders=[Slider.createFromTuples((-2*i,-10),(-2*i,10),borns=[-2,i]) \
                for i in range(0,nsliders)]
        buttons=[Button((i,0),(0.9,0.9),letter) \
                for (i,letter) in enumerate("abcdefghijklmnopqrstuvwxyz")]
        return cls(sliders+buttons)

    @classmethod
    def createRandomSlidersAndButtons(cls,nsliders=5,nbuttons=5,sparse=10):
        """Create some sliders and some buttons."""
        r=lambda : random.random()
        sliders=[Slider.createFromTuples((2*i+r(),r()),(i+r(),r())) for i in range(nsliders)]
        buttons=[Button((i+10*r(),10*r()),(r(),r())) for i in range(nbuttons)]
        return cls(sliders+buttons)

class WidgetTester1(WidgetTester,WidgetManager):
    """Class of widget tester for the WidgetManager1."""


class WidgetTester2(WidgetTester,WidgetManager2):
    """Class of widget tester for the WidgetManager2."""

if __name__=="__main__":
    wm=WidgetTester1.createSlidersAndButtons()
    wm()
